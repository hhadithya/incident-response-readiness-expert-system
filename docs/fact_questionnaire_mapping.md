# Fact and Questionnaire Model

The facts the system reasons over, and the questions that collect them. Rule definitions are in [rule_source_mapping.md](rule_source_mapping.md).

## Answer values

| Value | Meaning |
|---|---|
| `yes` | The practice is in place. |
| `no` | The practice is not in place. |
| `unknown` | The respondent does not know. |

Facts are phrased so that `yes` means the practice is present, and every rule fires on `no`.

`unknown` is not treated as `no`. A rule fires only when its condition is definitely met, so an unknown answer produces neither a gap nor a clean result. The system lists unknown answers separately as items it could not assess, since reporting a gap the organization may not have would be as wrong as missing one it does.

## Primitive facts

Collected from the user. One per rule, in the order the questionnaire asks them.

### Preparation and governance

| Fact | Variable | Question | Rule | Source |
|---|---|---|---|---|
| F01 | `ir-policy-exists` | Does your organization have a documented incident response policy? | R01 | GV.PO.R1 |
| F02 | `ir-roles-documented` | Are incident response roles and responsibilities documented in your organization's policies? | R02 | GV.RR-02.R1 |
| F03 | `ir-authority-designated` | Have the people with incident response responsibilities been given the authority they need to carry them out? | R03 | GV.RR-02.R2 |
| F04 | `ir-plan-exists` | Does your organization have an incident response plan? | R04 | ID.IM-04 |
| F05 | `ir-plan-reviewed-periodically` | Is the incident response plan reviewed and updated periodically, or whenever a significant improvement is needed? | R05 | ID.IM-04.R2 |
| F06 | `role-based-ir-training` | Does role based training for staff in specialized roles cover their incident response responsibilities? | R06 | PR.AT-02.R1 |

### Detection

| Fact | Variable | Question | Rule | Source |
|---|---|---|---|---|
| F07 | `logs-generated-and-available` | Are log records generated across your systems and made available for monitoring? | R07 | PR.PS-04 |
| F08 | `network-monitoring` | Are networks and network services monitored for potentially adverse events? | R08 | DE.CM-01.R1 |
| F09 | `endpoint-and-service-monitoring` | Are computing hardware, software and their data monitored for potentially adverse events? | R09 | DE.CM-09 |
| F10 | `event-correlation` | Is event information from different sources brought together and correlated? | R10 | DE.AE-03 |
| F11 | `alerts-reach-responders` | Do alerts and log analysis findings reach the staff and tools responsible for incident response? | R11 | DE.AE-06 |
| F12 | `incident-declaration-criteria` | Has your organization defined the criteria for deciding when an incident is declared? | R12 | DE.AE-08.R1 |

### Response

| Fact | Variable | Question | Rule | Source |
|---|---|---|---|---|
| F13 | `incident-triage-performed` | Is each new incident report reviewed to confirm an incident occurred and to estimate its severity and urgency? | R13 | RS.MA-02.R1 |
| F14 | `incidents-categorized-and-prioritized` | Are incidents categorized by type and prioritized for how quickly they are handled? | R14 | RS.MA-03 |
| F15 | `incident-status-tracked` | Is the status of every ongoing incident tracked, so that incidents needing escalation are identified? | R15 | RS.MA-04.R1 |
| F16 | `notification-procedures-defined` | Are there established procedures stating what must be reported about an incident, to whom, and when? | R16 | RS.CO-02.R2 |
| F17 | `containment-eradication-criteria` | Has your organization defined criteria and procedures for containing and eradicating incidents? | R17 | RS.MI.N1 |

### Recovery and improvement

| Fact | Variable | Question | Rule | Source |
|---|---|---|---|---|
| F18 | `backups-created-and-tested` | Are backups of data created, protected, maintained and tested? | R18 | PR.DS-11 |
| F19 | `recovery-initiation-criteria` | Has your organization defined the criteria for deciding when incident recovery should begin? | R19 | RS.MA-05 |
| F20 | `backup-integrity-verified` | Are backups and other restoration assets checked for integrity before they are used to restore systems? | R20 | RC.RP-03.R1 |
| F21 | `restored-assets-verified` | Are restored systems checked, and the incident's root causes remediated, before they return to production use? | R21 | RC.RP-05 |
| F22 | `root-cause-analysis` | Are incidents analyzed to find their underlying root causes? | R22 | RS.AN-03.R3 |
| F23 | `after-action-report` | Is an after action report produced at the end of each incident recovery? | R23 | RC.RP-06.R1 |

## Derived facts

Produced by rules, never asked. Each of R01 to R23 produces one gap fact, named in the rule mapping. The three derived rules each produce a state fact:

| Fact | Produced by | From |
|---|---|---|
| `detection-capability-incomplete` | R24 | `gap-no-log-availability`, `gap-no-network-monitoring`, `gap-no-endpoint-monitoring` |
| `response-management-inadequate` | R25 | `gap-no-incident-triage`, `gap-no-incident-prioritization`, `gap-no-incident-status-tracking` |
| `recovery-preparedness-inadequate` | R26 | `gap-no-tested-backups`, `gap-no-backup-integrity-verification`, `gap-no-restored-asset-verification`, `gap-no-recovery-initiation-criteria` |

## Coverage

23 questions, 23 primitive facts, 26 derived facts.

R01 to R23 each read one primitive fact, so every rule has its input and every question serves a rule. R24 to R26 read only gap facts. Nothing is asked twice and nothing is collected unused.

Questions are written for someone who manages IT or security, not for a specialist in the source document. Each asks about one practice and avoids the CSF terminology behind it. Two are compromises: F09 covers five NIST recommendations in one question, and F17 combines containment and eradication, which NIST treats as separate Subcategories under one set of criteria.
