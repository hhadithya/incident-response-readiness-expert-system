# Rule to Source Mapping

Every rule in this expert system is derived from NIST SP 800-61r3. This file is the traceability record: it states, for each rule, the exact location in the source document, the knowledge taken from it, and how that knowledge was turned into executable logic.

No domain expert was interviewed. No rule here originates from general cybersecurity intuition, from an unsourced best practice list, or from a language model. Where the source does not support a rule, the rule is not created.

## How the source is structured

Section 3 of NIST SP 800-61r3 is a CSF 2.0 Community Profile for cyber incident risk management, presented as two tables:

- Table 2, Preparation and Lessons Learned, covers the Govern, Identify and Protect Functions. PDF pages 19 to 31.
- Table 3, Incident Response, covers the Detect, Respond and Recover Functions. PDF pages 31 to 43.

Each row is a CSF Function, Category or Subcategory. Each row carries a priority assigned by NIST and, in the final column, numbered items of three kinds (PDF page 18, document page 10):

- `R` is a recommendation, something the organization should do.
- `C` is a consideration, something the organization should consider doing.
- `N` is a note, additional supporting information.

NIST states that an R, C or N designation appended to the row's CSF ID forms an identifier unique within the Community Profile, for example `GV.OC-03.R1`. This project uses that identifier scheme for citations.

## Priority

NIST assigns each row one of three priorities and defines them on PDF page 18 (document page 10):

- **High**: functions as a core incident response activity for most organizations.
- **Medium**: directly supports incident response activities for most organizations.
- **Low**: indirectly supports incident response activities for most organizations.

Rules carry the priority NIST gives the CSF element they are derived from. This priority is the source's own judgement of how central that outcome is to incident response. It is not a severity score for the organization's gap, and the system does not present it as one. NIST also states that these priorities are a starting point that organizations are encouraged to customize, so the system reports them as source information rather than as a verdict.

No rule is derived from a row NIST rated Low.

## Citation format

```
NIST SP 800-61r3, <CSF element ID>[.<item ID>], Table <2|3>, PDF p. <n> (document p. <n-8>)
```

Both page numbers are given because the PDF's page numbering and the document's printed page numbering differ by eight: printed page 1 is PDF page 9.

## Design constraints observed

- No global readiness score, percentage, grade or maturity level. NIST defines no such scale in this publication, so the system does not invent one. Output is a set of identified gaps with their supporting rules, recommendations and citations.
- No weighting of rules against each other beyond the priority NIST itself assigns.
- No thresholds such as a count of gaps that would trigger a rating.
- `UNKNOWN` is a distinct answer. It never stands in for `NO`. A rule fires only when its condition is definitely met, so an unknown input produces neither a gap nor a clean bill of health. The system reports unknown inputs separately as items it could not assess.

## Rule catalogue

27 candidate rules follow: 24 evaluate primitive facts supplied by the user, and 3 evaluate facts derived by other rules.

Naming conventions used below:

- Primitive facts are phrased positively, so that `yes` means the practice is present.
- Every rule fires on absence, so conditions test for `no`.
- Conclusions are named `gap_*` for primitive rules and describe a state for derived rules.

---

## Group A. Preparation and Governance

### R01. Incident response policy exists

- **Source**: NIST SP 800-61r3, GV.PO.R1, Table 2, PDF p. 21 (document p. 13)
- **NIST priority**: High
- **Source derived knowledge**: The Policy Category states that organizational cybersecurity policy is established, communicated and enforced. NIST's recommendation for this Category is that cybersecurity policies should include an incident response policy.
- **Supporting context**: Section 2.3 (PDF pp. 16 to 17, document pp. 8 to 9) lists the elements most incident response policies contain, including management commitment, scope, definitions, roles and authorities, prioritization guidelines and performance measures.
- **Primitive fact**: `ir_policy_exists`
- **Condition**: `ir_policy_exists = no`
- **Conclusion**: `gap_ir_policy_missing`
- **Recommendation**: Establish an incident response policy as part of the organization's cybersecurity policies.
- **Transformation note**: GV.PO is the only Category in Table 2 that NIST rates High, and its single recommendation is a direct statement of what the policy set must contain. The rule tests the presence of the artefact the recommendation names.

### R02. Incident response roles and responsibilities are documented in policy

- **Source**: NIST SP 800-61r3, GV.RR-02.R1, Table 2, PDF p. 21 (document p. 13)
- **NIST priority**: Medium
- **Source derived knowledge**: All roles and responsibilities involving cybersecurity incident response should be documented in the organization's policies. NIST's accompanying note observes that such roles typically exist throughout an organization and often extend to third parties under contract.
- **Primitive fact**: `ir_roles_documented`
- **Condition**: `ir_roles_documented = no`
- **Conclusion**: `gap_ir_roles_undocumented`
- **Recommendation**: Document all roles and responsibilities involving cybersecurity incident response in the organization's policies.
- **Transformation note**: Direct restatement of R1 as a presence test. Kept separate from R03 because NIST separates documenting responsibilities (R1) from granting authority (R2).

### R03. Authority is designated to those with incident response responsibilities

- **Source**: NIST SP 800-61r3, GV.RR-02.R2, Table 2, PDF p. 21 (document p. 13)
- **NIST priority**: Medium
- **Source derived knowledge**: All appropriate individuals or parties should be designated the authority necessary to fulfil their incident response related responsibilities.
- **Supporting context**: Section 2.3 (PDF p. 17, document p. 9) notes that policies commonly state which roles hold authority to confiscate, disconnect or shut down technology assets.
- **Primitive fact**: `ir_authority_designated`
- **Condition**: `ir_authority_designated = no`
- **Conclusion**: `gap_ir_authority_not_designated`
- **Recommendation**: Designate the authority each individual or party needs to carry out their incident response responsibilities.
- **Transformation note**: Assigned responsibility without matching authority is the specific failure R2 addresses, so the rule tests authority independently of R02.

### R04. An incident response plan is established

- **Source**: NIST SP 800-61r3, ID.IM-04, Table 2, PDF pp. 27 to 28 (document pp. 19 to 20)
- **NIST priority**: High
- **Source derived knowledge**: The Subcategory outcome is that incident response plans and other cybersecurity plans affecting operations are established, communicated, maintained and improved. NIST's note identifies the incident response plan as the roadmap for implementing the incident response capability.
- **Primitive fact**: `ir_plan_exists`
- **Condition**: `ir_plan_exists = no`
- **Conclusion**: `gap_ir_plan_missing`
- **Recommendation**: Establish and communicate an incident response plan that provides the roadmap for the organization's incident response capability.
- **Transformation note**: Grounded in the CSF Subcategory outcome statement itself, which is the source's normative text, with the note supplying the incident response framing. R04 tests establishment; R05 tests maintenance, which NIST states separately.

### R05. Cybersecurity plans are reviewed and updated periodically

- **Source**: NIST SP 800-61r3, ID.IM-04.R2, Table 2, PDF p. 28 (document p. 20)
- **NIST priority**: High
- **Source derived knowledge**: Review and update all cybersecurity plans periodically, or when a need for significant improvements is identified.
- **Primitive fact**: `ir_plan_reviewed_periodically`
- **Condition**: `ir_plan_reviewed_periodically = no`
- **Conclusion**: `gap_ir_plan_not_maintained`
- **Recommendation**: Review and update the incident response plan periodically and whenever a need for significant improvement is identified.
- **Transformation note**: The rule deliberately does not specify a review interval. NIST says periodically without naming a period, and supplying one would be an invented threshold.

### R06. Role based training covers incident response responsibilities

- **Source**: NIST SP 800-61r3, PR.AT-02.R1, Table 2, PDF p. 29 (document p. 21)
- **NIST priority**: Medium
- **Source derived knowledge**: Role based training should include incident related responsibilities. The Subcategory outcome is that individuals in specialized roles are given awareness and training so they can perform relevant tasks with cybersecurity risks in mind.
- **Primitive fact**: `role_based_ir_training`
- **Condition**: `role_based_ir_training = no`
- **Conclusion**: `gap_no_role_based_ir_training`
- **Recommendation**: Include incident related responsibilities in the role based training given to individuals in specialized roles.
- **Transformation note**: Scoped to role based training, as PR.AT-02 is, rather than to general awareness training, which is PR.AT-01 and carries no incident response recommendation.

### R07. Suppliers and other third parties are included in incident planning, response and recovery

- **Source**: NIST SP 800-61r3, GV.SC-08, Table 2, PDF p. 23 (document p. 15)
- **NIST priority**: Medium
- **Source derived knowledge**: The Subcategory outcome is that relevant suppliers and other third parties are included in incident planning, response and recovery activities. NIST notes that this Subcategory is specific to incident planning, response and recovery, and cross references its exercises and tests guidance.
- **Supporting context**: Section 2.2 (PDF p. 16, document p. 8) states that where responsibilities are transferred to a provider they should be clearly defined in a contract, and that the incident response team should be aware of the division of responsibilities, including authority to act on the organization's behalf.
- **Primitive fact**: `third_parties_in_ir_planning`
- **Condition**: `third_parties_in_ir_planning = no`
- **Conclusion**: `gap_third_parties_excluded_from_ir`
- **Recommendation**: Include relevant suppliers and other third parties in incident planning, response and recovery activities, and define the division of responsibilities in contract.
- **Transformation note**: Grounded in the Subcategory outcome text, which NIST's own note flags as specific to incident response. Applicability depends on the organization actually relying on third parties, which is why `unknown` and a not applicable answer must remain distinguishable. See the review items at the end of this file.

---

## Group B. Detection

### R08. Log records are generated and available for continuous monitoring

- **Source**: NIST SP 800-61r3, PR.PS-04, Table 2, PDF p. 30 (document p. 22)
- **NIST priority**: Medium
- **Source derived knowledge**: The Subcategory outcome is that log records are generated and made available for continuous monitoring. NIST notes that logs are particularly important for recording and preserving information vital to incident detection, response and recovery activities.
- **Primitive fact**: `logs_generated_and_available`
- **Condition**: `logs_generated_and_available = no`
- **Conclusion**: `gap_no_log_availability`
- **Recommendation**: Generate log records across organizational systems and make them available for continuous monitoring.
- **Transformation note**: The normative statement is the Subcategory outcome; the note establishes why it belongs in an incident response profile. Logging is placed in the detection group because every detection rule below depends on it, even though NIST locates PR.PS-04 in the preparation table.

### R09. Networks and network services are monitored

- **Source**: NIST SP 800-61r3, DE.CM-01.R1, Table 3, PDF p. 32 (document p. 24)
- **NIST priority**: High
- **Source derived knowledge**: Monitoring should include wired and wireless networks, network communications and flows, network services such as DNS and BGP, and the presence of unauthorized or rogue networks within facilities.
- **Primitive fact**: `network_monitoring`
- **Condition**: `network_monitoring = no`
- **Conclusion**: `gap_no_network_monitoring`
- **Recommendation**: Monitor wired and wireless networks, network flows and network services, and watch for unauthorized or rogue networks within facilities.
- **Transformation note**: R1 enumerates what network monitoring must cover. The rule tests whether network monitoring is performed at all, and the recommendation carries the enumeration through so the user sees the required coverage.

### R10. Computing hardware, software and their data are monitored

- **Source**: NIST SP 800-61r3, DE.CM-09.R1 to R5, Table 3, PDF p. 32 (document p. 24)
- **NIST priority**: High
- **Source derived knowledge**: NIST gives five recommendations for this Subcategory: monitor common attack vectors such as email, web, file sharing and collaboration services to detect malware, phishing, data leaks and exfiltration; monitor authentication attempts to identify attacks against credentials and unauthorized credential use; monitor software and hardware configurations for deviations from security baselines; monitor hardware and software, including protection mechanisms, for signs of tampering, failure or compromise; and monitor endpoints for cyber health issues.
- **Primitive fact**: `endpoint_and_service_monitoring`
- **Condition**: `endpoint_and_service_monitoring = no`
- **Conclusion**: `gap_no_endpoint_monitoring`
- **Recommendation**: Monitor computing hardware, software, runtime environments and their data, covering common attack vectors, authentication attempts, configuration baselines, signs of tampering, and endpoint cyber health.
- **Transformation note**: Five recommendations are collapsed into one fact because they share a single Subcategory outcome and splitting them would produce five questions an ordinary respondent could not answer separately. All five are preserved in the recommendation text so no source content is lost.

### R11. Event information is correlated from multiple sources

- **Source**: NIST SP 800-61r3, DE.AE-03.R1 and R2, Table 3, PDF p. 33 (document p. 25)
- **NIST priority**: High
- **Source derived knowledge**: The Subcategory outcome is that information is correlated from multiple sources. NIST recommends constantly transferring log data generated by other sources to a relatively small number of log servers, and using event correlation technology such as SIEM or SOAR to gather related data captured by multiple sources.
- **Primitive fact**: `event_correlation`
- **Condition**: `event_correlation = no`
- **Conclusion**: `gap_no_event_correlation`
- **Recommendation**: Centralize log data onto a small number of log servers and use event correlation technology to relate data captured by different sources.
- **Transformation note**: NIST names SIEM and SOAR as examples. The rule tests the capability, not any named product, because the source presents the technologies as examples that may become outdated.

### R12. Adverse event information reaches incident responders

- **Source**: NIST SP 800-61r3, DE.AE-06.R1 and R2, Table 3, PDF p. 34 (document p. 26)
- **NIST priority**: High
- **Source derived knowledge**: The Subcategory outcome is that information on adverse events is provided to authorized staff and tools. NIST recommends generating alerts and providing them to cybersecurity and incident response tools and staff, and making log analysis findings accessible to incident responders and other authorized personnel at all times.
- **Primitive fact**: `alerts_reach_responders`
- **Condition**: `alerts_reach_responders = no`
- **Conclusion**: `gap_alerts_not_reaching_responders`
- **Recommendation**: Generate alerts and route them to incident response staff and tools, and keep log analysis findings accessible to incident responders at all times.
- **Transformation note**: Detection that no one acts on is the failure this Subcategory addresses, so it is tested separately from whether monitoring exists at all.

### R13. Incident declaration criteria are defined and applied

- **Source**: NIST SP 800-61r3, DE.AE-08.R1, Table 3, PDF p. 34 (document p. 26)
- **NIST priority**: High
- **Source derived knowledge**: The Subcategory outcome is that incidents are declared when adverse events meet the defined incident criteria. NIST recommends applying incident criteria to the known and assumed characteristics of analyzed activity, taking known false positives into account, to determine whether an incident should be declared.
- **Primitive fact**: `incident_declaration_criteria`
- **Condition**: `incident_declaration_criteria = no`
- **Conclusion**: `gap_no_incident_declaration_criteria`
- **Recommendation**: Define incident criteria and apply them to analyzed activity, allowing for known false positives, to decide when to declare an incident.
- **Transformation note**: This is the boundary between the Detect and Respond Functions in the source's life cycle model, which is why it sits at the end of the detection group.

---

## Group C. Response

### R14. New incident reports are triaged and validated

- **Source**: NIST SP 800-61r3, RS.MA-02.R1, Table 3, PDF p. 35 (document p. 27)
- **NIST priority**: High
- **Source derived knowledge**: Perform a preliminary review of a new incident report to verify that a cybersecurity incident has occurred, then estimate the severity of the incident and the level of urgency needed to respond to it.
- **Primitive fact**: `incident_triage_performed`
- **Condition**: `incident_triage_performed = no`
- **Conclusion**: `gap_no_incident_triage`
- **Recommendation**: Perform a preliminary review of each new incident report to confirm an incident occurred, then estimate its severity and the urgency of response.
- **Transformation note**: Direct restatement of R1 as a presence test on the practice.

### R15. Incidents are categorized and prioritized

- **Source**: NIST SP 800-61r3, RS.MA-03.R1 and R2, Table 3, PDF pp. 35 to 36 (document pp. 27 to 28)
- **NIST priority**: High
- **Source derived knowledge**: Perform a more detailed review of incidents to categorize them by incident type, for example data breach, ransomware, account takeover or denial of service. Prioritize how quickly incident response should be performed for each incident based on its scope, likely impact, time critical nature and resource availability.
- **Supporting context**: RS.MA.R1 (PDF p. 34, document p. 26) states that because of resource limitations, incidents should not be handled on a first come, first served basis.
- **Primitive fact**: `incidents_categorized_and_prioritized`
- **Condition**: `incidents_categorized_and_prioritized = no`
- **Conclusion**: `gap_no_incident_prioritization`
- **Recommendation**: Categorize incidents by type and prioritize response speed according to scope, likely impact, time critical nature and resource availability.
- **Transformation note**: Categorization and prioritization are combined because they belong to one Subcategory and NIST presents prioritization as the purpose the categorization serves.

### R16. Incident status is tracked so escalation can be initiated

- **Source**: NIST SP 800-61r3, RS.MA-04.R1, Table 3, PDF p. 36 (document p. 28)
- **NIST priority**: High
- **Source derived knowledge**: Track and validate the status of all ongoing incidents so that incidents needing more response resources or a change in response strategy can be identified and the necessary changes initiated rapidly. NIST distinguishes escalation, which increases resources or time frames, from elevation, which involves a higher level of management.
- **Supporting context**: RS.MA.R3 (PDF p. 35, document p. 27) states that incident response status should be tracked for each incident along with pertinent information such as a summary, related indicators of compromise, the status and expected time frame for each assigned action, and next steps.
- **Primitive fact**: `incident_status_tracked`
- **Condition**: `incident_status_tracked = no`
- **Conclusion**: `gap_no_incident_status_tracking`
- **Recommendation**: Track and validate the status of every ongoing incident so that incidents needing more resources or a changed strategy are identified and escalated rapidly.
- **Transformation note**: NIST presents tracking as the mechanism that makes escalation possible, so the rule tests tracking and the recommendation states the escalation purpose.

### R17. Incident notification and coordination procedures are established

- **Source**: NIST SP 800-61r3, RS.CO-02.R2, Table 3, PDF p. 38 (document p. 30)
- **NIST priority**: High
- **Source derived knowledge**: Follow established procedures concerning incident coordination that include what must be reported to whom and at what times, for example initial notification and regular status updates. NIST's Category note adds that organizations should have mechanisms in place in advance to coordinate with affected parties about incidents when needed.
- **Supporting context**: RS.CO-02.R3 and R5 (PDF pp. 38 to 39, document pp. 30 to 31) address performing notifications in compliance with applicable laws and regulations, and notifying law enforcement and regulatory bodies based on criteria in the incident response plan.
- **Primitive fact**: `notification_procedures_defined`
- **Condition**: `notification_procedures_defined = no`
- **Conclusion**: `gap_no_notification_procedures`
- **Recommendation**: Establish incident coordination procedures that state what must be reported, to whom, and at what times, and align notifications with applicable legal and regulatory requirements.
- **Transformation note**: R2 is chosen as the grounding because it is the procedural precondition for the other notification recommendations in the same Subcategory.

### R18. Containment and eradication criteria and procedures are in place

- **Source**: NIST SP 800-61r3, RS.MI.N1, Table 3, PDF p. 40 (document p. 32)
- **NIST priority**: High
- **Source derived knowledge**: The Incident Mitigation Category outcome is that activities are performed to prevent expansion of an event and mitigate its effects. NIST notes that manually selecting containment and eradication actions may be easier and faster if the organization has criteria and procedures in place, and that such criteria could account for incident type and for the intended duration of the measure. The Subcategory notes add that containment prevents additional damage and that most incidents require some form of it, and that eradication eliminates persistence mechanisms and entry points.
- **Primitive fact**: `containment_eradication_criteria`
- **Condition**: `containment_eradication_criteria = no`
- **Conclusion**: `gap_no_containment_eradication_criteria`
- **Recommendation**: Define criteria and procedures for selecting containment and eradication actions, taking incident type and the intended duration of each measure into account.
- **Transformation note**: The rule is framed around criteria and procedures rather than around whether incidents get contained, because readiness is what this system assesses and because the source's statement about criteria is what applies before an incident occurs. This is the weakest grounding in the set: NIST phrases N1 conditionally rather than as a recommendation. See the review items at the end of this file.

---

## Group D. Recovery and Improvement

### R19. Backups are created, protected, maintained and tested

- **Source**: NIST SP 800-61r3, PR.DS-11, Table 2, PDF p. 30 (document p. 22)
- **NIST priority**: High
- **Source derived knowledge**: The Subcategory outcome is that backups of data are created, protected, maintained and tested. NIST notes that backups can be particularly important for recovery purposes when data integrity or availability is affected.
- **Supporting context**: The Recover Function note (PDF p. 41, document p. 33) lists restoring systems from clean backups first among recovery operations.
- **Primitive fact**: `backups_created_and_tested`
- **Condition**: `backups_created_and_tested = no`
- **Conclusion**: `gap_no_tested_backups`
- **Recommendation**: Create, protect, maintain and test backups of data.
- **Transformation note**: PR.DS-11 is the only Subcategory in the Protect Function that NIST rates High, which is why it is carried into the recovery group rather than treated as general data protection. Testing is part of the outcome statement, so the fact covers creation and testing together.

### R20. Criteria for initiating incident recovery are defined and applied

- **Source**: NIST SP 800-61r3, RS.MA-05.R1 and R2, Table 3, PDF p. 36 (document p. 28)
- **NIST priority**: High
- **Source derived knowledge**: The Subcategory outcome is that the criteria for initiating incident recovery are applied. NIST recommends applying incident recovery criteria to the known and assumed characteristics of the incident to determine when recovery processes should be initiated, and taking the possible operational disruption of recovery activities into account in that decision.
- **Primitive fact**: `recovery_initiation_criteria`
- **Condition**: `recovery_initiation_criteria = no`
- **Conclusion**: `gap_no_recovery_initiation_criteria`
- **Recommendation**: Define incident recovery criteria and apply them to the characteristics of each incident, allowing for the operational disruption recovery itself may cause, to decide when recovery should begin.
- **Transformation note**: NIST places this Subcategory in the Respond Function, but it governs the start of recovery, so it is grouped with recovery here. The citation records its true location.

### R21. Backup and restoration asset integrity is verified before use

- **Source**: NIST SP 800-61r3, RC.RP-03.R1, Table 3, PDF p. 42 (document p. 34)
- **NIST priority**: High
- **Source derived knowledge**: The Subcategory outcome is that the integrity of backups and other restoration assets is verified before they are used for restoration. NIST recommends checking restoration assets for indicators of compromise, file corruption and other integrity issues before use.
- **Primitive fact**: `backup_integrity_verified`
- **Condition**: `backup_integrity_verified = no`
- **Conclusion**: `gap_no_backup_integrity_verification`
- **Recommendation**: Check backups and other restoration assets for indicators of compromise, file corruption and other integrity issues before restoring from them.
- **Transformation note**: Distinct from R19. Having tested backups does not establish that their integrity is checked at the moment of restoration, which is the specific outcome RC.RP-03 defines.

### R22. Restored assets are verified before return to production

- **Source**: NIST SP 800-61r3, RC.RP-05.R1 and R2, Table 3, PDF p. 42 (document p. 34)
- **NIST priority**: High
- **Source derived knowledge**: The Subcategory outcome is that the integrity of restored assets is verified, systems and services are restored, and normal operating status is confirmed. NIST recommends checking restored assets for indicators of compromise and remediating the root causes of the incident before production use, and verifying the correctness and adequacy of restoration actions before putting a restored system online.
- **Primitive fact**: `restored_assets_verified`
- **Condition**: `restored_assets_verified = no`
- **Conclusion**: `gap_no_restored_asset_verification`
- **Recommendation**: Check restored assets for indicators of compromise and remediate the incident's root causes before returning systems to production use.
- **Transformation note**: R21 covers verification of the source of a restoration; R22 covers verification of its result. NIST states these as separate Subcategory outcomes.

### R23. Incident root cause analysis is performed

- **Source**: NIST SP 800-61r3, RS.AN-03.R3, Table 3, PDF p. 36 (document p. 28)
- **NIST priority**: High
- **Source derived knowledge**: The Subcategory outcome is that analysis is performed to establish what has taken place during an incident and its root cause. NIST recommends analyzing the incident to find the underlying or systemic root causes, and notes that this information may help identify weaknesses in cybersecurity risk management that should be addressed to prevent similar incidents in future.
- **Primitive fact**: `root_cause_analysis`
- **Condition**: `root_cause_analysis = no`
- **Conclusion**: `gap_no_root_cause_analysis`
- **Recommendation**: Analyze incidents to identify their underlying or systemic root causes, and use the findings to address the weaknesses that allowed them.
- **Transformation note**: Placed in the improvement group because NIST's note ties root cause analysis to preventing recurrence, which is the improvement loop in the source's life cycle model.

### R24. An after action report is produced when recovery concludes

- **Source**: NIST SP 800-61r3, RC.RP-06.R1, Table 3, PDF p. 42 (document p. 34)
- **NIST priority**: High
- **Source derived knowledge**: The Subcategory outcome is that the end of incident recovery is declared based on criteria and incident related documentation is completed. NIST recommends preparing an after action report documenting the incident itself, the response and recovery actions taken, and lessons learned.
- **Supporting context**: ID.IM-03.N3 (PDF pp. 27 to 28, document pp. 19 to 20) states that improvements are often identified when creating follow up reports or holding lessons learned meetings as an incident's recovery concludes.
- **Primitive fact**: `after_action_report`
- **Condition**: `after_action_report = no`
- **Conclusion**: `gap_no_after_action_report`
- **Recommendation**: Prepare an after action report at the end of each incident recovery documenting the incident, the actions taken, and the lessons learned.
- **Transformation note**: Direct restatement of R1. The ID.IM-03 note is cited as supporting context because it explains the report's role in the improvement loop.

---

## Group E. Derived rules

These three rules evaluate facts produced by the rules above rather than answers supplied by the user. They exist so that the system performs genuine multi step inference and so that goal directed queries have meaningful goals to prove.

Each is grounded in a Category or Function level statement in the source. NIST states that recommendations, considerations and notes made at a higher level of the CSF also apply to their component elements (PDF p. 18, document p. 10), which is the basis for treating a Category level statement as covering its Subcategories.

The conclusion wording of these three rules is this project's phrasing, not NIST's. See the review items below.

### R25. Continuous monitoring coverage is incomplete

- **Source**: NIST SP 800-61r3, DE.CM.R1, Table 3, PDF p. 31 (document p. 23)
- **NIST priority**: High
- **Source derived knowledge**: Continuous monitoring for unauthorized activity, deviations from expected activity and changes in security posture should involve the following types of assets at all times: networks and network services; computing hardware and software, runtime environments and their data; the physical environment; personnel activity and technology usage; and external service provider activities.
- **Derived facts required**: `gap_no_log_availability`, `gap_no_network_monitoring`, `gap_no_endpoint_monitoring`
- **Condition**: any one of the three is present
- **Conclusion**: `detection_capability_incomplete`
- **Recommendation**: Extend continuous monitoring so that it covers all the asset types listed in DE.CM.R1 at all times, and ensure log records are available to support it.
- **Transformation note**: R1 states a coverage requirement across named asset classes. The rule concludes that coverage is incomplete when any assessed class is missing. It is deliberately a disjunction, not a count or a proportion, because the source requires all the listed classes rather than a majority of them. The system assesses three of the five classes NIST lists; the physical environment (DE.CM-02) and external service provider activities (DE.CM-06) are not assessed, and the system states this limitation rather than implying full coverage.

### R26. Incident management is inadequate

- **Source**: NIST SP 800-61r3, RS.MA.R1, R2 and R3, Table 3, PDF pp. 34 to 35 (document pp. 26 to 27)
- **NIST priority**: High
- **Source derived knowledge**: NIST states that evaluating the overall risk from an incident and applying the appropriate prioritization are perhaps the most critical decision points in the incident response process. Because of resource limitations, incidents should not be handled on a first come, first served basis. Triage, prioritization, escalation, elevation and decisions about when to initiate recovery should all be based on a set of risk evaluation factors. The incident response status should be tracked for each incident.
- **Derived facts required**: `gap_no_incident_triage`, `gap_no_incident_prioritization`, `gap_no_incident_status_tracking`
- **Condition**: any one of the three is present
- **Conclusion**: `response_management_inadequate`
- **Recommendation**: Establish triage, prioritization and status tracking for incidents, all driven by a defined set of risk evaluation factors rather than by order of arrival.
- **Transformation note**: RS.MA.R2 names triage, prioritization and escalation together as activities that must rest on a common basis of risk evaluation factors. The rule treats the absence of any of them as a failure of the Category outcome, which is what R1 and R2 jointly describe.

### R27. Recovery preparedness is inadequate

- **Source**: NIST SP 800-61r3, RC.N1 and N2, Table 3, PDF p. 41 (document p. 33), with RC.RP.N1, PDF p. 42 (document p. 34)
- **NIST priority**: High
- **Source derived knowledge**: During incident recovery, personnel restore systems to normal operations, confirm that the systems are functioning normally and, where applicable, remediate vulnerabilities to prevent similar incidents. Recovery operations include restoring systems from clean backups. Executing the incident recovery plan involves selecting, prioritizing and performing recovery actions securely, verifying the integrity of recovered assets, declaring the end of incident recovery and completing incident documentation.
- **Derived facts required**: `gap_no_tested_backups`, `gap_no_backup_integrity_verification`, `gap_no_restored_asset_verification`, `gap_no_recovery_initiation_criteria`
- **Condition**: any one of the four is present
- **Conclusion**: `recovery_preparedness_inadequate`
- **Recommendation**: Put the elements the recovery plan depends on in place: tested backups, integrity verification of restoration assets, verification of restored assets, and defined criteria for when recovery begins.
- **Transformation note**: The Function and Category level notes describe recovery as a sequence that depends on clean backups, integrity verification and confirmation of normal operation. The rule concludes inadequacy when any of those dependencies is missing. This is the goal used to demonstrate backward reasoning, because proving it requires the engine to descend through four supporting rules to their primitive facts.

---

## Coverage summary

| Group | Rules | CSF Functions drawn on |
|---|---|---|
| A. Preparation and Governance | R01 to R07 | Govern, Identify, Protect |
| B. Detection | R08 to R13 | Protect, Detect |
| C. Response | R14 to R18 | Respond |
| D. Recovery and Improvement | R19 to R24 | Protect, Respond, Recover |
| E. Derived | R25 to R27 | Detect, Respond, Recover |

| Measure | Count |
|---|---|
| Candidate rules | 27 |
| Rules evaluating primitive facts | 24 |
| Rules evaluating derived facts | 3 |
| Distinct primitive facts | 24 |
| Distinct derived facts | 27 (24 gap facts, 3 state facts) |
| Rules from High priority CSF elements | 22 |
| Rules from Medium priority CSF elements | 5 |
| Rules from Low priority CSF elements | 0 |

## Checks performed on the candidate set

**Duplicates.** R02 and R03 both cite GV.RR-02 but separate recommendations within it, documenting responsibility against granting authority. R04 and R05 both cite ID.IM-04 but separate establishment from maintenance. R14, R15 and R16 cite three different Subcategories of RS.MA. R19 and R21 are distinct: one concerns whether backups are tested, the other whether their integrity is checked at restoration time. R21 and R22 are distinct: one verifies the source of a restoration, the other its result. No two rules test the same fact.

**Arbitrary thresholds.** None. No rule counts gaps, compares proportions, or applies an interval NIST does not state. R05 deliberately omits a review frequency for this reason.

**Arbitrary priorities.** None. Every priority is the one NIST assigns the cited CSF element, and its meaning is reported as NIST defines it.

**Scope.** No rule addresses ISO/IEC 27001, SOC 2, penetration testing, vulnerability scanning or general enterprise risk management. Rules drawn from the Protect Function are limited to the two Subcategories NIST flags as directly serving incident response, PR.DS-11 and PR.PS-04, plus the incident response training recommendation in PR.AT-02.

**Overlapping logic.** The three derived rules draw on disjoint sets of gap facts, so no gap contributes to more than one derived conclusion.

**Unsupported claims.** Each rule's source derived knowledge paraphrases text present at the cited location. No verbatim NIST text is presented as a quotation in the running system.

## Items requiring human review

1. **Derived rule wording.** The conclusions of R25, R26 and R27 use the words incomplete and inadequate. NIST does not apply those words to organizations. The underlying coverage and dependency claims are source backed, but the judgement wording is this project's. The alternative is neutral phrasing such as `detection_coverage_gaps_present`. This is the single largest interpretive step in the rule set and should be decided deliberately.

2. **R18 grounding strength.** RS.MI.N1 is a note phrased conditionally, saying that containment and eradication selection may be easier and faster if criteria and procedures are in place. That is weaker than a recommendation. The rule is defensible because the Category outcome itself is normative, but if a stricter standard is wanted, R18 is the first rule to drop. Doing so would leave 26 candidates.

3. **R07 applicability.** GV.SC-08 concerns suppliers and third parties. An organization that uses none cannot meaningfully answer yes or no. The fact model needs either a not applicable value for this question or a gating question before it. This is a Phase 2 decision but it originates here.

4. **R10 consolidation.** Five NIST recommendations map to one fact. The consolidation is documented and the recommendation text preserves all five, but an assessor may prefer five separate facts. Splitting would raise the primitive fact count to 28 and the rule count to 31.

5. **Candidate count.** 27 candidates is one above the 26 ceiling set for this stage. Dropping R18 brings it to 26. No rule was added to reach a number.

6. **Assessed coverage of DE.CM.** NIST lists five asset classes for continuous monitoring. The system assesses three. The physical environment (DE.CM-02) and external service provider activities (DE.CM-06) were left out to keep the questionnaire proportionate. Both are rated High by NIST, so this is a real coverage limitation that the README and the report must state. Adding them would bring the rule count to 29.

## Knowledge deliberately not turned into rules

Recording what was examined and set aside is part of the traceability record.

- All CSF elements NIST rates Low, which is most of the Govern Function's Organizational Context, Risk Management Strategy, Oversight and Supply Chain Categories.
- Risk assessment content in ID.RA. NIST states explicitly that risk assessment is outside the scope of this Profile beyond summarizing its importance for incident response.
- Asset management content in ID.AM. It is rated Medium and supports incident response indirectly, but assessing inventories would widen the system toward general IT asset management.
- Cyber threat intelligence in ID.RA-02, rated High. It is genuinely incident response relevant, but every recommendation attached to it concerns improving detection accuracy rather than a readiness practice an organization can straightforwardly confirm. Available if wanted.
- Protect Function Subcategories carrying only the generic PR note, covering identity management, access control, data confidentiality, platform security and infrastructure resilience. NIST states that recommendations on protecting assets are outside the Profile's scope.
- Considerations marked `C` throughout the source. These are things NIST says an organization should consider, not do, so they do not support a rule that concludes a gap exists.
