# src/actions/explore_q.py
import json
import uuid
import streamlit as st

def explore_app() -> bool:


    chance = """{\n  \"accidentado\": [\n    {\n      \"id\": \"d2f1a3b7-4c6e-4f3a-9f7a-2e9b5c8a1d4e\",\n      \"prioridad\": \"Alta\",\n      \"pregunta\": \"\u00bfPuede describir con detalle c\u00f3mo ocurri\u00f3 el accidente?\",\n      \"objetivo\": \"Obtener una narraci\u00f3n directa del accidentado para entender las circunstancias del accidente.\"\n    },\n    {\n      \"id\": \"a7c9e2f4-5b1d-4e8f-9a3c-7d6f2b8e0c1a\",\n      \"prioridad\": \"Alta\",\n      \"pregunta\": \"\u00bfSinti\u00f3 alguna molestia o dolor antes de que la caja cayera sobre su pie?\",\n      \"objetivo\": \"Determinar si hubo alguna se\u00f1al previa que pudiera haber evitado el accidente.\"\n    },\n    {\n      \"id\": \"f3b8d7a1-9e2c-4f5b-8a7d-3c1e6b9f0d2a\",\n      \"prioridad\": \"Media\",\n      \"pregunta\": \"\u00bfEstaba utilizando el equipo de protecci\u00f3n personal adecuado en el momento del accidente?\",\n      \"objetivo\": \"Verificar el uso correcto de medidas de seguridad para evaluar su impacto en el accidente.\"\n    },\n    {\n      \"id\": \"c5e7a9d3-1f4b-4a6e-8d2c-9b0f3e7a5d1c\",\n      \"prioridad\": \"Media\",\n      \"pregunta\": \"\u00bfHab\u00eda alguna condici\u00f3n en el lugar que dificultara la reposici\u00f3n de las cajas, como espacio reducido o piso resbaladizo?\",\n      \"objetivo\": \"Identificar factores ambientales que pudieron contribuir al accidente.\"\n    },\n    {\n      \"id\": \"e9a1b4c7-3d6f-4e8a-9b2c-5f0d7e3a1b9c\",\n      \"prioridad\": \"Alta\",\n      \"pregunta\": \"\u00bfRecibi\u00f3 alguna instrucci\u00f3n o capacitaci\u00f3n espec\u00edfica para la tarea que estaba realizando?\",\n      \"objetivo\": \"Evaluar si la formaci\u00f3n recibida fue adecuada para prevenir el accidente.\"\n    }\n  ],\n  \"testigos\": [\n    {\n      \"id\": \"b4d2f6a9-7c3e-4f1a-8d5b-2e9c0f7a3b1d\",\n      \"prioridad\": \"Alta\",\n      \"pregunta\": \"\u00bfQu\u00e9 observ\u00f3 exactamente en el momento en que ocurri\u00f3 el accidente?\",\n      \"objetivo\": \"Recopilar una versi\u00f3n independiente de los hechos para contrastar con la del accidentado.\"\n    },\n    {\n      \"id\": \"f1a9c3d7-5b2e-4f6a-9d8c-0e7b1a4f3c6d\",\n      \"prioridad\": \"Alta\",\n      \"pregunta\": \"\u00bfHab\u00eda alguna condici\u00f3n en el \u00e1rea que pudiera haber contribuido al accidente, como desorden o falta de se\u00f1alizaci\u00f3n?\",\n      \"objetivo\": \"Identificar posibles riesgos en el entorno que hayan influido en el accidente.\"\n    },\n    {\n      \"id\": \"c7e4a1b9-3d5f-4a8c-9b0e-2f6d7a3c1b8e\",\n      \"prioridad\": \"Media\",\n      \"pregunta\": \"\u00bfEl accidentado estaba cumpliendo con los procedimientos de seguridad establecidos?\",\n      \"objetivo\": \"Verificar el cumplimiento de normas de seguridad durante la tarea.\"\n    },\n    {\n      \"id\": \"a3f9d2b7-6c1e-4f8a-9d5b-0e7c3a1f4b6d\",\n      \"prioridad\": \"Media\",\n      \"pregunta\": \"\u00bfAlguien m\u00e1s estaba realizando tareas similares en el \u00e1rea al momento del accidente?\",\n      \"objetivo\": \"Determinar si hubo factores adicionales o personas involucradas que puedan aportar informaci\u00f3n.\"\n    },\n    {\n      \"id\": \"d8b1c7e3-4f6a-9d2c-0e7b-3a1f5c9d8e2b\",\n      \"prioridad\": \"Baja\",\n      \"pregunta\": \"\u00bfSe tomaron medidas inmediatas para asistir al accidentado tras el incidente?\",\n      \"objetivo\": \"Evaluar la respuesta inicial ante el accidente para mejorar protocolos de emergencia.\"\n    }\n  ],\n  \"supervisores\": [\n    {\n      \"id\": \"e2c7a9b4-1f3d-4a6e-8d5b-9c0f7a3e1d2b\",\n      \"prioridad\": \"Alta\",\n      \"pregunta\": \"\u00bfSe realizaron inspecciones de seguridad recientes en el \u00e1rea donde ocurri\u00f3 el accidente?\",\n      \"objetivo\": \"Verificar el estado de mantenimiento y seguridad del lugar antes del accidente.\"\n    },\n    {\n      \"id\": \"b9d1f3a7-6c4e-4f8a-9d0b-2e7c1a5f3d6e\",\n      \"prioridad\": \"Alta\",\n      \"pregunta\": \"\u00bfEl personal recibi\u00f3 capacitaci\u00f3n adecuada para la tarea de reposici\u00f3n de productos?\",\n      \"objetivo\": \"Confirmar que el equipo est\u00e1 preparado para realizar sus funciones de manera segura.\"\n    },\n    {\n      \"id\": \"c4e8a1b9-3d5f-4a7c-9b0e-2f6d7a3c1b8f\",\n      \"prioridad\": \"Media\",\n      \"pregunta\": \"\u00bfExisten procedimientos escritos para la reposici\u00f3n de productos en las g\u00f3ndolas?\",\n      \"objetivo\": \"Determinar si hay protocolos formales que regulen la actividad realizada.\"\n    },\n    {\n      \"id\": \"a7f9d2b3-6c1e-4f8a-9d5b-0e7c3a1f4b6e\",\n      \"prioridad\": \"Media\",\n      \"pregunta\": \"\u00bfSe han reportado incidentes similares anteriormente en esta \u00e1rea?\",\n      \"objetivo\": \"Identificar patrones o riesgos recurrentes que requieran atenci\u00f3n.\"\n    },\n    {\n      \"id\": \"d8b1c7e3-4f6a-9d2c-0e7b-3a1f5c9d8e2c\",\n      \"prioridad\": \"Alta\",\n      \"pregunta\": \"\u00bfQu\u00e9 medidas correctivas se han implementado tras el accidente para evitar que se repita?\",\n      \"objetivo\": \"Evaluar la respuesta de la supervisi\u00f3n para mejorar la seguridad en el lugar de trabajo.\"\n    }\n  ],\n  \"documentos\": [\n    {\n      \"id\": \"f3a1b9c7-2d4e-4f6a-8d5b-9c0f7a3e1d2c\",\n      \"prioridad\": \"Alta\",\n      \"documento\": \"Informe de accidente laboral\",\n      \"objetivo\": \"Registrar oficialmente los detalles del accidente para an\u00e1lisis y seguimiento.\"\n    },\n    {\n      \"id\": \"b9d1f3a7-6c4e-4f8a-9d0b-2e7c1a5f3d6f\",\n      \"prioridad\": \"Alta\",\n      \"documento\": \"Registro de capacitaci\u00f3n del accidentado\",\n      \"objetivo\": \"Verificar la formaci\u00f3n recibida por el trabajador para la tarea realizada.\"\n    },\n    {\n      \"id\": \"c4e8a1b9-3d5f-4a7c-9b0e-2f6d7a3c1b90\",\n      \"prioridad\": \"Media\",\n      \"documento\": \"Procedimientos operativos est\u00e1ndar para reposici\u00f3n de productos\",\n      \"objetivo\": \"Revisar los protocolos establecidos para la actividad en la que ocurri\u00f3 el accidente.\"\n    },\n    {\n      \"id\": \"a7f9d2b3-6c1e-4f8a-9d5b-0e7c3a1f4b6f\",\n      \"prioridad\": \"Media\",\n      \"documento\": \"Fotograf\u00edas del lugar del accidente\",\n      \"objetivo\": \"Documentar visualmente las condiciones del \u00e1rea donde ocurri\u00f3 el incidente.\"\n    },\n    {\n      \"id\": \"d8b1c7e3-4f6a-9d2c-0e7b-3a1f5c9d8e2d\",\n      \"prioridad\": \"Alta\",\n      \"documento\": \"Reporte m\u00e9dico del accidentado\",\n      \"objetivo\": \"Obtener informaci\u00f3n sobre la lesi\u00f3n sufrida para evaluar su gravedad y tratamiento.\"\n    }\n  ]\n}"""
    """
    Punto de entrada para la seccion de edición de preguntas, respuestas y documentos.
    Si el session_state está vacío, precarga la estructura EXAMPLE_JSON.
    Retorna True si hay contenido presente (al menos un elemento en alguna lista).
    """

    # -------------------------------------------------------------------
    # 1) Inicializar listas vacías en session_state si no existen
    # -------------------------------------------------------------------
    st.session_state.setdefault("accidentado", [])
    st.session_state.setdefault("testigos", [])
    st.session_state.setdefault("supervisores", [])
    st.session_state.setdefault("explora_json_q", "")

    # -------------------------------------------------------------------
    # 2) Si aún no hay datos (todas las listas vacías), carga lo datos del JSON st.session_state.preguntas_json
    # -------------------------------------------------------------------
    todas_vacias = (
        len(st.session_state["accidentado"]) == 0 and
        len(st.session_state["testigos"]) == 0 and
        len(st.session_state["supervisores"]) == 0
    )
    if todas_vacias:
        try:
            json_preguntas = json.loads(chance)
            #json_preguntas = json.loads(st.session_state.preguntas_json)
            # Asignar cada arreglo al session_state
            st.session_state["accidentado"] = json_preguntas["accidentado"]
            st.session_state["testigos"] = json_preguntas["testigos"]
            st.session_state["supervisores"] = json_preguntas["supervisores"]
            # Guardar también el texto bruto por si luego desean volver a cargarlo
            st.session_state["explora_json_q"] = st.session_state.preguntas_json
        except Exception as e:
            st.error(f"Error al cargar JSON de json_preguntas: {e}")

    status = False

    # -------------------------------------------------------------------
    # 3) Función para generar un nuevo elemento con campos vacíos
    # -------------------------------------------------------------------
    def nueva_entrada(tipo: str):
        entry = {
            "id": str(uuid.uuid4()),
        }
        if tipo in ("accidentado", "testigos", "supervisores"):
            entry.update({
                "pregunta": "",
                "objetivo": "",
                "respuesta": ""
            })
        return entry

    # -------------------------------------------------------------------
    # 4) Renderizar y editar preguntas (accidentado/testigos/supervisores)
    # -------------------------------------------------------------------
    def renderizar_seccion_preguntas(seccion_nombre: str, etiqueta_display: str):
        st.subheader(etiqueta_display)
        lista = st.session_state[seccion_nombre]
        if not lista:
            st.info("No hay elementos. Usa el botón de abajo para agregar nuevas entradas.")
        for idx, item in enumerate(lista.copy()):

            with st.container(border=True):

                if not item.get('pregunta'):
                    nueva_pregunta = st.text_input(
                        "Pregunta",
                        value=item.get("pregunta", ""),
                        key=f"{seccion_nombre}_{item['id']}_pregunta"
                    )
                else:
                    nueva_pregunta = st.write(f"##### {item.get('pregunta')}")


                if not item.get('objetivo'):
                    nuevo_objetivo = st.text_area(
                        "Objetivo",
                        value=item.get("objetivo", ""),
                        key=f"{seccion_nombre}_{item['id']}_objetivo",
                        height=70
                    )
                else:
                    nuevo_objetivo = st.write(f"Objetivo: {item.get('objetivo')}")


                nueva_respuesta = st.text_area(
                    "Respuesta",
                    value=item.get("respuesta", ""),
                    key=f"{seccion_nombre}_{item['id']}_respuesta",
                    height=90
                )

                col1, col2, col3 = st.columns([1, 1 ,1])

                if col1.button(
                        "Eliminar",
                        key=f"del_{seccion_nombre}_{item['id']}",
                        use_container_width=True
                ):
                    # Defino la función del diálogo SIN key
                    @st.dialog("Confirme eliminar pregunta")
                    def dialogo_confirmar():
                        st.write("Si elimina la pregunta, esta no se podrá recuperar.")
                        col1, col2, col3 = st.columns([1, 1 ,1])
                        if col1.button("Eliminar", use_container_width=True):
                            st.session_state[seccion_nombre].pop(idx)
                            st.rerun()
                        if col3.button("Cancelar", type="primary", use_container_width=True):
                            st.rerun()

                    # Invoco la función para que aparezca el diálogo
                    dialogo_confirmar()

                if col3.button(f"Guardar", key=f"save_{seccion_nombre}_{item['id']}", use_container_width=True):
                    st.session_state[seccion_nombre][idx].update({
                        "pregunta": nueva_pregunta,
                        "objetivo": nuevo_objetivo,
                        "respuesta": nueva_respuesta
                    })
                    st.success("Cambios guardados.")

        if st.button(f"Añadir nueva pregunta", key=f"add_{seccion_nombre}", use_container_width=True):
            st.session_state[seccion_nombre].append(nueva_entrada(seccion_nombre))
            st.rerun()

    # -------------------------------------------------------------------
    # 5) Mostrar cada seccion en la página principal
    # -------------------------------------------------------------------
    st.markdown("")
    renderizar_seccion_preguntas("accidentado", "Preguntas guía al accidentado/a")
    st.markdown("---")
    renderizar_seccion_preguntas("testigos", "Preguntas guía a testigos/participantes")
    st.markdown("---")
    renderizar_seccion_preguntas("supervisores", "Preguntas guía a supervisores o jefaturas")

    # -------------------------------------------------------------------
    # 6) Desarrollar metodo de guardar base datos
    # -------------------------------------------------------------------


    # -------------------------------------------------------------------
    # 7) Establecer status=True si hay al menos un elemento en alguna lista
    # -------------------------------------------------------------------
    if any([
        st.session_state["accidentado"],
        st.session_state["testigos"],
        st.session_state["supervisores"],
    ]):
        status = True

    return status