import Lake
open Lake DSL

package «fssGravitySectorV12» where
  -- Pure-Lean skeleton; no external (Mathlib) dependency required.
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib «FssGravitySector» where
  roots := #[`FssGravitySector.RoutingSkeleton]
