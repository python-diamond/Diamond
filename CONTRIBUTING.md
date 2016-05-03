Contributing to Netuitive's Diamond Project
===========================================

### Workflow for contributing

1. Create a branch directly in this repo or a fork (if you don't have push access). Please name branches within this repository `feature/<description>` or `fix/description`. For example, something like `feature/add_httpcode_collector.

1. Create an issue or open a pull request (PR). If you aren't sure your PR will solve the issue or may be controversial, we're okay with you opening an issue separately and linking to it in your PR. That way, if the PR is not accepted, the issue will remain and be tracked.

1.  Close (and reference) issues by the `closes #XXX` or `fixes #XXX` notation in the commit message. Please use a descriptive, useful commit message that could be used to understand why a particular change was made. Keep pushing commits to the initial branch using `--amend`/`--rebase` as  necessary, and don't mix unrelated issues in a single branch.

1. Clean up the branch (rebase with master to synchronize, squash, edit commits, etc.) to prepare for it to be merged.

### Merging contributions

1. After reviewing commits for descriptive commit messages, documentation, passed continuous integration (CI) tests, version bumps, and a changelog, a project maintainer can merge.


### Releasing

1. Create/update the changelog if necessary.