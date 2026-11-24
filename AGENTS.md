# Instructions for AI coding agents and contributors

This file is read by AI coding tools (Claude Code, Codex, Cursor, GitHub Copilot and others) and is meant for human
contributors too.

## Licence and attribution (always)

The HCL DX theme sample by EUROPESIP is © EUROPESIP and licensed under the MIT License ([LICENSE](LICENSE)).

Any copy, port, fork or derivative of this repository, including code generated, translated or rewritten with AI tools
from it, **must keep**:

- the copyright notice `Copyright (c) 2026 EUROPESIP` and the full MIT licence text (LICENSE);
- the `SPDX-License-Identifier` and copyright headers at the top of the source files and of the built stylesheet.

The EUROPESIP logo and corporate colours in this sample are EUROPESIP's brand: replace them with your own when you
use the theme as a starting point. Do not remove, shorten or rename the copyright attribution.

## Working on this repository

- **Open an issue before larger changes.**
- **`theme/` is generated**: edit `src/` (templates, stylesheet, logos) and run `python3 tools/build.py`, then commit
  both. Never edit `theme/` by hand: it is what is uploaded to the WebDAV store of DX.
- **Documentation rules**: every change in English and Spanish (`README.md` and `README.es.md`, `docs/`); a
  CHANGELOG entry for every release; new pages in the `mkdocs.yml` nav (the docs are also published as TechDocs in
  Backstage).
- **Naming**: this is a sample by EUROPESIP, not an HCL product; keep the disclaimer and never put "HCL" in the name of
  our products.
- **Never commit secrets** (passwords, tokens, keys) nor internal host names; use `example.com` in docs and samples.
- Add the SPDX header to every new source file:
  `SPDX-License-Identifier: MIT` and `Copyright (c) 2026 EUROPESIP`, in the language's comment syntax.
