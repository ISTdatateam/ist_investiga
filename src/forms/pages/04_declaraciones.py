import streamlit as st
from src.forms.data_form import init_session_fields
import time
from src.forms.data_form import explore_q_app_wrapper
from src.forms.data_form import get_qm
import json

qm = get_qm()

def run():

    # Flags que usaremos
    st.session_state.setdefault("prerelato_form_guardado", False)

    st.header("Declaraciones")
    st.write("En este momento el asistente va a analizar la información disponible hasta el momento y te va a proponer preguntas guía para realizar en las entrevistas")

    if st.button("Evaluar antecedentes con IA y generar preguntas guía", use_container_width=True):
        # Construir prompt inicial estructurado
        if not st.session_state.get("initial_story"):
            # Convertir fechas/horas a strings serializables
            fecha_accidente = st.session_state.fecha_accidente.isoformat() if hasattr(
                st.session_state.fecha_accidente, 'isoformat') else str(st.session_state.fecha_accidente)
            hora_accidente = st.session_state.hora_accidente.isoformat() if hasattr(st.session_state.hora_accidente,
                                                                                    'isoformat') else str(
                st.session_state.hora_accidente)

            preinitial_data = {
                "datos_generales": {
                    "nombre_accidentado": st.session_state.nombre_trabajador,
                    "fecha": fecha_accidente,
                    "hora": hora_accidente,
                    "actividad": st.session_state.actividad,
                    "local": st.session_state.nombre_local,
                    "lugar_accidente": st.session_state.lugar_accidente,
                    "lesion": st.session_state.naturaleza_lesion
                },
                "operaciones": {
                    "tarea": st.session_state.tarea,
                    "operacion": st.session_state.operacion
                },
                "contexto": {
                    "general": st.session_state.contexto,
                    "circunstancias": st.session_state.circunstancias
                }
            }

            st.session_state.preinitial_story = json.dumps(preinitial_data, ensure_ascii=False, indent=2)

            prompt = (
                f"Antecedentes: {st.session_state.preinitial_story}\n"
            )

            st.write(prompt)


            # Generar relato inicial con manejo de modelo
            with st.spinner(f"Generando preguntas para proceso de investigación..."):
                st.session_state.preguntas_json = qm.generar_pregunta(
                    "explora",
                    prompt
                )
                st.write(st.session_state.preguntas_entrevista)
                print(st.session_state.preguntas_entrevista)

    status = explore_q_app_wrapper()

    # Llamada a la función de medidas correctivas
    #if st.session_state.preguntas_json:
    #    status = explore_app_wrapper()


    # Botón Siguiente
    if st.button('Guardar todas las declaraciones', use_container_width=True, type="primary"):
        st.success("Sección Declaraciones guardada")
        #st.session_state['_page'] = 5
        time.sleep(1)
        st.rerun()
