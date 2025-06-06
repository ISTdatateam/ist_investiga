import streamlit as st
from src.forms.data_form import init_session_fields
import time
from src.forms.data_form import explore_app_wrapper
from src.forms.data_form import get_qm
import json

def run():

    st.header("Declaraciones y entrevistas")
    st.write("Aquí puedes cargar el texto de las declaraciones y entrevistas para que sea parte del análisis")

    st.divider()
    # Declaración del accidentado
    st.write("**Accidentado/a**")
    st.session_state.declaracion_accidentado = st.text_area(
        "Declaración Accidentado/a*",
        st.session_state.get('declaracion_accidentado', ''),
        height=150
    )
    st.divider()

    # Testigo 1
    st.write("**Testigo 1**")
    st.session_state.decl1_nombre = st.text_input(
        "Nombre Testigo 1*",
        st.session_state.get('decl1_nombre', ''),
        help="Ej: Indica el nombre con dos apellidos"
    )
    st.session_state.decl1_cargo = st.text_input(
        "Cargo Testigo 1*",
        st.session_state.get('decl1_cargo', ''),
        help="Ej: Indica el cargo del testigo"
    )
    st.session_state.decl1_rut = st.text_input(
        "RUT Testigo 1*",
        st.session_state.get('decl1_rut', ''),
        help="Ej: Indica el rut del testigo"
    )
    st.session_state.decl1_texto = st.text_area(
        "Texto Declaración 1*",
        st.session_state.get('decl1_texto', ''),
    )

    st.divider()

    # Testigo 2
    st.write("**Testigo 2**")
    st.session_state.decl2_nombre = st.text_input(
        "Nombre Testigo 2*",
        st.session_state.get('decl2_nombre', ''),
        help="Ej: Indica el nombre con dos apellidos"
    )
    st.session_state.decl2_cargo = st.text_input(
        "Cargo Testigo 2*",
        st.session_state.get('decl2_cargo', ''),
        help="Ej: Indica el cargo del testigo"
    )
    st.session_state.decl2_rut = st.text_input(
        "RUT Testigo 2*",
        st.session_state.get('decl2_rut', ''),
        help="Ej: Indica el rut del testigo"
    )
    st.session_state.decl2_texto = st.text_area(
        "Texto Declaración 2*",
        st.session_state.get('decl2_texto', ''),
    )

    if status:
        st.success("Se generaron las medidas correctamente.")

    if st.button("Guardar medidas correctivas", disabled=not status, use_container_width=True):
        st.success("Se guardaron las medidas correctamente.")

    # Botón Siguiente
    if st.button('Guardar declaraciones', use_container_width=True):
        st.success("Sección Declaraciones guardada")
        #st.session_state['_page'] = 5
        time.sleep(1)
        st.rerun()
