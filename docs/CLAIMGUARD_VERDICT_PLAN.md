# ClaimGuard verdict decision

Checked 17 October 2026. The design note that this records was not a file in the repository. `standard/STANDARD_V3.md` §4a is the text that governs. This note states the decision that §4a now carries.

## Conflicting evidence

When a supporting span and a contradicting span have the same warrant strength, the verdict is contested.

When the contradicting span is stronger, the verdict is contradicted.

When the contradicting span is the only bound evidence, the verdict is contradicted.

A weaker contradicting span does not override a stronger supporting span.

## What binds

A span binds only as an exact quote, after whitespace, case and Unicode quotes are normalised. Token overlap is not a match.

A mismatch of number, unit, entity or direction, in a span that otherwise aligns, is a contradiction. It is never support.

The quote is that span, with its offsets.

## Abstention

A question or an instruction is out of scope.

If the engine abstains and a span or a check is bound, the verdict still follows that evidence.

Out of scope is used when there is no placement and no bound evidence.

## Caller warrants

A caller may label a warrant. The label is advisory.

The grade is read from the text and from the source type. A caller cannot raise a source above that grade.

The response includes `warrant_declared_by_caller` and the graded warrant.

## summary.worst

`summary.worst` ranks by severity, not by the first-match order.

The severity order is contradicted, overstated, contested, unverified, out of scope, supported.

## Smoke

A confident claim with no sources is unverified (R19). It is not overstated. Overstated needs some evidence.
