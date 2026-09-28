# Rule to Source Mapping

Every rule in this system comes from NIST SP 800-61r3. This file records where each one came from.

## Reading the citations

Section 3 of the source is a CSF 2.0 Community Profile in two tables. Table 2 covers Preparation and Lessons Learned (Govern, Identify, Protect); Table 3 covers Incident Response (Detect, Respond, Recover). Each row is a CSF Function, Category or Subcategory with a priority and numbered items tagged `R` (recommendation), `C` (consideration) or `N` (note). NIST combines the two into identifiers such as `GV.RR-02.R2` (PDF p. 18).

Citations give the CSF element, the table and both page numbers, since PDF and printed numbering differ by eight.

Priorities are NIST's, defined on PDF p. 18. **High** is a core incident response activity, **Medium** directly supports incident response, **Low** supports it indirectly. They say how central an outcome is to incident response, not how serious an organization's gap is. No rule comes from a Low rated row.

Facts are phrased so `yes` means the practice is present, and every rule fires on `no`. NIST defines no scoring scale, so the system produces no score or grade, and no rule uses a threshold the source does not state.

---

## Group A. Preparation and Governance

**R01. Incident response policy exists**
*Source:* GV.PO.R1, Table 2, PDF p. 21 (doc p. 13), High. Cybersecurity policies should include an incident response policy.
*Rule:* if `ir-policy-exists` = no, then `gap-ir-policy-missing`
*Recommendation:* Establish an incident response policy as part of the organization's cybersecurity policies.

**R02. Incident response roles and responsibilities are documented**
*Source:* GV.RR-02.R1, Table 2, PDF p. 21 (doc p. 13), Medium. All roles and responsibilities involving incident response should be documented in the organization's policies.
*Rule:* if `ir-roles-documented` = no, then `gap-ir-roles-undocumented`
*Recommendation:* Document all incident response roles and responsibilities in the organization's policies.

**R03. Authority is designated to those with incident response responsibilities**
*Source:* GV.RR-02.R2, Table 2, PDF p. 21 (doc p. 13), Medium. All appropriate individuals or parties should be designated the authority necessary to fulfill their incident response related responsibilities.
*Rule:* if `ir-authority-designated` = no, then `gap-ir-authority-not-designated`
*Recommendation:* Designate the authority each person or party needs to carry out their incident response responsibilities.

**R04. An incident response plan is established**
*Source:* ID.IM-04, Table 2, PDF pp. 27 to 28 (doc pp. 19 to 20), High. Incident response plans and other cybersecurity plans affecting operations are established, communicated, maintained and improved. NIST describes the incident response plan as the roadmap for the incident response capability.
*Rule:* if `ir-plan-exists` = no, then `gap-ir-plan-missing`
*Recommendation:* Establish and communicate an incident response plan covering how incident response is carried out.

**R05. Cybersecurity plans are reviewed and updated periodically**
*Source:* ID.IM-04.R2, Table 2, PDF p. 28 (doc p. 20), High. Review and update all cybersecurity plans periodically, or when a need for significant improvement is identified.
*Rule:* if `ir-plan-reviewed-periodically` = no, then `gap-ir-plan-not-maintained`
*Recommendation:* Review and update the incident response plan periodically and whenever a significant improvement is needed.

**R06. Role based training covers incident response responsibilities**
*Source:* PR.AT-02.R1, Table 2, PDF p. 29 (doc p. 21), Medium. Role based training should include incident related responsibilities.
*Rule:* if `role-based-ir-training` = no, then `gap-no-role-based-ir-training`
*Recommendation:* Include incident related responsibilities in the role based training given to staff in specialized roles.

**R07. Log records are generated and available**
*Source:* PR.PS-04, Table 2, PDF p. 30 (doc p. 22), Medium. Log records are generated and made available for continuous monitoring. NIST notes logs are particularly important for incident detection, response and recovery.
*Rule:* if `logs-generated-and-available` = no, then `gap-no-log-availability`
*Recommendation:* Generate log records across organizational systems and make them available for continuous monitoring.

**R08. Networks and network services are monitored**
*Source:* DE.CM-01.R1, Table 3, PDF p. 32 (doc p. 24), High. Monitoring should include wired and wireless networks, network communications and flows, network services such as DNS and BGP, and the presence of rogue networks within facilities.
*Rule:* if `network-monitoring` = no, then `gap-no-network-monitoring`
*Recommendation:* Monitor wired and wireless networks, network flows and network services, and watch for rogue networks within facilities.

**R09. Computing hardware, software and their data are monitored**
*Source:* DE.CM-09.R1 to R5, Table 3, PDF p. 32 (doc p. 24), High. Monitor common attack vectors such as email, web and file sharing for malware, phishing and exfiltration; monitor authentication attempts; monitor configurations against security baselines; monitor for tampering, failure or compromise; and monitor endpoints for cyber health issues.
*Rule:* if `endpoint-and-service-monitoring` = no, then `gap-no-endpoint-monitoring`
*Recommendation:* Monitor computing hardware, software and their data, covering common attack vectors, authentication attempts, configuration baselines, signs of tampering and endpoint health.

**R10. Event information is correlated from multiple sources**
*Source:* DE.AE-03.R1 and R2, Table 3, PDF p. 33 (doc p. 25), High. Transfer log data to a relatively small number of log servers, and use event correlation technology such as SIEM or SOAR to gather related data captured by multiple sources.
*Rule:* if `event-correlation` = no, then `gap-no-event-correlation`
*Recommendation:* Centralize log data and use event correlation technology to relate data captured by different sources.

**R11. Adverse event information reaches incident responders**
*Source:* DE.AE-06.R1 and R2, Table 3, PDF p. 34 (doc p. 26), High. Generate alerts and provide them to incident response tools and staff, and make log analysis findings accessible to responders at all times.
*Rule:* if `alerts-reach-responders` = no, then `gap-alerts-not-reaching-responders`
*Recommendation:* Route alerts to incident response staff and tools, and keep log analysis findings accessible to responders at all times.

**R12. Incident declaration criteria are defined and applied**
*Source:* DE.AE-08.R1, Table 3, PDF p. 34 (doc p. 26), High. Incidents are declared when adverse events meet defined incident criteria. Apply those criteria to the characteristics of analyzed activity, allowing for known false positives.
*Rule:* if `incident-declaration-criteria` = no, then `gap-no-incident-declaration-criteria`
*Recommendation:* Define incident criteria and apply them to analyzed activity, allowing for known false positives, to decide when to declare an incident.

---

## Group C. Response

**R13. New incident reports are triaged and validated**
*Source:* RS.MA-02.R1, Table 3, PDF p. 35 (doc p. 27), High. Perform a preliminary review of a new incident report to verify an incident has occurred, then estimate its severity and the urgency of response.
*Rule:* if `incident-triage-performed` = no, then `gap-no-incident-triage`
*Recommendation:* Review each new incident report to confirm an incident occurred, then estimate its severity and response urgency.

**R14. Incidents are categorized and prioritized**
*Source:* RS.MA-03.R1 and R2, Table 3, PDF pp. 35 to 36 (doc pp. 27 to 28), High. Categorize incidents by type, and prioritize response speed by scope, likely impact, time critical nature and resource availability. RS.MA.R1 adds that incidents should not be handled first come, first served.
*Rule:* if `incidents-categorized-and-prioritized` = no, then `gap-no-incident-prioritization`
*Recommendation:* Categorize incidents by type and prioritize response speed by scope, likely impact, urgency and available resources.

**R15. Incident status is tracked so escalation can be initiated**
*Source:* RS.MA-04.R1, Table 3, PDF p. 36 (doc p. 28), High. Track and validate the status of all ongoing incidents so that those needing more resources or a changed strategy are identified and the changes initiated rapidly.
*Rule:* if `incident-status-tracked` = no, then `gap-no-incident-status-tracking`
*Recommendation:* Track and validate the status of every ongoing incident so those needing escalation are identified quickly.

**R16. Incident notification and coordination procedures are established**
*Source:* RS.CO-02.R2, Table 3, PDF p. 38 (doc p. 30), High. Follow established incident coordination procedures covering what must be reported, to whom, and at what times.
*Rule:* if `notification-procedures-defined` = no, then `gap-no-notification-procedures`
*Recommendation:* Establish coordination procedures stating what must be reported, to whom and when, aligned with applicable legal and regulatory requirements.

**R17. Containment and eradication criteria are in place**
*Source:* RS.MI-01 and RS.MI-02, with RS.MI.N1, Table 3, PDF pp. 40 to 41 (doc pp. 32 to 33), High. Incidents are contained, and incidents are eradicated. Containment prevents the expansion of an incident, and most incidents require some form of it; eradication eliminates persistence mechanisms and entry points. Selecting these actions is easier and faster where the organization has criteria and procedures in place, accounting for incident type and the intended duration of the measure.
*Rule:* if `containment-eradication-criteria` = no, then `gap-no-containment-eradication-criteria`
*Recommendation:* Define criteria and procedures for selecting containment and eradication actions, accounting for incident type and how long each measure is meant to last.

---

## Group D. Recovery and Improvement

**R18. Backups are created, protected, maintained and tested**
*Source:* PR.DS-11, Table 2, PDF p. 30 (doc p. 22), High. Backups of data are created, protected, maintained and tested. NIST notes backups are particularly important for recovery when data integrity or availability is affected.
*Rule:* if `backups-created-and-tested` = no, then `gap-no-tested-backups`
*Recommendation:* Create, protect, maintain and test backups of data.

**R19. Criteria for initiating incident recovery are defined**
*Source:* RS.MA-05.R1 and R2, Table 3, PDF p. 36 (doc p. 28), High. Apply incident recovery criteria to the characteristics of the incident to determine when recovery should be initiated, taking the possible operational disruption of recovery itself into account.
*Rule:* if `recovery-initiation-criteria` = no, then `gap-no-recovery-initiation-criteria`
*Recommendation:* Define recovery criteria and apply them to each incident, allowing for the disruption recovery may cause, to decide when recovery begins.

**R20. Backup and restoration asset integrity is verified before use**
*Source:* RC.RP-03.R1, Table 3, PDF p. 42 (doc p. 34), High. Check restoration assets for indicators of compromise, file corruption and other integrity issues before use.
*Rule:* if `backup-integrity-verified` = no, then `gap-no-backup-integrity-verification`
*Recommendation:* Check backups and other restoration assets for indicators of compromise and corruption before restoring from them.

**R21. Restored assets are verified before return to production**
*Source:* RC.RP-05.R1 and R2, Table 3, PDF p. 42 (doc p. 34), High. Check restored assets for indicators of compromise and remediate the incident's root causes before production use, and verify the correctness of restoration actions before putting a system online.
*Rule:* if `restored-assets-verified` = no, then `gap-no-restored-asset-verification`
*Recommendation:* Check restored assets for indicators of compromise and remediate root causes before returning systems to production.

**R22. Incident root cause analysis is performed**
*Source:* RS.AN-03.R3, Table 3, PDF p. 36 (doc p. 28), High. Analyze the incident to find the underlying or systemic root causes. NIST notes this helps identify weaknesses that should be addressed to prevent similar incidents.
*Rule:* if `root-cause-analysis` = no, then `gap-no-root-cause-analysis`
*Recommendation:* Analyze incidents to find their underlying root causes, and use the findings to address the weaknesses that allowed them.

**R23. An after action report is produced when recovery concludes**
*Source:* RC.RP-06.R1, Table 3, PDF p. 42 (doc p. 34), High. Prepare an after action report documenting the incident, the response and recovery actions taken, and lessons learned.
*Rule:* if `after-action-report` = no, then `gap-no-after-action-report`
*Recommendation:* Prepare an after action report at the end of each recovery documenting the incident, the actions taken and the lessons learned.

---

## Group E. Derived rules

These read facts produced by the rules above rather than answers from the user, so the system performs multi step inference and goal directed queries have something to prove. NIST states that recommendations made at Function or Category level also apply to their component elements (PDF p. 18), which is the basis for grounding them on higher level statements.

**R24. Continuous monitoring coverage is incomplete**
*Source:* DE.CM.R1, Table 3, PDF p. 31 (doc p. 23), High. Continuous monitoring should involve these asset types at all times: networks and network services; computing hardware and software, runtime environments and their data; the physical environment; personnel activity and technology usage; and external service provider activities.
*Rule:* if any of `gap-no-log-availability`, `gap-no-network-monitoring`, `gap-no-endpoint-monitoring`, then `detection-capability-incomplete`
*Recommendation:* Extend continuous monitoring to cover the asset types listed in DE.CM.R1 at all times, and make log records available to support it.

**R25. Incident management is inadequate**
*Source:* RS.MA.R1, R2 and R3, Table 3, PDF pp. 34 to 35 (doc pp. 26 to 27), High. Incidents should not be handled first come, first served. Triage, prioritization, escalation and elevation should all rest on a set of risk evaluation factors, and status should be tracked for each incident.
*Rule:* if any of `gap-no-incident-triage`, `gap-no-incident-prioritization`, `gap-no-incident-status-tracking`, then `response-management-inadequate`
*Recommendation:* Establish triage, prioritization and status tracking driven by defined risk evaluation factors rather than by order of arrival.

**R26. Recovery preparedness is inadequate**
*Source:* RC.N1 and N2, with RC.RP.N1, Table 3, PDF pp. 41 to 42 (doc pp. 33 to 34), High. Recovery operations include restoring from clean backups. Executing the recovery plan involves performing recovery actions securely, verifying the integrity of recovered assets, declaring the end of recovery and completing documentation.
*Rule:* if any of `gap-no-tested-backups`, `gap-no-backup-integrity-verification`, `gap-no-restored-asset-verification`, `gap-no-recovery-initiation-criteria`, then `recovery-preparedness-inadequate`
*Recommendation:* Put the elements recovery depends on in place: tested backups, integrity verification of restoration assets, verification of restored assets, and defined criteria for when recovery begins.

---

## Notes on individual rules

Most rules restate a NIST recommendation directly as a presence test. These needed a decision:

- **R02 and R03** both come from GV.RR-02 but test different things, because NIST separates documenting responsibility from granting authority.
- **R04 and R05** both come from ID.IM-04, separating whether a plan exists from whether it is maintained.
- **R05** names no review interval, because NIST says periodically without naming one.
- **R07** is grouped with detection although NIST places PR.PS-04 in the preparation table, because the detection rules depend on it.
- **R09** turns five NIST recommendations into one fact, since a respondent could not answer them separately. All five stay in the recommendation text.
- **R17** is framed around criteria rather than whether incidents get contained, since readiness is what the system assesses. It rests on the two Subcategory outcomes, which are normative, with the Category note explaining why criteria matter.
- **R19** sits with recovery although NIST places RS.MA-05 in Respond, because it governs when recovery starts.
- **R20 and R21** are distinct: one verifies the source of a restoration, the other its result.
- **R24 to R26** use disjunctions rather than counts, because the source requires all of the listed elements rather than most of them.

## Summary

| | Count |
|---|---|
| Rules | 26 |
| Reading primitive facts | 23 |
| Reading derived facts | 3 |
| Primitive facts | 23 |
| Derived facts | 26 |
| From High priority elements | 21 |
| From Medium priority elements | 5 |

## Known limits

- Continuous monitoring is assessed across three of the five asset classes DE.CM.R1 lists. The physical environment and external service provider activities are not assessed.
- The conclusions of R24 to R26 use the words incomplete and inadequate. The claims underneath are source backed; the wording is this project's.
- Every citation and priority in this file was checked line by line against the text of the source PDF.
- Not used: all Low rated elements; risk assessment (ID.RA), which NIST places outside this Profile's scope; asset management (ID.AM); threat intelligence (ID.RA-02); and the Protect Subcategories carrying only the generic note. Items marked `C` are not used, since NIST presents them as things to consider rather than to do.
