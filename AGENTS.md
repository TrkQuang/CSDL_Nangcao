# Autonomous Development Workflow

## Mission
When given a feature, bug, or improvement request, take ownership of the task from investigation through implementation and verification. Do not stop at advice or a plan when the requested work can safely be completed.

## 1. Understand Before Acting
- Inspect the repository structure, Git status, existing architecture, and relevant code before editing.
- Read existing project instructions and identify the actual package manager, test commands, and coding conventions.
- Preserve existing user changes. Never overwrite unrelated work.
- Ask a question only when a missing decision materially blocks safe implementation.

## 2. Automatically Select Skills
- Inspect available skill descriptions and activate the most relevant skill before performing specialized work.
- Use `using-superpowers` to follow the Superpowers skill-selection process when available.
- Use `find-skills` only when no installed skill adequately covers the task and further discovery is useful.
- For ambiguous requirements or substantial new features, use `brainstorming`.
- For structured specification-driven work, use Spec Kit in order: specify, plan, tasks, implement, as applicable.
- For bugs, use `systematic-debugging`.
- For test-first implementation, use `test-driven-development` when appropriate.
- For code review, use `ponytail-review` when available.
- Use `verification-before-completion` before claiming the task is complete.
- Do not invoke every skill indiscriminately. Avoid duplicate or conflicting workflows.

## 3. Plan Proportionally
- Small, clear changes: proceed directly after inspecting the relevant code.
- Medium or large changes: define acceptance criteria, implementation steps, and test strategy.
- Avoid generating unnecessary specifications for trivial fixes.
- Do not silently expand the requested scope.

## 4. Implement
- Follow the existing architecture and naming conventions.
- Reuse existing dependencies and components when appropriate.
- Add or update tests for changed behavior.
- Avoid unrelated refactors, dependency upgrades, and configuration changes.

## 5. Verify and Repair
- Run the most relevant tests, static checks, and production build available.
- Inspect failures and fix regressions caused by the changes.
- Repeat verification after fixes.
- If a command cannot run, state the reason and do not claim it passed.
- Inspect the final Git diff for unintended changes.

## 6. Safety Boundaries
- Do not expose secrets or copy them into logs.
- Do not delete user data, rewrite unrelated files, or perform destructive operations without explicit approval.
- Do not deploy, publish, push, alter production data, or incur costs without explicit approval.
- Ask before making irreversible or security-sensitive changes.

## 7. Completion Report
Report:
- What was implemented.
- Files changed and why.
- Skills used and why.
- Commands and tests actually run, with their results.
- Known limitations or remaining work.
- Whether any changes remain uncommitted.

Do not report success without evidence.