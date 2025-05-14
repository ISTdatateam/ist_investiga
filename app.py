import os
import sys
import streamlit as st
from docutils.nodes import sidebar
from streamlit_option_menu import option_menu
from src.forms.data_form import init_session_fields
import time

# Asegura que 'src' esté en el path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

if not st.session_state.get("initialized_fields", False):
    init_session_fields()
    st.session_state["initialized_fields"] = True



# Definición de páginas con íconos y rutas
PAGES = {
    1: ("🏭 Empresa", "forms.pages.01_empresa"),
    2: ("👷 Datos Trabajador", "forms.pages.02_trabajador"),
    3: ("⚠️ Detalle Accidente", "forms.pages.03_accidente"),
    4: ("📝 Declaraciones y Fotos", "forms.pages.04_declaraciones_fotos"),
    5: ("🧠 Relato IA", "forms.pages.05_relato_ia"),
    6: ("🔎 Hechos IA", "forms.pages.06_hechos_ia"),
    7: ("🌳 Árbol IA", "forms.pages.07_arbol_ia"),
    8: ("🛠️ Medidas Correctivas", "forms.pages.08_medidas_correctivas"),
    9: ("📄 Generar Informe", "forms.pages.09_informe")
}

# Página por defecto
if "_page" not in st.session_state:
    st.session_state["_page"] = 1

# Asegura que current siempre sea un int válido
try:
    current = int(st.session_state["_page"])
except (ValueError, TypeError):
    current = 1

page_keys = list(PAGES.keys())
page_labels = [PAGES[k][0] for k in page_keys]
def_index = page_keys.index(current)

# …tus imports y configuración anteriores…

# Menú lateral CON option_menu dentro de st.sidebar
with st.sidebar:
    selected_label = option_menu(
        menu_title="🚀 IST Investiga",
        options=page_labels,        # tus etiquetas con emoji
        icons=None,
        menu_icon="cast",
        default_index=def_index,
        orientation="vertical",
        key="page_menu"
    )

# Convertimos etiqueta a clave numérica
selected_idx = page_labels.index(selected_label)
selected = page_keys[selected_idx]

# Guardamos y cargamos la página
st.session_state["_page"] = selected
module_path = PAGES[selected][1]
page_module = __import__(module_path, fromlist=["run"])
time.sleep(1)
page_module.run()
