import streamlit as st

from src.ui import base_price_analysis, forex_pair_analysis

st.set_page_config(
    page_title="Forex Advisory",
    page_icon="📈",
    layout="wide",
)

page_base = st.Page(
    base_price_analysis.render,
    title="Base Price Analysis",
    url_path="base-price-analysis",
)
page_forex = st.Page(
    forex_pair_analysis.render,
    title="Forex Pair Analysis",
    url_path="forex-pair-analysis",
)

pg = st.navigation([page_base, page_forex], position="hidden")

col_logo, col_spacer, col_nav1, col_nav2 = st.columns([2, 3, 1.5, 1.5])

with col_logo:
    st.image("assets/ForexAdvisory.svg", width=120)

with col_nav1:
    if st.button(
        "Base Price Analysis",
        width="stretch",
        type="primary" if pg == page_base else "secondary",
    ):
        st.switch_page(page_base)

with col_nav2:
    if st.button(
        "Forex Pair Analysis",
        width="stretch",
        type="primary" if pg == page_forex else "secondary",
    ):
        st.switch_page(page_forex)

st.divider()

pg.run()
