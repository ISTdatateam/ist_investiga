import streamlit as st
from datetime import date, datetime
import time

def run():
    st.write(st.session_state)
    st.header("⚠️ Paso 3 – Detalle Accidente")

    st.session_state.fecha_accidente = st.date_input(
        '⚠️ Fecha del Accidente*',
        st.session_state.get('fecha_accidente', None)
    )
    st.session_state.hora_accidente = st.time_input(
        'Hora del Accidente*',
        st.session_state.get('hora_accidente', None)
    )
    st.session_state.lugar_accidente = st.text_input(
        "Lugar del Accidente*",
        st.session_state.get('lugar_accidente', ''),
        help="Ej: Indica el lugar donde ocurrió el accidente"
    )

    # Prepoblar el tipo de accidente
    opciones = ['Golpeado por', 'Atrapado en', 'Caída', 'Contacto eléctrico', 'Otro']
    prev_value = st.session_state.get('tipo_accidente', opciones[0])
    if prev_value in opciones:
        default_ind = opciones.index(prev_value)
    else:
        default_ind = 0

    st.session_state.tipo_accidente = st.selectbox(
        'Tipo de Accidente*',
        opciones,
        index=default_ind,
        help="Ej: Indica el tipo de accidente"
    )
    st.session_state.naturaleza_lesion = st.text_input(
        "Naturaleza de la Lesión*",
        st.session_state.get('naturaleza_lesion', ''),
        help="Ej: Indica el tipo de lesión asociada al accidente"
    )
    st.session_state.parte_afectada = st.text_input(
        "Parte afectada*",
        st.session_state.get('parte_afectada', ''),
        help="Ej: Indica la parte del cuerpo afectada por el accidente"
    )
    st.session_state.tarea = st.text_input(
        "Tarea efectuada*",
        st.session_state.get('tarea', ''),
        help="Ej: Tarea efectuada por el trabajador en el momento del accidente"
    )
    st.session_state.operacion = st.text_input(
        "Operación*",
        st.session_state.get('operacion', ''),
        help="Ej: agregar hint a partir de LCarrera"
    )

    # Daños a Personas
    st.session_state.daños_personas = st.radio(
        'Daños a Personas*',
        ['SI', 'NO'],
        index=0 if st.session_state.get('daños_personas') == 'SI' else 1,
        horizontal=True
    )
    # Daños a Propiedad
    st.session_state.daños_propiedad = st.radio(
        'Daños a Propiedad*',
        ['SI', 'NO'],
        index=0 if st.session_state.get('daños_propiedad') == 'SI' else 1,
        horizontal=True
    )
    # Pérdidas en Proceso
    st.session_state.perdidas_proceso = st.radio(
        'Pérdidas en Proceso*',
        ['SI', 'NO'],
        index=0 if st.session_state.get('perdidas_proceso') == 'SI' else 1,
        horizontal=True
    )
    if st.button("💾 Guardar y continuar", use_container_width=True):
        st.success("⚠️ Paso 3 – Detalle Accidente guardado")
        st.session_state['_page'] = 4
        time.sleep(1)
        st.rerun()
