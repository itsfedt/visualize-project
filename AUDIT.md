# Public-readiness audit — 2026-10-28

## A. Current-state verdict

This checkout is a portable instruction package for coding agents, with a Python installer and a Python architecture-output validator. It is not an autonomous architecture analyzer or application. Its audience is developers who want evidence-backed repository maps with editable diagrams and explicit uncertainty.

Primary evidence: `visualize-project-skill/install.py` copies the portable directory and selects a target wrapper. `portable/visualize-project/scripts/validate_architecture.py` reads generated files. The portable skill and wrappers instruct the host agent to discover, model, visualize, and verify. References define overview/deep outputs. Assets contain an illustrative model and Markdown template. There are no service entry points, APIs, database schemas, containers, infrastructure, authentication implementation, runtime package dependencies, or deployment configuration to audit.

The critical journey is: install into a host's skill directory → invoke overview/deep against a repository → agent records evidence in JSON → agent writes diagrams → external renderer creates SVG → validator checks structure → agent/human reviews evidence and visual quality. Only installation and structural validation are executable here. Host interpretation, tool permissions, renderer availability, factual accuracy, and visual inspection remain external steps.

The supplied directory has no `.git`, remote, or history. It cannot substantiate previous releases, committed-secret absence, or hosted CI status. New files are local changes, not a published release.

## B. Core strength

One evidence-bearing model can support several views without forcing deployment, runtime, and internal components into one diagram. Explicit confidence and verification records are useful differentiators from asking an agent to draw a diagram ad hoc. This is a sound workflow design, not yet a measured claim of superior output quality.

## C. Biggest credibility gaps

Ranking uses Impact × Evidence × Urgency, each scored 1–3. Equal scores are ordered by release relevance. Scores describe the initial finding; status describes the result of this work.

| Severity / score | Evidence and consequence | Smallest correction and objective verification | Status |
|---|---|---|---|
| BLOCKER / 27 | No recorded real host runs or rendered demo; evaluation file contained prompts only. The central accuracy/readability claim is unproven. | Run overview and deep on a fixed small repository; save input revision, host/model/renderer versions, outputs, evidence review and visual scores. Compare against an ordinary diagram prompt. | Open |
| BLOCKER / 27 | No license existed, leaving intended reuse terms unspecified. | Add a license explicitly selected by the owner; check the delivered distribution includes it. | MIT selected by user and added at repository root |
| HIGH / 27 | Installer removed the destination with `rmtree` before copying source. A missing wrapper or copy failure could destroy the old installation. | Stage first, preserve old directory during publish, roll back ordinary errors; inject copy and publish failures. | Fixed; regression tests pass |
| HIGH / 27 | Validator called `.get` and concatenated values without checking types; missing evidence was only a warning; SVG presence could pass with invalid content. | Validate core shape before graph checks, reject missing evidence/invalid SVG, enforce mode files; malformed and mutation cases must fail without tracebacks. | Fixed within documented structural scope |
| HIGH / 18 | No root README, test suite, or CI; setup relied on host knowledge. Design notes claimed a shared model prevents contradictions. | Give a first-use path and explicit limits; test fresh-copy installs, wrapper consistency, and failures; add CI. | Local checks pass; hosted CI remains unverified |

## D. Improvement plan, ordered by impact

1. **Prove the core journey before public promotion.** Use `references/skill-evals.md` and `verification-rubric.md` to record host execution and factual/visual results. Add only an evaluation fixture and its reviewed output, not new product features. The proof is reproducible artifact quality, not a screenshot of an unverified diagram.
2. **Make installation and verification trustworthy.** Completed changes to `install.py`, `scripts/validate_architecture.py`, and `tests/` directly address demonstrated data-loss and false-confidence paths. Failure injection and defective-package rejection matter more than additional diagram types.
3. **Make first use understandable.** Completed README, installation, design, schema, contribution, and license updates describe what actually runs. The remaining proof is a new developer completing the documented agent workflow on each supported host.
4. **Publish only after independent checks.** Run the configured Windows/Linux CI matrix in a real remote, establish the repository's release root, and attach the real evaluation artifacts. Do not invent a changelog, badges, release history, or deployment for a local distribution.

Selective comparisons: [Anthropic's skills repository](https://github.com/anthropics/skills) clearly distinguishes instruction packages and examples from guaranteed behavior; that distinction fits this project. Its broad catalog and plugin marketplace are unnecessary here. [ADR Tools](https://github.com/npryce/adr-tools) leads with a short first-use workflow and keeps executable examples in tests; those patterns fit a small developer tool. Its installation ecosystem and shell implementation do not need to be copied. Sources inspected on 2026-10-28; no popularity claims are needed to justify these patterns.

## E. Changes completed

- Staged installation, ordinary-error rollback, backup collision protection, linked-destination rejection, and concise error exits. Cached Python bytecode is excluded from installed copies. Concurrent installs and crash recovery remain explicitly limited.
- Validator type checks, version/timestamp checks, required evidence, flow-step shape, core identifiers, mode-required documents/diagrams, SVG XML validation, and containment checks for recognized Markdown SVG links. This does not validate every optional metadata field.
- Fourteen standard-library regression tests, including three hosts installed from a fresh copied distribution with spaces in its path, execution from an unrelated directory, replacement failures, malformed JSON values, and portable/wrapper body consistency.
- Ten-case reproducible structural evaluation, root onboarding, MIT license, contribution guidance, ignore rules, and read-only-permission CI matrix for Python 3.12/3.14 on Windows/Linux.
- Corrected documentation overclaims: sharing a model does not prevent contradictory diagrams; SVG XML validity does not prove rendering, factual accuracy, or visual quality.

## F. Verification matrix

PASS means the stated check ran successfully. FAIL includes required gates that remain unverified; it does not imply a demonstrated product defect in every case.

| Requirement | Evidence | Result |
|---|---|---|
| Clean install | Tests copy the distribution to a temporary path, install all three targets, compare installed assets, and execute the installed validator. Windows, Python 3.14.2. No pip dependencies. | PASS — fresh-copy utility scope; clean OS/host setup unverified |
| Core E2E | Installer-to-validator smoke passes. No real host invocation, Mermaid/D2 render, or independent visual review was completed. | FAIL — complete user journey unverified |
| Tests | `python -m unittest discover -s visualize-project-skill/tests -v`: 14 tests, 7.386 seconds, all pass. | PASS |
| CI fully green | Workflow added for four OS/Python combinations; no remote or hosted run exists here. | FAIL — unverified |
| Lint/type checks | AST parsing and `compileall` pass. No configured linter or static type checker is installed. Syntax checks are not substitutes. | FAIL — not established |
| Security | Reviewed two utility entry points; no network calls, shell execution, auth service, or credential store. A targeted secret-pattern scan of 24 source/document/config files found zero candidate files. No third-party Python runtime dependency set exists. | FAIL — full release gate unverified; no known critical issue found in bounded review |
| Authorization boundaries | No application auth boundary exists. Installer writes the selected target; link/backup refusal is tested. Agent permissions are host-controlled and not exercised end-to-end. | FAIL — host boundary unverified |
| Performance/evaluation | Structural suite: 10/10 expected outcomes; file-presence baseline: 1/10. Nine defective fixtures rejected, valid fixture accepted. | PASS — structural detection only; central product claim unverified |
| Documentation accuracy | Inspected implementation versus claims; wrapper body consistency passes; README/contribution local links checked. Remaining host behavior is labeled unverified. | PASS — bounded consistency review |
| Production build | Python compile/AST checks pass and copied distribution installs. There is no compiled application or deployment target. | PASS — distribution smoke equivalent only |
| No secrets committed | No Git history or index available; current-file pattern scan cannot establish history cleanliness. | FAIL — unverified |
| No unresolved blockers | Real agent/render/evidence/visual evaluation is outstanding. | FAIL |

### Evaluation conditions and limitations

Run from the repository root:

```sh
python visualize-project-skill/tests/evaluate_validator.py
python visualize-project-skill/tests/evaluate_validator.py --baseline
```

The baseline intentionally exits 1 because it fails the quality gate. It checks only that expected files exist; it is **not the original validator**. Both evaluations use the shipped illustrative JSON plus a tiny synthetic Mermaid/SVG package. Mutations cover non-object JSON, null collections, invalid items, absent evidence, dangling endpoints, invalid SVG, wrong mode, unsupported version, and invalid timestamp. Metric: correct acceptance/rejection with no traceback. Current result: 10/10; file-presence baseline: 1/10.

The current subprocess evaluation took 1.585 seconds on Windows/Python 3.14.2; the in-process presence baseline took 0.080 seconds. These are single-run observations with different execution overhead, not a speed comparison. No AI tokens, cost, repository-discovery latency, or diagram quality were measured. The dataset is deliberately small and constructed around known structural errors; it does not establish generalization or superiority over other architecture tools.

Recorded failures: the first sandboxed regression run failed on Windows temporary-directory permissions and was interrupted; an approved unrestricted rerun passed. An attempted comparison with the original validator failed because its saved sandbox-temporary path was not accessible in the later process; those results were excluded. The explicit presence-only baseline above is reproducible. No historical improvement percentage is claimed.

## G. Remaining risks

- No measured end-to-end agent behavior, cross-host compatibility, renderer execution, model-to-diagram fidelity, or visual demo. These are the most important remaining uncertainties.
- An evidence string can be false. The validator does not establish that a cited path exists or supports a claim; it also cannot detect secrets reliably or sanitize arbitrary SVG.
- The host may send repository content to its AI provider. Generated files persist architecture details. Retention/deletion is filesystem-based; no automatic retention service exists.
- Optional transient Mermaid installation is unpinned third-party code execution. Host/model/renderer changes can alter output and reproducibility.
- Forced replacement intentionally removes personal modifications after successful publication. Installs must be serialized; process termination can leave a recoverable sibling backup. Symlink checks are not a defense against a hostile process racing filesystem changes.
- Windows/Python 3.14.2 was exercised locally. Python 3.12 and Linux are configured in CI but not yet proven. No package vulnerability scanner, specialist secret scanner, or static type checker ran; absence of third-party Python dependencies is not proof that the interpreter or host is vulnerability-free.
- The four skill bodies duplicate instructions. A consistency test now catches drift, avoiding a speculative templating/build system.
- No remote, Git history, public security contact, or release record was available. The outer workspace is assumed to be the future repository root because it now contains the README, license, and workflow; publishing only the inner folder would omit them.

## H. Public-readiness verdict

**NOT READY**

The utilities are materially more reliable, locally tested, and documented, and reuse terms are now explicit. However, the central product promise still lacks a recorded real-agent and renderer evaluation, and hosted quality gates have not run. These are release evidence gaps, not reasons to expand the feature set. Complete the core workflow evaluation and CI before upgrading the verdict.
