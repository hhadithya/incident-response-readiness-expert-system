;;; Incident Response Readiness Expert System
;;; Knowledge base: templates and rules.
;;;
;;; Every rule corresponds to an entry in docs/rule_source_mapping.md and
;;; carries the NIST SP 800-61r3 location it was derived from. Rule IDs and
;;; fact names match that document.

(deftemplate answer
   (slot name)
   (slot value (allowed-symbols yes no unknown)))

(deftemplate finding
   (slot rule-id)
   (slot area (allowed-symbols preparation detection response recovery))
   (slot title)
   (slot asked)
   (multislot depends-on)
   (slot conclusion)
   (slot finding)
   (slot recommendation)
   (slot source)
   (slot page)
   (slot priority (allowed-symbols High Medium Low)))

;;; ------------------------------------------------------------------
;;; Group A. Preparation and governance
;;; ------------------------------------------------------------------

; R01 | NIST SP 800-61r3 | GV.PO.R1 | Table 2 | PDF p. 21
(defrule R01-incident-response-policy
   (answer (name ir-policy-exists) (value no))
   =>
   (assert (finding
      (rule-id R01)
      (area preparation)
      (title "Incident response policy")
      (asked ir-policy-exists)
      (conclusion gap-ir-policy-missing)
      (finding "The organization has no documented incident response policy.")
      (recommendation "Establish an incident response policy as part of the organization's cybersecurity policies.")
      (source "GV.PO.R1")
      (page "PDF p. 21 (doc p. 13)")
      (priority High))))

; R02 | NIST SP 800-61r3 | GV.RR-02.R1 | Table 2 | PDF p. 21
(defrule R02-roles-documented
   (answer (name ir-roles-documented) (value no))
   =>
   (assert (finding
      (rule-id R02)
      (area preparation)
      (title "Incident response roles and responsibilities")
      (asked ir-roles-documented)
      (conclusion gap-ir-roles-undocumented)
      (finding "Incident response roles and responsibilities are not documented in the organization's policies.")
      (recommendation "Document all incident response roles and responsibilities in the organization's policies.")
      (source "GV.RR-02.R1")
      (page "PDF p. 21 (doc p. 13)")
      (priority Medium))))

; R03 | NIST SP 800-61r3 | GV.RR-02.R2 | Table 2 | PDF p. 21
(defrule R03-authority-designated
   (answer (name ir-authority-designated) (value no))
   =>
   (assert (finding
      (rule-id R03)
      (area preparation)
      (title "Authority for incident response")
      (asked ir-authority-designated)
      (conclusion gap-ir-authority-not-designated)
      (finding "People holding incident response responsibilities have not been given the authority needed to carry them out.")
      (recommendation "Designate the authority each person or party needs to carry out their incident response responsibilities.")
      (source "GV.RR-02.R2")
      (page "PDF p. 21 (doc p. 13)")
      (priority Medium))))

; R04 | NIST SP 800-61r3 | ID.IM-04 | Table 2 | PDF pp. 27 to 28
(defrule R04-incident-response-plan
   (answer (name ir-plan-exists) (value no))
   =>
   (assert (finding
      (rule-id R04)
      (area preparation)
      (title "Incident response plan")
      (asked ir-plan-exists)
      (conclusion gap-ir-plan-missing)
      (finding "The organization has no incident response plan.")
      (recommendation "Establish and communicate an incident response plan covering how incident response is carried out.")
      (source "ID.IM-04")
      (page "PDF pp. 27 to 28 (doc pp. 19 to 20)")
      (priority High))))

; R05 | NIST SP 800-61r3 | ID.IM-04.R2 | Table 2 | PDF p. 28
(defrule R05-plan-maintenance
   (answer (name ir-plan-reviewed-periodically) (value no))
   =>
   (assert (finding
      (rule-id R05)
      (area preparation)
      (title "Plan review and update")
      (asked ir-plan-reviewed-periodically)
      (conclusion gap-ir-plan-not-maintained)
      (finding "The incident response plan is not reviewed and updated periodically.")
      (recommendation "Review and update the incident response plan periodically and whenever a significant improvement is needed.")
      (source "ID.IM-04.R2")
      (page "PDF p. 28 (doc p. 20)")
      (priority High))))

; R06 | NIST SP 800-61r3 | PR.AT-02.R1 | Table 2 | PDF p. 29
(defrule R06-role-based-training
   (answer (name role-based-ir-training) (value no))
   =>
   (assert (finding
      (rule-id R06)
      (area preparation)
      (title "Role based incident response training")
      (asked role-based-ir-training)
      (conclusion gap-no-role-based-ir-training)
      (finding "Role based training for staff in specialized roles does not cover their incident response responsibilities.")
      (recommendation "Include incident related responsibilities in the role based training given to staff in specialized roles.")
      (source "PR.AT-02.R1")
      (page "PDF p. 29 (doc p. 21)")
      (priority Medium))))

;;; ------------------------------------------------------------------
;;; Group B. Detection
;;; ------------------------------------------------------------------

; R07 | NIST SP 800-61r3 | PR.PS-04 | Table 2 | PDF p. 30
(defrule R07-log-availability
   (answer (name logs-generated-and-available) (value no))
   =>
   (assert (finding
      (rule-id R07)
      (area detection)
      (title "Log generation and availability")
      (asked logs-generated-and-available)
      (conclusion gap-no-log-availability)
      (finding "Log records are not generated across systems or are not available for monitoring.")
      (recommendation "Generate log records across organizational systems and make them available for continuous monitoring.")
      (source "PR.PS-04")
      (page "PDF p. 30 (doc p. 22)")
      (priority Medium))))

; R08 | NIST SP 800-61r3 | DE.CM-01.R1 | Table 3 | PDF p. 32
(defrule R08-network-monitoring
   (answer (name network-monitoring) (value no))
   =>
   (assert (finding
      (rule-id R08)
      (area detection)
      (title "Network monitoring")
      (asked network-monitoring)
      (conclusion gap-no-network-monitoring)
      (finding "Networks and network services are not monitored for potentially adverse events.")
      (recommendation "Monitor wired and wireless networks, network flows and network services, and watch for rogue networks within facilities.")
      (source "DE.CM-01.R1")
      (page "PDF p. 32 (doc p. 24)")
      (priority High))))

; R09 | NIST SP 800-61r3 | DE.CM-09.R1 to R5 | Table 3 | PDF p. 32
(defrule R09-endpoint-monitoring
   (answer (name endpoint-and-service-monitoring) (value no))
   =>
   (assert (finding
      (rule-id R09)
      (area detection)
      (title "Hardware, software and data monitoring")
      (asked endpoint-and-service-monitoring)
      (conclusion gap-no-endpoint-monitoring)
      (finding "Computing hardware, software and their data are not monitored for potentially adverse events.")
      (recommendation "Monitor computing hardware, software and their data, covering common attack vectors, authentication attempts, configuration baselines, signs of tampering and endpoint health.")
      (source "DE.CM-09.R1 to R5")
      (page "PDF p. 32 (doc p. 24)")
      (priority High))))

; R10 | NIST SP 800-61r3 | DE.AE-03.R1 and R2 | Table 3 | PDF p. 33
(defrule R10-event-correlation
   (answer (name event-correlation) (value no))
   =>
   (assert (finding
      (rule-id R10)
      (area detection)
      (title "Event correlation")
      (asked event-correlation)
      (conclusion gap-no-event-correlation)
      (finding "Event information from different sources is not brought together and correlated.")
      (recommendation "Centralize log data and use event correlation technology to relate data captured by different sources.")
      (source "DE.AE-03.R1 and R2")
      (page "PDF p. 33 (doc p. 25)")
      (priority High))))

; R11 | NIST SP 800-61r3 | DE.AE-06.R1 and R2 | Table 3 | PDF p. 34
(defrule R11-alerts-reach-responders
   (answer (name alerts-reach-responders) (value no))
   =>
   (assert (finding
      (rule-id R11)
      (area detection)
      (title "Alerts reaching responders")
      (asked alerts-reach-responders)
      (conclusion gap-alerts-not-reaching-responders)
      (finding "Alerts and log analysis findings do not reach the staff and tools responsible for incident response.")
      (recommendation "Route alerts to incident response staff and tools, and keep log analysis findings accessible to responders at all times.")
      (source "DE.AE-06.R1 and R2")
      (page "PDF p. 34 (doc p. 26)")
      (priority High))))

; R12 | NIST SP 800-61r3 | DE.AE-08.R1 | Table 3 | PDF p. 34
(defrule R12-incident-declaration-criteria
   (answer (name incident-declaration-criteria) (value no))
   =>
   (assert (finding
      (rule-id R12)
      (area detection)
      (title "Incident declaration criteria")
      (asked incident-declaration-criteria)
      (conclusion gap-no-incident-declaration-criteria)
      (finding "The organization has not defined the criteria for deciding when an incident is declared.")
      (recommendation "Define incident criteria and apply them to analyzed activity, allowing for known false positives, to decide when to declare an incident.")
      (source "DE.AE-08.R1")
      (page "PDF p. 34 (doc p. 26)")
      (priority High))))

;;; ------------------------------------------------------------------
;;; Group C. Response
;;; ------------------------------------------------------------------

; R13 | NIST SP 800-61r3 | RS.MA-02.R1 | Table 3 | PDF p. 35
(defrule R13-incident-triage
   (answer (name incident-triage-performed) (value no))
   =>
   (assert (finding
      (rule-id R13)
      (area response)
      (title "Incident triage")
      (asked incident-triage-performed)
      (conclusion gap-no-incident-triage)
      (finding "New incident reports are not reviewed to confirm an incident occurred and estimate its severity and urgency.")
      (recommendation "Review each new incident report to confirm an incident occurred, then estimate its severity and response urgency.")
      (source "RS.MA-02.R1")
      (page "PDF p. 35 (doc p. 27)")
      (priority High))))

; R14 | NIST SP 800-61r3 | RS.MA-03.R1 and R2 | Table 3 | PDF pp. 35 to 36
(defrule R14-categorization-and-prioritization
   (answer (name incidents-categorized-and-prioritized) (value no))
   =>
   (assert (finding
      (rule-id R14)
      (area response)
      (title "Incident categorization and prioritization")
      (asked incidents-categorized-and-prioritized)
      (conclusion gap-no-incident-prioritization)
      (finding "Incidents are not categorized by type or prioritized for how quickly they are handled.")
      (recommendation "Categorize incidents by type and prioritize response speed by scope, likely impact, urgency and available resources.")
      (source "RS.MA-03.R1 and R2")
      (page "PDF pp. 35 to 36 (doc pp. 27 to 28)")
      (priority High))))

; R15 | NIST SP 800-61r3 | RS.MA-04.R1 | Table 3 | PDF p. 36
(defrule R15-incident-status-tracking
   (answer (name incident-status-tracked) (value no))
   =>
   (assert (finding
      (rule-id R15)
      (area response)
      (title "Incident status tracking")
      (asked incident-status-tracked)
      (conclusion gap-no-incident-status-tracking)
      (finding "The status of ongoing incidents is not tracked, so incidents needing escalation may not be identified.")
      (recommendation "Track and validate the status of every ongoing incident so those needing escalation are identified quickly.")
      (source "RS.MA-04.R1")
      (page "PDF p. 36 (doc p. 28)")
      (priority High))))

; R16 | NIST SP 800-61r3 | RS.CO-02.R2 | Table 3 | PDF p. 38
(defrule R16-notification-procedures
   (answer (name notification-procedures-defined) (value no))
   =>
   (assert (finding
      (rule-id R16)
      (area response)
      (title "Notification and coordination procedures")
      (asked notification-procedures-defined)
      (conclusion gap-no-notification-procedures)
      (finding "There are no established procedures stating what must be reported about an incident, to whom, and when.")
      (recommendation "Establish coordination procedures stating what must be reported, to whom and when, aligned with applicable legal and regulatory requirements.")
      (source "RS.CO-02.R2")
      (page "PDF p. 38 (doc p. 30)")
      (priority High))))

; R17 | NIST SP 800-61r3 | RS.MI-01 and RS.MI-02, with RS.MI.N1 | Table 3 | PDF pp. 40 to 41
(defrule R17-containment-and-eradication
   (answer (name containment-eradication-criteria) (value no))
   =>
   (assert (finding
      (rule-id R17)
      (area response)
      (title "Containment and eradication criteria")
      (asked containment-eradication-criteria)
      (conclusion gap-no-containment-eradication-criteria)
      (finding "The organization has no defined criteria or procedures for containing and eradicating incidents.")
      (recommendation "Define criteria and procedures for selecting containment and eradication actions, accounting for incident type and how long each measure is meant to last.")
      (source "RS.MI-01 and RS.MI-02, with RS.MI.N1")
      (page "PDF pp. 40 to 41 (doc pp. 32 to 33)")
      (priority High))))

;;; ------------------------------------------------------------------
;;; Group D. Recovery and improvement
;;; ------------------------------------------------------------------

; R18 | NIST SP 800-61r3 | PR.DS-11 | Table 2 | PDF p. 30
(defrule R18-backups-tested
   (answer (name backups-created-and-tested) (value no))
   =>
   (assert (finding
      (rule-id R18)
      (area recovery)
      (title "Backups")
      (asked backups-created-and-tested)
      (conclusion gap-no-tested-backups)
      (finding "Backups of data are not created, protected, maintained and tested.")
      (recommendation "Create, protect, maintain and test backups of data.")
      (source "PR.DS-11")
      (page "PDF p. 30 (doc p. 22)")
      (priority High))))

; R19 | NIST SP 800-61r3 | RS.MA-05.R1 and R2 | Table 3 | PDF p. 36
(defrule R19-recovery-initiation-criteria
   (answer (name recovery-initiation-criteria) (value no))
   =>
   (assert (finding
      (rule-id R19)
      (area recovery)
      (title "Recovery initiation criteria")
      (asked recovery-initiation-criteria)
      (conclusion gap-no-recovery-initiation-criteria)
      (finding "The organization has not defined the criteria for deciding when incident recovery should begin.")
      (recommendation "Define recovery criteria and apply them to each incident, allowing for the disruption recovery may cause, to decide when recovery begins.")
      (source "RS.MA-05.R1 and R2")
      (page "PDF p. 36 (doc p. 28)")
      (priority High))))

; R20 | NIST SP 800-61r3 | RC.RP-03.R1 | Table 3 | PDF p. 42
(defrule R20-backup-integrity-verified
   (answer (name backup-integrity-verified) (value no))
   =>
   (assert (finding
      (rule-id R20)
      (area recovery)
      (title "Restoration asset integrity")
      (asked backup-integrity-verified)
      (conclusion gap-no-backup-integrity-verification)
      (finding "Backups and other restoration assets are not checked for integrity before they are used to restore systems.")
      (recommendation "Check backups and other restoration assets for indicators of compromise and corruption before restoring from them.")
      (source "RC.RP-03.R1")
      (page "PDF p. 42 (doc p. 34)")
      (priority High))))

; R21 | NIST SP 800-61r3 | RC.RP-05.R1 and R2 | Table 3 | PDF p. 42
(defrule R21-restored-assets-verified
   (answer (name restored-assets-verified) (value no))
   =>
   (assert (finding
      (rule-id R21)
      (area recovery)
      (title "Verification of restored assets")
      (asked restored-assets-verified)
      (conclusion gap-no-restored-asset-verification)
      (finding "Restored systems are not checked, and root causes are not remediated, before they return to production use.")
      (recommendation "Check restored assets for indicators of compromise and remediate root causes before returning systems to production.")
      (source "RC.RP-05.R1 and R2")
      (page "PDF p. 42 (doc p. 34)")
      (priority High))))

; R22 | NIST SP 800-61r3 | RS.AN-03.R3 | Table 3 | PDF p. 36
(defrule R22-root-cause-analysis
   (answer (name root-cause-analysis) (value no))
   =>
   (assert (finding
      (rule-id R22)
      (area recovery)
      (title "Root cause analysis")
      (asked root-cause-analysis)
      (conclusion gap-no-root-cause-analysis)
      (finding "Incidents are not analyzed to find their underlying root causes.")
      (recommendation "Analyze incidents to find their underlying root causes, and use the findings to address the weaknesses that allowed them.")
      (source "RS.AN-03.R3")
      (page "PDF p. 36 (doc p. 28)")
      (priority High))))

; R23 | NIST SP 800-61r3 | RC.RP-06.R1 | Table 3 | PDF p. 42
(defrule R23-after-action-report
   (answer (name after-action-report) (value no))
   =>
   (assert (finding
      (rule-id R23)
      (area recovery)
      (title "After action report")
      (asked after-action-report)
      (conclusion gap-no-after-action-report)
      (finding "No after action report is produced at the end of an incident recovery.")
      (recommendation "Prepare an after action report at the end of each recovery documenting the incident, the actions taken and the lessons learned.")
      (source "RC.RP-06.R1")
      (page "PDF p. 42 (doc p. 34)")
      (priority High))))

;;; ------------------------------------------------------------------
;;; Group E. Rules that read findings asserted by other rules
;;;
;;; These give the system a second round of forward chaining: the findings
;;; above become the facts these rules match on.
;;; ------------------------------------------------------------------

; R24 | NIST SP 800-61r3 | DE.CM.R1 | Table 3 | PDF p. 31
(defrule R24-detection-coverage-incomplete
   (finding (conclusion gap-no-log-availability|gap-no-network-monitoring|gap-no-endpoint-monitoring))
   (not (finding (rule-id R24)))
   =>
   (assert (finding
      (rule-id R24)
      (area detection)
      (title "Continuous monitoring coverage")
      (depends-on gap-no-log-availability gap-no-network-monitoring gap-no-endpoint-monitoring)
      (conclusion detection-capability-incomplete)
      (finding "Continuous monitoring does not cover all the asset types NIST expects it to cover at all times.")
      (recommendation "Extend continuous monitoring to cover the asset types listed in DE.CM.R1 at all times, and make log records available to support it.")
      (source "DE.CM.R1")
      (page "PDF p. 31 (doc p. 23)")
      (priority High))))

; R25 | NIST SP 800-61r3 | RS.MA.R1, R2 and R3 | Table 3 | PDF pp. 34 to 35
(defrule R25-incident-management-inadequate
   (finding (conclusion gap-no-incident-triage|gap-no-incident-prioritization|gap-no-incident-status-tracking))
   (not (finding (rule-id R25)))
   =>
   (assert (finding
      (rule-id R25)
      (area response)
      (title "Incident management")
      (depends-on gap-no-incident-triage gap-no-incident-prioritization gap-no-incident-status-tracking)
      (conclusion response-management-inadequate)
      (finding "Incident management does not rest on the triage, prioritization and tracking NIST expects.")
      (recommendation "Establish triage, prioritization and status tracking driven by defined risk evaluation factors rather than by order of arrival.")
      (source "RS.MA.R1, R2 and R3")
      (page "PDF pp. 34 to 35 (doc pp. 26 to 27)")
      (priority High))))

; R26 | NIST SP 800-61r3 | RC.N1 and N2, with RC.RP.N1 | Table 3 | PDF pp. 41 to 42
(defrule R26-recovery-preparedness-inadequate
   (finding (conclusion gap-no-tested-backups|gap-no-backup-integrity-verification|gap-no-restored-asset-verification|gap-no-recovery-initiation-criteria))
   (not (finding (rule-id R26)))
   =>
   (assert (finding
      (rule-id R26)
      (area recovery)
      (title "Recovery preparedness")
      (depends-on gap-no-tested-backups gap-no-backup-integrity-verification gap-no-restored-asset-verification gap-no-recovery-initiation-criteria)
      (conclusion recovery-preparedness-inadequate)
      (finding "The elements incident recovery depends on are not all in place.")
      (recommendation "Put the elements recovery depends on in place: tested backups, integrity verification of restoration assets, verification of restored assets, and defined criteria for when recovery begins.")
      (source "RC.N1 and N2, with RC.RP.N1")
      (page "PDF pp. 41 to 42 (doc pp. 33 to 34)")
      (priority High))))
