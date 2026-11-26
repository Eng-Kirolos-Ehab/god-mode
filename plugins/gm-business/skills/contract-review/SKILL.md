---
name: contract-review
description: Reviews a contract, agreement, offer letter, freelance/client scope or terms of service before signing - lists every obligation with its number and date, flags risky clauses (payment, scope creep, IP ownership, liability, termination, auto-renewal, non-compete, penalties), and writes the questions to ask and the changes to request. Arabic or English. Use when the user shares a contract/agreement/offer/quote/SOW/NDA/terms and asks "review this", "should I sign", "what am I agreeing to", "راجع العقد". Not legal advice.
argument-hint: "[paste or attach the contract]"
license: MIT
---

# contract-review

Read the whole document before answering. Quote the clause number (or the first words) for every point, so the user can find it.

## Ask first (one message, only what's missing)
- Which side the user is on (client / provider / employee) and what they actually agreed to verbally.
- The deal in one line: price, scope, timeline. Anything promised that should be in writing.

## Output (in the user's language)
1. **The deal in 5 lines**: who does what, for how much, by when, and how it ends.
2. **Your obligations**: a table of what you must do, by when (date or trigger), and the clause. Every number and date goes in it, exactly as written.
3. **Their obligations**: the same table. Gaps here are risks (for example, no payment deadline for them).
4. **Risky clauses**, worst first. For each one, rate the risk (🔴 high / 🟠 medium / 🟡 low), quote the clause, say what it means in plain words, give a realistic bad scenario, and propose wording to request instead. Check at least these:
   - **Payment:** when, milestones, late-payment terms, currency/FX, who pays fees, and whether money is held until "approval" with no deadline.
   - **Scope:** is it defined? Is there a change-request process with a price? What do "unlimited revisions" or "and any related work" cover?
   - **IP:** who owns the code/design/content, and when (on full payment or on signing). Can you reuse it and show it in your portfolio?
   - **Liability and penalties:** caps, indemnities, delay penalties, warranties, "fitness for purpose".
   - **Term and exit:** notice period, termination for convenience, what's owed on exit, auto-renewal, lock-in.
   - **Restrictions:** non-compete or non-solicit (length and region), exclusivity, confidentiality term.
   - **Disputes:** governing law, jurisdiction or arbitration location, language that prevails (Arabic vs English versions).
   - **Data:** personal data and hosting (PDPL in KSA, Egypt's data law, GDPR) if the work touches user data.
5. **Missing clauses** that should be there (acceptance criteria, support period, hosting/credentials handover, a payment schedule).
6. **Questions to ask before signing**: numbered and short.
7. **Verdict**: sign as is / sign after these changes / don't sign. One line on why.

## Rules
- Only what the document says. Never invent a clause, a law article or a number. If a law matters and you aren't sure, say "check with a lawyer about X".
- End with: "This is a practical review, not legal advice. For high-value or legally complex contracts, have a lawyer in the governing country review it."
- Don't send, sign, accept or reply to anyone. Messages to the other party stay drafts for the user to send.
