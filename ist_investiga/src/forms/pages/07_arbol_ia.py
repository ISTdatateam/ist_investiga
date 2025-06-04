import streamlit as st
from src.forms.data_form import get_qm
from src.models import causaltree
from src.report.generator import InformeGenerator
import io
import os
import tempfile
import time
from src.models.causaltree import getvalues
from src.forms.data_form import init_session_fields
from statsmodels.sandbox.regression.try_treewalker import data2

ig = InformeGenerator()
cst = causaltree

def run():
    # Inicializa session_state
    # -- Sólo inicializar la primera vez --

    qm = get_qm()
    st.header("Árbol de Causas")
    st.write("En este momento el asistente va a generar un árbol de causas estableciendo las relaciones entre los hechos identificados")

    # 2) Ya puedes trabajar con esos backups seguros:
    relatof = st.session_state.get('relatof')
    hechos  = st.session_state.get('hechos')

    if not st.session_state.get('arbol'):
        if st.button('Generar Árbol', use_container_width=True):
            with st.spinner("Generando arbol con IA.."):
                prompt = (
                    f"Relato: {relatof}\n"
                    f"Hechos: {hechos}"
                )
                st.session_state.arbol = qm.generar_pregunta('arbol_causas', prompt)
                st.session_state.arbol_from_5q = st.session_state.arbol
                st.rerun()
    else:
        cst.main()

    # El botón sólo se renderiza si ya existe el árbol
    if st.session_state.get('arbol') and st.button('Guardar Arbol', use_container_width=True):
        if st.session_state.nodes:
            # Asegúrate de que 'arbol_dot' contenga el DOT en st.session_state
            dot_src = st.session_state.get('arbol_dot')
            dot_src = dot_src.replace('{', '{\n    graph [dpi=300];', 1)

            if not dot_src:
                st.error("No hay definición DOT en session_state['arbol_dot']")
            else:
                # Genera los bytes PNG en memoria
                png_bytes = ig._generate_tree_image(dot_src)

                # Opcional: guardarlo en session_state si lo necesitas más tarde
                st.session_state.cause_tree_png_bytes = png_bytes

                # Mostrar la imagen en Streamlit
                buf = io.BytesIO(png_bytes)
                buf.seek(0)
                st.session_state.cause_tree_png = buf
                #st.image(buf, caption="Árbol de causas", use_column_width=True)

            """
            # 3.1) Generar DOT y exportar imagen
            cst.generate_dot()
            tmp = tempfile.mkdtemp()
            img_path = os.path.join(tmp, "cause_tree")
            ig._generate_tree_image(img_path)  # crea cause_tree.png

            png_file = f"{img_path}.png"
            if os.path.exists(png_file):
                st.session_state.cause_tree_png = png_file
                st.success("Árbol exportado y guardado!")
                # Cambiamos de herramienta y avanzamos
                st.session_state.selected_tool = "Ficha"
            """
        else:
            st.warning("¡El árbol está vacío!")

        # 3.2) Avanzar de página
        #st.session_state['_page'] = 8
        st.rerun()


