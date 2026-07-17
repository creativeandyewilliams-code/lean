/-!
# FMI-CNS expanded formalization candidate

Aggregator for the v16 load-bearing theorem package.  The source intentionally
uses explicit mathematical hypotheses and theorem parameters rather than
empirical axioms.  Run `lake build` and `lake env lean AxiomReport.lean` before
claiming kernel closure.
-/
import FmiCnsFull.Core.Types
import FmiCnsFull.Core.Semantics
import FmiCnsFull.Core.Signal
import FmiCnsFull.Reflective.Subspace
import FmiCnsFull.Projection.Conflation
import FmiCnsFull.FMI.Operations
import FmiCnsFull.FMI.Topology
import FmiCnsFull.FMI.Choice
import FmiCnsFull.Order.Composition
import FmiCnsFull.Order.Span
import FmiCnsFull.Fragmentation.Backlog
import FmiCnsFull.Fragmentation.Regional
import FmiCnsFull.Fragmentation.SemanticLoss
import FmiCnsFull.CNS.Lift
import FmiCnsFull.CNS.NearSingular
import FmiCnsFull.CNS.Dynamic
import FmiCnsFull.Governance.Options
import FmiCnsFull.Governance.ProjectionAdequacy
import FmiCnsFull.Propagation.Regenerative
import FmiCnsFull.GreatFilter.Necessary
import FmiCnsFull.GreatFilter.Admissibility
import FmiCnsFull.GreatFilter.Conditional
import FmiCnsFull.CST.Transport
import FmiCnsFull.CST.Closure
import FmiCnsFull.TopLevel.FormalCoherence
import FmiCnsFull.TopLevel.ConditionalFilter
import FmiCnsFull.External.Premises
import FmiCnsFull.Tests.FiniteExamples
import FmiCnsFull.Tests.Countermodels
import FmiCnsFull.Tests.MutationChecks
