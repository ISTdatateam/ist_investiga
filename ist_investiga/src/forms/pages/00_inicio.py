# src/forms/pages/00_inicio.py
import streamlit as st
from datetime import date, time, datetime, timedelta
from src.db import search_accidentes, fetch_accidente_full
from src.forms.data_form import init_session_fields  # limpia todos los campos
import time as t

# ------------------------------------------------------------------------
def run():
    st.title("Buscar o crear investigación")

    # ---------- filtros --------------------------------------------------
    filtro_rut = st.text_input("RUT del trabajador (obligatorio)")
    filtro_empresa = st.text_input("Empresa / Razón social contiene…")
    col1, col2 = st.columns(2)
    with col1:
        desde = st.date_input("Desde", value=None, format="YYYY-MM-DD")
    with col2:
        hasta = st.date_input("Hasta", value=None, format="YYYY-MM-DD")

    # ---------- búsqueda -------------------------------------------------
    if st.button("Buscar", use_container_width=True, disabled=not filtro_rut.strip()):
        resultados = search_accidentes(
            empresa   = filtro_empresa or None,
            rut_trab  = filtro_rut.strip(),
            fecha_ini = desde.isoformat() if desde else None,
            fecha_fin = hasta.isoformat() if hasta else None,
        )
        st.session_state["busqueda_resultados"] = resultados

    # ---------- resultados ----------------------------------------------
    if "busqueda_resultados" in st.session_state:
        res = st.session_state["busqueda_resultados"]

        if not res:
            st.warning("No se encontraron accidentes para este trabajador.")
            _boton_crear_nuevo(filtro_rut)
        else:
            st.dataframe(res, hide_index=True, use_container_width=True)

            sel = st.selectbox(
                "Selecciona un accidente para continuar la edición",
                options=[f'{r["accidente_id"]} – {r["empresa_sel"]} – {r["fecha_accidente"]}'
                         for r in res],
                placeholder="— Elegir —",
            )

            cols = st.columns(2)
            with cols[0]:
                if sel and st.button("Cargar accidente seleccionado", use_container_width=True):
                    acc_id = int(sel.split("–")[0].strip())
                    _load_accidente_en_session(acc_id)
                    st.success("Cargando datos...")
                    t.sleep(0.5)
                    st.session_state["_page"] = 1
                    st.rerun()

            with cols[1]:
                _boton_crear_nuevo(filtro_rut)

# ------------------------------------------------------------------------
def _boton_crear_nuevo(rut: str):
    if st.button("Crear nuevo accidente", use_container_width=True, key="btn_nuevo"):
        st.session_state.clear()
        init_session_fields()
        st.session_state.rut_trabajador = rut.strip()
        st.success("Generando nueva investigación...")
        t.sleep(0.5)
        st.session_state["_page"] = 1
        st.rerun()

# ------------------------------------------------------------------------
def _load_accidente_en_session(accidente_id: int):
    """Carga todos los datos de BD a session_state para edición."""
    st.session_state.clear()
    init_session_fields()

    data = fetch_accidente_full(accidente_id)
    if not data:
        st.error("No se encontró el accidente en la base de datos.")
        st.stop()

    # ---------------- Empresa / Centro ----------------------------------
    for campo in (
        "empresa_id", "centro_id", "empresa_sel", "rut_empresa", "actividad",
        "direccion_empresa", "telefono", "representante_legal",
        "region", "comuna", "nombre_local", "direccion_centro",
    ):
        st.session_state[campo] = data.get(campo)

    # ---------------- Trabajador ----------------------------------------
    if data.get("trabajador_id"):
        for campo in (
            "trabajador_id", "nombre_trabajador", "rut_trabajador",
            "nacionalidad", "estado_civil", "domicilio",
        ):
            st.session_state[campo] = data.get(campo)

        # fecha_nacimiento puede venir como str
        fnac = data.get("fecha_nacimiento")
        if fnac and isinstance(fnac, str):
            st.session_state.fecha_nacimiento = datetime.strptime(fnac, "%Y-%m-%d").date()
        else:
            st.session_state.fecha_nacimiento = fnac

    # ---------------- Accidente -----------------------------------------
    st.session_state.accidente_id      = data["accidente_id"]
    st.session_state.fecha_accidente   = _str_to_date(data["fecha_accidente"])
    st.session_state.hora_accidente    = _str_to_time(data["hora_accidente"])
    st.session_state.lugar_accidente   = data["lugar_accidente"]
    st.session_state.tipo_accidente    = data["tipo_accidente"]
    st.session_state.naturaleza_lesion = data["naturaleza_lesion"]
    st.session_state.parte_afectada    = data["parte_afectada"]
    st.session_state.tarea             = data["tarea"]
    st.session_state.operacion         = data["operacion"]
    st.session_state.cargo_trabajador  = data["cargo_trabajador"]
    st.session_state.contrato          = data["contrato"]
    st.session_state.antiguedad_empresa= data["antiguedad_empresa"]
    st.session_state.antiguedad_cargo  = data["antiguedad_cargo"]
    st.session_state.danos_personas    = data["danos_personas"]
    st.session_state.danos_propiedad   = data["danos_propiedad"]
    st.session_state.perdidas_proceso  = data["perdidas_proceso"]
    st.session_state.resumen           = data["resumen"]
    st.session_state.relato            = data["relato"]
    st.session_state.contexto          = data["contexto"]
    st.session_state.circunstancias    = data["circunstancias"]
    st.session_state.preinitial_story  = data["preinitial_story"]
    st.session_state.preguntas_entrevista = data["preguntas_entrevista"]

# ------------------------------------------------------------------------
def _str_to_time(hora_val) -> time | None:
    """Convierte str 'HH:MM:SS', datetime.time, datetime.timedelta o None → datetime.time"""
    if hora_val in (None, ""):
        return None

    # ya es time
    if isinstance(hora_val, time):
        return hora_val

    # viene como timedelta (driver MySQL)
    if isinstance(hora_val, timedelta):
        total_seconds = int(hora_val.total_seconds())
        h = (total_seconds // 3600) % 24
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return time(h, m, s)

    # viene como datetime.datetime
    if isinstance(hora_val, datetime):
        return hora_val.time()

    # viene como string 'HH:MM[:SS]'
    if isinstance(hora_val, str):
        parts = list(map(int, hora_val.split(":")))
        while len(parts) < 3:
            parts.append(0)
        return time(*parts[:3])

    # Tipo inesperado → registra y devuelve None
    st.warning(f"Formato de hora no reconocido: {type(hora_val)}")
    return None

def _str_to_date(fecha_val) -> date | None:
    """Devuelve un datetime.date a partir de str 'YYYY-MM-DD' o date, o None."""
    if not fecha_val:
        return None
    if isinstance(fecha_val, date):
        return fecha_val                     # ya es date
    # si viniera como datetime.datetime, toma solo la parte de fecha
    if isinstance(fecha_val, datetime):
        return fecha_val.date()
    # caso string
    return datetime.strptime(fecha_val, "%Y-%m-%d").date()