import streamlit as st
import streamlit.components.v1 as components
import datetime
import time

def run():
    with st.expander("Debug"):
        st.write(st.session_state)
    st.header("👷 Paso 2 – Datos Trabajador")

    st.session_state.nombre_trabajador = st.text_input(
        "👷 Nombre Completo*",
        st.session_state.get('nombre_trabajador', 'completar nombre'),
        help="Ej: Indica el nombre con dos apellidos"
    )
    st.session_state.rut_trabajador = st.text_input(
        "RUT Trabajador*",
        st.session_state.get('rut_trabajador', ''),
        help="Ej: Indica el rut del trabajador"
    )
    st.session_state.fecha_nacimiento = st.date_input(
        'Fecha de Nacimiento*',
        st.session_state.get('fecha_nacimiento', None)
    )
    st.session_state.edad = st.number_input(
        "Edad*",
        min_value=18,
        max_value=100,
        value=st.session_state.get('edad', None),
        help="Ej: Indica la edad del trabajador a la fecha del accidente"
    )
    st.session_state.nacionalidad = st.text_input(
        "Nacionalidad*",
        st.session_state.get('nacionalidad', ''),
        help="Ej: Indica la nacionalidad del trabajor"
    )

    #Propoblar el estado civil del trabajor
    options = ['Soltero/a', 'Casado/a', 'Viudo/a', 'Divorciado/a']
    prev = st.session_state.get('estado_civil', options[0])
    if prev in options:
        default_idx = options.index(prev)
    else:
        default_idx = 0

    st.session_state.estado_civil = st.selectbox(
        "Estado Civil*",
        options,
        index=default_idx,
        help="Ej: Indica el estado civil del trabajador"
    )

    # Propoblar el tipo contrato del trabajor
    opciones = ['Indefinido', 'Plazo Fijo', 'Honorarios']
    prev_value = st.session_state.get('contrato', opciones[0])
    if prev_value in opciones:
        default_ind = opciones.index(prev_value)
    else:
        default_ind = 0

    st.session_state.contrato = st.selectbox(
        'Tipo de Contrato*',
        opciones,
        index=default_ind,
        help="Ej: Indica el tipo de contrato del trabajador"
    )
    st.session_state.cargo_trabajador = st.text_input(
        "Cargo*",
        st.session_state.get('cargo_trabajador', ''),
        help="Ej: Indica el cargo del trabajor"
    )
    st.session_state.antiguedad_cargo = st.text_input(
        "Antigüedad en el cargo*",
        st.session_state.get('antiguedad_cargo', ''),
        help="Ej: Indica antigüedad en el cargo del trabajor"
    )
    st.session_state.domicilio = st.text_input(
        'Domicilio*',
        st.session_state.get('domicilio', ''),
        help="Ej: Indica el domicilio del trabajador"
    )
    # Botón que guarda y avanza
    if st.button("💾 Guardar y continuar", use_container_width=True):
        st.success("Sección Datos Trabajador guardada")
        st.session_state['_page'] = 3
        time.sleep(1)
        st.rerun()
