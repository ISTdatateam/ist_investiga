import streamlit as st
from src.forms.data_form import medidas_app_wrapper

def run():
    # Asegúrate de que la clave edited_measures siempre exista
    if 'edited_measures' not in st.session_state:
        st.session_state['edited_measures'] = []  # o {} según lo que uses

    st.header("🛠️ Paso 8 – Medidas Correctivas")

    with st.expander("Debug"):
        st.write(st.session_state)

    # Llamada a la función de medidas correctivas
    medidas_app_wrapper()

    # Botón Siguiente para pasar a Generar Informe
    if st.button('Siguiente ▶'):
        st.rerun()
