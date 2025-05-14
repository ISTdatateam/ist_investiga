import streamlit as st
import streamlit.components.v1 as components
import time

def run():

    st.header("👷 Paso 2 – Datos Trabajador")

    # Cada input escribe automáticamente en st.session_state['<key>']
    st.write(st.session_state)

    st.session_state.nombre_trabajador = st.text_input(
        "👷 Nombre Completo*",
        st.session_state.get('nombre_trabajador', 'completar nombre'),
        help="Ej: Indica el nombre con dos apellidos"
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
        st.success("Sección Datos Trabajador guardada")
        st.session_state['_page'] = 3
        time.sleep(1)
        st.rerun()
