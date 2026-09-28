# Knowledge Sources

This file records every source from which domain knowledge in this expert system is derived. No rule may exist without an entry here and a matching row in [rule_source_mapping.md](rule_source_mapping.md).

## S1, primary source

| Field | Value |
|---|---|
| Identifier | NIST SP 800-61r3 |
| Full title | *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile* |
| Revision | Revision 3 |
| Publisher | National Institute of Standards and Technology (NIST), U.S. Department of Commerce |
| Date | April 2025 |
| Local copy | [`references/NIST.SP.800-61r3.pdf`](../references/NIST.SP.800-61r3.pdf) |
| Role | Primary source of domain knowledge |

The local copy is committed to the repository so that any reader can verify each cited section against the exact document that was used.

## Additional sources

None. No source other than S1 has been used.

If an additional source becomes necessary it must be an official NIST or CISA publication, approved before use, added to this file together with the reason it was required, and referenced explicitly by the rules that depend on it.

## Source policy

These constraints are binding for this project:

- Domain rules are never invented, inferred from general intuition, or generated without a source.
- Blogs, vendor material, forum posts, unsourced best practice lists, and language model output are not acceptable sources.
- Numeric thresholds, weightings, and scores are not introduced unless an authoritative source explicitly defines them.
- Where a desirable rule cannot be grounded in an approved source, the gap is reported rather than filled.

## Citation format

Each rule cites its source as:

```
NIST SP 800-61r3, <section number or CSF 2.0 Function, Category or Subcategory identifier>, p. <page>
```
