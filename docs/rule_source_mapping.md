# Rule to Source Mapping

Every rule in this expert system comes from NIST SP 800-61r3. This file records where each one came from and how the source statement became executable logic.

## Reading the citations

Section 3 of the source is a CSF 2.0 Community Profile in two tables: Table 2 covers Preparation and Lessons Learned (Govern, Identify, Protect), Table 3 covers Incident Response (Detect, Respond, Recover). Each row is a CSF Function, Category or Subcategory, carries a priority, and holds numbered items in its last column tagged `R` (recommendation), `C` (consideration) or `N` (note). NIST combines the two into identifiers such as `GV.RR-02.R2` (PDF p. 18).

Citations give the CSF element, the table, and both page numbers, since the PDF and printed numbering differ by eight:

```
GV.PO.R1, Table 2, PDF p. 21 (doc p. 13)
```

Priorities are NIST's own, defined on PDF p. 18: **High** is a core incident response activity, **Medium** directly supports incident response, **Low** supports it indirectly. They describe how central the outcome is to incident response, not how severe an organization's gap is. No rule is taken from a Low rated row.

Facts are phrased so that `yes` means the practice is present, and every rule fires on `no`. `unknown` never counts as `no`.

The source defines no scoring scale, so the system produces no score, grade or maturity level, and no rule uses a threshold or interval that NIST does not state.

---

## Group A. Preparation and Governance

### R01. Incident response policy exists

**Source:** GV.PO.R1, Table 2, PDF p. 21 (doc p. 13). Priority High.
**Knowledge:** Cybersecurity policies should include an incident response policy.
**Fact:** `ir_policy_exists`
**Conclusion:** `gap_ir_policy_missing`
**Recommendation:** Establish an incident response policy as part of the organization's cybersecurity policies.
**Transformation:** Presence test on the artefact the recommendation names. Section 2.3 (PDF pp. 16 to 17) lists what such a policy usually contains.

### R02. Incident response roles and responsibilities are documented

**Source:** GV.RR-02.R1, Table 2, PDF p. 21 (doc p. 13). Priority Medium.
**Knowledge:** All roles and responsibilities involving cybersecurity incident response should be documented in the organization's policies.
**Fact:** `ir_roles_documented`
**Conclusion:** `gap_ir_roles_undocumented`
**Recommendation:** Document all incident response roles and responsibilities in the organization's policies.
**Transformation:** Direct restatement. Kept separate from R03 because NIST separates documenting responsibility from granting authority.

### R03. Authority is designated to those with incident response responsibilities

**Source:** GV.RR-02.R2, Table 2, PDF p. 21 (doc p. 13). Priority Medium.
**Knowledge:** All appropriate individuals or parties should be designated the authority necessary to fulfil their incident response related responsibilities.
**Fact:** `ir_authority_designated`
**Conclusion:** `gap_ir_authority_not_designated`
**Recommendation:** Designate the authority each person or party needs to carry out their incident response responsibilities.
**Transformation:** Responsibility without matching authority is the failure this recommendation addresses, so it is tested on its own.

### R04. An incident response plan is established

**Source:** ID.IM-04, Table 2, PDF pp. 27 to 28 (doc pp. 19 to 20). Priority High.
**Knowledge:** Incident response plans and other cybersecurity plans affecting operations are established, communicated, maintained and improved. NIST describes the incident response plan as the roadmap for implementing the incident response capability.
**Fact:** `ir_plan_exists`
**Conclusion:** `gap_ir_plan_missing`
**Recommendation:** Establish and communicate an incident response plan covering how the organization's incident response capability is carried out.
**Transformation:** Grounded in the Subcategory outcome statement. R04 tests establishment, R05 tests maintenance, which NIST states separately.

### R05. Cybersecurity plans are reviewed and updated periodically

**Source:** ID.IM-04.R2, Table 2, PDF p. 28 (doc p. 20). Priority High.
**Knowledge:** Review and update all cybersecurity plans periodically, or when a need for significant improvement is identified.
**Fact:** `ir_plan_reviewed_periodically`
**Conclusion:** `gap_ir_plan_not_maintained`
**Recommendation:** Review and update the incident response plan periodically and whenever a significant improvement is needed.
**Transformation:** No review interval is specified, because NIST names none and inventing one would be an unsupported threshold.

### R06. Role based training covers incident response responsibilities

**Source:** PR.AT-02.R1, Table 2, PDF p. 29 (doc p. 21). Priority Medium.
**Knowledge:** Role based training should include incident related responsibilities.
**Fact:** `role_based_ir_training`
**Conclusion:** `gap_no_role_based_ir_training`
**Recommendation:** Include incident related responsibilities in the role based training given to staff in specialized roles.
**Transformation:** Scoped to role based training, as PR.AT-02 is. General awareness training (PR.AT-01) carries no incident response recommendation.

### R07. Suppliers and third parties are included in incident planning, response and recovery

**Source:** GV.SC-08, Table 2, PDF p. 23 (doc p. 15). Priority Medium.
**Knowledge:** Relevant suppliers and other third parties are included in incident planning, response and recovery activities. NIST notes this Subcategory is specific to incident response. Section 2.2 (PDF p. 16) adds that transferred responsibilities should be defined in contract, including authority to act for the organization.
**Fact:** `third_parties_in_ir_planning`
**Conclusion:** `gap_third_parties_excluded_from_ir`
**Recommendation:** Include relevant suppliers and third parties in incident planning, response and recovery, and define the division of responsibilities in contract.
**Transformation:** Accepts `not_applicable` as well as yes, no and unknown, since an organization that uses no third parties cannot answer meaningfully.

---

## Group B. Detection

### R08. Log records are generated and available

**Source:** PR.PS-04, Table 2, PDF p. 30 (doc p. 22). Priority Medium.
**Knowledge:** Log records are generated and made available for continuous monitoring. NIST notes that logs are particularly important for information vital to incident detection, response and recovery.
**Fact:** `logs_generated_and_available`
**Conclusion:** `gap_no_log_availability`
**Recommendation:** Generate log records across organizational systems and make them available for continuous monitoring.
**Transformation:** Grouped with detection because the detection rules depend on it, although NIST places PR.PS-04 in the preparation table.

### R09. Networks and network services are monitored

**Source:** DE.CM-01.R1, Table 3, PDF p. 32 (doc p. 24). Priority High.
**Knowledge:** Monitoring should include wired and wireless networks, network communications and flows, network services such as DNS and BGP, and the presence of unauthorized or rogue networks within facilities.
**Fact:** `network_monitoring`
**Conclusion:** `gap_no_network_monitoring`
**Recommendation:** Monitor wired and wireless networks, network flows and network services, and watch for rogue networks within facilities.
**Transformation:** The rule tests whether network monitoring is performed; the recommendation carries NIST's coverage list through to the user.

### R10. Computing hardware, software and their data are monitored

**Source:** DE.CM-09.R1 to R5, Table 3, PDF p. 32 (doc p. 24). Priority High.
**Knowledge:** Monitor common attack vectors such as email, web, file sharing and collaboration services for malware, phishing and exfiltration; monitor authentication attempts; monitor configurations against security baselines; monitor for tampering, failure or compromise; and monitor endpoints for cyber health issues.
**Fact:** `endpoint_and_service_monitoring`
**Conclusion:** `gap_no_endpoint_monitoring`
**Recommendation:** Monitor computing hardware, software and their data, covering common attack vectors, authentication attempts, configuration baselines, signs of tampering and endpoint health.
**Transformation:** Five recommendations under one Subcategory become one fact, since a respondent could not answer them separately. All five are kept in the recommendation text.

### R11. Event information is correlated from multiple sources

**Source:** DE.AE-03.R1 and R2, Table 3, PDF p. 33 (doc p. 25). Priority High.
**Knowledge:** Transfer log data to a relatively small number of log servers, and use event correlation technology such as SIEM or SOAR to gather related data captured by multiple sources.
**Fact:** `event_correlation`
**Conclusion:** `gap_no_event_correlation`
**Recommendation:** Centralize log data and use event correlation technology to relate data captured by different sources.
**Transformation:** Tests the capability rather than any named product, since NIST presents the technologies as examples that may date.

### R12. Adverse event information reaches incident responders

**Source:** DE.AE-06.R1 and R2, Table 3, PDF p. 34 (doc p. 26). Priority High.
**Knowledge:** Generate alerts and provide them to cybersecurity and incident response tools and staff, and make log analysis findings accessible to incident responders at all times.
**Fact:** `alerts_reach_responders`
**Conclusion:** `gap_alerts_not_reaching_responders`
**Recommendation:** Route alerts to incident response staff and tools, and keep log analysis findings accessible to responders at all times.
**Transformation:** Detection that no one acts on is the failure this Subcategory addresses, so it is tested separately from whether monitoring exists.

### R13. Incident declaration criteria are defined and applied

**Source:** DE.AE-08.R1, Table 3, PDF p. 34 (doc p. 26). Priority High.
**Knowledge:** Incidents are declared when adverse events meet defined incident criteria. Apply those criteria to the known and assumed characteristics of analyzed activity, allowing for known false positives.
**Fact:** `incident_declaration_criteria`
**Conclusion:** `gap_no_incident_declaration_criteria`
**Recommendation:** Define incident criteria and apply them to analyzed activity, allowing for known false positives, to decide when to declare an incident.
**Transformation:** Placed last in the detection group because it is the boundary between Detect and Respond in the source's life cycle model.

---

## Group C. Response

### R14. New incident reports are triaged and validated

**Source:** RS.MA-02.R1, Table 3, PDF p. 35 (doc p. 27). Priority High.
**Knowledge:** Perform a preliminary review of a new incident report to verify an incident has occurred, then estimate its severity and the urgency of response.
**Fact:** `incident_triage_performed`
**Conclusion:** `gap_no_incident_triage`
**Recommendation:** Review each new incident report to confirm an incident occurred, then estimate its severity and response urgency.
**Transformation:** Direct restatement as a presence test.

### R15. Incidents are categorized and prioritized

**Source:** RS.MA-03.R1 and R2, Table 3, PDF pp. 35 to 36 (doc pp. 27 to 28). Priority High.
**Knowledge:** Categorize incidents by type, for example data breach, ransomware, account takeover or denial of service, and prioritize response speed by scope, likely impact, time critical nature and resource availability. RS.MA.R1 adds that incidents should not be handled first come, first served.
**Fact:** `incidents_categorized_and_prioritized`
**Conclusion:** `gap_no_incident_prioritization`
**Recommendation:** Categorize incidents by type and prioritize response speed by scope, likely impact, urgency and available resources.
**Transformation:** Combined into one fact because NIST presents prioritization as the purpose categorization serves.

### R16. Incident status is tracked so escalation can be initiated

**Source:** RS.MA-04.R1, Table 3, PDF p. 36 (doc p. 28). Priority High.
**Knowledge:** Track and validate the status of all ongoing incidents so that those needing more resources or a changed strategy are identified and the changes initiated rapidly. RS.MA.R3 adds what to track per incident, including a summary, related indicators of compromise and next steps.
**Fact:** `incident_status_tracked`
**Conclusion:** `gap_no_incident_status_tracking`
**Recommendation:** Track and validate the status of every ongoing incident so those needing escalation are identified quickly.
**Transformation:** NIST presents tracking as the mechanism that makes escalation possible, so the rule tests tracking and the recommendation states its purpose.

### R17. Incident notification and coordination procedures are established

**Source:** RS.CO-02.R2, Table 3, PDF p. 38 (doc p. 30). Priority High.
**Knowledge:** Follow established incident coordination procedures covering what must be reported, to whom, and at what times. Related recommendations in the same Subcategory address compliance with notification laws and notifying law enforcement and regulators.
**Fact:** `notification_procedures_defined`
**Conclusion:** `gap_no_notification_procedures`
**Recommendation:** Establish coordination procedures stating what must be reported, to whom and when, aligned with applicable legal and regulatory requirements.
**Transformation:** R2 is used as the grounding because it is the procedural precondition for the other notification recommendations in the Subcategory.

### R18. Containment and eradication criteria are in place

**Source:** RS.MI.N1, Table 3, PDF p. 40 (doc p. 32). Priority High.
**Knowledge:** Activities are performed to prevent expansion of an event and mitigate its effects. Selecting containment and eradication actions is easier and faster where the organization has criteria and procedures in place, accounting for incident type and the intended duration of the measure.
**Fact:** `containment_eradication_criteria`
**Conclusion:** `gap_no_containment_eradication_criteria`
**Recommendation:** Define criteria and procedures for selecting containment and eradication actions, accounting for incident type and how long each measure is meant to last.
**Transformation:** Framed around criteria rather than whether incidents get contained, since readiness is what the system assesses. This is the weakest grounding in the set, as NIST phrases the note conditionally rather than as a recommendation.

---

## Group D. Recovery and Improvement

### R19. Backups are created, protected, maintained and tested

**Source:** PR.DS-11, Table 2, PDF p. 30 (doc p. 22). Priority High.
**Knowledge:** Backups of data are created, protected, maintained and tested. NIST notes backups are particularly important for recovery when data integrity or availability is affected, and lists restoring from clean backups first among recovery operations (PDF p. 41).
**Fact:** `backups_created_and_tested`
**Conclusion:** `gap_no_tested_backups`
**Recommendation:** Create, protect, maintain and test backups of data.
**Transformation:** PR.DS-11 is the only Protect Subcategory NIST rates High, which is why it is treated as recovery preparedness rather than general data protection.

### R20. Criteria for initiating incident recovery are defined

**Source:** RS.MA-05.R1 and R2, Table 3, PDF p. 36 (doc p. 28). Priority High.
**Knowledge:** Apply incident recovery criteria to the characteristics of the incident to determine when recovery should be initiated, taking the possible operational disruption of recovery itself into account.
**Fact:** `recovery_initiation_criteria`
**Conclusion:** `gap_no_recovery_initiation_criteria`
**Recommendation:** Define recovery criteria and apply them to each incident, allowing for the disruption recovery may cause, to decide when recovery begins.
**Transformation:** NIST places this in Respond, but it governs the start of recovery, so it is grouped here. The citation records its true location.

### R21. Backup and restoration asset integrity is verified before use

**Source:** RC.RP-03.R1, Table 3, PDF p. 42 (doc p. 34). Priority High.
**Knowledge:** The integrity of backups and other restoration assets is verified before use. Check them for indicators of compromise, file corruption and other integrity issues.
**Fact:** `backup_integrity_verified`
**Conclusion:** `gap_no_backup_integrity_verification`
**Recommendation:** Check backups and other restoration assets for indicators of compromise and corruption before restoring from them.
**Transformation:** Distinct from R19: tested backups do not establish that integrity is checked at the moment of restoration.

### R22. Restored assets are verified before return to production

**Source:** RC.RP-05.R1 and R2, Table 3, PDF p. 42 (doc p. 34). Priority High.
**Knowledge:** Check restored assets for indicators of compromise and remediate the incident's root causes before production use, and verify the correctness and adequacy of restoration actions before putting a system online.
**Fact:** `restored_assets_verified`
**Conclusion:** `gap_no_restored_asset_verification`
**Recommendation:** Check restored assets for indicators of compromise and remediate root causes before returning systems to production.
**Transformation:** R21 verifies the source of a restoration, R22 its result. NIST states these as separate outcomes.

### R23. Incident root cause analysis is performed

**Source:** RS.AN-03.R3, Table 3, PDF p. 36 (doc p. 28). Priority High.
**Knowledge:** Analyze the incident to find the underlying or systemic root causes. NIST notes this helps identify weaknesses in cybersecurity risk management that should be addressed to prevent similar incidents.
**Fact:** `root_cause_analysis`
**Conclusion:** `gap_no_root_cause_analysis`
**Recommendation:** Analyze incidents to find their underlying root causes, and use the findings to address the weaknesses that allowed them.
**Transformation:** Grouped with improvement because NIST ties root cause analysis to preventing recurrence.

### R24. An after action report is produced when recovery concludes

**Source:** RC.RP-06.R1, Table 3, PDF p. 42 (doc p. 34). Priority High.
**Knowledge:** Prepare an after action report documenting the incident, the response and recovery actions taken, and lessons learned. ID.IM-03.N3 adds that improvements are often identified when creating such reports or holding lessons learned meetings.
**Fact:** `after_action_report`
**Conclusion:** `gap_no_after_action_report`
**Recommendation:** Prepare an after action report at the end of each recovery documenting the incident, the actions taken and the lessons learned.
**Transformation:** Direct restatement.

---

## Group E. Derived rules

These three rules read facts produced by the rules above rather than answers from the user, so the system performs multi step inference and goal directed queries have something to prove. NIST states that recommendations made at Function or Category level also apply to their component elements (PDF p. 18), which is the basis for grounding them on higher level statements.

### R25. Continuous monitoring coverage is incomplete

**Source:** DE.CM.R1, Table 3, PDF p. 31 (doc p. 23). Priority High.
**Knowledge:** Continuous monitoring should involve these asset types at all times: networks and network services; computing hardware and software, runtime environments and their data; the physical environment; personnel activity and technology usage; and external service provider activities.
**Inputs:** `gap_no_log_availability`, `gap_no_network_monitoring`, `gap_no_endpoint_monitoring`
**Condition:** any one present
**Conclusion:** `detection_capability_incomplete`
**Recommendation:** Extend continuous monitoring to cover the asset types listed in DE.CM.R1 at all times, and make log records available to support it.
**Transformation:** A disjunction rather than a count, because the source requires all the listed classes rather than most of them. The system assesses three of the five; the physical environment (DE.CM-02) and external service provider activities (DE.CM-06) are not assessed, and this is stated as a limitation.

### R26. Incident management is inadequate

**Source:** RS.MA.R1, R2 and R3, Table 3, PDF pp. 34 to 35 (doc pp. 26 to 27). Priority High.
**Knowledge:** Evaluating overall risk from an incident and applying the appropriate prioritization are among the most critical decision points in incident response. Incidents should not be handled first come, first served. Triage, prioritization, escalation and elevation should all rest on a set of risk evaluation factors, and status should be tracked for each incident.
**Inputs:** `gap_no_incident_triage`, `gap_no_incident_prioritization`, `gap_no_incident_status_tracking`
**Condition:** any one present
**Conclusion:** `response_management_inadequate`
**Recommendation:** Establish triage, prioritization and status tracking driven by defined risk evaluation factors rather than by order of arrival.
**Transformation:** RS.MA.R2 names these activities together as resting on a common basis, so the absence of any one is a failure of the Category outcome.

### R27. Recovery preparedness is inadequate

**Source:** RC.N1 and N2, Table 3, PDF p. 41 (doc p. 33), with RC.RP.N1, PDF p. 42 (doc p. 34). Priority High.
**Knowledge:** During recovery, personnel restore systems to normal operations, confirm they function normally and remediate vulnerabilities where applicable. Recovery operations include restoring from clean backups. Executing the recovery plan involves performing recovery actions securely, verifying the integrity of recovered assets, declaring the end of recovery and completing documentation.
**Inputs:** `gap_no_tested_backups`, `gap_no_backup_integrity_verification`, `gap_no_restored_asset_verification`, `gap_no_recovery_initiation_criteria`
**Condition:** any one present
**Conclusion:** `recovery_preparedness_inadequate`
**Recommendation:** Put the elements recovery depends on in place: tested backups, integrity verification of restoration assets, verification of restored assets, and defined criteria for when recovery begins.
**Transformation:** The source describes recovery as a sequence depending on these elements, so the absence of any one makes the sequence unsupported. This is the goal used to demonstrate backward reasoning, since proving it descends through four supporting rules.

---

## Summary

| | Count |
|---|---|
| Rules | 27 |
| Rules reading primitive facts | 24 |
| Rules reading derived facts | 3 |
| Primitive facts | 24 |
| Derived facts | 27 (24 gap facts, 3 state facts) |
| From High priority CSF elements | 22 |
| From Medium priority CSF elements | 5 |

| Group | Rules | CSF Functions |
|---|---|---|
| A. Preparation and Governance | R01 to R07 | Govern, Identify, Protect |
| B. Detection | R08 to R13 | Protect, Detect |
| C. Response | R14 to R18 | Respond |
| D. Recovery and Improvement | R19 to R24 | Protect, Respond, Recover |
| E. Derived | R25 to R27 | Detect, Respond, Recover |

No two rules test the same fact or produce the same conclusion, and every derived fact read by R25 to R27 is produced by an earlier rule.

## Known limits of this rule set

- Continuous monitoring is assessed across three of the five asset classes NIST lists in DE.CM.R1. The physical environment and external service provider activities are not assessed.
- The conclusions of R25, R26 and R27 use the words incomplete and inadequate. The coverage and dependency claims are source backed; the judgement wording is this project's.
- R18 rests on a note phrased conditionally rather than on a recommendation, making it the weakest grounding in the set.
- Areas examined and not used: all Low rated CSF elements; risk assessment (ID.RA), which NIST places outside this Profile's scope; asset management (ID.AM); threat intelligence (ID.RA-02); and the Protect Subcategories carrying only the generic note. Items marked `C` are not used, since NIST presents them as things to consider rather than to do.
