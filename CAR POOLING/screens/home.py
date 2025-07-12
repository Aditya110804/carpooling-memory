import streamlit as st

def show():
    st.markdown("<h1 style='text-align: center;'>🚗 Smart Ride Pooling</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-size:20px;'>Welcome! Pool your ride smartly and safely.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register", use_container_width=True):
            st.session_state.page = "register_user"
    with col2:
        if st.button("Login", use_container_width=True):
            st.session_state.page = "login"