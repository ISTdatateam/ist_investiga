import streamlit as st
from ia.questions import QuestionManager
from forms.data_form import init_session_fields
import time

def run():
    # Inicializa session_state (edades, fechas, textos, etc.)
    # -- Sólo inicializar la primera vez --
    if not st.session_state.get("initialized_fields", False):
        init_session_fields()
        st.session_state["initialized_fields"] = True
    st.header("🔎 Paso 6 – Hechos IA")

    # Instancia tu QM con la misma API key
    qm = QuestionManager(st.secrets.get("OPENAI_API_KEY", ""))

    st.write("Lee detenidamente el relato del accidente, puedes hacer los últimos ajustes.")
    st.write("Luego continua con el botón identificar hechos.")

    #st.session_state.relatof = '''El día 07 de noviembre de 2024, a las 12:30 horas, María del Rosario Parraguez Merino, de 52 años y con 11 años de experiencia como operadora en la sección de perecibles, realizaba la tarea de traslado de mercadería en el área de trabajo. En ese momento, trasladaba jugos hacia la bodega utilizando un carro de supermercado. El entorno consistía en un pasillo de trastienda, caracterizado por un espacio reducido y la presencia de gavetas de almacenamiento, entre ellas una gaveta de Red Húmeda que se encontraba abierta. Durante el desplazamiento por este pasillo, María del Rosario golpeó el dedo meñique de la mano derecha contra la gaveta abierta, lo que le provocó un corte en dicha zona. El accidente fue reportado el mismo día, 07-11-2024. En cuanto a las condiciones de trabajo, María no había recibido entrenamiento específico para identificar y evitar riesgos en pasillos estrechos. La empresa no contaba con reglas claras para mantener los pasillos libres y seguros en todo momento. Los pasillos y las gavetas no estaban diseñados para prevenir golpes al mover carros de tamaño grande. Sin embargo, sí existían señalizaciones que indicaban mantener las gavetas cerradas en los pasillos.'''

    with st.form(key="form_hechos"):

        st.text_area('Relato procesado por IA, siempre revisalo.', key='relatof', value=st.session_state.relatof, height=400)

        if st.session_state.hechos:
            # Mostrar hechos identificados
            st.text_area(
                'Hechos Identificados',
                value=st.session_state.hechos,
                height=400,
                key='hechos'
            )
        else:
            # Botón para identificar hechos
            if st.form_submit_button('🔎 Identificar Hechos'):
                # Genera hechos basados en el relato
                st.session_state.hechos = qm.generar_pregunta(
                    'hechos', st.session_state.relatof
                )
                #print(st.session_state.relatof)
                st.rerun()

        # Si ya hay hechos, permite avanzar
        if st.session_state.hechos and st.form_submit_button('Siguiente ▶'):
            #print("🔍 DEBUG-STATE antes de arbol:", {
            #    'relatof': bool(st.session_state.get('relatof')),
            #    'hechos': bool(st.session_state.get('hechos'))
            #})
            st.session_state['_page'] = 7
            st.rerun()
