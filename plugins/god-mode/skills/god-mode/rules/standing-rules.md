# Standing Rules

Each rule came from a real correction or incident in day-to-day work with Claude Code. They are written so any project can use them.

## Working with the user
- **One question at a time** during discovery. Ask, then wait for the answer before the next one.
- **Extend, don't replace.** Read the existing code and data model first and reuse their patterns. Don't propose a parallel new system.
- **Ask about scope.** When a product serves several kinds of customers or workspaces, ask which ones a change applies to before building it.
- **Short, spaced replies.** One item per line, no walls of text.

## Safety
- **No delete without written OK.** That covers files, apps, caches and DB rows. List what could be removed and wait for item-by-item approval in chat. A spoken "OK" isn't enough.
- **Messages stay drafts.** For emails, fill in To, Subject, body and attachment, check that the Subject field really has text, then leave it as a draft. The user presses Send.
- **No real-world side effects while testing.** No real orders, payments, couriers or notifications. Test against a local or staging DB.
- **Back up before every production write** and record the rollback statement next to the change.
- **Force-update floors.** Never raise an app's minimum-version setting above what is actually live on that store, and check which number the app really compares (an internal constant can differ from the store build number).

## Quality
- **QA before every build.** Before sending any APK or IPA, run a full review of every request plus an error-scenario pass that tries ways customers misuse the app. Open the changed screens yourself, since API checks miss UI regressions.
- **Fetch before you edit.** When others (or an admin panel) can push to a repo, `git fetch` and compare with the remote before touching code.
- **Use the source's own categories.** When importing data that already has categories, use them exactly. Don't invent a finer grouping.
- **Send required fields explicitly.** Generic "re-submit the form as-is" scripts can silently clear a required field.
- **Old builds can't be patched.** Text and translations compiled into an installed app stay as they are until the user updates. Plan server-side changes with that in mind.

## Git & delivery
- **A branch per round of work**, named with the date (e.g. `edits-YYYY-MM-DD`), set as the default branch.
- **A README on every branch:** what it is, what's new, a table of branches and the change history, readable from the GitHub front page.
- **Desktop app standard:** install and download tracking in the admin, a push-update flow (update now with auto-restart, or remind me later), and a What's New screen.

## Job applications
- **Researched note first.** Every CV opens with a short narrative note to that company: its mission, its products, the recruiter's name, or "Hiring Team" when no name is found. Never guess a name.
- **Honest about gaps.** When the gap is learnable, apply, say so plainly, give evidence of fast learning, and offer a trial period.

## Messaging
- **Chat-app formatting.** Use line breaks (Shift+Enter in web chat apps), one numbered question per line, and send it all as one message.

## Agents
- **Narrow helpers stay narrow.** When a shared task board exists, tell a helper agent which items are NOT its job. Otherwise it may pick them up and write to live systems twice.
