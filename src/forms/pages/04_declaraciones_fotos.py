import streamlit as st
from forms.data_form import init_session_fields


def run():
    # -- Sólo inicializar la primera vez --
    if not st.session_state.get("initialized_fields", False):
        init_session_fields()
        st.session_state["initialized_fields"] = True

    st.header("📝 Paso 4 – Declaraciones y Fotos")

    with st.form(key="form_declaraciones"):
        # Declaración del accidentado
        st.text_area(
            'Declaración Accidentado/a*',
            value=st.session_state.declaracion_accidentado,
            height=150,
            key='declaracion_accidentado'
        )
        st.divider()

        # Testigo 1
        st.write("**Testigo 1**")
        st.text_input(
            'Nombre Testigo 1*',
            value=st.session_state.decl1_nombre,
            key='decl1_nombre'
        )
        st.text_input(
            'Cargo Testigo 1*',
            value=st.session_state.decl1_cargo,
            key='decl1_cargo'
        )
        st.text_input(
            'RUT Testigo 1*',
            value=st.session_state.decl1_rut,
            key='decl1_rut'
        )
        st.text_area(
            'Texto Declaración 1*',
            value=st.session_state.decl1_texto,
            key='decl1_texto'
        )
        st.divider()

        # Testigo 2
        st.write("**Testigo 2**")
        st.text_input(
            'Nombre Testigo 2*',
            value=st.session_state.decl2_nombre,
            key='decl2_nombre'
        )
        st.text_input(
            'Cargo Testigo 2*',
            value=st.session_state.decl2_cargo,
            key='decl2_cargo'
        )
        st.text_input(
            'RUT Testigo 2*',
            value=st.session_state.decl2_rut,
            key='decl2_rut'
        )
        st.text_area(
            'Texto Declaración 2*',
            value=st.session_state.decl2_texto,
            key='decl2_texto'
        )

        # Fotos del accidente
        st.file_uploader(
            'Fotos del Lugar',
            type=['png', 'jpg', 'jpeg', 'pdf'],
            accept_multiple_files=True,
            key='fotos_accidente'
        )

        # Botón Siguiente
        if st.form_submit_button('Siguiente ▶'):
            st.session_state['_page'] = 5
            st.rerun()
