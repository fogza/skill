# Skills

Reusable Codex skills maintained by fogza.

## design-md-studio

[Skill instructions](design-md-studio/SKILL.md)

Review or prepare a DESIGN.md through project-context discovery, focused interviews, minimal design tokens, visual previews, edits and comments. Save the reviewed document only after explicit confirmation.

- Preserve existing design evidence and framework scales before proposing presets.
- Reuse relevant Impeccable discovery/design guidance and Visualize review capabilities when available.
- Keep a working fallback for edits and comments when the host feedback bridge is unavailable.
- Do not modify frontend source, PRODUCT.md, or configuration as a side effect.

## Install

Clone this repository, then copy the `design-md-studio` directory into your personal Codex skills directory (`$CODEX_HOME/skills`, or `~/.codex/skills` when unset). Preserve an existing installation rather than overwriting local edits without reviewing them.

Invoke the installed skill with `$design-md-studio`.

The skill discovers supporting skills by name rather than hardcoded machine paths. Impeccable and Visualize improve the workflow; their availability and host capabilities are checked at use time. The review helper uses Python 3.9+ standard library. Its JavaScript regression checks use Node.js.

## Verification

Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s design-md-studio/scripts
node design-md-studio/scripts/test_review_logic.cjs
```

The interactive preview does not grant file-write approval. Review submissions and comments are draft input; the human confirms the final DESIGN.md revision separately.
