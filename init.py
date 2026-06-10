import base64
from pathlib import Path

import streamlit

from src.ui import base_price_analysis, forex_pair_analysis


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

base_price_analysis_page = streamlit.Page(
    base_price_analysis.render,
    title="Base Price Analysis",
    url_path="base-price-analysis",
)

forex_pair_analysis_page = streamlit.Page(
    forex_pair_analysis.render,
    title="Forex Pair Analysis",
    url_path="forex-pair-analysis",
)

page = streamlit.navigation(
    [base_price_analysis_page, forex_pair_analysis_page], position="hidden"
)

column_logo, column_spacer, column_navigation_first, column_navigation_second = (
    streamlit.columns([2, 3, 1.5, 1.5])
)

with column_logo:
    render_svg("assets/ForexAdvisory.svg", 120)

with column_navigation_first:
    if streamlit.button(
        "Base Price Analysis",
        width="stretch",
        type="primary" if page == base_price_analysis_page else "secondary",
    ):
        streamlit.switch_page(base_price_analysis_page)

with column_navigation_second:
    if streamlit.button(
        "Forex Pair Analysis",
        width="stretch",
        type="primary" if page == forex_pair_analysis_page else "secondary",
    ):
        streamlit.switch_page(forex_pair_analysis_page)

streamlit.divider()

page.run()
