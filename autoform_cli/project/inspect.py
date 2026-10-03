"""Inspect a local Lean project's configuration without running Lake, Lean, or Git.

Compatibility is decided by two files: `lean-toolchain` and the Mathlib entry
that `lake-manifest.json` locks, which is what `lake build` materializes.
`lakefile.toml` is read for the package name, targets, and a staleness check;
`lakefile.lean` is never evaluated.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from .catalog import ReleaseCatalog, canonical_git_url, load_release_catalog

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    import tomli as tomllib  # type: ignore[no-redef]

PROJECT_INSPECTION_SCHEMA = "autoform-project-inspection/v1"
_MAX_FILE_BYTES = 1024 * 1024
_ROOT_MARKERS = ("lakefile.lean", "lakefile.toml", "lean-toolchain")
_MANIFEST = "lake-manifest.json"
_OVERRIDES = ".lake/package-overrides.json"
_AUTOFORM_PATHS = (
    "blueprint",
    "mkdocs.yml",
    ".github/workflows/autoform-verify.yml",
    ".github/workflows/blueprint-pages.yml",
)


@dataclass(frozen=True, slots=True)
class ProjectDiagnostic:
    severity: str
    code: str
    message: str
    path: str | None = None


@dataclass(frozen=True, slots=True)
class LakeTarget:
    kind: str
    name: str


@dataclass(frozen=True, slots=True)
class LakeProject:
    config: str
    name: str | None
    version: str | None
    targets: tuple[LakeTarget, ...]


@dataclass(frozen=True, slots=True)
class MathlibLock:
    """The Mathlib package entry Lake will materialize."""

    type: str
    source: str
    url: str | None = None
    input_rev: str | None = None
    rev: str | None = None
    dir: str | None = None


@dataclass(frozen=True, slots=True)
class ProjectCompatibility:
    status: str
    release: str | None
    recommended_release: str


@dataclass(frozen=True, slots=True)
class ProjectInspection:
    project_root: str | None
    lake: LakeProject | None
    lean_toolchain: str | None
    mathlib: MathlibLock | None
    autoform_paths: tuple[str, ...]
    compatibility: ProjectCompatibility
    diagnostics: tuple[ProjectDiagnostic, ...]

    @property
    def ok(self) -> bool:
        return not any(diagnostic.severity == "error" for diagnostic in self.diagnostics)

    def as_dict(self) -> dict[str, object]:
        return {**asdict(self), "ok": self.ok, "schema": PROJECT_INSPECTION_SCHEMA}

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), sort_keys=True, separators=(",", ":"))


def inspect_project(target: str | Path, *, catalog: ReleaseCatalog | None = None) -> ProjectInspection:
    catalog = catalog or load_release_catalog()
    diagnostics: list[ProjectDiagnostic] = []
    try:
        start = Path(target).expanduser().resolve(strict=True)
        if not start.is_dir():
            start = start.parent
        root = next(
            (
                directory
                for directory in (start, *start.parents)
                if any(_present(directory / marker) for marker in _ROOT_MARKERS)
            ),
            None,
        )
    except (OSError, RuntimeError, ValueError):
        diagnostics.append(ProjectDiagnostic("error", "target-unreadable", "The inspection target cannot be resolved."))
        return _result(catalog, diagnostics)
    if root is None:
        diagnostics.append(
            ProjectDiagnostic("error", "project-not-found", "No enclosing Lean project (lakefile or lean-toolchain).")
        )
        return _result(catalog, diagnostics)

    lake, requirement = _inspect_lake(root, diagnostics)
    toolchain = _inspect_toolchain(root, diagnostics)
    if not _present(root / _MANIFEST):
        diagnostics.append(
            ProjectDiagnostic(
                "warning",
                "missing-lake-manifest",
                "There is no lake-manifest.json, so the locked Mathlib is unknown.",
                _MANIFEST,
            )
        )
    locked = _locked_mathlib(root, _MANIFEST, diagnostics)
    overridden = _locked_mathlib(root, _OVERRIDES, diagnostics)
    if overridden is not None:
        diagnostics.append(
            ProjectDiagnostic(
                "warning",
                "mathlib-overridden",
                "Lake uses the Mathlib from package-overrides.json instead of the manifest's.",
                _OVERRIDES,
            )
        )
    elif locked is not None and requirement is not None and _is_stale(requirement, locked):
        diagnostics.append(
            ProjectDiagnostic(
                "warning",
                "lake-manifest-stale",
                "lakefile.toml requests a different Mathlib than the manifest locks; Lake builds the locked one.",
                _MANIFEST,
            )
        )
    return _result(
        catalog,
        diagnostics,
        project_root="/".join([".."] * (len(start.parts) - len(root.parts))) or ".",
        lake=lake,
        lean_toolchain=toolchain,
        mathlib=overridden or locked,
        autoform_paths=tuple(path for path in _AUTOFORM_PATHS if _exists_exactly(root, path)),
    )


def _result(
    catalog: ReleaseCatalog,
    diagnostics: list[ProjectDiagnostic],
    *,
    project_root: str | None = None,
    lake: LakeProject | None = None,
    lean_toolchain: str | None = None,
    mathlib: MathlibLock | None = None,
    autoform_paths: tuple[str, ...] = (),
) -> ProjectInspection:
    errors = any(diagnostic.severity == "error" for diagnostic in diagnostics)
    release = None
    if errors or lean_toolchain is None or mathlib is None:
        status = "indeterminate"
        if not errors:
            diagnostics.append(
                ProjectDiagnostic(
                    "warning",
                    "release-indeterminate",
                    "The Lean toolchain or the locked Mathlib is unknown, so compatibility cannot be checked.",
                )
            )
    else:
        release = catalog.match(lean_toolchain, mathlib.url, mathlib.rev) if mathlib.type == "git" else None
        status = "supported" if release is not None else "unlisted"
        if release is None:
            diagnostics.append(
                ProjectDiagnostic(
                    "warning",
                    "release-unlisted",
                    "This Lean and Mathlib pair is not in the bundled release catalog.",
                )
            )
    return ProjectInspection(
        project_root=project_root,
        lake=lake,
        lean_toolchain=lean_toolchain,
        mathlib=mathlib,
        autoform_paths=autoform_paths,
        compatibility=ProjectCompatibility(
            status, release.id if release is not None else None, catalog.recommended.id
        ),
        diagnostics=tuple(sorted(diagnostics, key=lambda item: (item.severity, item.code, item.path or ""))),
    )


def _inspect_lake(root: Path, diagnostics: list[ProjectDiagnostic]) -> tuple[LakeProject | None, dict | None]:
    if _present(root / "lakefile.lean"):
        diagnostics.append(
            ProjectDiagnostic(
                "warning",
                "lakefile-lean-not-evaluated",
                "lakefile.lean takes precedence and is not evaluated; its package name and targets are unknown.",
                "lakefile.lean",
            )
        )
        return LakeProject("lakefile.lean", None, None, ()), None
    if not _present(root / "lakefile.toml"):
        diagnostics.append(
            ProjectDiagnostic("error", "missing-lake-config", "The project has no lakefile.toml or lakefile.lean.")
        )
        return None, None
    text = _read_text(root, "lakefile.toml", diagnostics)
    if text is None:
        return None, None
    try:
        config = tomllib.loads(text)
    except (tomllib.TOMLDecodeError, RecursionError):
        diagnostics.append(
            ProjectDiagnostic("error", "invalid-lakefile-toml", "lakefile.toml is not valid TOML.", "lakefile.toml")
        )
        return None, None
    targets = tuple(
        LakeTarget(kind, entry["name"])
        for kind in ("lean_lib", "lean_exe")
        for entry in _tables(config.get(kind))
        if isinstance(entry.get("name"), str)
    )
    # Lake keeps the last of several requirements with the same name.
    requirement = next(
        (entry for entry in reversed(_tables(config.get("require"))) if entry.get("name") == "mathlib"), None
    )
    lake = LakeProject("lakefile.toml", _string(config.get("name")), _string(config.get("version")), targets)
    return lake, requirement


def _inspect_toolchain(root: Path, diagnostics: list[ProjectDiagnostic]) -> str | None:
    if not _present(root / "lean-toolchain"):
        diagnostics.append(ProjectDiagnostic("error", "missing-lean-toolchain", "The project has no lean-toolchain."))
        return None
    text = _read_text(root, "lean-toolchain", diagnostics)
    if text is None:
        return None
    toolchain = text.strip()
    if not toolchain or any(character.isspace() for character in toolchain):
        diagnostics.append(
            ProjectDiagnostic(
                "error", "invalid-lean-toolchain", "lean-toolchain must name exactly one toolchain.", "lean-toolchain"
            )
        )
        return None
    return toolchain


def _locked_mathlib(root: Path, relative: str, diagnostics: list[ProjectDiagnostic]) -> MathlibLock | None:
    """Read the Mathlib entry of a Lake manifest or package-overrides file, if any."""

    if not _present(root / relative):
        return None
    text = _read_text(root, relative, diagnostics)
    if text is None:
        return None
    try:
        payload = json.loads(text)
        packages = payload["packages"]
        version = payload.get("version", payload.get("schemaVersion"))  # overrides use schemaVersion
        if not _supported_manifest_version(version) or not isinstance(packages, list):
            raise ValueError(relative)
    except (AttributeError, KeyError, RecursionError, TypeError, ValueError):
        diagnostics.append(
            ProjectDiagnostic("error", "invalid-lake-manifest", f"{relative} is not a Lake manifest Autoform reads.", relative)
        )
        return None
    # Lake keeps the last of several packages with the same name.
    entry = next(
        (package for package in reversed(packages) if isinstance(package, dict) and package.get("name") == "mathlib"),
        None,
    )
    if entry is None:
        return None
    if entry.get("type") == "path":
        return MathlibLock("path", relative, dir=_string(entry.get("dir")))
    return MathlibLock(
        "git",
        relative,
        url=_string(entry.get("url")),
        input_rev=_string(entry.get("inputRev")),
        rev=_string(entry.get("rev")),
    )


def _supported_manifest_version(version: object) -> bool:
    """Lake 4.x reads integer versions from 7 and semantic versions below 2.0.0."""

    if isinstance(version, bool):
        return False
    if isinstance(version, int):
        return version >= 7
    return isinstance(version, str) and version.split(".", 1)[0] in {"0", "1"}


def _is_stale(requirement: dict, locked: MathlibLock) -> bool:
    revision = requirement.get("rev")
    git = requirement.get("git")
    return locked.type == "git" and (
        (isinstance(revision, str) and revision != locked.input_rev)
        or (isinstance(git, str) and canonical_git_url(git) != canonical_git_url(locked.url))
    )


def _read_text(root: Path, relative: str, diagnostics: list[ProjectDiagnostic]) -> str | None:
    """Read a small UTF-8 regular file; never opens FIFOs or devices."""

    path = root / relative
    try:
        if not path.is_file():
            raise OSError(relative)
        with path.open("rb") as handle:
            data = handle.read(_MAX_FILE_BYTES + 1)
        if len(data) > _MAX_FILE_BYTES:
            raise OSError(relative)
        return data.decode("utf-8")
    except (OSError, UnicodeError):
        diagnostics.append(
            ProjectDiagnostic(
                "error", "unreadable-file", f"{relative} is not a readable UTF-8 file of at most 1 MiB.", relative
            )
        )
        return None


def _present(path: Path) -> bool:
    try:
        return path.exists() or path.is_symlink()
    except OSError:
        return True


def _exists_exactly(root: Path, relative: str) -> bool:
    """Whether a path exists with exactly this spelling, even on a case-insensitive filesystem.

    A Lean library named `Blueprint` must not be mistaken for the `blueprint` vault.
    """

    directory = root
    for part in relative.split("/"):
        try:
            if part not in os.listdir(directory):
                return False
        except OSError:
            return False
        directory = directory / part
    return True


def _tables(value: object) -> list[dict]:
    return [entry for entry in value if isinstance(entry, dict)] if isinstance(value, list) else []


def _string(value: object) -> str | None:
    return value if isinstance(value, str) else None
