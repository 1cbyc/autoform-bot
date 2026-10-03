from __future__ import annotations

import os
from pathlib import Path

import pytest

from autoform_cli.lean import snapshot_project_sources


@pytest.mark.skipif(os.name != "nt", reason="Windows capability boundary")
def test_windows_source_snapshot_fails_closed_without_handle_relative_enumeration(
    tmp_path: Path,
) -> None:
    (tmp_path / "A.lean").write_text(
        "theorem notReadUnsafely : True := trivial\n",
        encoding="utf-8",
    )

    with pytest.raises(OSError, match="safe directory traversal is unavailable"):
        snapshot_project_sources(tmp_path)
