# Stage 2.0-A — MASS Domain Library Scope

**Version:** 0.1

**Status:** Controlled scope decision; package architecture remains for 2.0-B/2.0-C.
**Basis:** Accepted [Domain Evidence Matrix v0.1](domain-evidence-matrix.md) and MASS-SK-1.0 baseline contracts.

## 1. Purpose

This document defines the semantic scope of the Stage 2 MASS Domain Library (DL). It identifies which declarative maritime-domain semantics may be developed above the released MASS Semantic Kernel, which areas require further semantic decisions, and which work belongs to other framework layers or later stages.

The scope supports traceability:

```text
evidence → domain semantics → Kernel anchor → package allocation → CQ
```

This is a scope decision, not a package design or implementation specification. Candidate concepts listed here are not SysML definitions and do not imply that any Stage 2 package already exists.

## 2. Baseline Contract

MASS-SK-1.0, identified by `MASSKernel_v1.0.sysml`, is the stable semantic foundation and is not modified or reinterpreted by Stage 2. Domain Library concepts extend or use that contract; they do not silently replace it.

Stage 2 shall preserve, at minimum:

- `ModeOfOperation ≠ OperationalCondition`.
- `DegradedState` and `FallbackState` are operational conditions, not modes of operation.
- ODD and Operational Envelope remain distinct operational specifications; detailed ODD predicates and automatic membership evaluation are outside the Kernel.
- `RemoteOperationsCentre` is associated/referenced operational structure, not a composite part of `MaritimeAutonomousSurfaceShip`.
- `performer`, `supervisor`, and `authority holder` remain distinct roles.
- `ModeFunctionAssignment` continues to represent mode, function, performer, supervisor, authority holder, and effective ODD without being replaced by one `AutonomyLevel`.
- Operational assessment, collision-risk evidence/results, and safety applicability retain their Kernel context and traceability anchors.
- Communication degradation is not itself a `FallbackState`; it may contribute evidence of capability or effective-ODD impact and thereby inform `OperationalConditionAssessment`.
- DCPA and TCPA are domain evidence/measure candidates, not Kernel primitives.

If proposed DL semantics expose a genuine deficiency in a protected Kernel contract, record it for formal change control. Do not repair it by altering the released baseline within Stage 2.

## 3. Domain Concept Admission Rule

Every concept admitted to the Domain Library shall satisfy at least one of these criteria and document its evidence, Kernel anchor or supporting dependency, and intended CQ traceability:

1. **Kernel specialization:** specializes a relevant MASS-SK-1.0 abstraction without changing that abstraction's meaning.
2. **Semantic-chain concretization:** gives declarative domain meaning to an existing Kernel chain, role, context, evidence, result, condition, or extension point.
3. **Justified supporting domain concept:** is needed by a concept in either category above and records why it is needed and the dependency it supports. A direct Kernel specialization parent is not required for this category.

Lack of a direct Kernel parent alone does not establish a Kernel gap. Admission does not make a concept a Kernel primitive. A candidate remains conditional until its semantic meaning is sufficiently clear and 2.0-B assigns package responsibility.

## 4. In-Scope Semantic Areas

The following declarative semantic areas are admitted to Stage 2 scope, subject to the per-area limits and open decisions in Section 7:

- **Sensing and evidence description:** domain descriptions of sensing sources, observations, sensor identity, and evidence used by navigation or assessment. Kernel anchors include `TechnicalAgent`, `NavigationFunction`, and `AssessmentEvidence`.
- **Communication context:** declarative representation of communication systems/links, connectivity states, and handover/failover events as operational context or evidence. Anchors include `RemoteOperationSession`, `OperationalDesignDomain`, and `OperationalConditionAssessment`.
- **ODD dimension vocabulary:** declarative environmental, geographic, traffic, infrastructure, communication, positioning, and capability-dependency conditions associated with `OperationalDesignDomain`. This does not include automatic evaluation of whether a MASS or function is inside an ODD or Operational Envelope.
- **Maritime collision-risk evidence:** domain descriptions of DCPA, TCPA, CPA, relative bearing/velocity, COG, SOG, and their provenance as evidence relevant to `CollisionRiskAssessment` and `CollisionRiskResult`.
- **Metadata and provenance:** source, timestamp, uncertainty, confidence, prediction horizon, and assessment-method provenance when justified as supporting concepts for evidence, assessments, or results.
- **Fallback strategy vocabulary:** declarative descriptions of candidate strategies such as reduced speed, stop, loiter, safe anchoring, remote-control request, return to safe area, or minimum-risk maneuver. Selection, optimization, and execution are not admitted as algorithms.
- **COLREG applicability and safety response:** declarative encounter-specific role/obligation descriptions and concrete safety-constraint applicability linked to `COLREGSituation`, `SafetyApplicabilityContext`, `SafetyConstraint`, `MASSFunction`, or `ControlAction`. This does not include automatic encounter classification or complete STPA semantics.

These areas concretize the baseline's extension points and the deferred **DL-GAP-01** (violation-specific fallback strategies), **DL-GAP-02** (maritime collision-risk evidence), and **DL-GAP-03** (concrete safety applicability rules). The gaps remain deferred until their Stage 2 semantics are designed; this scope document does not claim that they are implemented or closed.

## 5. Conditionally In-Scope Concepts

The following may enter the DL only after the stated semantic questions are resolved. Their presence in the matrix is not admission of a named definition:

- **Perception and situation representation:** E-02 may define a stable vocabulary and declarative hand-off from observation/fusion to a represented situation. Do not define a single `Perception` type before terminology and boundaries are decided.
- **Situation awareness:** E-03 must distinguish human situation awareness, machine situation assessment, a shared/operational picture, and an information artifact. Do not define one `SituationAwareness` type until a separate semantic decision identifies its meaning, producer, consumer, and identity.
- **Decision:** E-04 must distinguish behavior, occurrence, result, and policy/control choice. Do not define a generic `Decision` concept until the intended semantic role is decided; more than one concept may be required.
- **ROC decomposition and support:** E-06 concepts such as `OperatorWorkstation`, `HumanMachineInterface`, `DecisionSupport`, `SituationAwarenessSupport`, and `SupervisoryControl` may be considered after their structural, informational, behavioral, and authority semantics are distinguished.
- **Operational environment:** E-08 concepts such as VTS, port, mixed traffic, waterway, positioning infrastructure, and external communication infrastructure may be included where needed to describe ODD context or evidence. Their roles as environment, infrastructure, service, organization, or contextual reference must first be decided.
- **Control detail:** E-14 may add declarative command, feedback, or authority-dependent control semantics that concretize `ControlAction` and `ModeFunctionAssignment`. It excludes executable control logic and must preserve distinct performer, supervisor, and authority-holder roles.

No final package allocation for these concepts is made here.

## 6. Explicitly Out-of-Scope Areas

The following are outside the declarative MASS Domain Library scope defined by this document:

- Executable or automatic algorithms: TCPA/CPA calculation, sensor-fusion algorithms, automatic COLREG encounter classification, maneuver optimization, automatic fallback selection, and automatic ODD/Operational Envelope membership evaluation. These belong to Analysis & Simulation or a later explicitly authorized stage.
- Runtime execution engines, transition guards, automatic activation/derivation of functions or remote operation, and automatic generation of snapshots from assignments.
- Complete STPA constructs and analysis workflows, including losses, hazards, unsafe control actions, causal scenarios, controllers, controlled processes, and feedback-control analysis. Safety-related declarative domain applicability may be in scope; STPA integration remains a later safety-engineering stage.
- Reference Architecture decomposition, deployment topology, and system instantiation. The DL supplies reusable domain semantics; architecture allocates and uses them.
- Organizational responsibility and legal liability as current Kernel or core DL concepts. Preserve `operational authority ≠ organizational responsibility ≠ legal liability`; any future treatment requires a separate architecture decision.
- Any change to MASS-SK-1.0 semantics, including changing multiplicities or relationships to accommodate a DL concept.

## 7. Decisions for E-01…E-16

These decisions define scope disposition, not final terminology, package ownership, or a claim that the concept is implemented.

| ID | Stage 2.0-A scope decision | Conditions / deferred decision |
|---|---|---|
| E-01 Sensing | **In scope** as declarative sensing-source and observation semantics linked to `TechnicalAgent`, `NavigationFunction`, and `AssessmentEvidence`. | Decide whether `SensorSystem` is a system, technical agent, or supporting concept; specify observation and `FusionResult` boundaries. Fusion algorithms are excluded. |
| E-02 Perception chain | **Conditional**: a declarative observation/fusion/situation-representation chain may be admitted after terminology review. | Keep “perceived situation” and the sensing/navigation boundary unresolved; no single `Perception` definition is approved. |
| E-03 Situation Awareness | **Conditional; semantic decision required.** | Keep human awareness, machine assessment, shared/operational picture, and information artifact distinct as candidates. No unified `SituationAwareness` type. |
| E-04 Decision | **Conditional; semantic decision required.** | Distinguish behavior, occurrence, result, and policy/control choice. No generic `Decision` definition is approved. |
| E-05 Communications | **In scope** as declarative communication context, connectivity state, and handover/failover evidence related to remote operation and operational assessment. | Decide system/link/state/event boundaries and how evidence informs capability/effective ODD. Communication degradation is not `FallbackState`. |
| E-06 ROC decomposition | **Conditional** as domain semantics supporting remote operations. | Resolve the meanings and dependencies of workstation, HMI, decision/situation support, and supervisory control. Do not make ROC a composite part of MASS or merge operational roles. |
| E-07 ODD dimensions | **In scope** for declarative condition and dimension vocabulary associated with `OperationalDesignDomain`. | Define dimensions, units/representation, applicability, and evidence. Automatic ODD/OE membership calculation is excluded. |
| E-08 Operational environment | **Conditional** for environmental and infrastructure context needed to describe ODD conditions or evidence. | Decide entity versus service versus contextual-reference semantics for VTS, port, waterways, traffic, and infrastructure. No package ownership is assigned. |
| E-09 Maritime collision-risk evidence | **In scope** for declarative domain evidence associated with `AssessmentEvidence`, `CollisionRiskAssessment`, and `CollisionRiskResult`; this addresses the subject of **DL-GAP-02**. | Define units, reference frames, time basis, uncertainty, and whether values are observed or derived. DCPA/TCPA are not Kernel primitives; automatic calculation is excluded. |
| E-10 Metadata / provenance | **In scope** as justified supporting concepts for evidence, assessment, and result traceability. | Decide reusable metadata shape and applicability; avoid duplicate provenance semantics. Included as an evidence/provenance part of **DL-GAP-02**, not a new Kernel gap. |
| E-11 Fallback semantics | **In scope** for declarative violation-specific strategy descriptions under **DL-GAP-01**. | Define strategy meaning and relation to assessed condition separately from selection/execution. No automatic selection; degradation alone does not imply `FallbackState`. |
| E-12 COLREG applicability | **In scope** for declarative encounter-role and obligation applicability under **DL-GAP-03**. | Define how obligations depend on encounter context and evidence. Keep roles, encounter classification, and assessment distinct; automatic classification is excluded. |
| E-13 Safety response | **In scope** for concrete declarative safety constraints and their applicability under **DL-GAP-03**. | Refine applicability using Kernel subject/context anchors. Full STPA semantics and analysis are outside this scope. |
| E-14 Control semantics | **Conditional** for declarative command, feedback, and authority-dependent control concepts linked to `ControlAction` and `ModeFunctionAssignment`. | Decide the declarative boundary and preserve performer/supervisor/authority-holder distinctions. Executable control logic and STPA control-loop analysis are excluded. |
| E-15 Responsibility / Liability | **Out of scope; deferred/future semantic area.** | Preserve `operational authority ≠ organizational responsibility ≠ legal liability`. No Kernel or current core DL allocation without a later architecture decision. |
| E-16 Executable algorithms | **Out of scope** for the declarative Domain Library. | Assign automatic calculation, fusion, classification, optimization, and fallback selection to Analysis & Simulation or a later explicitly authorized stage. |

## 8. Cross-Domain Semantic Chains

The following chains provide scope-level traceability between admitted and conditional areas. Arrows describe candidate information or semantic dependencies, not new Kernel relationships or approved package dependencies.

1. **Sensing, situation, decision, and control**

   ```text
   Sensor → Observation → Fusion → Situation representation → Decision → ControlAction
   ```

   E-02, E-03, and E-04 remain unresolved until their semantic decisions are made.

2. **Degradation and operational condition**

   ```text
   Sensor/Communication degradation → evidence degradation → capability impact
   → effectiveODD impact → OperationalConditionAssessment → Degraded/Fallback
   ```

   Degradation can inform capability/ODD assessment; it is not itself a `FallbackState`. `ModeOfOperation` remains orthogonal to `OperationalCondition`.

3. **Remote operation, communications, and authority**

   ```text
   MASS ↔ Communication ↔ ROC ↔ RemoteOperator
   ↔ Supervision/Authority ↔ MASSFunction
   ```

   This chain does not imply ROC containment in MASS or collapse the performer, supervisor, and authority-holder roles.

4. **Environment, ODD, and assessment**

   ```text
   Environment + Traffic + Port/VTS + Communications + Positioning
   → ODD conditions → effectiveODD → operational assessment
   ```

   E-07 and E-08 define candidate declarative context; they do not automatically evaluate ODD membership.

5. **Collision-risk evidence and result**

   ```text
   Observation / maritime evidence + provenance
   → CollisionRiskAssessment → CollisionRiskResult
   ```

   The chain refines the existing traceability contract; calculations that produce evidence remain outside the DL.

6. **Fallback and safety applicability**

   ```text
   OperationalConditionAssessment / encounter context
   → applicable strategy or safety constraint
   → separately authorized control action
   ```

   Strategy selection, safety analysis execution, and control execution are not implied by declarative descriptions.

## 9. Boundary Between 2.0-A and 2.0-B / 2.0-C

**2.0-A — Domain Library Scope (this document)** decides the semantic subject matter, admission rule, conditional areas, exclusions, and protected Kernel boundaries.

**2.0-B — Package Responsibility** must decide package boundaries and ownership, including:

- whether proposed packages such as `MASSSensing`, `MASSCommunication`, `MASSMetadata`, or `MASSControl` are retained, renamed, split, or combined;
- the boundary between sensing and navigation, and between ODD conditions and operational-environment context;
- whether separate `MASSRemoteOperations` and `MASSOperationalEnvironment` packages should exist;
- the disposition and responsibility of `MASSCore`;
- ownership of unresolved/conditional E-02, E-03, E-04, E-06, E-08, and E-14 concepts.

**2.0-C — Dependency Matrix** must decide import/dependency relationships and directions after package responsibility is known. This scope document does not prescribe an import graph, dependency direction, or package-level API.

All three follow-on decisions must preserve the baseline contract and retain concept-to-Kernel-anchor and concept-to-CQ traceability. No CQ identifiers or pass results are created by this scope document.

## 10. Acceptance Criteria

The Stage 2 Domain Library scope is acceptable when:

1. each E-01…E-16 area has an explicit scope disposition in Section 7;
2. every admitted concept has a Kernel anchor, semantic-chain position, or explicit supporting-concept rationale/dependency;
3. DL-GAP-01, DL-GAP-02, and DL-GAP-03 remain traceable without implying that they are implemented or closed;
4. declarative domain semantics are separated from executable behavior, Reference Architecture, and STPA analysis;
5. `SituationAwareness`, `Decision`, and `Perception` remain unresolved until their separate semantic decisions;
6. `ModeOfOperation`/`OperationalCondition`, ODD/Operational Envelope, ROC association, and performer/supervisor/authority-holder distinctions are preserved;
7. package ownership, import graph, dependency direction, `MASSRemoteOperations`, `MASSOperationalEnvironment`, and `MASSCore` disposition remain for 2.0-B/2.0-C;
8. MASS-SK-1.0 source and protected baseline artifacts remain unchanged;
9. any later SysML package proposal demonstrates consistency with this scope and the Kernel contract, and receives its own integration validation.

## 11. Final Scope Decision

Stage 2 MASS Domain Library scope is **approved for declarative domain semantics** that specialize the Kernel, concretize its existing semantic chains, or supply explicitly justified supporting concepts. The admitted areas include sensing/evidence, communication context, ODD dimensions, maritime collision-risk evidence and provenance, fallback strategy descriptions, COLREG applicability, and declarative safety applicability.

Situation-awareness, decision, perception, ROC decomposition, operational-environment concept boundaries, and detailed control semantics remain conditional on explicit semantic decisions. Package allocation and dependency design are not decided here. Executable algorithms, complete STPA semantics, Reference Architecture allocation, and responsibility/liability remain outside the current DL scope.

This document does not modify MASS-SK-1.0, does not create Stage 2 SysML packages, does not claim normative SysML v2/KerML verification, and does not report new OpenSysML, Pilot, SK1–SK16, or CQ1–CQ12 results.

## Sources and Evidence Status

- [Domain Evidence Matrix v0.1](domain-evidence-matrix.md) — Stage 2 evidence areas, candidate anchors, gaps, and open decisions.
- [MASS-SK-1.0 manifest](../../MASSKernel_v1.0_manifest.md) — released baseline inventory and structural anchors.
- [MASS-SK-1.0 scope boundary](../../MASSKernel_v1.0_scope_boundary.md) — deferred DL gaps and Kernel/Domain Library boundary.
- [MASS-SK-1.0 change-control record](../../MASSKernel_v1.0_change_control.md) — immutable baseline policy and protected contracts.
- [MASS-SK-1.0 validation record](../../MASSKernel_v1.0_validation_record.md) — historical validation evidence; not rerun for this document.
- [MASSKernel_v1.0.sysml](../../MASSKernel_v1.0.sysml) — released source anchors.

Hypha was not used. This document introduces no new normative SysML v2/KerML interpretation; the baseline references above are project contracts, not claims of a new standards verification.
