#05_relato_ia.py
import streamlit as st
from src.forms.data_form import init_session_fields, get_qm
from src.ia.questions import InvestigationApp


def run():

    with st.expander("Debug"):
        st.write(st.session_state)

    # Flags que usaremos
    st.session_state.setdefault("relato_form_guardado", False)
    st.session_state.setdefault("relatof", "")
    st.session_state.setdefault("contexto", "")
    st.session_state.setdefault("circunstancias", "")

    st.header("🧠 Paso 5 – Construcción del relato")

    qm = get_qm()

    # 2️⃣  Mostrar el formulario para CONTEXTO y CIRCUNSTANCIAS
    with st.form("form_relato"):
        contexto_input = st.text_area(
            "Contexto",
            key="contexto_input",  # clave temporal
            value=st.session_state.contexto,
            height=150
        )
        circunstancias_input = st.text_area(
            "Circunstancias",
            key="circunstancias_input",  # clave temporal
            value=st.session_state.circunstancias,
            height=150
        )

        guardar = st.form_submit_button("💾 Guardar datos")

    # 3️⃣  Acciones tras GUARDAR
    if guardar:
        st.session_state.contexto = contexto_input
        st.session_state.circunstancias = circunstancias_input
        st.session_state.relato_form_guardado = True
        st.success("✅ Datos guardados. Ahora puedes generar el relato con IA.")

    # 4️⃣  Botón externo = Ejecutar IA (solo habilitado si el form está guardado)
    btn_disabled = not st.session_state.relato_form_guardado
    if st.button("🧠 Ejecutar IA", disabled=btn_disabled):
        # Construir prompt inicial (solo una vez)
        if not st.session_state.get("initial_story"):
            st.session_state.initial_story = "\n".join([
                f"Datos generales del accidente",
                f"Nombre accidentado: {st.session_state.nombre_trabajador}",
                f"Fecha: {st.session_state.fecha_accidente}",
                f"Hora: {st.session_state.hora_accidente}",
                f"Actividad: {st.session_state.actividad}",
                f"Local: {st.session_state.nombre_local}",
                f"Lugar: {st.session_state.lugar_accidente}",
                f"Lesión: {st.session_state.naturaleza_lesion}",
                f"Tarea: {st.session_state.tarea}",
                f"Operación: {st.session_state.operacion}",
                f"Declaraciones y testimonios",
                f"Declaración Accidentado: {st.session_state.declaracion_accidentado}",
                f"Nombre Testigo 1: {st.session_state.decl1_nombre}",
                f"Texto Declaración 1: {st.session_state.decl1_texto}",
                f"Nombre Testigo 2: {st.session_state.decl2_nombre}",
                f"Texto Declaración 2: {st.session_state.decl2_texto}",
                f"Contexto y circunstancias",
                f"Contexto: {st.session_state.contexto}",
                f"Circunstancias: {st.session_state.circunstancias}",
            ])

        # Generar relato inicial
        st.session_state.relatof = qm.generar_pregunta(
            "relato_inicial",
            st.session_state.initial_story
        )

        # Marcar flujo activo y reiniciar flag (si quisieras obligar a re-guardar antes de una nueva ejecución)
        st.session_state['invest_active'] = True
        st.session_state.relato_form_guardado = False
        st.rerun()

    # 5️⃣  Si ya existe relato, pasamos a la app de investigación
    if st.session_state.get("relatof") and st.session_state.get("invest_active"):
        app = InvestigationApp(st.secrets.get("OPENAI_API_KEY", ""))
        app.run()
