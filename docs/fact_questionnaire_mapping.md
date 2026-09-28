# Fact and Questionnaire Model

The facts the system reasons over, and the questions that collect them. Rule definitions are in [rule_source_mapping.md](rule_source_mapping.md).

## Answer values

| Value | Meaning |
|---|---|
| `yes` | The practice is in place. |
| `no` | The practice is not in place. |
| `unknown` | The respondent does not know. |
| `not_applicable` | Accepted for F07 only. |

Facts are phrased so that `yes` means the practice is present, and every rule fires on `no`.

`unknown` is not treated as `no`. A rule fires only when its condition is definitely met, so an unknown answer produces neither a gap nor a clean result. The system lists unknown answers separately as items it could not assess, since reporting a gap the organization may not have would be as wrong as missing one it does.

`not_applicable` exists because F07 asks about suppliers and third parties. An organization that uses none cannot answer yes or no honestly, and treating that as a gap would be a false finding.

## Primitive facts

Collected from the user. One per rule, in the order the questionnaire asks them.

### Preparation and governance

| Fact | Variable | Question | Rule | Source |
|---|---|---|---|---|
| F01 | `ir_policy_exists` | Does your organization have a documented incident response policy? | R01 | GV.PO.R1 |
| F02 | `ir_roles_documented` | Are incident response roles and responsibilities documented in your organization's policies? | R02 | GV.RR-02.R1 |
| F03 | `ir_authority_designated` | Have the people with incident response responsibilities been given the authority they need to carry them out? | R03 | GV.RR-02.R2 |
| F04 | `ir_plan_exists` | Does your organization have an incident response plan? | R04 | ID.IM-04 |
| F05 | `ir_plan_reviewed_periodically` | Is the incident response plan reviewed and updated periodically, or whenever a significant improvement is needed? | R05 | ID.IM-04.R2 |
| F06 | `role_based_ir_training` | Does role based training for staff in specialized roles cover their incident response responsibilities? | R06 | PR.AT-02.R1 |
| F07 | `third_parties_in_ir_planning` | Are relevant suppliers and third parties included in incident planning, response and recovery activities? | R07 | GV.SC-08 |

### Detection

| Fact | Variable | Question | Rule | Source |
|---|---|---|---|---|
| F08 | `logs_generated_and_available` | Are log records generated across your systems and made available for monitoring? | R08 | PR.PS-04 |
| F09 | `network_monitoring` | Are networks and network services monitored for potentially adverse events? | R09 | DE.CM-01.R1 |
| F10 | `endpoint_and_service_monitoring` | Are computing hardware, software and their data monitored for potentially adverse events? | R10 | DE.CM-09 |
| F11 | `event_correlation` | Is event information from different sources brought together and correlated? | R11 | DE.AE-03 |
| F12 | `alerts_reach_responders` | Do alerts and log analysis findings reach the staff and tools responsible for incident response? | R12 | DE.AE-06 |
| F13 | `incident_declaration_criteria` | Has your organization defined the criteria for deciding when an incident is declared? | R13 | DE.AE-08.R1 |

### Response

| Fact | Variable | Question | Rule | Source |
|---|---|---|---|---|
| F14 | `incident_triage_performed` | Is each new incident report reviewed to confirm an incident occurred and to estimate its severity and urgency? | R14 | RS.MA-02.R1 |
| F15 | `incidents_categorized_and_prioritized` | Are incidents categorized by type and prioritized for how quickly they are handled? | R15 | RS.MA-03 |
| F16 | `incident_status_tracked` | Is the status of every ongoing incident tracked, so that incidents needing escalation are identified? | R16 | RS.MA-04.R1 |
| F17 | `notification_procedures_defined` | Are there established procedures stating what must be reported about an incident, to whom, and when? | R17 | RS.CO-02.R2 |
| F18 | `containment_eradication_criteria` | Has your organization defined criteria and procedures for containing and eradicating incidents? | R18 | RS.MI.N1 |

### Recovery and improvement

| Fact | Variable | Question | Rule | Source |
|---|---|---|---|---|
| F19 | `backups_created_and_tested` | Are backups of data created, protected, maintained and tested? | R19 | PR.DS-11 |
| F20 | `recovery_initiation_criteria` | Has your organization defined the criteria for deciding when incident recovery should begin? | R20 | RS.MA-05 |
| F21 | `backup_integrity_verified` | Are backups and other restoration assets checked for integrity before they are used to restore systems? | R21 | RC.RP-03.R1 |
| F22 | `restored_assets_verified` | Are restored systems checked, and the incident's root causes remediated, before they return to production use? | R22 | RC.RP-05 |
| F23 | `root_cause_analysis` | Are incidents analyzed to find their underlying root causes? | R23 | RS.AN-03.R3 |
| F24 | `after_action_report` | Is an after action report produced at the end of each incident recovery? | R24 | RC.RP-06.R1 |

## Derived facts

Produced by rules, never asked. Each primitive rule produces one gap fact; the three derived rules produce one state fact each.

### Gap facts

`gap_ir_policy_missing` (R01), `gap_ir_roles_undocumented` (R02), `gap_ir_authority_not_designated` (R03), `gap_ir_plan_missing` (R04), `gap_ir_plan_not_maintained` (R05), `gap_no_role_based_ir_training` (R06), `gap_third_parties_excluded_from_ir` (R07), `gap_no_log_availability` (R08), `gap_no_network_monitoring` (R09), `gap_no_endpoint_monitoring` (R10), `gap_no_event_correlation` (R11), `gap_alerts_not_reaching_responders` (R12), `gap_no_incident_declaration_criteria` (R13), `gap_no_incident_triage` (R14), `gap_no_incident_prioritization` (R15), `gap_no_incident_status_tracking` (R16), `gap_no_notification_procedures` (R17), `gap_no_containment_eradication_criteria` (R18), `gap_no_tested_backups` (R19), `gap_no_recovery_initiation_criteria` (R20), `gap_no_backup_integrity_verification` (R21), `gap_no_restored_asset_verification` (R22), `gap_no_root_cause_analysis` (R23), `gap_no_after_action_report` (R24)

### State facts

| Fact | Produced by | From |
|---|---|---|
| `detection_capability_incomplete` | R25 | `gap_no_log_availability`, `gap_no_network_monitoring`, `gap_no_endpoint_monitoring` |
| `response_management_inadequate` | R26 | `gap_no_incident_triage`, `gap_no_incident_prioritization`, `gap_no_incident_status_tracking` |
| `recovery_preparedness_inadequate` | R27 | `gap_no_tested_backups`, `gap_no_backup_integrity_verification`, `gap_no_restored_asset_verification`, `gap_no_recovery_initiation_criteria` |

## Coverage

24 questions, 24 primitive facts, 27 derived facts.

Rules R01 to R24 each read exactly one primitive fact, so every rule has the input it needs and every question serves a rule. Rules R25 to R27 read only gap facts produced by R01 to R24. No fact is collected twice and no fact is unused.

## Question wording

Questions are written for someone who manages IT or security in the organization, not for a specialist in the source document. Each asks about one practice, avoids the CSF terminology the rule is derived from, and can be answered without reading NIST SP 800-61r3.

Two are worth a second look before the interface is built:

- **F10** covers five NIST recommendations in one question. Asking about all five separately would be more precise but harder to answer.
- **F18** combines containment and eradication. NIST treats them as separate Subcategories but describes one set of criteria covering both.
