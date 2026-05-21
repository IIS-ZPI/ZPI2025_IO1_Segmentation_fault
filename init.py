from enum import Enum

import streamlit

from src.ui import (
    base_price_analysis,
    forex_pair_analysis,
    home,
)

streamlit.set_page_config(
    page_title="Forex Advisory",
    page_icon="📈",
    layout="wide",
)


class Screen(Enum):
    HOME = "Home"
    BASE_PRICE_ANALYSIS = "Base Price Analysis"
    FOREX_PAIR_ANALYSIS = "Forex Pair Analysis"


def initialize_state():
    if "screen" not in streamlit.session_state:
        streamlit.session_state.screen = Screen.HOME


def render_dashboard():
    streamlit.image("assets/ForexAdvisory.svg", width=120)

    selected_screen = streamlit.segmented_control(
        "Navigation",
        [
            Screen.BASE_PRICE_ANALYSIS.value,
            Screen.FOREX_PAIR_ANALYSIS.value,
        ],
        default=None,
        selection_mode="single",
        label_visibility="collapsed",
    )

    if selected_screen is None:
        streamlit.session_state.screen = Screen.HOME
    elif selected_screen == Screen.BASE_PRICE_ANALYSIS.value:
        streamlit.session_state.screen = Screen.BASE_PRICE_ANALYSIS
    elif selected_screen == Screen.FOREX_PAIR_ANALYSIS.value:
        streamlit.session_state.screen = Screen.FOREX_PAIR_ANALYSIS

    streamlit.divider()


def render_screen():
    if streamlit.session_state.screen == Screen.HOME:
        home.render()
    elif streamlit.session_state.screen == Screen.BASE_PRICE_ANALYSIS:
        base_price_analysis.render()
    elif streamlit.session_state.screen == Screen.FOREX_PAIR_ANALYSIS:
        forex_pair_analysis.render()


def run():
    initialize_state()
    render_dashboard()
    render_screen()


if __name__ == "__main__":
    run()
