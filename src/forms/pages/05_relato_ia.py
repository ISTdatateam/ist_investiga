#05_relato_ia.py
import streamlit as st
from forms.data_form import init_session_fields, get_qm
from ia.questions import InvestigationApp

'''
st.session_state.initial_story = """IDENTIFICACIÓN		1.NOMBRE	MARIA DEL ROSARIO PARRAGUEZ MERINO
		2. RUT	10.965.002-1
		3. EDAD	52 AÑOS
		4.  FECHA ACCIDENTE:	07-11-2024
		5.  HORA ACCIDENTE:	12:30 HRS
		6.  FECHA AVISO ACCIDENTE:	07-11-2024
		7.  SECCIÓN:	PERECIBLES
		8. CARGO:	OPERADORA
		9. ANTIGÜEDAD EN EL CARGO:	11 AÑOS
		10. ZONA DEL CUERPO LESIONADA:	DEDO MEÑIQUE MANO DERECHA
		11. TIPO DE ACCIDENTE: 	GOLPE CONTRA
		12.TAREA REALIZADA:	TRASLADO DE MERCADERIA 
La colaboradora antes individualizada quien se desempeña como operador perecible, se encontraba trasladando jugos a bodega con carro de supermercado cuando, al pasar por pasillo de trastienda, se golpea el dedo meñique de la mano derecha con gaveta de Red Húmeda que se encontraba abierta generándole un corte en la zona antes mencionada. """
'''

def run():
    # 1️⃣  Inicialización de variables de sesión
    #if not st.session_state.get("initialized_fields", False):
    #    init_session_fields()
    #    st.session_state["initialized_fields"] = True

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
                f"Fecha: {st.session_state.fecha_accidente}",
                f"Hora: {st.session_state.hora_accidente}",
                f"Actividad: {st.session_state.actividad}",
                f"Local: {st.session_state.nombre_local}",
                f"Lugar: {st.session_state.lugar_accidente}",
                f"Lesión: {st.session_state.naturaleza_lesion}",
                f"Tarea: {st.session_state.tarea}",
                f"Operación: {st.session_state.operacion}",
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
