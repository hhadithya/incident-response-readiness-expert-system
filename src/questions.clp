;;; The questionnaire.
;;;
;;; One question per rule that reads a user supplied fact. Question ids and
;;; fact names match docs/fact_questionnaire_mapping.md. Questions are asked
;;; in the order they appear here.

(deftemplate question
   (slot id)
   (slot name)
   (slot area (allowed-symbols preparation detection response recovery))
   (slot text))

(deffacts questionnaire

   (question (id F01) (area preparation) (name ir-policy-exists)
      (text "Does your organization have a documented incident response policy?"))
   (question (id F02) (area preparation) (name ir-roles-documented)
      (text "Are incident response roles and responsibilities documented in your organization's policies?"))
   (question (id F03) (area preparation) (name ir-authority-designated)
      (text "Have the people with incident response responsibilities been given the authority they need to carry them out?"))
   (question (id F04) (area preparation) (name ir-plan-exists)
      (text "Does your organization have an incident response plan?"))
   (question (id F05) (area preparation) (name ir-plan-reviewed-periodically)
      (text "Is the incident response plan reviewed and updated periodically, or whenever a significant improvement is needed?"))
   (question (id F06) (area preparation) (name role-based-ir-training)
      (text "Does role based training for staff in specialized roles cover their incident response responsibilities?"))

   (question (id F07) (area detection) (name logs-generated-and-available)
      (text "Are log records generated across your systems and made available for monitoring?"))
   (question (id F08) (area detection) (name network-monitoring)
      (text "Are networks and network services monitored for potentially adverse events?"))
   (question (id F09) (area detection) (name endpoint-and-service-monitoring)
      (text "Are computing hardware, software and their data monitored for potentially adverse events?"))
   (question (id F10) (area detection) (name event-correlation)
      (text "Is event information from different sources brought together and correlated?"))
   (question (id F11) (area detection) (name alerts-reach-responders)
      (text "Do alerts and log analysis findings reach the staff and tools responsible for incident response?"))
   (question (id F12) (area detection) (name incident-declaration-criteria)
      (text "Has your organization defined the criteria for deciding when an incident is declared?"))

   (question (id F13) (area response) (name incident-triage-performed)
      (text "Is each new incident report reviewed to confirm an incident occurred and to estimate its severity and urgency?"))
   (question (id F14) (area response) (name incidents-categorized-and-prioritized)
      (text "Are incidents categorized by type and prioritized for how quickly they are handled?"))
   (question (id F15) (area response) (name incident-status-tracked)
      (text "Is the status of every ongoing incident tracked, so that incidents needing escalation are identified?"))
   (question (id F16) (area response) (name notification-procedures-defined)
      (text "Are there established procedures stating what must be reported about an incident, to whom, and when?"))
   (question (id F17) (area response) (name containment-eradication-criteria)
      (text "Has your organization defined criteria and procedures for containing and eradicating incidents?"))

   (question (id F18) (area recovery) (name backups-created-and-tested)
      (text "Are backups of data created, protected, maintained and tested?"))
   (question (id F19) (area recovery) (name recovery-initiation-criteria)
      (text "Has your organization defined the criteria for deciding when incident recovery should begin?"))
   (question (id F20) (area recovery) (name backup-integrity-verified)
      (text "Are backups and other restoration assets checked for integrity before they are used to restore systems?"))
   (question (id F21) (area recovery) (name restored-assets-verified)
      (text "Are restored systems checked, and the incident's root causes remediated, before they return to production use?"))
   (question (id F22) (area recovery) (name root-cause-analysis)
      (text "Are incidents analyzed to find their underlying root causes?"))
   (question (id F23) (area recovery) (name after-action-report)
      (text "Is an after action report produced at the end of each incident recovery?")))
