"""Integration layer between Python and the CLIPS expert system.

This module holds no domain knowledge. It loads the existing .clp files,
turns answers into the same `answer` facts the CLI asserts, lets CLIPS run,
and reads back the `finding` facts the rules produced. Every conclusion,
recommendation and source citation comes from CLIPS.
"""

from pathlib import Path

import clips

SRC = Path(__file__).resolve().parents[1] / "src"
KNOWLEDGE_FILES = ("rules.clp", "questions.clp")

VALUES = ("yes", "no", "unknown")


class KnowledgeBaseError(RuntimeError):
    pass


def _text(value):
    return str(value).strip('"')


class ExpertSystem:
    """A CLIPS environment loaded with the incident response knowledge base."""

    def __init__(self, src=SRC):
        self.src = Path(src)
        self.env = clips.Environment()
        self._load()

    def _load(self):
        for name in KNOWLEDGE_FILES:
            path = self.src / name
            if not path.exists():
                raise KnowledgeBaseError(f"CLIPS file not found: {path}")
            try:
                self.env.load(str(path))
            except clips.CLIPSError as exc:
                raise KnowledgeBaseError(f"{path.name} failed to load: {exc}") from exc
        self.env.reset()
        if not list(self.env.rules()):
            raise KnowledgeBaseError("the knowledge base loaded but defines no rules")
        self._questions = [
            {
                "id": _text(f["id"]),
                "name": _text(f["name"]),
                "area": _text(f["area"]),
                "text": _text(f["text"]),
            }
            for f in self.env.facts()
            if f.template.name == "question"
        ]
        if not self._questions:
            raise KnowledgeBaseError("the knowledge base defines no questions")

    def questions(self):
        """The questionnaire, in the order questions.clp declares it.

        Read once when the environment loads, so asking for it later does not
        reset working memory and discard the findings already there.
        """
        return list(self._questions)

    def question(self, name):
        for q in self._questions:
            if q["name"] == name:
                return q
        return None

    def assess(self, answers):
        """Assert the answers, run CLIPS, and return the findings it asserted.

        `answers` maps a fact name to yes, no or unknown. CLIPS decides what
        follows; nothing here interprets an answer.
        """
        unknown_value = {n: v for n, v in answers.items() if v not in VALUES}
        if unknown_value:
            raise ValueError(f"answers must be yes, no or unknown: {unknown_value}")

        unrecognised = set(answers) - {q["name"] for q in self._questions}
        if unrecognised:
            raise ValueError(f"no such question: {sorted(unrecognised)}")

        self.env.reset()
        template = self.env.find_template("answer")
        for name, value in answers.items():
            template.assert_fact(name=clips.Symbol(name), value=clips.Symbol(value))

        try:
            self.env.run()
        except clips.CLIPSError as exc:
            raise KnowledgeBaseError(f"inference failed: {exc}") from exc

        return sorted(
            (self._finding(f) for f in self.env.facts()
             if f.template.name == "finding"),
            key=lambda f: f["rule_id"],
        )

    def _finding(self, fact):
        asked = _text(fact["asked"])
        return {
            "rule_id": _text(fact["rule-id"]),
            "area": _text(fact["area"]),
            "title": _text(fact["title"]),
            "finding": _text(fact["finding"]),
            "recommendation": _text(fact["recommendation"]),
            "conclusion": _text(fact["conclusion"]),
            "source": _text(fact["source"]),
            "page": _text(fact["page"]),
            "priority": _text(fact["priority"]),
            "asked": None if asked == "nil" else asked,
            "depends_on": [_text(d) for d in fact["depends-on"]],
        }

    def supporting_findings(self, finding, all_findings):
        """The findings a rollup rule rested on, named by the rules that made them."""
        by_conclusion = {f["conclusion"]: f for f in all_findings}
        return [by_conclusion[c] for c in finding["depends_on"] if c in by_conclusion]
