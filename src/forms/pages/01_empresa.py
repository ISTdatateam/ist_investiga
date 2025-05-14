import streamlit as st
from src.forms.data_form import load_locales, init_session_fields
import time

def run():

    st.header("📋 Paso 1 – Empresa y Centro de Trabajo")

    df_locales = load_locales()
    # Limpieza de espacios
    for col in df_locales.select_dtypes(include='object'):
        df_locales[col] = df_locales[col].str.strip()

    # 1. Empresa
    st.subheader("🏭 1. Empresa")
    razones = sorted(df_locales['Razón Social'].dropna().unique())
    empresa = st.selectbox("Razón Social*", razones, key='empresa_sel')
    st.session_state.empresa = empresa

    # RUT (solo lectura)
    rut_vals = df_locales[df_locales['Razón Social'] == empresa]['Rut'].unique()
    st.text_input("RUT Empresa*", value=rut_vals[0] if len(rut_vals) else '', disabled=True)

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

    # Región
    regiones = sorted(df_emp['Región'].dropna().unique())
    st.session_state.region = st.selectbox("Región*", regiones, key='region_sel')

    # Comuna
    df_reg = df_emp[df_emp['Región'] == st.session_state.region]
    comunas = sorted(df_reg['Comuna'].dropna().unique())
    st.session_state.comuna = st.selectbox("Comuna*", comunas, key='comuna_sel')

    # Nombre de Centro
    df_com = df_reg[df_reg['Comuna'] == st.session_state.comuna]
    centros = sorted(df_com['Nombre_Centro'].dropna().unique())
    st.session_state.nombre_local = st.selectbox(
        "Nombre de Centro*", centros, key='centro_sel'
    )

    # Dirección del Centro (solo lectura)
    direc_vals = df_com[df_com['Nombre_Centro'] == st.session_state.nombre_local]['Dirección'].unique()
    st.text_input(
        "Dirección Centro*",
        value=direc_vals[0] if len(direc_vals) else '',
        disabled=True
    )

    # Botón de guardado y avance
    if st.button("💾 Guardar y continuar", use_container_width=True):
        st.success("Sección Empresa y Centro guardada")
        st.session_state['_page'] = 2
        time.sleep(1)
        #st.rerun()
