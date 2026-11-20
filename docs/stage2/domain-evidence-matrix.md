# Stage 2 — Domain Evidence Matrix v0.1

**Status:** Architecture input; candidate concepts and allocations are not approved package design.

**Scope:** Documentation only. This matrix does not modify or reinterpret MASS-SK-1.0 and does not define SysML packages.

## 1. Purpose

The Domain Evidence Matrix is the first controlled architecture artifact for Stage 2. It records domain evidence, semantic questions, stable Kernel anchors, candidate package allocations, known deferred gaps, and decisions needed before package design.

Its purpose is to provide traceability:

```text
evidence → domain semantics → Kernel anchor → package allocation → CQ
```

The matrix is an input to:

- **2.0-A — Domain Library Scope**;
- **2.0-B — Package Responsibility**;
- **2.0-C — Dependency Matrix**.

The matrix does not claim that a candidate concept is already part of the Domain Library, that a competency question (CQ) has been added or passed, or that a new Semantic Kernel gap exists.

## 2. Architectural rule

Every concept proposed for Stage 2 must be justified by at least one of these relationships:

1. it specializes a relevant MASS-SK-1.0 Kernel abstraction;
2. it concretizes an existing Kernel semantic chain or extension point; or
3. it is a supporting domain concept needed by a concept in category 1 or 2, with an explicit rationale and dependency.

A direct Kernel specialization parent is not mandatory for a supporting concept. Absence of such a parent alone is not evidence of a Kernel gap. No Stage 2 concept becomes a Kernel primitive automatically.

## 3. Evidence Matrix

Priority is a proposed Stage 2 sequencing aid only: **P1** foundational traceability or a named deferred gap; **P2** domain refinement dependent on unresolved semantics; **P3** explicitly deferred or outside the current declarative scope. Priority does not approve scope or allocation.

| ID | Evidence / Rationale | Proposed Concept or Semantic Area | Kernel Anchor | Semantic Chain | Candidate Package | DL-GAP | Priority | Status | Open Decision |
|---|---|---|---|---|---|---|---|---|---|
| E-01 | MASS-SK-1.0 provides `TechnicalAgent`, `NavigationFunction`, and generic `AssessmentEvidence`; detailed sensing concepts are domain refinement, not a reason to expand the Kernel. | `SensorSystem`, `NavigationSensor`, `Observation`, `SensorFusion`, `FusionResult` | `TechnicalAgent`; `NavigationFunction`; `AssessmentEvidence` | Sensor → Observation → Fusion → situation representation | `MASSSensing` | — | P1 | Candidate; scope and responsibilities pending 2.0-A/B | Decide whether `SensorSystem` is a system, technical agent, or a supporting specialization; define observation and fusion-result boundaries without embedding fusion algorithms. |
| E-02 | The proposed perception sequence is not yet a settled domain vocabulary or type hierarchy. | Observation → Fusion → perceived situation | `NavigationFunction`; `AssessmentEvidence`; operational assessment context | Sensor → Observation → Fusion → perceived situation | `MASSSensing` / `MASSNavigation` | — | P2 | Terminology review required; no single concept admitted | Define “perception”, “fusion”, and “perceived situation”; decide ownership of the hand-off between sensing and navigation. |
| E-03 | The Kernel supplies assessment/context anchors but does not establish that “situation awareness” is one kind of entity. Candidate meanings have different semantic roles. | Human situation awareness; machine situation assessment; shared/operational picture; information artifact | `OperationalAssessmentContext`; `OperationalConditionAssessment`; `AssessmentEvidence`; `RemoteOperationContext` | Situation representation → assessment / shared information → decision | Unresolved; decide in 2.0-A/B | — | P2 | Semantics unresolved; do not define a single `SituationAwareness` type | Decide which candidates are cognitive capability, assessment activity/result, shared representation, or information artifact; define their producers, consumers, and identity. |
| E-04 | MASS-SK-1.0 distinguishes behavioral functions, occurrence contexts, assessment results, and control actions. A generic “decision” could denote any of these and must not collapse them. | Decision as behavior; occurrence; result; policy/control choice | `MASSFunction`; `OperationalAssessmentContext`; `OperationalConditionAssessment`; `ControlAction` | situation representation → decision (meaning unresolved) → ControlAction | Unresolved; decide in 2.0-A/B | — | P2 | Semantics unresolved; no definition admitted | Decide whether each use means a decision process, decision event, decision result, policy selection, or issued control choice, and whether more than one concept is required. |
| E-05 | The baseline identifies MASS–ROC association, remote-operation sessions, ODD, and operational-condition assessment; communication-specific entities and degradation details are not Kernel primitives. | `CommunicationSystem`, `CommunicationLink`, `ConnectivityState`, `Handover`, `Failover` | `RemoteOperationSession`; `OperationalDesignDomain`; `OperationalConditionAssessment` | MASS ↔ Communication ↔ ROC ↔ RemoteOperator ↔ Supervision/Authority ↔ MASSFunction | `MASSCommunication` | — | P1 | Candidate; scope and responsibilities pending 2.0-A/B | Define system versus link, connectivity-state scope, and how handover/failover evidence affects capability and ODD assessment. Do not equate loss of communication directly with `FallbackState`. |
| E-06 | The Kernel already distinguishes `RemoteOperationsCentre`, `RemoteOperator`, session, function, performer, supervisor, and authority holder. ROC workstations and support capabilities are decomposition candidates, not a basis for making ROC a MASS part. | `OperatorWorkstation`, `HumanMachineInterface`, `DecisionSupport`, `SituationAwarenessSupport`, `SupervisoryControl` | `RemoteOperationsCentre`; `RemoteOperator`; `RemoteOperationSession` | MASS ↔ Communication ↔ ROC ↔ RemoteOperator ↔ Supervision/Authority ↔ MASSFunction | Unresolved; package allocation and decomposition required | — | P2 | Package allocation unresolved | Decide which concepts are ROC structure, human-machine interaction, information support, supervision behavior, or control authority; preserve distinct performer, supervisor, and authority-holder semantics. |
| E-07 | The scope boundary defers detailed environmental predicates. The existing `OperationalDesignDomain` is the anchor for specifying conditions, not a physical vessel part. | Environmental; geographic; traffic; infrastructure; communication; positioning; capability-dependency dimensions | `OperationalDesignDomain`; `OperationalEnvelope`; `OperationalConditionAssessment` | Environment + Traffic + Port/VTS + Communications + Positioning → ODD conditions → effectiveODD → operational assessment | Candidate: ODD-related Domain Library package; exact package name/responsibility pending 2.0-B | — | P1 | Candidate dimensions; definition and allocation pending | Define dimension vocabulary, units/representation, applicability, and evidence needed to determine effective ODD; retain the distinction between ODD and Operational Envelope. |
| E-08 | Ports, VTS, waterways, traffic, and infrastructure are environmental/domain context candidates. The Kernel does not make these physical parts of a MASS or assign their package ownership. | VTS; port; mixed traffic; waterway; positioning infrastructure; external communication infrastructure | `OperationalDesignDomain`; `RemoteOperationsCentre`; `RemoteOperationSession` | Environment + Traffic + Port/VTS + Communications + Positioning → ODD conditions → effectiveODD → operational assessment | Unresolved; package allocation explicitly open | — | P2 | Package allocation unresolved | Decide which are environment entities, infrastructure systems, organizations/services, or contextual references; determine ownership and dependencies without treating ROC as a composite part of `MaritimeAutonomousSurfaceShip`. |
| E-09 | The scope boundary explicitly identifies generic `AssessmentEvidence` and defers maritime collision-risk evidence. Numerical values and sensor observations are domain evidence, not Kernel primitives. | DCPA; TCPA; CPA; relative bearing; relative velocity; COG; SOG | `AssessmentEvidence`; `CollisionRiskAssessment`; `CollisionRiskResult`; `COLREGSituation` | Observation/evidence → CollisionRiskAssessment → CollisionRiskResult | Allocation unresolved; candidate collision-risk or navigation package | DL-GAP-02 | P1 | Deferred gap candidate; exact concept definitions and allocation pending | Define units, reference frames, time basis, uncertainty, source, and whether each value is observation, derived measure, or assessment input. Keep automatic calculation outside declarative Domain Library scope unless separately approved. |
| E-10 | The deferred evidence list includes source identity, timestamp, uncertainty, confidence, prediction horizon, and risk-method provenance. Provenance can support evidence and assessments without changing their Kernel meaning. | Source; timestamp; uncertainty; confidence; prediction horizon; assessment-method provenance | `AssessmentEvidence`; `CollisionRiskAssessment`; `CollisionRiskResult`; `OperationalConditionAssessment` | evidence → provenance/metadata → assessment → result | `MASSMetadata` | DL-GAP-02 (evidence provenance subset) | P1 | Candidate supporting domain concepts; dependency and scope pending | Decide whether these are metadata features or separately reusable supporting concepts; specify which evidence/assessment objects require each and avoid duplicate provenance semantics. |
| E-11 | MASS-SK-1.0 can require a `FallbackState` for an Operational Envelope violation, but explicitly leaves the violation-specific strategy open. | Reduced speed; stop; loiter; safe anchoring; remote-control request; return to safe area; minimum-risk maneuver | `FallbackState`; `OperationalEnvelope`; `OperationalConditionAssessment` | Sensor/Communication degradation → evidence degradation → capability impact → effectiveODD impact → `OperationalConditionAssessment` → Degraded/Fallback | Unresolved; decide in 2.0-A/B | DL-GAP-01 | P1 | Deferred gap; candidate strategies are not selected or ranked | Define the conditions and authority for selecting a strategy, the strategy versus its execution/control action, and the relationship to assessed operational condition. Do not make communication degradation itself a `FallbackState`. |
| E-12 | The baseline represents encounter situations and a safety applicability context; detailed give-way/stand-on obligations and rule applicability are explicitly deferred. | Give-way / stand-on roles and encounter-specific obligations | `COLREGSituation`; `SafetyApplicabilityContext` | encounter / situation → applicability context → obligation / safety response | Unresolved; candidate safety or navigation package, allocation pending | DL-GAP-03 | P1 | Deferred gap; applicability semantics and allocation pending | Decide how roles and obligations depend on encounter context and evidence; keep encounter classification, obligation, and assessment distinct. No automatic encounter-classification algorithm is included here. |
| E-13 | The Kernel provides `SafetyConstraint`, `SafetyApplicabilityContext`, and `ControlAction`, while concrete safety rules are deferred. | Concrete safety constraints applicable to situation, function, or control action | `SafetyConstraint`; `SafetyApplicabilityContext`; `ControlAction` | situation / function / control action → safety applicability → applicable constraint | Unresolved; safety package responsibility pending 2.0-B | DL-GAP-03 | P1 | Deferred gap; no new rule set admitted | Decide constraint categories, applicability inputs, and traceability to hazard/loss or other safety work; avoid duplicating Kernel subject/context semantics. |
| E-14 | The baseline `ControlAction` is intentionally minimal; detailed commands, feedback, timing, and STPA-compatible control structures are deferred. Function allocation is separately represented by `ModeFunctionAssignment`. | Commands; feedback; authority-dependent control action | `ControlAction`; `ModeFunctionAssignment` | decision → ControlAction → affected system / feedback | `MASSControl` | — | P2 | Candidate; control scope and relationship to assignment pending | Decide declarative command/feedback semantics and how authority constrains a control action; do not merge performer, supervisor, and authority-holder roles. |
| E-15 | Responsibility and liability are not current Kernel or core Domain Library concepts. Operational role semantics do not establish organizational or legal responsibility. | Responsibility / Liability (deferred future semantic area) | `RemoteOperator`; `RemoteOperationSession`; `ModeFunctionAssignment` only as operational-role anchors, not liability definitions | MASS ↔ ROC ↔ RemoteOperator ↔ Supervision/Authority; organizational/legal accountability remains outside this chain | Deferred; no current package allocation | — | P3 | Deferred / future decision | Preserve `operational authority ≠ organizational responsibility ≠ legal liability`. Do not place liability in the Kernel or current core Domain Library without a later architecture decision. |
| E-16 | The scope boundary assigns calculations and automatic evaluation to Analysis & Simulation or later stages, not declarative Domain Library semantics. | Automatic TCPA calculation; sensor-fusion algorithms; automatic COLREG encounter classification; maneuver optimization; automatic fallback selection | Relevant domain inputs/results may anchor to `AssessmentEvidence`, `COLREGSituation`, `OperationalConditionAssessment`, or `FallbackState`; algorithms do not specialize these merely by consuming them | evidence / situation / assessment inputs → executable analysis → derived result or proposed response | Analysis & Simulation or subsequent stages; outside current declarative Domain Library scope | — | P3 | Out of current scope unless explicitly allocated later | Decide execution ownership, inputs/outputs, and validation strategy in a later-stage architecture decision; do not encode executable algorithms as declarative domain definitions in this work. |

## 4. Semantic Chains

These chains organize traceability across candidate areas; they do not assert that every arrow is already a Kernel relationship or an approved Domain Library dependency.

1. **Sensing, decision, and control**

   ```text
   Sensor → Observation → Fusion → Situation representation → Decision → ControlAction
   ```

   The meanings and boundaries of “situation representation” and “Decision” remain open under E-02 through E-04.

2. **Degradation and operational condition**

   ```text
   Sensor/Communication degradation → evidence degradation → capability impact
   → effectiveODD impact → OperationalConditionAssessment → Degraded/Fallback
   ```

   A degradation is evidence or a capability/ODD impact, not itself a `FallbackState`. The existing Kernel distinction between `ModeOfOperation` and `OperationalCondition` remains unchanged.

3. **Remote operation and supervision**

   ```text
   MASS ↔ Communication ↔ ROC ↔ RemoteOperator
   ↔ Supervision/Authority ↔ MASSFunction
   ```

   The chain does not make ROC a composite part of `MaritimeAutonomousSurfaceShip` and does not merge performer, supervisor, and authority holder.

4. **ODD context and assessment**

   ```text
   Environment + Traffic + Port/VTS + Communications + Positioning
   → ODD conditions → effectiveODD → operational assessment
   ```

   Detailed dimensions and evidence rules remain candidate Domain Library semantics; the Kernel's ODD/OE contract is protected.

## 5. Protected Kernel Contracts and Modeling Constraints

The following are constraints on subsequent Stage 2 design, taken from the baseline scope and change-control records. This matrix does not redefine them:

- Keep `ModeOfOperation` and `OperationalCondition` as separate semantic dimensions. Do not treat `DegradedState` or `FallbackState` as modes.
- Preserve the Kernel's performer, supervisor, and authority-holder distinctions.
- Preserve `RemoteOperationsCentre` as associated/referenced operational structure, not a composite part of `MaritimeAutonomousSurfaceShip`.
- Preserve the existing ODD and Operational Envelope semantics and assessment traceability.
- Do not introduce `AutonomyLevel` as a replacement for `ModeOfOperation` or `ModeFunctionAssignment`.
- Do not treat DCPA or TCPA as Kernel primitives.
- Do not model communication degradation directly as `FallbackState`; it may affect capability/ODD assessment and thereby operational condition.
- Do not interpret absence of a direct Kernel specialization parent as a new Kernel gap when an explicitly justified supporting concept can supply the needed domain semantics.
- Any genuine deficiency in a protected Kernel contract must be recorded and processed under change control; it is not resolved by editing the released baseline in Stage 2.

## 6. Traceability and Decision Gates

For 2.0-A through 2.0-C, each concept proposed for admission should retain or add:

1. its evidence/rationale and semantic meaning;
2. its Kernel anchor, chain position, or explicit supporting-concept dependency;
3. its package owner and dependency direction, once decided;
4. its relation to an existing or proposed CQ (or an explicit statement that no CQ mapping is yet approved);
5. its unresolved decisions, status, and any relevant DL-GAP.

Package candidates marked **unresolved** are not assignments. Package ownership, dependencies, and CQ traceability are decisions for the named downstream work items; they must not be silently inferred from this matrix.

## 7. Evidence Sources and Limitations

This v0.1 matrix is grounded in the repository's existing MASS-SK-1.0 contracts:

- [Baseline manifest](../../MASSKernel_v1.0_manifest.md) — production inventory and the Kernel concepts available as anchors.
- [Scope boundary](../../MASSKernel_v1.0_scope_boundary.md) — in-scope/out-of-scope boundary, DL-GAP-01 through DL-GAP-03, deferred algorithms, and the Kernel/Domain Library boundary.
- [Change-control record](../../MASSKernel_v1.0_change_control.md) — protected architectural decisions and Stage 2 integration policy.
- [Released Kernel source](../../MASSKernel_v1.0.sysml) — source definitions referenced as anchors in this matrix.

No new normative SysML v2/KerML claim is made in this document. Hypha was not used for this matrix; it does not claim normative verification. The referenced Stage 1 validation records are historical baseline evidence, not checks rerun for this documentation change.
