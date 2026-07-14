import streamlit as st
import time

st.set_page_config(layout="centered")

if 'estado' not in st.session_state:
    st.session_state.estado = 'inicio'

def iniciar():
    st.session_state.estado = 'memo'

main_container = st.empty()

with main_container.container():
    if st.session_state.estado == 'inicio':
        st.write("Inicio")
        st.button("Iniciar", on_click=iniciar)

    elif st.session_state.estado == 'memo':
        st.write("Memoriza: 12345")
        time.sleep(2)
        st.session_state.estado = 'input'
        st.rerun()

    elif st.session_state.estado == 'input':
        st.write("Input")
        st.text_input("Ingresa")
