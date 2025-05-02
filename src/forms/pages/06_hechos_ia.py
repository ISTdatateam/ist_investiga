import streamlit as st
from ia.questions import QuestionManager
from forms.data_form import init_session_fields

def run():
    # 1️⃣  Inicialización
    if not st.session_state.get("initialized_fields", False):
        init_session_fields()
        st.session_state["initialized_fields"] = True

    # Asegura la existencia de los flags que usaremos
    st.session_state.setdefault("form_hechos_guardado", False)
    st.session_state.setdefault("relatof", "")
    st.session_state.setdefault("hechos", "")

    st.header("🔎 Paso 6 – Hechos IA")

    qm = QuestionManager(st.secrets.get("OPENAI_API_KEY", ""))

    # 2️⃣ Formulario = escribe / guarda el relato
    with st.form("form_hechos"):
        relatof_input = st.text_area(
            "Relato procesado por IA · revísalo antes de guardar",
            key="relatof_input",             # clave nueva (no pisa relatof hasta guardar)
            value=st.session_state.relatof,
            height=400
        )

        guardar = st.form_submit_button("💾 Guardar relato")

    # 3️⃣ Acciones tras guardar
    if guardar:
        st.session_state.relatof = relatof_input
        st.session_state.form_hechos_guardado = True
        st.success("✅ Relato guardado. Ahora puedes identificar los hechos.")

    # 4️⃣ Botón externo = identificar hechos (solo habilitado si ya se guardó)
    identificar_disabled = not st.session_state.form_hechos_guardado
    if st.button("🔎 Identificar hechos", disabled=identificar_disabled):
        st.session_state.hechos = qm.generar_pregunta(
            "hechos",
            st.session_state.relatof
        )
        # Opcional: resetea el flag para forzar una nueva edición si se quiere volver a correr
        st.session_state.form_hechos_guardado = False
        st.rerun()

    # 5️⃣ Mostrar hechos (si existen) y botón Siguiente
    if st.session_state.hechos:
        st.text_area(
            "Hechos identificados",
            value=st.session_state.hechos,
            key="hechos_view",
            height=400
        )
        if st.button("Siguiente ▶"):
            st.session_state["_page"] = 7
            st.rerun()
