import streamlit as st
from forms.data_form import get_qm
from models import causaltree
from report.generator import InformeGenerator
import os
import tempfile
import time
from models.causaltree import getvalues
from forms.data_form import init_session_fields
from statsmodels.sandbox.regression.try_treewalker import data2

ig = InformeGenerator()
cst = causaltree

print("OJO AQUI! INICIO", getvalues(st.session_state.relatof,st.session_state.hechos))



def run():
    # Inicializa session_state
    # -- Sólo inicializar la primera vez --
    if not st.session_state.get("initialized_fields", False):
        init_session_fields()
        st.session_state["initialized_fields"] = True


    qm = get_qm()

    st.header("🌳 Paso 7 – Árbol de Causas IA")

    with st.expander("Debug"):
        st.write(st.session_state)

    # Generación de árbol de causas

    #print("🔍 DEBUG-STATE antes de if not st.session_state.get('arbol'):", {
    #    'relatof': bool(st.session_state.get('relatof')),
    #    'hechos': bool(st.session_state.get('hechos'))
    #})
    # 1) Al principio del run, respalda si aún no lo has hecho:
    st.session_state.setdefault('relatof_backup', st.session_state.get('relatof', ''))
    st.session_state.setdefault('hechos_backup',  st.session_state.get('hechos',  ''))

    # 2) Ya puedes trabajar con esos backups seguros:
    relatof_cuidado = st.session_state['relatof_backup']
    hechos_cuidado  = st.session_state['hechos_backup']

    if not st.session_state.get('arbol'):
        if st.button('🌳 Generar Árbol', use_container_width=True):
            prompt = (
                f"Relato: {relatof_cuidado}\n"
                f"Hechos: {hechos_cuidado}"
            )
            st.session_state.arbol = qm.generar_pregunta('arbol_causas', prompt)
            st.session_state.arbol_from_5q = st.session_state.arbol
            #print("🔍 DEBUG-STATE despues de crear arbol_from_5q:", {
            #    'relatof': bool(st.session_state.get('relatof')),
            #    'hechos': bool(st.session_state.get('hechos'))
            #})
            #print(st.session_state.relatof)
            #print(st.session_state.hechos)

            st.rerun()
    else:
        # Mostrar JSON bruto
        #st.subheader("Árbol de Causas")
        #st.json(st.session_state.arbol)

        # Inserta árbol interactivo
        #st.markdown("---")
        #st.subheader("🔗 Árbol de Causas Interactivo")
        cst.main()

    # Botones de navegación
    cols = st.columns([1, 2])
    with cols[0]:
        if st.button('◀ Atrás', use_container_width=True):
            st.session_state['_page'] = 6
            st.rerun()

    with cols[1]:
        # El botón sólo se renderiza si ya existe el árbol
        if st.session_state.get('arbol') and st.button('Siguiente ▶', use_container_width=True):
            print("OJO AQUI! FIN",
                  getvalues(
                      st.session_state['relatof_backup'],
                      st.session_state['hechos_backup'])
                  )
            if st.session_state.nodes:
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
                else:
                    st.error("No se encontró el PNG generado.")
            else:
                st.warning("¡El árbol está vacío!")

            # 3.2) Avanzar de página
            st.session_state['_page'] = 8
            st.rerun()


