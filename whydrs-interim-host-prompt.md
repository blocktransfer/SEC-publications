Create a new PR in the WhyDRS documents repository titled:

**🌱 Set up interim host**

Set up a minimal interim web host for the existing documentation. Scaffold the current docs into a simple web server/site that can serve the repository’s documentation without substantially rewriting or reorganizing the underlying content.

This is intentionally temporary infrastructure. Existing links, paths, anchors, or other references may break as a result of moving the docs behind this interim host, and **that is acceptable for this PR**. Do not spend time building compatibility redirects or preserving every old URL unless they are trivial.

Keep the implementation as simple and lightweight as practical. Reuse the repository’s existing structure where possible rather than introducing a large framework or unnecessary build system.

Before making changes, inspect the repository and determine the simplest appropriate way to serve the existing documentation. Implement it, run any relevant checks or build commands, and verify that the docs can actually be served.

Create the PR against `main`.

The PR description should clearly explain:
- that this scaffolds the existing documentation into a simple interim web host;
- that the goal is to get the documentation hosted and navigable with minimal infrastructure;
- that some existing links or URLs are expected to break during this interim stage and that this is knowingly acceptable;
- what was added or changed to make the site runnable;
- how to run or preview it locally, if applicable.

Do not present broken-link compatibility as unfinished work that blocks this PR. It is explicitly outside the scope of this interim hosting step.

Follow the repository’s existing conventions where they exist. Do not make unrelated content edits.
