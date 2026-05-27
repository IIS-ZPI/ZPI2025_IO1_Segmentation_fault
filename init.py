from enum import Enum

import streamlit

from src.ui import (
    base_price_analysis,
    forex_pair_analysis,
)

streamlit.set_page_config(
    page_title="Forex Advisory",
    page_icon="📈",
    layout="wide",
)


class Screen(Enum):
    BASE_PRICE_ANALYSIS = "Base Price Analysis"
    FOREX_PAIR_ANALYSIS = "Forex Pair Analysis"


def initialize_state():
    if "screen" not in streamlit.session_state:
        streamlit.session_state.screen = Screen.BASE_PRICE_ANALYSIS


def render_dashboard():
    streamlit.image("assets/ForexAdvisory.svg", width=120)

    col1, col2 = streamlit.columns(2)

    with col1:
        if streamlit.button("Base Price Analysis", use_container_width=True):
            streamlit.session_state.screen = Screen.BASE_PRICE_ANALYSIS

    with col2:
        if streamlit.button("Forex Pair Analysis", use_container_width=True):
            streamlit.session_state.screen = Screen.FOREX_PAIR_ANALYSIS

    streamlit.divider()


def render_screen():
    if streamlit.session_state.screen == Screen.BASE_PRICE_ANALYSIS:
        base_price_analysis.render()
    elif streamlit.session_state.screen == Screen.FOREX_PAIR_ANALYSIS:
        forex_pair_analysis.render()


def run():
    initialize_state()
    render_dashboard()
    render_screen()


if __name__ == "__main__":
    run()
