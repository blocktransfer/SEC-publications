# Published examination review policy

Examination folders become protected when their own README.md contains a valid publish date strictly before today's UTC date. Accepted formats are "15 Sep 2025" and "2025-09-15" in a leading fenced metadata block or YAML front matter. Missing READMEs, missing metadata blocks or publish tags, empty values, and unrecognized or invalid dates do not require approval. Dates today or in the future do not require approval either. When no changed folder qualifies, the required status passes with "No publication approval required" and no approval request. GitHub still needs this passing status to satisfy the branch ruleset. API failures continue to fail the check.

Changes anywhere in examinations/<folder>/, including deleted and renamed files, are checked against BOTH the base and proposed-head README dates. Once either version is published, editing that folder requires a GitHub APPROVED review on the current head commit from another human with write/admin repository access. A new push requires fresh approval. Folder rules apply automatically on future publication dates, without editing a list. Other folders remain unblocked by this date-based status.

The trusted workflow runs with pull_request_target and workflow_run, checking out ONLY main. An unprivileged pull_request_review workflow emits a numeric PR number artifact, not code; a privileged workflow then independently fetches current PR changes, publication dates and reviews from GitHub. This avoids running untrusted PR code with write privileges. A failed review signal cannot grant approval; manually rerun the trusted check if a review event does not deliver its artifact.

## Required GitHub settings after merge

This repository cannot install branch rulesets by committing files. A repository administrator must visit https://github.com/blocktransfer/SEC-publications/settings/rules and add an active MAIN branch ruleset:

1. Require a pull request before merging, without bypass permissions.
2. Require the commit status named published-examination-approval to pass. Where available, select GitHub Actions as the expected source.
3. Block force pushes and deletions. Independently protect the workflow and helper scripts from unreviewed changes (e.g. code-owner review or dedicated administrative rules).
4. Verify with a test PR changing examinations/response-8/README.md that it cannot merge without approval and succeeds after an eligible reviewer approves the current SHA.

The workflow does not itself prohibit direct pushes or merges; ruleset configuration is essential. You may separately require GitHub-native approval for all PRs as defense-in-depth, though that would also affect unpublished folders.
