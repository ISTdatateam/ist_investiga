import streamlit as st
from src.forms.data_form import export_docx_wrapper
from src.forms.data_form import init_session_fields



def run():

    st.header("Paso 9 – Generar Informe")

    with st.expander("Debug"):
        st.write(st.session_state)

    # Formulario para datos básicos del informe
    with st.form(key="form_informe", clear_on_submit=False):
        st.text_input(
            'Informe N°*',
            value=st.session_state.informe_numero,
            key='informe_numero'
        )
        st.text_input(
            'Investigador*',
            value=st.session_state.investigador,
            key='investigador'
        )
        st.date_input(
            'Fecha Informe',
            value=st.session_state.fecha_informe,
            key='fecha_informe'
        )
        # Capturamos si el usuario hace submit
        submitted = st.form_submit_button('Generar Informe', use_container_width=True)

    # Ejecutar generación fuera del bloque form
    if submitted:

        try:
            # Llamada al wrapper que genera y despliega el documento
            export_docx_wrapper()
            st.success('Informe generado correctamente')
        except Exception as e:
            st.error(f'Error al generar informe: {e}')

