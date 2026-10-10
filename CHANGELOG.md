# Changelog

All notable public changes to this resource are documented here.

## 2.3.0 — 2026-10-10

- Added 80 models, platforms and benchmarks across all ten categories, and
  promoted 7 previously held records whose conditions are now met, taking the
  displayed catalog to 486. Every addition and promotion passed a separate
  review agent instructed to refute it. Some additions are canonical older
  models the index lacked (e.g. GearNet, HIPT, CTransPath, AIMNet2, MACE-OFF).
- Re-reviewed all 44 held records: 7 promoted, 4 retired with documented
  reasons (xTrimoGene is now an alias of scFoundation), 33 kept with refreshed
  conditions. Moved Molexar to the register after its official code was
  withdrawn. 37 candidates remain under review.
- Opened a calibrated-uncertainty lane: added the MUBen benchmark and stated
  the confidence outputs of AlphaFold2, AlphaFold 3 and EVE where primary
  sources support it.
- Corrected 32 existing records for moved repositories and hub organisations,
  journal versions of preprints, access and licence wording, and archived
  upstream code. Fixed the UMA documentation link that had failed the weekly
  link audit since 2026-09-14.
- Added a separate `evidence_review_date` to the resource metadata.
- Recorded method, coverage limits and every decision in
  `evidence/DISCOVERY_AUDIT_2026-10-10.md` and `evidence/refresh-2026-10-10/`.

## 2.2.0 — 2026-09-11

- Added or promoted 11 models and benchmarks across RNA, DNA, protein,
  molecular and benchmark categories, taking the displayed catalog to 400.
  Re-reviewed all 39 previous HOLD conditions; 44 candidates remain held.
- Corrected GPN-MSA's publication and deprecation information and moved ALICE
  to a reversible HOLD after its official repository and model access failed.
  Preserved stable IDs, prior evidence and unchanged verification dates.
- Distinguished code, weights, datasets, gating and reuse terms, including
  RIBOSPAN's custom licence and separately licensed model archives.
- Enabled accurate dated evidence paths with file-existence validation,
  rebuilt all distributions deterministically and recorded the full source,
  link and independent review evidence for this refresh.

## 2.1.1 — 2026-08-14

- Added a visible version-and-date badge to the index header, generated from
  `resource_metadata.json`, so the most recent published update is legible at
  a glance and refreshes automatically with every release.
- No catalog records, evidence classifications, or data distributions changed.

## 2.1.0 — 2026-08-13

- Added 42 verified records across all ten modalities from a delegated discovery and verification refresh covering the mid-June to mid-August window plus older catalog gaps.
- Promoted ChemBERTa-3, the Virchow family, and the H-optimus family out of the under-review register after their recorded reconsideration conditions were met, encoding member-specific access and licence terms rather than one family-level flag.
- Re-reviewed every under-review candidate against primary sources, added ten new holds, refreshed fourteen hold reasons with materially new evidence, and grew the register to 39 entries.
- Removed the dead model-hub link from the scMulan record, completing the correction prescribed by the 2026-07-13 source audit.
- Made the link audit polite per host so burst-induced rate limiting cannot be misread as an availability finding, and fixed artifact upload in the continuous quality workflow.

No DOI is assigned to this release.

## 2.0.1 — 2026-07-14

- Increased the index's main reading text, explanatory details, and column headings for more comfortable use while preserving the compact research-table layout.
- Kept badges, filters, metadata, catalog records, and evidence classifications unchanged.

## 2.0.0 — 2026-07-14

- Refreshed the displayed foundation-model catalog through separate delegated review lanes with adversarial coordinator cross-checking.
- Moved unresolved or out-of-scope records to a non-displayed review register while preserving stable identifiers and decisions.
- Added schema-validated JSON, JSON-LD metadata, provenance, evidence dates, content and code licences, and release-level metadata.
- Added a reproducible agent-neutral maintenance protocol, deterministic builds, strict release validation, link auditing, and continuous quality checks.
- Redesigned the interactive index for clearer filtering, responsive use, and accessibility.

No DOI is assigned to this release.
