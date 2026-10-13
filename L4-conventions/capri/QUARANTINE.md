# Quarantined runs (2026-10-07/08)
Rows written from 2026-10-07 onward (queue_L4c, queue_L4d, drift checks) are excluded from all analysis.
Cause: the subscription CLI (`claude -p`) now injects a user-context block into every run even with --system-prompt replaced:
the account email (a US university address), today's date, an environment section with the model name, and, when run inside
the repo, the project auto-memory. 0 of 5,019 rows from Oct 3-5 mention the email; 14 of ~500 rows from Oct 7-8 do. The
email hints that the principal is American, which confounds a study of US-default units. `--bare` removes the block but needs
an API key; CLAUDE_CODE_USER_EMAIL and CLAUDE_CODE_SIMPLE did not help on the subscription. The "Sonnet drift" found on Oct 8
(card condition: 3% -> 53% silent errors) was measured under this contamination and is not established.
