;;; Test scenarios.
;;;
;;; Load after src/main.clp, then run (run-tests).
;;;
;;; Each scenario sets all 23 answers, runs the system, and compares the
;;; rules that fired against the rules expected. Expected rule lists were
;;; worked out from docs/rule_source_mapping.md, not from program output.

(deffunction answer-all (?value)
   (foreach ?q (find-all-facts ((?q question)) TRUE)
      (assert (answer (name (fact-slot-value ?q name)) (value ?value)))))

(deffunction set-answer (?name ?value)
   (bind ?existing (find-all-facts ((?a answer)) (eq ?a:name ?name)))
   (foreach ?a ?existing (retract ?a))
   (assert (answer (name ?name) (value ?value))))

(deffunction set-answers (?value $?names)
   (foreach ?n ?names (set-answer ?n ?value)))

(deffunction fired-rules ()
   (bind ?ids (create$))
   (foreach ?f (sort after-rule-id (find-all-facts ((?f finding)) TRUE))
      (bind ?ids (create$ ?ids (fact-slot-value ?f rule-id))))
   ?ids)

(deffunction absent-from (?wanted ?have)
   (bind ?out (create$))
   (foreach ?w ?wanted
      (if (not (member$ ?w ?have)) then (bind ?out (create$ ?out ?w))))
   ?out)

(deffunction check (?id ?description $?expected)
   (run)
   (bind ?actual (fired-rules))
   (bind ?missing (absent-from ?expected ?actual))
   (bind ?unexpected (absent-from ?actual ?expected))
   (bind ?ok (and (= (length$ ?missing) 0) (= (length$ ?unexpected) 0)))
   (printout t crlf ?id "  " ?description crlf
      "     expected : " (if (= (length$ ?expected) 0) then "none"
                             else (implode$ ?expected)) crlf
      "     actual   : " (if (= (length$ ?actual) 0) then "none"
                             else (implode$ ?actual)) crlf
      "     result   : " (if ?ok then "PASS" else "FAIL") crlf)
   (if (> (length$ ?missing) 0) then
      (printout t "     missing  : " (implode$ ?missing) crlf))
   (if (> (length$ ?unexpected) 0) then
      (printout t "     unexpected: " (implode$ ?unexpected) crlf))
   ?ok)

;;; ------------------------------------------------------------------

(deffunction test-T01 ()
   (reset)
   (answer-all yes)
   (check T01 "Broadly prepared organization, no gaps expected"))

(deffunction test-T02 ()
   (reset)
   (answer-all yes)
   (set-answers no ir-policy-exists ir-roles-documented ir-authority-designated
                   ir-plan-exists ir-plan-reviewed-periodically role-based-ir-training)
   (check T02 "Preparation and governance weak"
      R01 R02 R03 R04 R05 R06))

(deffunction test-T03 ()
   (reset)
   (answer-all yes)
   (set-answers no logs-generated-and-available network-monitoring
                   endpoint-and-service-monitoring event-correlation
                   alerts-reach-responders incident-declaration-criteria)
   (check T03 "Detection weak, rollup R24 expected"
      R07 R08 R09 R10 R11 R12 R24))

(deffunction test-T04 ()
   (reset)
   (answer-all yes)
   (set-answers no incident-triage-performed incidents-categorized-and-prioritized
                   incident-status-tracked notification-procedures-defined
                   containment-eradication-criteria)
   (check T04 "Response weak, rollup R25 expected"
      R13 R14 R15 R16 R17 R25))

(deffunction test-T05 ()
   (reset)
   (answer-all yes)
   (set-answers no backups-created-and-tested recovery-initiation-criteria
                   backup-integrity-verified restored-assets-verified
                   root-cause-analysis after-action-report)
   (check T05 "Recovery weak, rollup R26 expected"
      R18 R19 R20 R21 R22 R23 R26))

(deffunction test-T06 ()
   (reset)
   (answer-all unknown)
   (check T06 "Every answer unknown, nothing may be concluded"))

(deffunction test-T07 ()
   (reset)
   (answer-all yes)
   (set-answer network-monitoring no)
   (set-answer logs-generated-and-available unknown)
   (set-answer endpoint-and-service-monitoring unknown)
   (check T07 "One detection gap beside two unknowns, only that gap counts"
      R08 R24))

;;; A rollup must rest on findings that exist, and must name all of them.

(deffunction test-T08 ()
   (reset)
   (answer-all yes)
   (set-answers no backups-created-and-tested backup-integrity-verified)
   (run)
   (bind ?r26 (find-fact ((?f finding)) (eq ?f:rule-id R26)))
   (bind ?ok FALSE)
   (if (> (length$ ?r26) 0) then
      (bind ?supports (create$))
      (foreach ?c (fact-slot-value (nth$ 1 ?r26) depends-on)
         (bind ?found (find-fact ((?f finding)) (eq ?f:conclusion ?c)))
         (if (> (length$ ?found) 0) then
            (bind ?supports (create$ ?supports
               (fact-slot-value (nth$ 1 ?found) rule-id)))))
      (bind ?ok (and (member$ R18 ?supports) (member$ R20 ?supports)
                     (= (length$ ?supports) 2))))
   (printout t crlf "T08  R26 explains itself with every supporting finding" crlf
      "     expected : R18 R20" crlf
      "     actual   : " (if (> (length$ ?r26) 0) then (implode$ ?supports)
                             else "R26 did not fire") crlf
      "     result   : " (if ?ok then "PASS" else "FAIL") crlf)
   ?ok)

;;; A finding must carry the source its rule was derived from.

(deffunction test-T09 ()
   (reset)
   (answer-all no)
   (run)
   (bind ?checks (create$ R01 "GV.PO.R1" R09 "DE.CM-09.R1 to R5"
                          R18 "PR.DS-11" R23 "RC.RP-06.R1"))
   (bind ?ok TRUE)
   (bind ?i 1)
   (while (< ?i (length$ ?checks))
      (bind ?id (nth$ ?i ?checks))
      (bind ?want (nth$ (+ ?i 1) ?checks))
      (bind ?f (find-fact ((?f finding)) (eq ?f:rule-id ?id)))
      (if (or (= (length$ ?f) 0)
              (neq (fact-slot-value (nth$ 1 ?f) source) ?want))
         then
         (bind ?ok FALSE)
         (printout t "     " ?id " source mismatch, wanted " ?want crlf))
      (bind ?i (+ ?i 2)))
   (printout t crlf "T09  Findings carry the NIST source of their rule" crlf
      "     checked  : R01 R09 R18 R23" crlf
      "     result   : " (if ?ok then "PASS" else "FAIL") crlf)
   ?ok)

;;; ------------------------------------------------------------------

(deffunction run-tests ()
   (printout t crlf)
   (rule-line "=")
   (printout t "  TEST SCENARIOS" crlf)
   (rule-line "=")
   (bind ?results (create$ (test-T01) (test-T02) (test-T03) (test-T04) (test-T05)
                           (test-T06) (test-T07) (test-T08) (test-T09)))
   (bind ?passed 0)
   (foreach ?r ?results (if ?r then (bind ?passed (+ ?passed 1))))
   (printout t crlf)
   (rule-line "=")
   (printout t "  " (length$ ?results) " tests, " ?passed " passed, "
      (- (length$ ?results) ?passed) " failed" crlf)
   (rule-line "=")
   (printout t crlf))
