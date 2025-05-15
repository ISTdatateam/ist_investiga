import streamlit as st
from src.ia.questions import QuestionManager
from src.forms.data_form import init_session_fields

def run():


    # Asegura la existencia de los flags que usaremos
    st.session_state.setdefault("form_hechos_guardado", False)
    st.session_state.setdefault("relatof", "")
    st.session_state.setdefault("hechos", "")

    st.header("🔎 Paso 6 – Hechos IA")

    with st.expander("Debug"):
        st.write(st.session_state)

    qm = QuestionManager(st.secrets.get("OPENAI_API_KEY", ""))

    # 2️⃣ Formulario = escribe / guarda el relato
    with st.form("form_hechos"):
        relatof_input = st.text_area(
            "Relato procesado por IA · revísalo antes de guardar",
            key="relatof_input",             # clave nueva (no pisa relatof hasta guardar)
            value=st.session_state.relatof,
            height=400
        )

        guardar = st.form_submit_button("Guardar relato procesado por IA")

    # 3️⃣ Acciones tras guardar
    if guardar:
        st.session_state.relatof = relatof_input
        st.session_state.form_hechos_guardado = True
        st.success("✅ Relato guardado. Ahora puedes identificar los hechos.")
        print(st.session_state.relatof)



    # 4️⃣ Botón externo = identificar hechos (solo habilitado si ya se guardó)
    identificar_disabled = not st.session_state.form_hechos_guardado
    if st.button("Identificar hechos con IA", disabled=identificar_disabled, use_container_width=True):
        relatof = st.session_state.relatof
        st.session_state.hechos = qm.generar_pregunta(
            "hechos",
            relatof
        )
        st.session_state.form_hechos_guardado = False

    #Mostrar hechos (si existen) y botón Siguiente
    if st.session_state.hechos:
        st.text_area(
            "Hechos identificados",
            value=st.session_state.hechos,
            key="hechos_view",
            height=400
        )
        if st.button("Guardar hechos generados por IA", use_container_width=True):
            st.session_state.hechos = st.session_state.get('hechos_view', '')
            st.rerun()
