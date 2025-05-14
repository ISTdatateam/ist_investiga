import streamlit as st
from datetime import date, datetime


def run():

    st.header("⚠️ Paso 3 – Detalle Accidente")

    st.write(st.session_state)

    # Formulario de detalle de accidente
    with st.form(key="form_accidente"):
        # Fecha
        st.date_input(
            '⚠️ Fecha del Accidente*',
            key='fecha_accidente'
        )

        # Hora
        st.time_input(
            'Hora del Accidente*',
            key='hora_accidente'
        )

        # Lugar
        st.text_input(
            'Lugar del Accidente*',
            value=st.session_state.get('lugar_accidente', 'Ej: Bodega zona 3'),
            key='lugar_accidente'
        )

        # Tipo de Accidente
        tipos = ['Golpeado por', 'Atrapado en', 'Caída', 'Contacto eléctrico', 'Otro']
        default_tipo = tipos.index(st.session_state.get('tipo_accidente')) if st.session_state.get('tipo_accidente') in tipos else 0
        st.selectbox(
            'Tipo de Accidente*',
            tipos,
            index=default_tipo,
            key='tipo_accidente'
        )

        # Naturaleza de la Lesión
        st.text_input(
            'Naturaleza de la Lesión*',
            value=st.session_state.get('naturaleza_lesion', ''),
            key='naturaleza_lesion'
        )

        # Parte Afectada
        st.text_input(
            'Parte Afectada*',
            value=st.session_state.get('parte_afectada', ''),
            key='parte_afectada'
        )

        # Tarea
        st.text_input(
            'Tarea*',
            value=st.session_state.get('tarea', ''),
            key='tarea'
        )

        # Operación
        st.text_input(
            'Operación*',
            value=st.session_state.get('operacion', ''),
            key='operacion'
        )

        # Daños a Personas
        st.radio(
            'Daños a Personas*',
            ['SI', 'NO'],
            index=0 if st.session_state.get('daños_personas') == 'SI' else 1,
            key='daños_personas',
            horizontal=True
        )

        # Daños a Propiedad
        st.radio(
            'Daños a Propiedad*',
            ['SI', 'NO'],
            index=0 if st.session_state.get('daños_propiedad') == 'SI' else 1,
            key='daños_propiedad',
            horizontal=True
        )

        # Pérdidas en Proceso
        st.radio(
            'Pérdidas en Proceso*',
            ['SI', 'NO'],
            index=0 if st.session_state.get('perdidas_proceso') == 'SI' else 1,
            key='perdidas_proceso',
            horizontal=True
        )

        # Botón de envío
        if st.form_submit_button('Siguiente ▶'):
            st.session_state['_page'] = 4
            st.rerun()
