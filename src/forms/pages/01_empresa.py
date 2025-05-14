import streamlit as st
import time
from ..data_form import load_locales

def run():
    st.write(st.session_state)
    st.header("📋 Paso 1 – Empresa y Centro de Trabajo")

    df_locales = load_locales()
    # Limpieza de espacios
    for col in df_locales.select_dtypes(include='object'):
        df_locales[col] = df_locales[col].str.strip()

    # 1. Empresa
    st.subheader("🏭 1. Empresa")
    #prepoblar el campo empresa
    razones = sorted(df_locales['Razón Social'].dropna().unique())
    prev_empresa = st.session_state.get("empresa_sel", razones[0] if razones else "")
    idx_empresa = razones.index(prev_empresa) if prev_empresa in razones else 0
    st.session_state.empresa_sel = st.selectbox(
        "Razón Social*",
        razones,
        index=idx_empresa,
        help="Selecciona la razón social de la empresa"
    )

    empresa =  st.session_state.empresa_sel

    # prepoblar el rut
    rut_vals = df_locales[df_locales['Razón Social'] == empresa]['Rut'].unique()
    default_rut = st.session_state.get("rut_empresa", rut_vals[0] if len(rut_vals) else "")

    st.session_state.rut_empresa = st.text_input(
        "RUT Empresa*",
        value=default_rut,
        disabled=True
    )
    if len(rut_vals):
        st.session_state["rut_empresa"] = rut_vals[0]

    # Actividad, Dirección y Teléfono
    st.session_state.actividad = st.text_input(
        "Actividad Económica*",
        st.session_state.get('actividad', ''),
        help="Ej: SUPERMERCADO"
    )
    st.session_state.direccion_empresa = st.text_input(
        "Dirección Empresa*",
        st.session_state.get('direccion_empresa', ''),
        help="Ej: Av. Irarrázaval 4354"
    )
    st.session_state.telefono = st.text_input(
        "Teléfono Empresa*",
        st.session_state.get('telefono', ''),
        help="Ej: +56912345678"
    )

    # 2. Centro de Trabajo
    st.subheader("📍 2. Centro de Trabajo")
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
    if st.button("💾 Guardar y continuar", use_container_width=True):
        st.success("Sección Empresa y Centro guardada")
        st.rerun()
