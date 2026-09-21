# Execution Adapter Specification

## 1. Purpose

This document defines this repository's **Execution Adapter**: which AI platform actually carries out an agent's work at a given pipeline stage, and how a stage's instructions are handed to that platform and its output received back, regardless of which platform it is.

This is a different concern from [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md), which is a **Storage Adapter** -- it defines where artifacts are tracked and stored (files, Issues, PRs, labels) once produced. This document defines who or what produces them. The two are independent: a run executed on Claude, ChatGPT, or Copilot all write to the same GitHub-light storage layer, unchanged.

The need for this document is not new -- it was deferred, not overlooked. [PRD.md](../PRD.md) section 4 already requires "the business artifact model must remain portable beyond a particular automation engine or agent runtime," and [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md)'s Purpose already states it "does not define the implementation of any particular model or automation engine." Both left the actual adapter undefined until an automation phase existed to need it. Decided 2026-09-03: that phase has started, and platform-agnostic execution -- run this automatically, or run any single stage by hand on whichever platform is at hand (Claude, ChatGPT, or Copilot) -- is an explicit goal of it.

**Scope, decided 2026-09-03:** this document defines the invocation contract only -- what a platform must be given, and what it must return, to correctly execute one pipeline stage. It does not define how a given platform's internal mechanics (tool-calling format, context-window handling, its own prompting conventions) get normalized, and it does not define credential or configuration management for any platform. Those stay out of scope so this document does not overreach into implementation detail before [FRAMEWORK-CONFIGURATION-SPEC.md](FRAMEWORK-CONFIGURATION-SPEC.md)'s companion Tool Contract (per-stage callable functions, not yet written) exists to build on.

## 2. Relationship to Other Artifacts

- [BUSINESS-AGENT-WORKFLOW.md](BUSINESS-AGENT-WORKFLOW.md) and [TECHNICAL-AGENT-WORKFLOW.md](TECHNICAL-AGENT-WORKFLOW.md) already define, per stage, the ordered Processing steps, the Input Contract, and the Output Contract. This document does not change any of that -- it defines how a platform receives that same input and returns that same output. If this document and either workflow document ever disagree about what a stage must produce, the workflow document is authoritative.
- [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md) is the sibling Storage Adapter. Nothing here changes its artifact mapping, labels, or automation triggers -- a Business PR is a Business PR whichever platform produced its contents.
- [FRAMEWORK-CONFIGURATION-SPEC.md](FRAMEWORK-CONFIGURATION-SPEC.md) section 13 (Platform and Storage Adapters) maps framework concepts to this repository's storage tooling only. It does not cover execution platform -- this document is that missing sibling table, kept separate rather than folded in, so the two adapter concerns stay as cleanly divided as they are conceptually.
- [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md) defines each agent's May/May-not boundary platform-agnostically. This document does not add or remove anything from those lists -- a Business Agent run on ChatGPT still may not approve its own Business PR, exactly as on Claude.
- A platform-neutral Tool Contract (per-stage callable functions derived from each workflow document's Processing/Output tables) and a stage-level runner/orchestrator are both still undesigned -- later items on the automation roadmap discussed with Manali 2026-09-03. This document is deliberately narrow enough not to presuppose either.

## 3. Governing Principle

**The workflow contract is canonical; the execution platform is a projection, never a second source of truth for what a stage must do.** The same principle [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md) section 3 applies to storage applies here to execution:

- A stage's Input Contract and Output Contract, as defined in BUSINESS-AGENT-WORKFLOW.md or TECHNICAL-AGENT-WORKFLOW.md, do not change based on which platform executes the stage. A platform that cannot produce the full Output Contract has not correctly executed the stage, whatever it did return.
- No platform gets its own version of a workflow document. There is one BUSINESS-AGENT-WORKFLOW.md and one TECHNICAL-AGENT-WORKFLOW.md; every platform is handed the same document as its instruction set.
- Any pipeline stage must be executable, in isolation, by any configured platform -- not only as part of a full end-to-end run. Section 5 below states the contract that makes this possible.

## 4. Per-Platform Invocation Mapping

Decided 2026-09-03: all three platforms Manali named are specified now, even though only Claude is implemented today (item 4 on the automation roadmap). ChatGPT and Copilot are specified to the same invocation-contract depth as Claude, not left as placeholders.

| Platform | Invocation Mechanism | Input Delivery | Output Capture | Notes |
| --- | --- | --- | --- | --- |
| Claude | Claude Code (CLI, local or bridged) or a Claude Agent SDK session, run with repository access | The relevant workflow document (BUSINESS-AGENT-WORKFLOW.md or TECHNICAL-AGENT-WORKFLOW.md) as the session's instructions, plus direct read access to the repository files that satisfy that stage's Input Contract | Direct: commits, file edits, and PR creation happen in the same session, against the repository directly | Reference implementation platform (item 4). Direct file access means no packaging step is needed between input contract and actual files. **Built 2026-09-09**: [.claude/agents/business-agent.md](https://github.com/manalimatkar/product-management/blob/main/.claude/agents/business-agent.md) is the real, invokable form of this row for the Business Agent -- declared tool access (`Read, Grep, Glob, Write, Edit, Bash`) plus this same "workflow document as instructions" mechanism, not a rewrite of it. Technical Agent and Developer Agent definitions are not yet built. |
| ChatGPT | A configured GPT, or a plain API/chat session, without native git repository access | The relevant workflow document supplied as context, plus the specific files that satisfy that stage's Input Contract packaged into the conversation (pasted or uploaded) -- ChatGPT cannot read the repository on its own | Indirect: ChatGPT returns the stage's output as text or a patch; a human, or a thin wrapper script once the orchestrator (roadmap item 5) exists, applies it as an actual commit against the repository | Until an automated wrapper exists, applying ChatGPT's output to the repository is a manual step -- documented here as the current fallback, not a gap in this specification. |
| Copilot | Copilot Chat or agent mode inside an IDE with the repository open, or the Copilot CLI | Same as Claude -- the relevant workflow document as instructions, direct read access to the repository files satisfying the Input Contract | Direct, same as Claude -- Copilot's IDE/CLI integration edits and commits against the repository directly | Mirrors Claude's mechanism since both have native repository access; differs from ChatGPT for that reason. |

Whichever platform runs a stage, it is given exactly two things and nothing else: **(a)** the relevant workflow document as its complete instruction set, and **(b)** the Input Contract that document's own section 3 already defines. No platform-specific prompt rewrites the workflow document's steps -- per section 3's governing principle, doing so would make the platform a second source of truth for what the stage must do.

## 5. Stage-Level Invocation

This section states the contract that satisfies Manali's explicit requirement (2026-09-03): the ability to run one specific stage of the pipeline, on any platform, without running the full end-to-end sequence.

Both BUSINESS-AGENT-WORKFLOW.md section 4 and TECHNICAL-AGENT-WORKFLOW.md section 4 already number their Processing steps in dependency order and cite what governs each one. That existing structure is what makes stage-level invocation possible, without any change to either document:

- Any single numbered step (or the smallest reasonable group of consecutive steps that share one output, e.g. Business Agent steps 11-13, Epic/Story/Acceptance-Criteria generation) may be invoked on its own, on any platform from section 4's table, **provided every artifact that step's own governing section lists as a precondition already exists in the repository at the state that step expects.**
- This is the same precondition a full end-to-end run would have satisfied naturally by the time it reached that step -- stage-level invocation does not relax any entry condition, it only skips re-running the steps that already produced what's needed.
- A platform invoked for a single stage is not told the stage number in some new vocabulary -- it is handed the same workflow document and the same Input Contract as a full run, and simply produces one step's Output Contract because that is all its scoped instruction covers. This document does not need a second, per-step contract format; the workflow documents' own step tables already are that format.
- Verifying that a step's precondition actually holds before invoking it is a job for the not-yet-built orchestrator (roadmap item 5) or for a human running the step by hand -- this document defines that the contract supports it, not the tool that checks it automatically.

## 6. Identity and Attribution Across Platforms

Whichever platform executes a stage, the artifact it produces is attributed to the role performing the work -- `ROLE-006` Business Agent, `ROLE-007` Technical Agent, or `ROLE-008` Developer Agent, per [FRAMEWORK-CONFIGURATION-SPEC.md](FRAMEWORK-CONFIGURATION-SPEC.md) section 10 -- never to the platform's own name. A commit or PR produced via Claude Code is authored as the Business Agent role, exactly as one produced via Copilot or applied by hand from a ChatGPT session would be. This keeps [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md)'s `Traces to:` convention and every review-gate rule in [FRAMEWORK-CONFIGURATION-SPEC.md](FRAMEWORK-CONFIGURATION-SPEC.md) section 11 working unchanged regardless of execution platform -- a gate never needs to know which platform ran a stage, only which role did.

## 7. Open Decisions

- Should ChatGPT's manual apply-the-output step (section 4) be replaced with a scripted wrapper once the stage-level runner/orchestrator (automation roadmap item 5) exists, or does ChatGPT stay a manual-apply platform by design given it has no native repository access?
- What is the exact packaging format for input delivered to a platform without native repository access (ChatGPT), beyond "the relevant files, supplied as context"? Deferred until this repository actually runs a stage on ChatGPT for the first time.
- How is a platform's output verified as conforming to a stage's Output Contract before being accepted -- an automated check, or human review every time? Likely a concern for the Tool Contract (roadmap item 3) rather than this document, but not yet resolved either place.
- Should this document define fallback behavior when a preferred platform is unavailable (rate-limited, offline), or does that stay an operator decision made at run time?
- Should Execution Adapter choice be recorded per-run (e.g. a field alongside the Stage Trace) so a completed artifact's provenance shows which platform executed it, the way GITHUB-PLATFORM-ADAPTER-SPEC.md records storage provenance? Not addressed here.
