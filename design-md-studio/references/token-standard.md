# Token standard

Framework-aware and product-neutral: no fonts, palette, financial terminology, directory layout, or visual identity from the project where this skill was created is a default.

## Layers and naming

1. **Framework foundation:** retain the installed version's standard font, type, spacing, radius, container and effect scales. Record the version/source and actual overrides, not every default. Without a framework a shared CSS scale serves the same purpose; do not install Tailwind to normalize a document.
2. **Semantic roles:** prefer familiar pairs such as background/foreground, primary/primary-foreground, secondary/secondary-foreground, card/card-foreground, popover/popover-foreground, plus muted, border, input, ring and destructive only when needed.
3. **Components:** reference shared roles/scales. Add a special token for a real reusable distinction, not each field of each card. Equal values do not prove equal roles; different names can duplicate one responsibility.

Tailwind namespaces include `--color-*`, `--font-*`, `--text-*`, `--font-weight-*`, `--tracking-*`, `--leading-*`, `--container-*`, `--radius-*`, `--shadow-*`, `--ease-*`, `--animate-*`. Use them with that framework, not as mandatory naming on every platform. Custom `--z-*` variables do not automatically create utility classes.

Pair text sizes with related line-height/weight (e.g. `--text-article-prose` and `--text-article-prose--line-height`) only when a specific role needs a distinct treatment. Preserve coherent incumbent naming; renaming is a reviewed proposal, not a prerequisite.

Use stable semantic names across themes. Theme overrides choose values rather than `button-light`/`button-dark` implementations. Preserve the user's theme selector. Keep physical primitive color scales stable in new systems; explain incumbent exceptions. Do not copy a reference's misleading `white` primitive if it turns dark under a theme.

An accent-foreground name alone does not prove readable contrast: validate the intended pair. Keep product status, system errors and destructive actions distinct where needed. Add only relevant chart, selection, and domain roles.

## Findings

Show evidence, original/proposed name and value, reason, affected references and uncertainty. Distinguish unused-within-checked-scope from verified unused. Do not assume compiled CSS variables were all hand-authored, or judge quality by token count.

Check overlapping responsibilities, unnecessary framework aliases, unresolved references, ambiguous roles, inconsistent scales, code/document drift, missing theme pairs and inaccessible intended combinations. Separate stylistic alternatives from defects. Preserve custom content whose purpose has not been disproved.

## Portable DESIGN.md output

Consult the current official specification when compatibility matters. The checked baseline supports metadata name, optional version/description/omitted, and groups colors, typography, rounded, spacing, components. YAML may be front matter or interleaved fenced blocks; define each top-level key once. References use `{path.to.token}`; composite typography references are permitted in components.

Canonical sections in order when included: Overview; Colors; Typography; Layout; Elevation & Depth; Shapes; Components; Do's and Don'ts. Omit irrelevant sections honestly. Component properties: backgroundColor, textColor, typography, rounded, padding, size, height, width. Describe motion, layering, shadows and unsupported properties in relevant prose, not invented schema groups. CSS namespaces are not YAML schema keys.

For multiple themes retain an existing interoperable format where possible. For a new document use one colors map with explicitly theme-qualified value keys and one documented semantic mapping table; components describe one role across themes. Do not invent nested color objects or a top-level themes key. Resolve CSS var expressions from evidence instead of exporting missing dependencies as standalone values. Preserve original valid color syntax.

Framework scales may be intentionally omitted from YAML with a reason and framework version/source in relevant prose. Document overrides and usage instead of duplicating a default theme. Include enough project-specific exact values or resolvable references to make the document useful independently.

## Sources

- [Resurf CSS](https://resurf.so/_next/static/css/fb0974b4e6dab424.css): inspiration for categories, aliases, states, themes, typography groups and layer names. Palette, fonts, sizes and high z-index numbers are examples, not defaults. Hashed URLs may disappear; do not fetch it every run or claim a changed bundle was inspected.
- [DESIGN.md article](https://designmd.app/what-is-design-md): tokens plus human-readable intent, concrete values and practical guardrails.
- [Official format](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md): authoritative for schema; verify before claiming conformance to a newer version.
- [Tailwind theme variables](https://tailwindcss.com/docs/theme): namespaces/utility mapping; determine the installed framework version first.
