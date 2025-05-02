import streamlit as st
from forms.data_form import init_session_fields
import streamlit.components.v1 as components

def run():
    # -- Sólo inicializar la primera vez --
    if not st.session_state.get("initialized_fields", False):
        init_session_fields()
        st.session_state["initialized_fields"] = True

    st.header("👷 Paso 2 – Datos Trabajador")

    # Cada input escribe automáticamente en st.session_state['<key>']
    nombre = st.text_input(
        '👷 Nombre Completo*',
        value=st.session_state.get('nombre_trabajador', ''),
        key='nombre_trabajador',
    )
    rut = st.text_input(
        'RUT Trabajador*',
        value=st.session_state.get('rut_trabajador', ''),
        key='rut_trabajador',
    )
    fecha = st.date_input(
        'Fecha de Nacimiento*',
        value=st.session_state.get('fecha_nacimiento', None),
        key='fecha_nacimiento',
    )
    edad = st.number_input(
        'Edad*',
        min_value=18,
        max_value=100,
        value=st.session_state.get('edad', 18),
        key='edad',
    )
    nac = st.text_input(
        'Nacionalidad*',
        value=st.session_state.get('nacionalidad', ''),
        key='nacionalidad',
    )
    ec = st.selectbox(
            'Estado Civil*',
            ['Soltero/a', 'Casado/a', 'Viudo/a', 'Divorciado/a'],
            key='estado_civil'
        )
    contrato = st.selectbox(
        'Tipo de Contrato*',
        ['Indefinido', 'Plazo Fijo', 'Honorarios'],
        key='contrato'
    )
    cargo = st.text_input(
        'Cargo*',
        value=st.session_state.get('cargo_trabajador', ''),
        key='cargo_trabajador'
    )
    antig = st.text_input(
        'Antigüedad en el Cargo*',
        value=st.session_state.get('antiguedad_cargo', ''),
        key='antiguedad_cargo'
    )
    dom = st.text_input(
        'Domicilio*',
        value=st.session_state.get('domicilio', ''),
        key='domicilio'
    )

    # Botón que guarda y avanza
    if st.button("💾 Guardar y continuar", use_container_width=True):
        # Opcional: mostrar mensaje de éxito
        st.success("Sección Datos Trabajador guardada")
        # Avanzar al siguiente paso
        st.session_state['_page'] = 3
        st.rerun()
