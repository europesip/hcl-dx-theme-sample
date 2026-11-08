#!/usr/bin/env python3
"""Builds the theme folder (theme/) from src/: the templates of every language and the stylesheet with the logos
embedded. Run it after changing src/ and commit the result: theme/ is what is uploaded to DX.

    python3 tools/build.py
"""
import base64
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "src", ROOT / "theme"

TEXT = {
    "en": dict(header="Main header", home="Home", product="Portal", navigation="Main navigation", main="Main content",
               complementary="Complementary content",
               tagline="Sample theme for HCL DX, by EUROPESIP.", source="Source code of the theme",
               legal="Sample theme · MIT licence · HCL and HCL DX are trademarks of HCL Technologies. EUROPESIP is not affiliated with HCL."),
    "es": dict(header="Cabecera", home="Inicio", product="Portal", navigation="Navegación principal", main="Contenido principal",
               complementary="Contenido complementario",
               tagline="Tema de ejemplo para HCL DX, de EUROPESIP.", source="Código fuente del tema",
               legal="Tema de ejemplo · Licencia MIT · HCL y HCL DX son marcas de HCL Technologies. EUROPESIP no está afiliada a HCL."),
}


def data_uri(png: pathlib.Path) -> str:
    return "data:image/png;base64," + base64.b64encode(png.read_bytes()).decode()


def main() -> None:
    tpl = (SRC / "theme.template.html").read_text(encoding="utf-8")
    alternates = "".join(f'\n<link rel="alternate" href="nls/theme_{l}.html" hreflang="{l}">' for l in TEXT)
    # theme.html: English, and the links that make DX render the template of the language of the user
    (OUT / "theme.html").write_text(tpl.format(lang="en", alternates=alternates, **TEXT["en"]), encoding="utf-8-sig")  # DX needs the BOM to read UTF-8
    for lang, t in TEXT.items():
        (OUT / "nls" / f"theme_{lang}.html").write_text(tpl.format(lang=lang, alternates="", **t), encoding="utf-8-sig")

    css = (SRC / "europesip.css").read_text(encoding="utf-8").replace("@@LOGO_WHITE@@", data_uri(OUT / "images" / "europesip-white.png"))
    (OUT / "css" / "europesip.css").write_text(css, encoding="utf-8")

    # The theme module (scoped to this theme): our stylesheet, on top of the client framework modules of DX
    module = {"modules": [{"id": "europesip_theme",
                           "prereqs": [{"id": "wp_client_main"}, {"id": "wp_client_ext"}, {"id": "wp_custom_page_style"}, {"id": "wp_high_contrast"}],
                           "contributions": [{"type": "head", "sub-contributions": [{"type": "css", "uris": [{"value": "/css/europesip.css"}]}]}]}]}
    (OUT / "contributions" / "europesip.json").write_text(json.dumps(module, indent=2) + "\n", encoding="utf-8")

    # The profile: which modules every page of the theme loads (and which only when the page is edited)
    profile = {"moduleIDs": ["europesip_theme", "wp_dynamicContentSpots_85", "wp_toolbar_host_view", "wp_portlet_css", "wp_status_bar",
                             "wp_layout_windowstates", "wp_portal", "wp_analytics_aggregator", "wp_ic4_wai_resources", "wp_gridlayout"],
               "deferredModuleIDs": ["wp_toolbar_host_edit", "wcm_inplaceEdit", "wp_skin_cam", "wp_toolbar_gridlayout_inlineedit",
                                     "wp_contextmenu_live_object", "wp_analytics_tags", "wp_content_targeting_cam"],
               "titles": [{"value": "EUROPESIP", "lang": "en"}, {"value": "EUROPESIP", "lang": "es"}],
               "descriptions": [{"value": "Modules of the EUROPESIP sample theme", "lang": "en"},
                                {"value": "Módulos del tema de ejemplo de EUROPESIP", "lang": "es"}]}
    (OUT / "profiles" / "profile_europesip.json").write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Layouts: the hidden container first (required by DX), then the visible containers. ibmMainContainer is required.
    hidden = ('<div class="hiddenWidgetsDiv">\n'
              '\t<!-- applications in this container are hidden -->\n'
              '\t<div class="component-container hiddenWidgetsContainer ibmDndRow wpthemeCol12of12 wpthemeFull wpthemeRow" name="ibmHiddenWidgets"></div>\n'
              '</div>\n')
    col = '\t<div class="component-container wpthemeCol ibmDndColumn {w} {extra}" name="{name}"></div>\n'
    row = '\t<div class="component-container wpthemeRow ibmDndRow wpthemeCol12of12 wpthemeFull" name="{name}"></div>\n'
    layouts = {
        "1Column": ("One column", "Una columna", '<div class="wptheme1Col">\n' + col.format(w="wpthemeCol12of12 wpthemeFull", extra="wpthemePrimary", name="ibmMainContainer") + "</div>\n"),
        "2ColumnEqual": ("Two equal columns", "Dos columnas iguales", '<div class="wptheme2Col">\n'
                         + col.format(w="wpthemeCol6of12", extra="wpthemePrimary", name="ibmMainContainer")
                         + col.format(w="wpthemeCol6of12", extra="wpthemeSecondary", name="secondary") + "</div>\n"),
        "3ColumnEqual": ("Three equal columns", "Tres columnas iguales", '<div class="wptheme3Col">\n'
                         + col.format(w="wpthemeCol4of12", extra="wpthemePrimary", name="ibmMainContainer")
                         + col.format(w="wpthemeCol4of12", extra="wpthemeSecondary", name="secondary")
                         + col.format(w="wpthemeCol4of12", extra="wpthemeTertiary", name="tertiary") + "</div>\n"),
        "TopColumn2ColumnUnequal": ("A row on top, then two columns (2/3 + 1/3)", "Una fila arriba y dos columnas (2/3 + 1/3)", '<div class="wptheme2Col">\n'
                                    + row.format(name="headline")
                                    + col.format(w="wpthemeCol8of12", extra="wpthemePrimary", name="ibmMainContainer")
                                    + col.format(w="wpthemeCol4of12", extra="wpthemeSecondary", name="secondary") + "</div>\n"),
    }
    for name, (en, es, body) in layouts.items():
        d = OUT / "layout-templates" / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "layout.html").write_text(f"<!-- {en} · {es} -->\n" + hidden + body, encoding="utf-8")
    print("theme/ built:", sum(1 for p in OUT.rglob("*") if p.is_file()), "files")


if __name__ == "__main__":
    main()
