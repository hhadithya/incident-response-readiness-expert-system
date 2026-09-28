# Knowledge Sources

This file records every source from which domain knowledge in this expert system is derived. No rule may exist without an entry here and a matching entry in [rule_source_mapping.md](rule_source_mapping.md).

## S1, primary source

| Field | Value |
|---|---|
| Identifier used in this project | NIST SP 800-61r3 |
| Title | Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile |
| Series and number | NIST Special Publication 800-61, Revision 3 |
| Authors | Alex Nelson, Sanjay Rekhi, Murugiah Souppaya, Karen Scarfone |
| Publisher | National Institute of Standards and Technology, U.S. Department of Commerce, Gaithersburg, MD |
| Publication date | April 2025 |
| Pages | 48 (PDF), 40 numbered |
| DOI | https://doi.org/10.6028/NIST.SP.800-61r3 |
| Publication page | https://csrc.nist.gov/pubs/sp/800/61/r3/final |
| Official PDF | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf |
| Local copy | [`references/NIST.SP.800-61r3.pdf`](../references/NIST.SP.800-61r3.pdf) |
| Supersedes | NIST SP 800-61 Revision 2, Computer Security Incident Handling Guide |
| Role in this project | Primary and only source of domain knowledge |

### Citation as given by NIST

> Nelson A, Rekhi S, Souppaya M, Scarfone K (2025) Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile. (National Institute of Standards and Technology, Gaithersburg, MD), NIST Special Publication (SP) NIST SP 800-61r3. https://doi.org/10.6028/NIST.SP.800-61r3

The DOI resolves to the official PDF URL above. The local copy was checked against the publication page and carries the same title, revision, date and DOI. It is committed to this repository so that any reader can verify each citation against the exact document used.

## Additional sources

None. No source other than S1 has been used.

If an additional source becomes necessary it must be an official NIST or CISA publication, approved before use, added to this file together with the reason it was required, and referenced explicitly by the rules that depend on it.

Note that S1 itself cites other publications, for example SP 800-84 on exercises and SP 800-184 on recovery. Those are not used here. Where S1 refers to another document, this project takes only what S1 itself states.

## Source policy

These constraints are binding for this project:

- Domain rules are never invented, inferred from general intuition, or generated without a source.
- Blogs, vendor material, forum posts, unsourced best practice lists, and language model output are not acceptable sources.
- Numeric thresholds, weightings, and scores are not introduced unless an authoritative source explicitly defines them. S1 defines none, so the system produces no readiness score, grade or maturity level.
- Priorities attached to rules are the priorities S1 assigns the cited CSF element, reported with the meaning S1 gives them.
- Where a desirable rule cannot be grounded in an approved source, the gap is recorded rather than filled.
- Verbatim source text is not reproduced in program output. Rules carry paraphrases together with exact citations.

## Citation format

```
NIST SP 800-61r3, <CSF element ID>[.<item ID>], Table <2|3>, PDF p. <n> (document p. <n-8>)
```

CSF element IDs are the Function, Category and Subcategory identifiers used by the CSF 2.0 Community Profile in Section 3 of S1, for example `GV.RR-02`. Item IDs are the numbered recommendations, considerations and notes in each row's final column, for example `R2`. S1 defines this combined identifier scheme on PDF page 18.

Both page numbers are given because the PDF's page numbering and the document's printed page numbering differ by eight: printed page 1 is PDF page 9.

## No expert interview

No domain expert was interviewed for this project. Interviewing an expert is not mandatory for this assignment provided all domain knowledge is grounded in a valid external source. Knowledge was acquired by document analysis of S1, and every rule records the location in S1 it came from.
