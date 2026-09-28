"""The rules and questions, derived from NIST SP 800-61r3.

Every rule here corresponds to an entry in docs/rule_source_mapping.md and
carries the source location it was taken from. Rule IDs, fact names and
conclusions match that document exactly.
"""

from .models import (Answer, AnswerIs, Derived, FactBase, Group, Question,
                     Rule, SourceReference)

PREP, DETECT, RESPOND, RECOVER = (Group.PREPARATION, Group.DETECTION,
                                  Group.RESPONSE, Group.RECOVERY)


def _src(element, table, pdf_page, doc_page, priority, knowledge):
    return SourceReference(element=element, table=table, pdf_page=pdf_page,
                           doc_page=doc_page, priority=priority, knowledge=knowledge)


def _gap(rule_id, name, group, fact, conclusion, recommendation, source):
    """A rule that reports a gap when the user answers no."""
    return Rule(rule_id=rule_id, name=name, group=group,
                conditions=(AnswerIs(fact, Answer.NO),),
                conclusion=conclusion, recommendation=recommendation, source=source)


def _rollup(rule_id, name, group, gaps, conclusion, recommendation, source):
    """A rule that fires when any of the given gaps has been concluded."""
    return Rule(rule_id=rule_id, name=name, group=group,
                conditions=tuple(Derived(g) for g in gaps), match="any",
                conclusion=conclusion, recommendation=recommendation, source=source)


RULES = (
    _gap("R01", "Incident response policy exists", PREP,
         "ir_policy_exists", "gap_ir_policy_missing",
         "Establish an incident response policy as part of the organization's "
         "cybersecurity policies.",
         _src("GV.PO.R1", "Table 2", "21", "13", "High",
              "Cybersecurity policies should include an incident response policy.")),

    _gap("R02", "Incident response roles and responsibilities are documented", PREP,
         "ir_roles_documented", "gap_ir_roles_undocumented",
         "Document all incident response roles and responsibilities in the "
         "organization's policies.",
         _src("GV.RR-02.R1", "Table 2", "21", "13", "Medium",
              "All roles and responsibilities involving incident response should be "
              "documented in the organization's policies.")),

    _gap("R03", "Authority is designated to those with incident response responsibilities",
         PREP, "ir_authority_designated", "gap_ir_authority_not_designated",
         "Designate the authority each person or party needs to carry out their "
         "incident response responsibilities.",
         _src("GV.RR-02.R2", "Table 2", "21", "13", "Medium",
              "All appropriate individuals or parties should be designated the authority "
              "necessary to fulfill their incident response related responsibilities.")),

    _gap("R04", "An incident response plan is established", PREP,
         "ir_plan_exists", "gap_ir_plan_missing",
         "Establish and communicate an incident response plan covering how incident "
         "response is carried out.",
         _src("ID.IM-04", "Table 2", "27 to 28", "19 to 20", "High",
              "Incident response plans and other cybersecurity plans affecting operations "
              "are established, communicated, maintained and improved. NIST describes the "
              "incident response plan as the roadmap for the incident response capability.")),

    _gap("R05", "Cybersecurity plans are reviewed and updated periodically", PREP,
         "ir_plan_reviewed_periodically", "gap_ir_plan_not_maintained",
         "Review and update the incident response plan periodically and whenever a "
         "significant improvement is needed.",
         _src("ID.IM-04.R2", "Table 2", "28", "20", "High",
              "Review and update all cybersecurity plans periodically, or when a need for "
              "significant improvement is identified.")),

    _gap("R06", "Role based training covers incident response responsibilities", PREP,
         "role_based_ir_training", "gap_no_role_based_ir_training",
         "Include incident related responsibilities in the role based training given to "
         "staff in specialized roles.",
         _src("PR.AT-02.R1", "Table 2", "29", "21", "Medium",
              "Role based training should include incident related responsibilities.")),

    _gap("R07", "Suppliers and third parties are included in incident planning, response "
         "and recovery", PREP,
         "third_parties_in_ir_planning", "gap_third_parties_excluded_from_ir",
         "Include relevant suppliers and third parties in incident planning, response and "
         "recovery, and define the division of responsibilities in contract.",
         _src("GV.SC-08", "Table 2", "23", "15", "Medium",
              "Relevant suppliers and other third parties are included in incident "
              "planning, response and recovery activities.")),

    _gap("R08", "Log records are generated and available", DETECT,
         "logs_generated_and_available", "gap_no_log_availability",
         "Generate log records across organizational systems and make them available for "
         "continuous monitoring.",
         _src("PR.PS-04", "Table 2", "30", "22", "Medium",
              "Log records are generated and made available for continuous monitoring. "
              "NIST notes logs are particularly important for incident detection, response "
              "and recovery.")),

    _gap("R09", "Networks and network services are monitored", DETECT,
         "network_monitoring", "gap_no_network_monitoring",
         "Monitor wired and wireless networks, network flows and network services, and "
         "watch for rogue networks within facilities.",
         _src("DE.CM-01.R1", "Table 3", "32", "24", "High",
              "Monitoring should include wired and wireless networks, network "
              "communications and flows, network services such as DNS and BGP, and the "
              "presence of rogue networks within facilities.")),

    _gap("R10", "Computing hardware, software and their data are monitored", DETECT,
         "endpoint_and_service_monitoring", "gap_no_endpoint_monitoring",
         "Monitor computing hardware, software and their data, covering common attack "
         "vectors, authentication attempts, configuration baselines, signs of tampering "
         "and endpoint health.",
         _src("DE.CM-09.R1 to R5", "Table 3", "32", "24", "High",
              "Monitor common attack vectors such as email, web and file sharing for "
              "malware, phishing and exfiltration; monitor authentication attempts; "
              "monitor configurations against security baselines; monitor for tampering, "
              "failure or compromise; and monitor endpoints for cyber health issues.")),

    _gap("R11", "Event information is correlated from multiple sources", DETECT,
         "event_correlation", "gap_no_event_correlation",
         "Centralize log data and use event correlation technology to relate data "
         "captured by different sources.",
         _src("DE.AE-03.R1 and R2", "Table 3", "33", "25", "High",
              "Transfer log data to a relatively small number of log servers, and use "
              "event correlation technology such as SIEM or SOAR to gather related data "
              "captured by multiple sources.")),

    _gap("R12", "Adverse event information reaches incident responders", DETECT,
         "alerts_reach_responders", "gap_alerts_not_reaching_responders",
         "Route alerts to incident response staff and tools, and keep log analysis "
         "findings accessible to responders at all times.",
         _src("DE.AE-06.R1 and R2", "Table 3", "34", "26", "High",
              "Generate alerts and provide them to incident response tools and staff, and "
              "make log analysis findings accessible to responders at all times.")),

    _gap("R13", "Incident declaration criteria are defined and applied", DETECT,
         "incident_declaration_criteria", "gap_no_incident_declaration_criteria",
         "Define incident criteria and apply them to analyzed activity, allowing for known "
         "false positives, to decide when to declare an incident.",
         _src("DE.AE-08.R1", "Table 3", "34", "26", "High",
              "Incidents are declared when adverse events meet defined incident criteria. "
              "Apply those criteria to the characteristics of analyzed activity, allowing "
              "for known false positives.")),

    _gap("R14", "New incident reports are triaged and validated", RESPOND,
         "incident_triage_performed", "gap_no_incident_triage",
         "Review each new incident report to confirm an incident occurred, then estimate "
         "its severity and response urgency.",
         _src("RS.MA-02.R1", "Table 3", "35", "27", "High",
              "Perform a preliminary review of a new incident report to verify an incident "
              "has occurred, then estimate its severity and the urgency of response.")),

    _gap("R15", "Incidents are categorized and prioritized", RESPOND,
         "incidents_categorized_and_prioritized", "gap_no_incident_prioritization",
         "Categorize incidents by type and prioritize response speed by scope, likely "
         "impact, urgency and available resources.",
         _src("RS.MA-03.R1 and R2", "Table 3", "35 to 36", "27 to 28", "High",
              "Categorize incidents by type, and prioritize response speed by scope, likely "
              "impact, time critical nature and resource availability. RS.MA.R1 adds that "
              "incidents should not be handled first come, first served.")),

    _gap("R16", "Incident status is tracked so escalation can be initiated", RESPOND,
         "incident_status_tracked", "gap_no_incident_status_tracking",
         "Track and validate the status of every ongoing incident so those needing "
         "escalation are identified quickly.",
         _src("RS.MA-04.R1", "Table 3", "36", "28", "High",
              "Track and validate the status of all ongoing incidents so that those needing "
              "more resources or a changed strategy are identified and the changes "
              "initiated rapidly.")),

    _gap("R17", "Incident notification and coordination procedures are established", RESPOND,
         "notification_procedures_defined", "gap_no_notification_procedures",
         "Establish coordination procedures stating what must be reported, to whom and "
         "when, aligned with applicable legal and regulatory requirements.",
         _src("RS.CO-02.R2", "Table 3", "38", "30", "High",
              "Follow established incident coordination procedures covering what must be "
              "reported, to whom, and at what times.")),

    _gap("R18", "Containment and eradication criteria are in place", RESPOND,
         "containment_eradication_criteria", "gap_no_containment_eradication_criteria",
         "Define criteria and procedures for selecting containment and eradication "
         "actions, accounting for incident type and how long each measure is meant to last.",
         _src("RS.MI.N1", "Table 3", "40", "32", "High",
              "Activities are performed to prevent expansion of an event and mitigate its "
              "effects. Selecting containment and eradication actions is easier and faster "
              "where the organization has criteria and procedures in place, accounting for "
              "incident type and the intended duration of the measure.")),

    _gap("R19", "Backups are created, protected, maintained and tested", RECOVER,
         "backups_created_and_tested", "gap_no_tested_backups",
         "Create, protect, maintain and test backups of data.",
         _src("PR.DS-11", "Table 2", "30", "22", "High",
              "Backups of data are created, protected, maintained and tested. NIST notes "
              "backups are particularly important for recovery when data integrity or "
              "availability is affected.")),

    _gap("R20", "Criteria for initiating incident recovery are defined", RECOVER,
         "recovery_initiation_criteria", "gap_no_recovery_initiation_criteria",
         "Define recovery criteria and apply them to each incident, allowing for the "
         "disruption recovery may cause, to decide when recovery begins.",
         _src("RS.MA-05.R1 and R2", "Table 3", "36", "28", "High",
              "Apply incident recovery criteria to the characteristics of the incident to "
              "determine when recovery should be initiated, taking the possible operational "
              "disruption of recovery itself into account.")),

    _gap("R21", "Backup and restoration asset integrity is verified before use", RECOVER,
         "backup_integrity_verified", "gap_no_backup_integrity_verification",
         "Check backups and other restoration assets for indicators of compromise and "
         "corruption before restoring from them.",
         _src("RC.RP-03.R1", "Table 3", "42", "34", "High",
              "Check restoration assets for indicators of compromise, file corruption and "
              "other integrity issues before use.")),

    _gap("R22", "Restored assets are verified before return to production", RECOVER,
         "restored_assets_verified", "gap_no_restored_asset_verification",
         "Check restored assets for indicators of compromise and remediate root causes "
         "before returning systems to production.",
         _src("RC.RP-05.R1 and R2", "Table 3", "42", "34", "High",
              "Check restored assets for indicators of compromise and remediate the "
              "incident's root causes before production use, and verify the correctness of "
              "restoration actions before putting a system online.")),

    _gap("R23", "Incident root cause analysis is performed", RECOVER,
         "root_cause_analysis", "gap_no_root_cause_analysis",
         "Analyze incidents to find their underlying root causes, and use the findings to "
         "address the weaknesses that allowed them.",
         _src("RS.AN-03.R3", "Table 3", "36", "28", "High",
              "Analyze the incident to find the underlying or systemic root causes. NIST "
              "notes this helps identify weaknesses that should be addressed to prevent "
              "similar incidents.")),

    _gap("R24", "An after action report is produced when recovery concludes", RECOVER,
         "after_action_report", "gap_no_after_action_report",
         "Prepare an after action report at the end of each recovery documenting the "
         "incident, the actions taken and the lessons learned.",
         _src("RC.RP-06.R1", "Table 3", "42", "34", "High",
              "Prepare an after action report documenting the incident, the response and "
              "recovery actions taken, and lessons learned.")),

    _rollup("R25", "Continuous monitoring coverage is incomplete", DETECT,
            ("gap_no_log_availability", "gap_no_network_monitoring",
             "gap_no_endpoint_monitoring"),
            "detection_capability_incomplete",
            "Extend continuous monitoring to cover the asset types listed in DE.CM.R1 at "
            "all times, and make log records available to support it.",
            _src("DE.CM.R1", "Table 3", "31", "23", "High",
                 "Continuous monitoring should involve these asset types at all times: "
                 "networks and network services; computing hardware and software, runtime "
                 "environments and their data; the physical environment; personnel activity "
                 "and technology usage; and external service provider activities.")),

    _rollup("R26", "Incident management is inadequate", RESPOND,
            ("gap_no_incident_triage", "gap_no_incident_prioritization",
             "gap_no_incident_status_tracking"),
            "response_management_inadequate",
            "Establish triage, prioritization and status tracking driven by defined risk "
            "evaluation factors rather than by order of arrival.",
            _src("RS.MA.R1, R2 and R3", "Table 3", "34 to 35", "26 to 27", "High",
                 "Incidents should not be handled first come, first served. Triage, "
                 "prioritization, escalation and elevation should all rest on a set of risk "
                 "evaluation factors, and status should be tracked for each incident.")),

    _rollup("R27", "Recovery preparedness is inadequate", RECOVER,
            ("gap_no_tested_backups", "gap_no_backup_integrity_verification",
             "gap_no_restored_asset_verification", "gap_no_recovery_initiation_criteria"),
            "recovery_preparedness_inadequate",
            "Put the elements recovery depends on in place: tested backups, integrity "
            "verification of restoration assets, verification of restored assets, and "
            "defined criteria for when recovery begins.",
            _src("RC.N1 and N2, with RC.RP.N1", "Table 3", "41 to 42", "33 to 34", "High",
                 "Recovery operations include restoring from clean backups. Executing the "
                 "recovery plan involves performing recovery actions securely, verifying "
                 "the integrity of recovered assets, declaring the end of recovery and "
                 "completing documentation.")),
)


QUESTIONS = (
    Question("F01", "ir_policy_exists",
             "Does your organization have a documented incident response policy?", PREP),
    Question("F02", "ir_roles_documented",
             "Are incident response roles and responsibilities documented in your "
             "organization's policies?", PREP),
    Question("F03", "ir_authority_designated",
             "Have the people with incident response responsibilities been given the "
             "authority they need to carry them out?", PREP),
    Question("F04", "ir_plan_exists",
             "Does your organization have an incident response plan?", PREP),
    Question("F05", "ir_plan_reviewed_periodically",
             "Is the incident response plan reviewed and updated periodically, or whenever "
             "a significant improvement is needed?", PREP),
    Question("F06", "role_based_ir_training",
             "Does role based training for staff in specialized roles cover their incident "
             "response responsibilities?", PREP),
    Question("F07", "third_parties_in_ir_planning",
             "Are relevant suppliers and third parties included in incident planning, "
             "response and recovery activities?", PREP,
             (Answer.YES, Answer.NO, Answer.UNKNOWN, Answer.NOT_APPLICABLE)),

    Question("F08", "logs_generated_and_available",
             "Are log records generated across your systems and made available for "
             "monitoring?", DETECT),
    Question("F09", "network_monitoring",
             "Are networks and network services monitored for potentially adverse events?",
             DETECT),
    Question("F10", "endpoint_and_service_monitoring",
             "Are computing hardware, software and their data monitored for potentially "
             "adverse events?", DETECT),
    Question("F11", "event_correlation",
             "Is event information from different sources brought together and correlated?",
             DETECT),
    Question("F12", "alerts_reach_responders",
             "Do alerts and log analysis findings reach the staff and tools responsible for "
             "incident response?", DETECT),
    Question("F13", "incident_declaration_criteria",
             "Has your organization defined the criteria for deciding when an incident is "
             "declared?", DETECT),

    Question("F14", "incident_triage_performed",
             "Is each new incident report reviewed to confirm an incident occurred and to "
             "estimate its severity and urgency?", RESPOND),
    Question("F15", "incidents_categorized_and_prioritized",
             "Are incidents categorized by type and prioritized for how quickly they are "
             "handled?", RESPOND),
    Question("F16", "incident_status_tracked",
             "Is the status of every ongoing incident tracked, so that incidents needing "
             "escalation are identified?", RESPOND),
    Question("F17", "notification_procedures_defined",
             "Are there established procedures stating what must be reported about an "
             "incident, to whom, and when?", RESPOND),
    Question("F18", "containment_eradication_criteria",
             "Has your organization defined criteria and procedures for containing and "
             "eradicating incidents?", RESPOND),

    Question("F19", "backups_created_and_tested",
             "Are backups of data created, protected, maintained and tested?", RECOVER),
    Question("F20", "recovery_initiation_criteria",
             "Has your organization defined the criteria for deciding when incident "
             "recovery should begin?", RECOVER),
    Question("F21", "backup_integrity_verified",
             "Are backups and other restoration assets checked for integrity before they "
             "are used to restore systems?", RECOVER),
    Question("F22", "restored_assets_verified",
             "Are restored systems checked, and the incident's root causes remediated, "
             "before they return to production use?", RECOVER),
    Question("F23", "root_cause_analysis",
             "Are incidents analyzed to find their underlying root causes?", RECOVER),
    Question("F24", "after_action_report",
             "Is an after action report produced at the end of each incident recovery?",
             RECOVER),
)


def rule(rule_id):
    for r in RULES:
        if r.rule_id == rule_id:
            return r
    raise KeyError(rule_id)


def rules_concluding(fact):
    return [r for r in RULES if r.conclusion == fact]


def question_for(fact):
    for q in QUESTIONS:
        if q.fact == fact:
            return q
    raise KeyError(fact)


def fact_base_from(answers):
    base = FactBase()
    for fact, value in answers.items():
        base.record(fact, value if isinstance(value, Answer) else Answer.parse(value))
    return base


def validate():
    """Check the knowledge base is internally consistent.

    Returns a list of problems, empty when the knowledge base is sound.
    """
    problems = []

    seen_rules = set()
    for r in RULES:
        if r.rule_id in seen_rules:
            problems.append(f"duplicate rule id {r.rule_id}")
        seen_rules.add(r.rule_id)

    conclusions = {}
    for r in RULES:
        if r.conclusion in conclusions:
            problems.append(f"{r.rule_id} and {conclusions[r.conclusion]} share the "
                            f"conclusion {r.conclusion}")
        conclusions[r.conclusion] = r.rule_id

    asked = {q.fact for q in QUESTIONS}
    seen_facts = set()
    for q in QUESTIONS:
        if q.fact in seen_facts:
            problems.append(f"duplicate question fact {q.fact}")
        seen_facts.add(q.fact)

    used_primitive = set()
    for r in RULES:
        if not r.name or not r.recommendation:
            problems.append(f"{r.rule_id} is missing a name or recommendation")
        if not r.source.element or not r.source.knowledge:
            problems.append(f"{r.rule_id} is missing source metadata")
        if r.source.priority not in ("High", "Medium", "Low"):
            problems.append(f"{r.rule_id} has an unrecognized priority "
                            f"{r.source.priority!r}")
        for c in r.conditions:
            if isinstance(c, AnswerIs):
                used_primitive.add(c.fact)
                if c.fact not in asked:
                    problems.append(f"{r.rule_id} reads {c.fact}, which no question asks")
            elif isinstance(c, Derived):
                if c.fact not in conclusions:
                    problems.append(f"{r.rule_id} needs {c.fact}, which no rule concludes")
                elif c.fact == r.conclusion:
                    problems.append(f"{r.rule_id} depends on its own conclusion")

    for fact in sorted(asked - used_primitive):
        problems.append(f"question for {fact} is not used by any rule")

    for q in QUESTIONS:
        if Answer.YES not in q.allowed or Answer.NO not in q.allowed:
            problems.append(f"{q.fact_id} must allow yes and no")

    if len(RULES) < 20:
        problems.append(f"only {len(RULES)} rules, at least 20 are required")

    return problems
