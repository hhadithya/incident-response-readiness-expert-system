;;; Reporting and explanation.
;;;
;;; Everything shown here is read from the finding facts the rules asserted
;;; and the answer facts they matched on. Nothing is recomputed, so what the
;;; user reads is what the rule actually concluded.

(deffunction rule-line (?ch)
   (bind ?i 0)
   (while (< ?i 74) (printout t ?ch) (bind ?i (+ ?i 1)))
   (printout t crlf))

(deffunction area-label (?area)
   (switch ?area
      (case preparation then "Preparation and governance")
      (case detection then "Detection")
      (case response then "Response")
      (case recovery then "Recovery and improvement")
      (default ?area)))

(deffunction after-rule-id (?a ?b)
   (> (str-compare (str-cat (fact-slot-value ?a rule-id))
                   (str-cat (fact-slot-value ?b rule-id))) 0))

(deffunction findings-in (?area)
   (sort after-rule-id (find-all-facts ((?f finding)) (eq ?f:area ?area))))

(deffunction report ()
   (bind ?all (find-all-facts ((?f finding)) TRUE))
   (printout t crlf)
   (rule-line "=")
   (printout t "  ASSESSMENT RESULT" crlf)
   (rule-line "=")
   (if (= (length$ ?all) 0) then
      (printout t crlf
         "  No readiness gaps were identified from your answers." crlf crlf)
      else
      (printout t crlf "  " (length$ ?all)
         " finding(s). Each names the rule that produced it and the NIST" crlf
         "  reference that rule was derived from." crlf)
      (foreach ?area (create$ preparation detection response recovery)
         (bind ?group (findings-in ?area))
         (if (> (length$ ?group) 0) then
            (printout t crlf)
            (rule-line "-")
            (printout t "  " (area-label ?area) crlf)
            (rule-line "-")
            (foreach ?f ?group
               (printout t crlf
                  "  [" (fact-slot-value ?f rule-id) "] "
                  (fact-slot-value ?f title)
                  "   (NIST priority: " (fact-slot-value ?f priority) ")" crlf
                  "      Finding        : " (fact-slot-value ?f finding) crlf
                  "      Recommendation : " (fact-slot-value ?f recommendation) crlf
                  "      Source         : NIST SP 800-61r3, "
                  (fact-slot-value ?f source) ", "
                  (fact-slot-value ?f page) crlf))))))

;;; A rule that read an answer explains itself with the question that was put
;;; to the user and the answer given. A rule that read other findings explains
;;; itself with those findings, so the chain back to the user's answers stays
;;; visible.

(deffunction explain-answer (?name)
   (bind ?q (find-fact ((?q question)) (eq ?q:name ?name)))
   (bind ?a (find-fact ((?a answer)) (eq ?a:name ?name)))
   (if (> (length$ ?q) 0) then
      (printout t "      Question " (fact-slot-value (nth$ 1 ?q) id) ": "
                  (fact-slot-value (nth$ 1 ?q) text) crlf))
   (if (> (length$ ?a) 0) then
      (printout t "      You answered: " (fact-slot-value (nth$ 1 ?a) value) crlf)
      else
      (printout t "      Fact: " ?name crlf)))

(deffunction explain-supports (?conclusions)
   (foreach ?c ?conclusions
      (bind ?found (find-fact ((?f finding)) (eq ?f:conclusion ?c)))
      (if (> (length$ ?found) 0) then
         (bind ?s (nth$ 1 ?found))
         (printout t "      [" (fact-slot-value ?s rule-id) "] "
                     (fact-slot-value ?s title) crlf))))

(deffunction explain-trigger (?f)
   (if (neq (fact-slot-value ?f asked) nil) then
      (explain-answer (fact-slot-value ?f asked))
      else
      (printout t "      These findings, already established by other rules:" crlf)
      (explain-supports (fact-slot-value ?f depends-on))))

(deffunction explain-fact (?f)
   (printout t crlf)
   (rule-line "=")
   (printout t "  RULE " (fact-slot-value ?f rule-id) "   "
      (fact-slot-value ?f title) crlf
      "  Area: " (area-label (fact-slot-value ?f area)) crlf)
   (rule-line "=")
   (printout t crlf "  Triggered because" crlf)
   (explain-trigger ?f)
   (printout t crlf
      "  Concluded" crlf
      "      " (fact-slot-value ?f conclusion) crlf crlf
      "  Finding" crlf
      "      " (fact-slot-value ?f finding) crlf crlf
      "  Recommendation" crlf
      "      " (fact-slot-value ?f recommendation) crlf crlf
      "  Source" crlf
      "      NIST SP 800-61r3" crlf
      "      " (fact-slot-value ?f source) crlf
      "      " (fact-slot-value ?f page) crlf
      "      NIST priority for this outcome: " (fact-slot-value ?f priority) crlf)
   (rule-line "=")
   (printout t crlf))

(deffunction explain (?id)
   (bind ?match (find-all-facts ((?f finding)) (eq ?f:rule-id ?id)))
   (if (= (length$ ?match) 0) then
      (printout t crlf "  No finding was produced by rule " ?id
         " in this assessment." crlf crlf)
      else
      (foreach ?f ?match (explain-fact ?f))))

(deffunction explain-all ()
   (bind ?all (sort after-rule-id (find-all-facts ((?f finding)) TRUE)))
   (if (= (length$ ?all) 0) then
      (printout t crlf "  There are no findings to explain." crlf crlf)
      else
      (foreach ?f ?all (explain-fact ?f))))
