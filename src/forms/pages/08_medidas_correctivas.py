import streamlit as st
from forms.data_form import medidas_app_wrapper


def run():
    # Inicializa session_state si es primera ejecución
    # Asegúrate de que la clave edited_measures siempre exista
    if 'edited_measures' not in st.session_state:
        st.session_state['edited_measures'] = []  # o {} según lo que uses


    st.header("🛠️ Paso 8 – Medidas Correctivas")

    # Llamada a la función de medidas correctivas
    medidas_app_wrapper()

    # Mostrar medidas editadas si existen
    #if 'edited_measures' in st.session_state:
    #    st.json(st.session_state.edited_measures)

    # Botón Siguiente para pasar a Generar Informe
    if st.button('Siguiente ▶'):
        st.session_state['_page'] = 9
        st.rerun()
