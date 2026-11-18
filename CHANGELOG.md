# Release history

## Unreleased

- `catalog-info.yaml` (commented) so that the EUROPESIP developer portal (Backstage) shows the theme in its catalog (#1).
  Metadata only: it is not part of the theme nor of the release archive.
- TechDocs for Backstage (#3): `mkdocs.yml` and a docs home page (`docs/index.md`, `docs/index.es.md`), so the
  EUROPESIP Internal Developer Portal shows the documentation of the theme. No change to the theme.

## 1.0.0 · 2026-11-08

- First release: page template (English and Spanish), stylesheet with the EUROPESIP colours and logo, theme module,
  profile and four layouts, written from scratch. `europesip-theme-1.0.0.tar.gz` (in the release) is the `theme/`
  folder, ready for the DXTheme resource of the HCL DX Script Application operator. Tested with HCL DX Compose CF239
  (DX behind Keycloak with OpenID Connect).
