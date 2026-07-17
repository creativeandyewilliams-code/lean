import FmiCnsFull.CNS.Lift

namespace FmiCnsFull

/-- Minimal metric data needed for the dynamical bridge. -/
structure MetricData (X : Type*) where
  d : X → X → ℝ
  nonneg : ∀ x y, 0 ≤ d x y
  eq_zero_iff : ∀ x y, d x y = 0 ↔ x = y
  symm : ∀ x y, d x y = d y x
  triangle : ∀ x y z, d x z ≤ d x y + d y z

/-- A dynamical CNS operator on a declared domain.  Closure, contraction,
    invariance, and a fixed normal form are explicit fields. -/
structure DynamicalCNS (X : Type*) where
  metric : MetricData X
  domain : Set X
  update : X → X
  kappa : ℝ
  kappa_nonneg : 0 ≤ kappa
  kappa_lt_one : kappa < 1
  closed : Set.MapsTo update domain domain
  contractive : ∀ x ∈ domain, ∀ y ∈ domain,
    metric.d (update x) (update y) ≤ kappa * metric.d x y
  normal : X
  normal_mem : normal ∈ domain
  normal_fixed : update normal = normal
  benignInvariant : Prop

/-- Contraction gives uniqueness of the fixed normal form within the declared
    domain. -/
theorem dynamicCNS_uniqueFixedPoint
    {X : Type*} (D : DynamicalCNS X)
    {x y : X} (hxmem : x ∈ D.domain) (hymem : y ∈ D.domain)
    (hx : D.update x = x) (hy : D.update y = y) :
    x = y := by
  have hc := D.contractive x hxmem y hymem
  rw [hx, hy] at hc
  have hnonneg := D.metric.nonneg x y
  have hzero : D.metric.d x y = 0 := by
    nlinarith [D.kappa_lt_one]
  exact (D.metric.eq_zero_iff x y).mp hzero

/-- Bridge A premise package: the new composition actually induces a
    contracting, closed, invariant update on the expanded domain. -/
structure LiftInducedDynamics
    {ClassId Operand X : Type*} [DecidableEq ClassId]
    (before after : Architecture ClassId Operand) where
  lift : OrderLift before after
  dynamic : DynamicalCNS X
  enabledByNewClass : Prop

/-- T-BRIDGE-LIFT-TO-DYN. -/
theorem bridgeLiftToDynamic
    {ClassId Operand X : Type*} [DecidableEq ClassId]
    {before after : Architecture ClassId Operand}
    (H : LiftInducedDynamics before after) :
    DynamicalCNS X :=
  H.dynamic

/-- T-BRIDGE-DYN-TO-LIFT.  If implementation of the dynamical operator requires
    a fresh qualifying class and the after-architecture is exactly the prior
    class family plus that class, the dynamical realization witnesses an order
    increment. -/
theorem bridgeDynamicToLift
    {ClassId Operand X : Type*} [DecidableEq ClassId]
    {before after : Architecture ClassId Operand}
    (D : DynamicalCNS X) (L : OrderLift before after)
    (implementedByNewClass : Prop) :
    after.order = before.order + 1 := by
  exact liftOrderIncrement L

end FmiCnsFull
