;;; Incident Response Readiness Expert System
;;;
;;; Load this file from the repository root, then run (start).

(load* "src/rules.clp")
(load* "src/questions.clp")
(load* "src/explanations.clp")

(deffunction line (?ch)
   (bind ?i 0)
   (while (< ?i 74) (printout t ?ch) (bind ?i (+ ?i 1)))
   (printout t crlf))

(deffunction area-title (?area)
   (switch ?area
      (case preparation then "Preparation and governance")
      (case detection then "Detection")
      (case response then "Response")
      (case recovery then "Recovery and improvement")
      (default ?area)))

(deffunction banner ()
   (printout t crlf)
   (line "=")
   (printout t "  INCIDENT RESPONSE READINESS EXPERT SYSTEM" crlf)
   (line "=")
   (printout t crlf
      "  Assesses whether your organization has key cybersecurity incident" crlf
      "  response practices in place, and recommends improvements." crlf crlf
      "  Knowledge source: NIST SP 800-61r3, Incident Response Recommendations" crlf
      "  and Considerations for Cybersecurity Risk Management (April 2025)." crlf crlf
      "  This is an educational system built for a university assignment. It is" crlf
      "  not an official NIST assessment, not a compliance or certification" crlf
      "  tool, and not professional security advice." crlf crlf
      "  Answer each question with yes, no or unknown. An unknown answer is not" crlf
      "  treated as a no: it is reported separately as something not assessed." crlf crlf))

(deffunction ask (?id ?text)
   (printout t crlf ?id ". " ?text crlf "     yes / no / unknown > ")
   (bind ?reply (lowcase (read)))
   (while (not (member$ ?reply (create$ yes no unknown y n u)))
      (printout t "     Please answer yes, no or unknown > ")
      (bind ?reply (lowcase (read))))
   (switch ?reply
      (case y then yes)
      (case n then no)
      (case u then unknown)
      (default ?reply)))

(deffunction ask-all ()
   (bind ?area none)
   (foreach ?q (find-all-facts ((?q question)) TRUE)
      (if (neq (fact-slot-value ?q area) ?area) then
         (bind ?area (fact-slot-value ?q area))
         (printout t crlf)
         (line "-")
         (printout t "  " (area-title ?area) crlf)
         (line "-"))
      (assert (answer
         (name (fact-slot-value ?q name))
         (value (ask (fact-slot-value ?q id) (fact-slot-value ?q text)))))))

(deffunction not-assessed ()
   (bind ?unknowns (find-all-facts ((?a answer)) (eq ?a:value unknown)))
   (if (> (length$ ?unknowns) 0) then
      (printout t crlf)
      (line "-")
      (printout t "  NOT ASSESSED" crlf)
      (line "-")
      (printout t crlf
         "  You answered unknown to the following, so no conclusion was drawn" crlf
         "  about them either way:" crlf crlf)
      (foreach ?a ?unknowns
         (printout t "    " (fact-slot-value ?a name) crlf))
      (printout t crlf)))

(deffunction start ()
   (reset)
   (banner)
   (ask-all)
   (run)
   (report)
   (not-assessed)
   (printout t "  For the reasoning behind any finding, run (explain RXX), for example" crlf
               "  (explain R01). Run (explain-all) for every finding in full." crlf crlf)
   (line "=")
   (printout t crlf))

(printout t crlf "Loaded. Run (start) to begin an assessment." crlf crlf)
