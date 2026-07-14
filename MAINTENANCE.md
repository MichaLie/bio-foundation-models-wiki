# Maintenance protocol

This is the canonical, agent-neutral operating guide for the Biological Foundation Models index. `CLAUDE.md`, `AGENTS.md`, and `.claude/skills/` are adapters to this file; if they disagree, this file wins.

## Purpose and boundary

The resource is a curated decision aid covering reusable biological foundation models plus clearly labelled platforms and benchmarks. A model must be pretrained, reusable, and broader than one task. Pathology and spatial imaging route to `spatial`; datasets/leaderboards to `benchmark`; serving/tooling hubs to `platform`.

The index is curated, not a paper feed. A new publication is not sufficient evidence for inclusion. Do not infer scientific superiority, clinical fitness, or legal reuse from presence in the catalog.

## Sources of truth

- `models_final.json`: canonical displayed records; the only release catalog data edited by hand or a reviewed migration.
- `records_under_review.json`: complete non-displayed HOLD candidates, with reserved IDs, reasons, evidence, and reconsideration conditions.
- `schema.json`: JSON Schema 2020-12 contract.
- `resource_metadata.json`: resource identity, dates, version, provenance, creator/publisher/licence decisions.
- `build.py`: deterministic build and synchronization entry point.
- `validate_catalog.py`: preview/release validation.
- `evidence/`: dated discovery and link-audit evidence.
- `docs/` and the root HTML/Markdown/JSON-LD files: generated distributions; never hand-edit them.

Counts are derived from `models_final.json`; never hard-code a count in agent instructions.

## Record identity and dates

- Preserve every existing `id`, even after a rename. Add old names to `aliases`.
- New records receive a unique `bfm-*` ID, `date_added`, and an evidence-backed `verified` date.
- `verified` means the record's claims and cited sources were checked on that date. A rebuild is not verification and must never refresh it.
- Use `date_modified` only when a record materially changes.
- Do not reintroduce relative `new` flags.

## Update workflow

1. Read this file, `schema.json`, and the latest dated evidence note.
2. Build normalized current name and alias sets before discovery.
3. Choose mode:
   - Quick correction/addition: bounded known records, still fully verified.
   - Full refresh: independent discovery lanes covering all 10 modalities, followed by shuffled adversarial review.
4. Verify current primary sources: matching paper/DOI, official repository/project/model hub, released artifacts, and exact licence/access wording. Never guess a URL.
5. Prefer HOLD over optimistic inclusion when identity, scope, artifacts, or terms remain unclear. Store HOLD candidates in `records_under_review.json`, never in the displayed catalog.
6. Apply releaseable changes to `models_final.json` and HOLD changes to the under-review register, preferably through a dated idempotent migration for a large refresh.
7. Record accepted, held, rejected, merged, and materially corrected decisions in a dated `evidence/` note.
8. Build, validate, audit links, inspect the rendered preview, and only then consider release.

Access wording must distinguish code, weights, data, API/server, gating, non-commercial terms, and no-licence/all-rights-reserved states. `noncommercial: false` is not proof of a permissive licence.

A promotion from the under-review register must satisfy its recorded `reconsider_when` condition, refresh primary evidence, preserve the stable ID, and pass the full gate. The validator fails if a held ID appears in both stores or leaks into the displayed catalog.

## Local verification

```bash
python3 build.py
python3 validate_catalog.py
python3 scripts/audit_links.py --workers 24 --timeout 20
git diff --check
```

The public, agent-neutral harness in [`maintenance/`](maintenance/README.md) runs these gates, full JSON Schema 2020-12 format validation, normalized identity/date checks, report generation, and isolated synthetic fault injection. The checked-in GitHub workflow runs quality gates on changes and a live-link audit on a schedule; it has read-only repository permissions and contains no deployment job.

`build.py` rebuilds twice and fails if generated artifacts are not byte-stable. Preview validation permits unresolved governance items only as explicit warnings.

Rendered-table regression check: above 900 px, scroll the catalog and verify that the table-header top is exactly aligned with the bottom of the sticky controls. At 900 px and below, controls and table headers must both be static, the table wrapper may scroll horizontally, and the document itself must not overflow. Test at least one wide desktop, 1024 px, 900 px, and 390 px viewport after changing filters, table CSS, fonts, or header content.

The public design is generated from `build_html.py`. Source Sans 3 is self-hosted in `assets/fonts/` under the SIL Open Font License and copied into `docs/assets/fonts/` by `build.py`; do not add a runtime font service or edit the generated HTML. Preserve the shared crisp layout and this index's green identity accent while keeping semantic status colors, table behavior, focus states, and mobile geometry accessible.

Before release, run:

```bash
python3 validate_catalog.py --release
```

Release mode must fail if record verification, catalogue licence, formal publisher identity, versioning, or distribution synchronization is unresolved. Do not weaken the gate to make it green.

## FAIR and fork checklist

A forker must update `resource_metadata.json` to their real landing page, repository, creator, publisher, licence, version, and provenance; rebuild all distributions; and validate the embedded and standalone JSON-LD. Never copy Michaela/ELIXIR identity or imply institutional endorsement without authority. Choose a licence only after confirming rights to the catalog content and code.

Stable URLs, JSON/JSON-LD, schema, checksums, provenance, sitemap/robots, and open protocol access support FAIRness. They do not replace current evidence, a licence, a PID/version policy, or community governance.

For this release line, catalog data/metadata/original documentation are CC BY 4.0 and maintenance/build code is MIT. External artifacts, services, logos, and trademarks retain their own terms. Michaela Liegertová is the individual publisher; IMG CAS is affiliation only, and ELIXIR-CZ is dedication/community context only.

Provenance separates `baseline_commit`/`baseline_commit_url` (the revision from which the refresh was derived) from `release_ref` (the immutable release URL). Keep `release_ref: null` during ordinary preview work. During an explicitly authorized final packaging step, set it to the planned release URL matching `repository/releases/tag/v<resource_version>`; after publication and before announcement, verify that the exact URL resolves. Do not try to embed the hash of the commit that contains itself.

## Publication boundary

Local editing, building, testing, and commits are preparation. Push, merge, Pages deployment, DOI minting, release creation, and public FAIR badges require explicit human approval after the release validator and preview review pass. No agent instruction authorizes publication by itself.
