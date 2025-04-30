import streamlit as st
from forms.data_form import init_session_fields


def run():
    # Inicializa session_state si es primera ejecución
    init_session_fields()
    st.header("👷 Paso 2 – Datos Trabajador")

    # Formulario de datos del trabajador
    with st.form(key="form_trabajador"):
        # Entrada de datos sin valor explícito para permitir la persistencia automática
        st.text_input('👷 Nombre Completo*', key='nombre_trabajador')
        st.text_input('RUT Trabajador*', key='rut_trabajador')
        st.date_input('Fecha de Nacimiento*', key='fecha_nacimiento')
        st.number_input('Edad*', min_value=18, max_value=100, key='edad')
        st.text_input('Nacionalidad*', key='nacionalidad')
        st.selectbox(
            'Estado Civil*',
            ['Soltero/a', 'Casado/a', 'Viudo/a', 'Divorciado/a'],
            key='estado_civil'
        )
        st.selectbox(
            'Tipo de Contrato*',
            ['Indefinido', 'Plazo Fijo', 'Honorarios'],
            key='contrato'
        )
        st.text_input('Cargo*', key='cargo_trabajador')
        st.text_input('Antigüedad en el Cargo*', key='antiguedad_cargo')
        st.text_input('Domicilio*', key='domicilio')

        # Botón de envío
        if st.form_submit_button('Siguiente ▶'):
            st.session_state['_page'] = 3
            st.rerun()
