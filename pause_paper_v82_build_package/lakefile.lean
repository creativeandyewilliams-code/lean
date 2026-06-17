import Lake
open Lake DSL

package «pausePaperV82» where
  -- Pure-Lean skeleton; no external (Mathlib) dependency required.
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib «ClaimStatusRouting» where
  roots := #[`ClaimStatusRouting.RoutingSkeleton]
