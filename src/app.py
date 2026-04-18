from enum import Enum

import streamlit

from src.ui import base_price_analysis, forex_pair_analysis


class Screen(Enum):
    BASE_PRICE_ANALYSIS = "base_price_analysis"
    FOREX_PAIR_ANALYSIS = "forex_pair_analysis"


def initialize_state():
    if "screen" not in streamlit.session_state:
        streamlit.session_state.screen = Screen.BASE_PRICE_ANALYSIS


def initialize_routing():
    if streamlit.session_state.screen == Screen.BASE_PRICE_ANALYSIS:
        base_price_analysis.render()
    elif streamlit.session_state.screen == Screen.FOREX_PAIR_ANALYSIS:
        forex_pair_analysis.render()


def render_dashboard():
    navbar = streamlit.columns(3)

    with navbar[0]:
        streamlit.image("assets/ForexAdvisory.png")

    with navbar[1]:
        if streamlit.button(
            "Base Price Analysis",
            type="primary"
            if streamlit.session_state.screen == Screen.BASE_PRICE_ANALYSIS
            else "secondary",
        ):
            streamlit.session_state.screen = Screen.BASE_PRICE_ANALYSIS
            streamlit.rerun()

    with navbar[2]:
        if streamlit.button(
            "Forex Pair Analysis",
            type="primary"
            if streamlit.session_state.screen == Screen.FOREX_PAIR_ANALYSIS
            else "secondary",
        ):
            streamlit.session_state.screen = Screen.FOREX_PAIR_ANALYSIS
            streamlit.rerun()

    streamlit.divider()


def run():
    initialize_state()
    render_dashboard()
    initialize_routing()
