=======================
Contribution guidelines
=======================
These guidelines are aimed to ease code review process and establish unified
contribution process.

Submitting changes
------------------
- Fork and clone the repository.
- Make a branch off of `master` branch.
- When ready - push the branch and create a pull request to `master` branch.
- Make sure that the CI build passes.

Making commits
--------------
- Split your logically separate changes into separate commits.
- Split formatting changes into separate commits.
- Provide detailed descriptions for your commits so it would be easier for
  the other contributors to review/investigate the code written by you.
- The commit messages must be formatted in Linux-style way:
    * Summary line no longer than 50-75 characters.
    * Blank line.
    * Explanation body wrapped at 75 columns.

Code review
-----------
- At least 2 developers from the core team must approve a pull request before
  it could be merged.

Branching strategy
------------------
- The main branch is `master`.
- Contributors create topic branches for each bugfix/feature/etc off of `master`
  and merge them back to `master`.
- At a release time - a release branch is made.
- To backport a change to a release-branch - it first must be committed to
  `master` branch or a relevant release-branch and then cherry-picked to
  older release-branches.
- Each release must be tagged.
