# Architecture Specification

Instructions for drawing the system diagram in Lucidchart. Every box below exists in the code; nothing is added to make the diagram look fuller.

Export as `docs/architecture.png`.

## Canvas

Portrait, top to bottom flow. One main column, with the CLIPS terminal entering from the left and the knowledge files entering from the right.

## Boxes

Numbered in drawing order. Widths are suggestions; keep the main column boxes the same width as each other.

| # | Box | Text inside | Shape |
|---|---|---|---|
| 1 | User | `User` | Rounded rectangle |
| 2 | Desktop UI | `Tkinter Desktop UI`<br>`app/desktop_app.py`<br>`23 questions, Yes / No / Unknown` | Rectangle |
| 3 | Adapter | `CLIPSpy Adapter`<br>`app/clips_adapter.py`<br>`no domain logic` | Rectangle |
| 4 | Working memory | `CLIPS Working Memory`<br>`answer facts` | Rectangle |
| 5 | Engine | `CLIPS Forward-Chaining Engine`<br>`pattern matcher, agenda` | Rectangle, emphasised |
| 6 | Knowledge base | `Knowledge Base`<br>`src/rules.clp`<br>`26 NIST-derived rules` | Rectangle |
| 7 | Findings | `Finding Facts`<br>`rule-id, finding, recommendation,`<br>`source, page, priority` | Rectangle |
| 8 | Results view | `Results and Explanation View`<br>`findings grouped by area` | Rectangle |
| 9 | CLI | `CLIPS Terminal`<br>`src/main.clp`<br>`src/explanations.clp` | Rectangle, to the left |
| 10 | Source | `NIST SP 800-61r3`<br>`CSF 2.0 Community Profile` | Document shape, to the right of box 6 |
| 11 | Questions | `src/questions.clp`<br>`23 questions` | Rectangle, small, right of box 2 |

Boxes 4, 5, 6 and 7 are all inside CLIPS. Draw a labelled container around them:

> **CLIPS Environment**

That container is the single most important thing in the diagram. It shows the reasoning happens in CLIPS, and that Python sits outside it.

## Arrows

| From | To | Label | Direction |
|---|---|---|---|
| 1 User | 2 Desktop UI | `answers questions` | down |
| 11 Questions | 2 Desktop UI | `question text` | left |
| 2 Desktop UI | 3 Adapter | `answers as a dictionary` | down |
| 3 Adapter | 4 Working memory | `asserts (answer (name ...) (value ...))` | down |
| 4 Working memory | 5 Engine | `facts` | down |
| 6 Knowledge base | 5 Engine | `rule conditions` | left, into the engine |
| 10 Source | 6 Knowledge base | `each rule cites an element and page` | left |
| 5 Engine | 7 Findings | `matching rules fire and assert` | down |
| 7 Findings | 5 Engine | `findings satisfy R24, R25, R26` | curved, back up the right side |
| 7 Findings | 3 Adapter | `reads finding facts` | up the left side |
| 3 Adapter | 8 Results view | `findings as Python data` | down |
| 8 Results view | 1 User | `findings, recommendations, sources` | curved, back up to the user |
| 9 CLI | 4 Working memory | `same facts, same rules` | right, dashed |

## The two arrows that carry the argument

**`7 Findings` back to `5 Engine`.** This is the second round of forward chaining. R24, R25 and R26 match on findings the first round asserted, not on answers. Without this arrow the diagram shows a lookup table rather than an inference engine. Label it clearly and let it curve visibly rather than hiding behind other boxes.

**`9 CLI` to `4 Working memory`, dashed.** This shows the terminal reaching the same working memory and the same rules as the desktop app. It is the evidence that there is one knowledge base and two interfaces, not two systems. Dashed to mark it as an alternative path rather than part of the main flow.

## Styling

Keep it plain. No gradients, no drop shadows, no icons.

- One fill colour for the Python boxes (2, 3, 8, 11)
- A different fill for the boxes inside the CLIPS Environment container (4, 5, 6, 7)
- White or no fill for User (1), CLI (9) and the NIST document (10)
- Emphasise box 5 with a heavier border, since it is where inference happens
- Solid arrows throughout except the dashed CLI arrow

## What not to draw

- No database, file store, network, or server. There are none.
- No scoring, rating or percentage component. The system produces none.
- No separate "explanation engine". Explanations are read from the same finding facts the results view uses, so box 8 covers both.
- No backward chaining or goal query path. Not implemented.

## Checking the diagram against the code

| The diagram claims | Where to verify |
|---|---|
| 26 rules | `(length$ (get-defrule-list))` in CLIPS, or count `defrule` in `src/rules.clp` |
| 23 questions | `deffacts questionnaire` in `src/questions.clp` |
| The adapter holds no domain logic | `app/clips_adapter.py` branches on no answer value |
| Findings carry source and page | the `finding` template at the top of `src/rules.clp` |
| Findings feed back into the engine | R24, R25 and R26 in `src/rules.clp` match on `(finding ...)` |
| Both interfaces use one knowledge base | both load `src/rules.clp`, and neither defines rules of its own |
