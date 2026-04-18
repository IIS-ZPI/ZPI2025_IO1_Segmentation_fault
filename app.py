import streamlit as st

from screens import base_price_analysis, forex_pair_analysis

if "page" not in st.session_state:
    st.session_state.page = "base_price_analysis"

col1, col2 = st.columns(2)

with col1:
    if st.button("Base Price Analysis"):
        st.session_state.page = "base_price_analysis"

with col2:
    if st.button("Forex Pair Analysis"):
        st.session_state.page = "forex_pair_analysis"

st.divider()

if st.session_state.page == "base_price_analysis":
    base_price_analysis.show()

elif st.session_state.page == "forex_pair_analysis":
    forex_pair_analysis.show()
