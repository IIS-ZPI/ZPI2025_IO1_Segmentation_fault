import base64
from pathlib import Path

import streamlit

from src.ui import base_price_analysis, forex_pair_analysis, i18n


def render_svg(path: str, width: int) -> None:
    svg_data = base64.b64encode(Path(path).read_bytes()).decode()
    streamlit.markdown(
        f'<img src="data:image/svg+xml;base64,{svg_data}" width="{width}" draggable="false">',
        unsafe_allow_html=True,
    )


streamlit.set_page_config(
    page_title="Forex Advisory",
    page_icon="📈",
    layout="wide",
)

if "language" not in streamlit.session_state:
    streamlit.session_state["language"] = i18n.DEFAULT_LANGUAGE


def on_language_change() -> None:
    streamlit.session_state["language"] = i18n.LANGUAGES[
        streamlit.session_state["language_name"]
    ]

base_price_analysis_page = streamlit.Page(
    base_price_analysis.render,
    title=i18n.translate("base_price_analysis"),
    url_path="base-price-analysis",
)

forex_pair_analysis_page = streamlit.Page(
    forex_pair_analysis.render,
    title=i18n.translate("forex_pair_analysis"),
    url_path="forex-pair-analysis",
)

page = streamlit.navigation(
    [base_price_analysis_page, forex_pair_analysis_page], position="hidden"
)

(
    column_logo,
    column_spacer,
    column_language,
    column_navigation_first,
    column_navigation_second,
) = streamlit.columns([2, 2, 1.2, 1.5, 1.5])

with column_logo:
    render_svg("assets/ForexAdvisory.svg", 120)

with column_language:
    language_names = list(i18n.LANGUAGES.keys())
    name_for_code = {code: name for name, code in i18n.LANGUAGES.items()}
    current_language_name = name_for_code[streamlit.session_state["language"]]
    streamlit.selectbox(
        i18n.translate("language"),
        language_names,
        index=language_names.index(current_language_name),
        key="language_name",
        on_change=on_language_change,
    )

with column_navigation_first:
    if streamlit.button(
        i18n.translate("base_price_analysis"),
        width="stretch",
        type="primary" if page == base_price_analysis_page else "secondary",
    ):
        streamlit.switch_page(base_price_analysis_page)

with column_navigation_second:
    if streamlit.button(
        i18n.translate("forex_pair_analysis"),
        width="stretch",
        type="primary" if page == forex_pair_analysis_page else "secondary",
    ):
        streamlit.switch_page(forex_pair_analysis_page)

streamlit.divider()

page.run()
