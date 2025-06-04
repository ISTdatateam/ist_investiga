import streamlit as st
import time as t
from ..data_form import load_locales
from src.db import upsert_holding, upsert_empresa, upsert_centro_trabajo

HOLDING_ID_DEFAULT = 1

def run():
    st.header("Empresa y Centro de Trabajo")

    df_locales = load_locales()
    # Limpieza de espacios
    for col in df_locales.select_dtypes(include='object'):
        df_locales[col] = df_locales[col].str.strip()

    # 1. Empresa
    st.subheader("1. Empresa")
    #Pre-poblar el campo empresa
    holding_nombre = st.text_input("Holding", "SMU")
    razones = sorted(df_locales['Razón Social'].dropna().unique())
    #Ajustado para demo de ULTRAMAR razones[0] por ""
    prev_empresa = st.session_state.get("empresa_sel", 'ULTRAMAR AGENCIA MARITIMA' if razones else "")
    idx_empresa = razones.index(prev_empresa) if prev_empresa in razones else 0
    st.session_state.empresa_sel = st.selectbox(
        "Razón Social*",
        razones,
        index=idx_empresa,
        help="Selecciona la razón social de la empresa"
    )

    empresa =  st.session_state.empresa_sel

    #prepoblar el rut
    rut_vals = df_locales[df_locales['Razón Social'] == empresa]['Rut'].unique()
    #Ajustado para demo de ULTRAMAR rut_vals[0] por '80.992.000-3'
    default_rut = st.session_state.get("rut_empresa", rut_vals[0] if len(rut_vals) else "")

    st.session_state.rut_empresa = st.text_input(
        "RUT Empresa*",
        value=default_rut,
        disabled=True
    )
    if len(rut_vals):
        st.session_state["rut_empresa"] = rut_vals[0]

    df_emp = df_locales[df_locales['Razón Social'] == empresa]

    """
    # prepoblar el campo direccion
    df_direcciones = df_locales[df_locales['Razón Social'] == empresa]
    df_direcciones["Direccion_Completa"] = df_emp["Dirección"].fillna("") + ", " + df_emp[
        "Comuna"].fillna("")
    direcciones = sorted(df_direcciones['Direccion_Completa'].dropna().unique())
    prev = st.session_state.get('Dirección', direcciones[0])
    idx = direcciones.index(prev) if prev in direcciones else 0

    st.session_state.direccion_empresa = st.selectbox(
        "Direccion empresa*",
        direcciones,
        index=idx,
        key="dirección_sel",  # aquí Streamlit guarda en 'region_sel'
        help="Selecciona la dirección principal de la empresa"
    )
    """

    if not st.session_state.direccion_empresa:
        #st.session_state.direccion_empresa = "El Bosque Norte 500, Piso 18, Las Condes"
        #st.session_state.direccion_empresa = "Av. Santa Maria 2450, Providencia"
         st.session_state.direccion_empresa = "Cerro El Plomo 5680, Las Condes"
    st.session_state.direccion_empresa = st.text_input(
        "Dirección Empresa*",
        st.session_state.get('direccion_empresa', ''),
        help="Ej: Av. Irarrázaval 4354"
    )

    if not st.session_state.telefono:
        st.session_state.telefono = "+56991502039"
    st.session_state.telefono = st.text_input(
        "Teléfono Empresa*",
        st.session_state.get('telefono', ''),
        help="Ej: +56912345678"
    )

    if not st.session_state.representante_legal:
        st.session_state.representante_legal = "Gerardo Salinas Mendoza"
    st.session_state.representante_legal = st.text_input(
        "Representante legal*",
        st.session_state.get('representante_legal', ''),
        help="Marcelo Gálvez Saldías"
    )

    if not st.session_state.actividad:
        st.session_state.actividad = "Supermercados"
    st.session_state.actividad = st.text_input(
        "Actividad Económica*",
        st.session_state.get('actividad', ''),
        help="Ej: Supermercado"
    )

    # 2. Centro de Trabajo
    st.subheader("2. Centro de Trabajo")
    df_emp = df_locales[df_locales['Razón Social'] == empresa]

    # prepoblar el campo región
    regiones = sorted(df_emp['Región'].dropna().unique())
    prev = st.session_state.get("region", regiones[0])
    idx = regiones.index(prev) if prev in regiones else 0

    st.session_state.region = st.selectbox(
        "Región*",
        regiones,
        index=idx,
        key="region_sel",  # aquí Streamlit guarda en 'region_sel'
        help="Selecciona la región del centro de trabajo"
    )
    #st.session_state.region = st.selectbox("Región*", regiones, key='region_sel')

    # prepoblar el campo comuna
    df_reg = df_emp[df_emp['Región'] == st.session_state.region]
    comunas = sorted(df_reg['Comuna'].dropna().unique())
    prev_comuna = st.session_state.get("comuna", comunas[0] if comunas else "")
    idx_comuna = comunas.index(prev_comuna) if prev_comuna in comunas else 0
    st.session_state.comuna =  st.selectbox(
        "Comuna*",
        comunas,
        index=idx_comuna,
        key="comuna_sel",
        help="Selecciona la comuna del centro"
    )

    # prepoblar el campo Nombre del centro
    df_com = df_reg[df_reg['Comuna'] == st.session_state.comuna]
    centros = sorted(df_com['Nombre_Centro'].dropna().unique())
    prev_centro = st.session_state.get("nombre_local", centros[0] if centros else "")
    idx_centro = centros.index(prev_centro) if prev_centro in centros else 0
    st.session_state.nombre_local =  st.selectbox(
        "Nombre de Centro*",
        centros,
        index=idx_centro,
        key="centro_sel",
        help="Selecciona el nombre del centro de trabajo"
    )

    # Prepoblar campo dirección del ct
    direc_vals = df_com[df_com['Nombre_Centro'] == st.session_state.nombre_local]['Dirección'].unique()
    default_dir = st.session_state.get(
        "direccion_centro",
        direc_vals[0] if len(direc_vals) else ""
    )
    st.text_input(
        "Dirección Centro*",
        value=default_dir,
        disabled=True
    )

    if len(direc_vals):
        st.session_state["direccion_centro"] = direc_vals[0]

    # Botón de guardado y avance
    if st.button("Guardar datos", use_container_width=True):
        holding_id = None
        if holding_nombre.strip():
            holding_id = upsert_holding(holding_nombre.strip())

        # 1. Empresa ---------------------------------------------------------
        empresa_id = upsert_empresa(
            holding_id,
            {
                "holding_id": HOLDING_ID_DEFAULT,
                "empresa_sel": st.session_state.empresa_sel,
                "rut": st.session_state.rut_empresa,
                "act": st.session_state.actividad,
                "dir": st.session_state.direccion_empresa,
                "tel": st.session_state.telefono,
                "rep": st.session_state.representante_legal,
                "reg": st.session_state.region,
                "com": st.session_state.comuna,
            },
        )
        # 2. Centro de trabajo ----------------------------------------------
        centro_id = upsert_centro_trabajo(
            empresa_id,
            st.session_state.nombre_local,
            st.session_state.direccion_centro,
        )

        # 3. Guarda las PK en sesión para las páginas siguientes ------------
        st.session_state.empresa_id = empresa_id
        st.session_state.centro_id = centro_id

        st.success("Empresa y Centro de Trabajo guardados en la base de datos")
        t.sleep(0.5)
        #st.success("Avanzando a datos del trabajador/a..")
        #st.session_state["_page"] = 2
        #t.sleep(0.5)
        st.rerun()