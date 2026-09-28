import Skel.Vendor

namespace Skel.Semantics

syntax "semanticMacro" : term

macro_rules
  | `(semanticMacro) => `(1)

def expandedMacro : Nat := semanticMacro

def opaqueSeed : Nat := 1

opaque opaqueWitness : Nat := opaqueSeed

theorem usesOpaque : opaqueWitness = opaqueWitness := rfl

def selectedProposition : Prop := Vendor.Choice.proposition

def «quoted.helper» : Nat := 1

theorem usesQuoted : «quoted.helper» = 1 := rfl

def notationMarker : Nat := 1

def interpolationSmoke : String := s!"value {"a--b"}"

def matchBody : Nat → Nat
  | 0 => 10
  | n + 1 => n

def visible._helper : Nat := 1

def visible : Nat := visible._helper

def firstOnLine : Nat := 1 theorem secondOnLine : firstOnLine = 1 := rfl

def safeValue : Nat := 1

unsafe def unsafeValue : Nat := 1

partial def partialValue (n : Nat) : Nat := partialValue n

universe u

def universeNamed (α : Type u) : Type u := α

end Skel.Semantics
