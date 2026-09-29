"""Desktop interface for the Incident Response Readiness Expert System.

The reasoning belongs to CLIPS. This window collects answers, hands them to
the adapter, and displays the findings CLIPS asserts. It contains no rules
and makes no judgement about any answer.

Run from the repository root:  python app/desktop_app.py
"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.clips_adapter import ExpertSystem, KnowledgeBaseError

TITLE = "Incident Response Readiness Expert System"

INTRO = ("Assesses selected incident response practices using rules derived from "
         "NIST SP 800-61r3.\nAnswer each question. Unknown is a real answer: it is "
         "never counted as a gap.")

AREA_NAMES = {
    "preparation": "Preparation and governance",
    "detection": "Detection",
    "response": "Response",
    "recovery": "Recovery and improvement",
}

CHOICES = (("Yes", "yes"), ("No", "no"), ("Unknown", "unknown"))


class ScrollableFrame(ttk.Frame):
    """A frame that scrolls vertically, for content taller than the window."""

    def __init__(self, parent):
        super().__init__(parent)
        canvas = tk.Canvas(self, highlightthickness=0)
        bar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.body = ttk.Frame(canvas)

        window = canvas.create_window((0, 0), window=self.body, anchor="nw")
        canvas.configure(yscrollcommand=bar.set)

        self.body.bind("<Configure>",
                       lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfigure(window, width=e.width))

        canvas.pack(side="left", fill="both", expand=True)
        bar.pack(side="right", fill="y")

        self.canvas = canvas
        for widget in (canvas, self.body):
            widget.bind("<Enter>", self._bind_wheel)
            widget.bind("<Leave>", self._unbind_wheel)

    def _bind_wheel(self, _event):
        self.canvas.bind_all("<MouseWheel>", self._on_wheel)

    def _unbind_wheel(self, _event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_wheel(self, event):
        self.canvas.yview_scroll(-int(event.delta / 120), "units")

    def to_top(self):
        self.canvas.yview_moveto(0)


class Application(ttk.Frame):

    def __init__(self, root, system):
        super().__init__(root, padding=(16, 12))
        self.root = root
        self.system = system
        self.choice = {}
        self.pack(fill="both", expand=True)

        self._header()
        self.questionnaire = self._build_questionnaire()
        self.results = None
        self._buttons()

    def _header(self):
        head = ttk.Frame(self)
        head.pack(fill="x", pady=(0, 10))
        ttk.Label(head, text=TITLE, font=("Segoe UI", 15, "bold")).pack(anchor="w")
        ttk.Label(head, text=INTRO, foreground="#444", justify="left").pack(
            anchor="w", pady=(4, 0))
        ttk.Separator(head).pack(fill="x", pady=(10, 0))

    def _build_questionnaire(self):
        frame = ScrollableFrame(self)
        frame.pack(fill="both", expand=True)

        area = None
        for question in self.system.questions():
            if question["area"] != area:
                area = question["area"]
                ttk.Label(frame.body, text=AREA_NAMES.get(area, area),
                          font=("Segoe UI", 11, "bold")).pack(
                    anchor="w", pady=(14, 2), padx=4)
                ttk.Separator(frame.body).pack(fill="x", padx=4, pady=(0, 6))

            self._question_row(frame.body, question)
        return frame

    def _question_row(self, parent, question):
        row = ttk.Frame(parent)
        row.pack(fill="x", padx=4, pady=(6, 0))

        ttk.Label(row, text=f"{question['id']}.  {question['text']}",
                  wraplength=760, justify="left").pack(anchor="w")

        picked = tk.StringVar(value="")
        self.choice[question["name"]] = picked

        options = ttk.Frame(row)
        options.pack(anchor="w", padx=(22, 0), pady=(2, 0))
        for label, value in CHOICES:
            ttk.Radiobutton(options, text=label, value=value,
                            variable=picked).pack(side="left", padx=(0, 16))

    def _buttons(self):
        ttk.Separator(self).pack(fill="x", pady=(10, 0))
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(10, 0))

        self.run_button = ttk.Button(bar, text="Run Assessment", command=self.run)
        self.run_button.pack(side="left")
        ttk.Button(bar, text="Reset", command=self.reset).pack(side="left", padx=8)
        ttk.Button(bar, text="Exit", command=self.root.destroy).pack(side="right")

        self.status = ttk.Label(bar, text="", foreground="#555")
        self.status.pack(side="left", padx=16)

    # ----------------------------------------------------------------

    def collected_answers(self):
        """Answers as chosen, with anything unanswered left out."""
        return {name: var.get() for name, var in self.choice.items() if var.get()}

    def run(self):
        answers = self.collected_answers()
        unanswered = [n for n, var in self.choice.items() if not var.get()]

        if unanswered:
            proceed = messagebox.askyesno(
                "Unanswered questions",
                f"{len(unanswered)} question(s) have no answer.\n\n"
                "They will be recorded as Unknown, which reports them as not "
                "assessed rather than treating them as gaps.\n\nContinue?",
                parent=self.root)
            if not proceed:
                return
            for name in unanswered:
                answers[name] = "unknown"
                self.choice[name].set("unknown")

        try:
            findings = self.system.assess(answers)
        except (KnowledgeBaseError, ValueError) as exc:
            messagebox.showerror("Assessment failed", str(exc), parent=self.root)
            return

        self.show_results(findings, answers)

    def reset(self):
        for var in self.choice.values():
            var.set("")
        if self.results is not None:
            self.results.destroy()
            self.results = None
            self.questionnaire.pack(fill="both", expand=True)
            self.run_button.state(["!disabled"])
        self.questionnaire.to_top()
        self.status.config(text="")

    def show_results(self, findings, answers):
        self.questionnaire.pack_forget()
        if self.results is not None:
            self.results.destroy()

        self.results = ScrollableFrame(self)
        self.results.pack(fill="both", expand=True)
        body = self.results.body
        self.run_button.state(["disabled"])

        not_assessed = sorted(n for n, v in answers.items() if v == "unknown")

        if not findings:
            ttk.Label(body, text="No readiness gaps were identified.",
                      font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(14, 4), padx=4)
            ttk.Label(body, wraplength=780, justify="left", foreground="#444",
                      text="None of the rules in the knowledge base matched your "
                           "answers.").pack(anchor="w", padx=4)
        else:
            ttk.Label(body, text=f"{len(findings)} finding(s)",
                      font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(14, 2), padx=4)
            ttk.Label(body, foreground="#444", wraplength=780, justify="left",
                      text="Each was produced by a rule in the CLIPS knowledge base. "
                           "The source is the NIST location that rule came from."
                      ).pack(anchor="w", padx=4, pady=(0, 6))

            area = None
            for finding in findings:
                if finding["area"] != area:
                    area = finding["area"]
                    ttk.Label(body, text=AREA_NAMES.get(area, area),
                              font=("Segoe UI", 11, "bold")).pack(
                        anchor="w", pady=(12, 2), padx=4)
                    ttk.Separator(body).pack(fill="x", padx=4, pady=(0, 4))
                self._finding_card(body, finding, findings, answers)

        if not_assessed:
            ttk.Label(body, text="Not assessed",
                      font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(16, 2), padx=4)
            ttk.Separator(body).pack(fill="x", padx=4, pady=(0, 4))
            ttk.Label(body, wraplength=780, justify="left", foreground="#444",
                      text="You answered Unknown to the following, so no conclusion "
                           "was drawn either way:").pack(anchor="w", padx=4)
            for name in not_assessed:
                question = self.system.question(name)
                label = f"{question['id']}. {question['text']}" if question else name
                ttk.Label(body, text=f"    {label}", wraplength=760,
                          justify="left").pack(anchor="w", padx=4, pady=(2, 0))

        bar = ttk.Frame(body)
        bar.pack(fill="x", pady=(18, 8), padx=4)
        ttk.Button(bar, text="New Assessment", command=self.reset).pack(side="left")
        ttk.Button(bar, text="Back to Answers",
                   command=lambda: self.back_to_questions()).pack(side="left", padx=8)

        self.results.to_top()
        self.status.config(text=f"{len(findings)} finding(s)")

    def back_to_questions(self):
        if self.results is not None:
            self.results.destroy()
            self.results = None
        self.questionnaire.pack(fill="both", expand=True)
        self.run_button.state(["!disabled"])

    def _finding_card(self, parent, finding, findings, answers):
        card = ttk.Frame(parent, relief="solid", borderwidth=1, padding=10)
        card.pack(fill="x", padx=4, pady=5)

        ttk.Label(card, font=("Segoe UI", 10, "bold"),
                  text=f"{finding['rule_id']}   {finding['title']}"
                  ).pack(anchor="w")
        ttk.Label(card, foreground="#666",
                  text=f"NIST priority for this outcome: {finding['priority']}"
                  ).pack(anchor="w", pady=(0, 6))

        for label, value in (("Finding", finding["finding"]),
                             ("Recommendation", finding["recommendation"])):
            line = ttk.Frame(card)
            line.pack(fill="x", anchor="w", pady=(0, 4))
            ttk.Label(line, text=f"{label}:", width=16,
                      font=("Segoe UI", 9, "bold")).pack(side="left", anchor="n")
            ttk.Label(line, text=value, wraplength=600, justify="left").pack(
                side="left", anchor="w")

        source = ttk.Frame(card)
        source.pack(fill="x", anchor="w")
        ttk.Label(source, text="Source:", width=16,
                  font=("Segoe UI", 9, "bold")).pack(side="left", anchor="n")
        ttk.Label(source, wraplength=600, justify="left", foreground="#444",
                  text=f"NIST SP 800-61r3, {finding['source']}, {finding['page']}"
                  ).pack(side="left", anchor="w")

        ttk.Button(card, text="View Explanation",
                   command=lambda: self.show_explanation(finding, findings, answers)
                   ).pack(anchor="w", pady=(8, 0))

    def show_explanation(self, finding, findings, answers):
        window = tk.Toplevel(self.root)
        window.title(f"Rule {finding['rule_id']}")
        window.geometry("640x560")
        window.transient(self.root)

        frame = ScrollableFrame(window)
        frame.pack(fill="both", expand=True, padx=14, pady=12)
        body = frame.body

        ttk.Label(body, font=("Segoe UI", 13, "bold"),
                  text=f"Rule {finding['rule_id']}   {finding['title']}").pack(anchor="w")
        ttk.Label(body, foreground="#555",
                  text=f"Area: {AREA_NAMES.get(finding['area'], finding['area'])}"
                  ).pack(anchor="w", pady=(2, 10))

        def section(heading, lines):
            ttk.Separator(body).pack(fill="x", pady=(8, 6))
            ttk.Label(body, text=heading, font=("Segoe UI", 10, "bold")).pack(anchor="w")
            for line in lines:
                ttk.Label(body, text=line, wraplength=560, justify="left").pack(
                    anchor="w", padx=(12, 0), pady=(3, 0))

        section("Triggered because", self._trigger_lines(finding, findings, answers))
        section("Concluded", [finding["conclusion"]])
        section("Finding", [finding["finding"]])
        section("Recommendation", [finding["recommendation"]])
        section("Source", ["NIST SP 800-61r3",
                           finding["source"],
                           finding["page"],
                           f"NIST priority for this outcome: {finding['priority']}"])

        ttk.Separator(body).pack(fill="x", pady=(10, 8))
        ttk.Button(body, text="Close", command=window.destroy).pack(anchor="w")

    def _trigger_lines(self, finding, findings, answers):
        """What made the rule fire, taken from the finding CLIPS asserted."""
        if finding["asked"]:
            question = self.system.question(finding["asked"])
            given = answers.get(finding["asked"], "")
            if question:
                return [f"Question {question['id']}: {question['text']}",
                        f"You answered: {given}"]
            return [f"{finding['asked']} = {given}"]

        supporting = self.system.supporting_findings(finding, findings)
        lines = ["These findings, already established by other rules:"]
        lines += [f"    {f['rule_id']}   {f['title']}" for f in supporting]
        return lines


def main():
    try:
        system = ExpertSystem()
    except KnowledgeBaseError as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Cannot start", f"{exc}\n\nThe CLIPS knowledge base in "
                                             "src/ could not be loaded.")
        return 1

    root = tk.Tk()
    root.title(TITLE)
    root.geometry("880x720")
    root.minsize(720, 520)
    Application(root, system)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
