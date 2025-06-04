import streamlit as st
from datetime import date, datetime
import time
import json
from pathlib import Path
from src.db import insert_accidente          # NUEVO import


# Configuración de directorios
CONFIG_DIR = Path(__file__).parent.parent / "config"

def run():

    @st.cache_data
    def cargar_tipos():
        with open(CONFIG_DIR/'tipos_accidente.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    tipos_data = cargar_tipos()

    st.header("Datos Accidente")

    st.session_state.fecha_accidente = st.date_input(
        'Fecha del Accidente*',
        st.session_state.get('fecha_accidente', None),
        max_value = date.today(),
        format = "DD/MM/YYYY"
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

    # Tipo de accidente
    tipos = [item['tipo'] for item in tipos_data]
    descripciones = {item['tipo']: item['descripcion'] for item in tipos_data}
    prev = st.session_state.get('tipo_accidente', tipos[0])
    default_index = tipos.index(prev) if prev in tipos else 0
    st.session_state.tipo_accidente = st.selectbox(
        'Tipo de Accidente*',
        tipos,
        index=default_index,
        help="Selecciona el tipo de accidente"
    )
    seleccion = st.session_state.tipo_accidente
    st.write(descripciones.get(seleccion, "Sin descripción disponible."))

    st.session_state.naturaleza_lesion = st.text_input(
        "Describa la lesión*",
        st.session_state.get('naturaleza_lesion', ''),
        help="Indicar la lesión en términos de sus características principales por ejemplo (Contusión, Golpe, Herida). Cuando se presenten lesiones múltiples, se sugiere indicar la más severa. En caso de haber lesiones de igual magnitud, se sugiere señalarlas como lesiones múltiples."
    )
    st.session_state.parte_afectada = st.text_input(
        "Parte afectada*",
        st.session_state.get('parte_afectada', ''),
        help="Se clasifica la parte del cuerpo que resultó directamente afectada por la lesión. Cuando la lesión afecta varias partes o diferentes miembros principales del cuerpo, debe utilizarse la categoría “partes múltiples”. Ejemplos: Mano, dedos, pie, tronco, cabeza."
    )
    st.session_state.tarea = st.text_input(
        "Tarea que se ejecutaba*",
        st.session_state.get('tarea', ''),
        help="Es la actividad laboral desarrollada por el accidentado al momento de ocurrencia del accidente, por ejemplo: soldar, tejer, transportar carga, escribir, almacenar, reparar, etc."
    )
    st.session_state.operacion = st.text_input(
        "Operación específica*",
        st.session_state.get('operacion', ''),
        help="Corresponde a la acción que se realizaba justo al momento del accidente"
    )

    # Daños a Personas
    st.session_state.daños_personas = st.radio(
        'Daños a Personas*',
        ['SI', 'NO'],
        index=0 if st.session_state.get('daños_personas') == 'SI' else 1,
        horizontal=True,
        help="Especificar si se produjo daño a las personas."
    )
    # Daños a Propiedad
    st.session_state.daños_propiedad = st.radio(
        'Daños a Propiedad*',
        ['SI', 'NO'],
        index=0 if st.session_state.get('daños_propiedad') == 'SI' else 1,
        horizontal=True,
        help = ": Especificar si es que se produce daño a las instalaciones, equipos, materiales."
    )
    # Pérdidas en Proceso
    st.session_state.perdidas_proceso = st.radio(
        'Pérdidas en Proceso*',
        ['SI', 'NO'],
        index=0 if st.session_state.get('perdidas_proceso') == 'SI' else 1,
        horizontal=True,
        help = ": Especificar si se produjo paralización del proceso productivo."

    )
    st.session_state.contexto = st.text_area(
        "Tarea que se realizaba (Detalle del proceso habitual)",
        key="contexto_input",  # clave temporal
        value=st.session_state.contexto,
        height=200
    )
    st.session_state.circunstancias = st.text_area(
        "Circunstancias del accidente (Situación específica del accidente)",
        key="circunstancias_input",  # clave temporal
        value=st.session_state.circunstancias,
        height=200
    )

    if st.button("Guardar accidente", use_container_width=True):
        missing = [k for k in ("centro_id", "trabajador_id") if k not in st.session_state]
        if missing:
            st.error("Falta definir Empresa/Centro o Trabajador antes de registrar el accidente.")
            st.stop()

        accidente_id = insert_accidente(
            centro_id=st.session_state.centro_id,
            trabajador_id=st.session_state.trabajador_id,
            fecha_accidente=st.session_state.fecha_accidente.isoformat(),
            hora_accidente=st.session_state.hora_accidente.strftime("%H:%M:%S"),
            lugar_accidente=st.session_state.lugar_accidente.strip(),
            tipo_accidente=st.session_state.tipo_accidente,
            naturaleza_lesion=st.session_state.naturaleza_lesion,
            parte_afectada=st.session_state.parte_afectada,
            tarea=st.session_state.tarea.strip(),
            operacion=st.session_state.operacion.strip(),
            # ----- snapshot trabajador  -----
            cargo_trabajador=st.session_state.cargo_trabajador,
            contrato=st.session_state.contrato,
            antiguedad_empresa=st.session_state.antiguedad_empresa,
            antiguedad_cargo=st.session_state.antiguedad_cargo,
            # ----- consecuencias -------------
            danos_personas=st.session_state.daños_personas,
            danos_propiedad=st.session_state.daños_propiedad,
            perdidas_proceso=st.session_state.perdidas_proceso,
            # Resumen / relato quedan en blanco por ahora
            contexto=st.session_state.contexto,
            circunstancias=st.session_state.circunstancias,
            preinitial_story=st.session_state.preinitial_story,
            preguntas_entrevista=st.session_state.preguntas_entrevista,
            resumen=None,
            relato=None,
        )

        st.session_state.accidente_id = accidente_id
        st.success("Accidente guardado correctamente")
        time.sleep(1)
        st.rerun()
