# corrective.py – Ultima version sin clave y con fecha seleccionable
# ================================================================

import json
import datetime
from typing import List

import streamlit as st

from src.forms.data_form import get_qm

# ------------------------------------------------------------------
# Estado de la sesión
# ------------------------------------------------------------------

st.session_state.setdefault("edited_measures", [])

# ------------------------------------------------------------------
# Generación de medidas correctivas
# ------------------------------------------------------------------

def generate_measures():
    """Construye la entrada para la IA y genera las medidas."""

    relato_parts: List[str] = []
    for key in ("relatof", "hechos", "arbol"):
        val = st.session_state.get(key)
        if val:
            relato_parts.append(
                json.dumps(val, indent=2, ensure_ascii=False)
                if key == "arbol" else str(val)
            )

    relato = "\n".join(relato_parts)

    qm = get_qm()
    ai_response = qm.generar_pregunta("medidas", relato)

    # Intentamos aislar un bloque JSON
    json_block = ai_response
    if "```" in ai_response:
        try:
            json_block = ai_response.split("```json")[1].split("```")[0].strip()
        except Exception:
            pass

    try:
        result = json.loads(json_block)
        st.session_state.edited_measures = result.get("medidas", [])
        st.success("Medidas generadas y formateadas correctamente.")
    except Exception as err:
        st.error(f"Error al procesar el JSON de la IA: {err}")
        st.write(json_block)

# ------------------------------------------------------------------
# Editor de medidas correctivas
# ------------------------------------------------------------------

def show_measures_editor():
    st.markdown("### Medidas Propuestas")
    tipo_opts = ["Ingenieril", "Administrativa", "EPP"]
    prioridad_opts = ["Alta", "Media", "Baja"]

    for idx, m in enumerate(st.session_state.edited_measures.copy()):
        with st.expander(f"Medida {idx + 1}: {m.get('descripcion', '')[:40]}…"):
            col1, col2 = st.columns(2)

            # --- Columna izquierda: Tipo y Plazo (date_input) ---
            with col1:
                tipo = st.selectbox(
                    "Tipo",
                    tipo_opts,
                    index=tipo_opts.index(m.get("tipo", tipo_opts[0])) if m.get("tipo") in tipo_opts else 0,
                    key=f"tipo_{idx}"
                )

                # Date picker – intenta usar la fecha existente
                plazo_str = m.get("plazo")
                try:
                    default_date = datetime.date.fromisoformat(plazo_str) if plazo_str else datetime.date.today()
                except ValueError:
                    default_date = datetime.date.today()

                plazo_date = st.date_input(
                    "Plazo (fecha límite)",
                    value=default_date,
                    key=f"plazo_{idx}"
                )

            # --- Columna derecha: Responsable y Prioridad ---
            with col2:
                responsable = st.text_input(
                    "Responsable",
                    m.get("responsable", ""),
                    key=f"resp_{idx}"
                )

                prioridad = st.selectbox(
                    "Prioridad",
                    prioridad_opts,
                    index=prioridad_opts.index(m.get("prioridad", prioridad_opts[1])) if m.get("prioridad") in prioridad_opts else 1,
                    key=f"prio_{idx}"
                )

            descripcion = st.text_area(
                "Descripción",
                m.get("descripcion", ""),
                key=f"desc_{idx}",
                height=120,
            )

            cols = st.columns(2)
            with cols[0]:
                if st.button("Guardar cambios", key=f"save_{idx}"):
                    st.session_state.edited_measures[idx].update({
                        "tipo": tipo,
                        "prioridad": prioridad,
                        "plazo": plazo_date.isoformat(),
                        "responsable": responsable,
                        "descripcion": descripcion,
                    })
                    st.success(f"Medida {idx + 1} actualizada.")
            with cols[1]:
                if st.button("Eliminar", key=f"del_{idx}"):
                    st.session_state.edited_measures.pop(idx)
                    st.rerun()

# ------------------------------------------------------------------
# Función principal – expuesta al resto de la app
# ------------------------------------------------------------------

def medidas_app() -> bool:
    """Punto de entrada para la sección de medidas correctivas."""

    st.session_state.setdefault("edited_measures", [])
    status = False

    if st.button("Generar medidas correctivas con IA"):
        if not any(st.session_state.get(k) for k in ("relatof", "hechos", "arbol")):
            st.warning("Faltan datos: asegúrate de haber guardado relato, hechos y árbol.")
        else:
            with st.spinner("Analizando hechos y generando medidas correctivas con IA…"):
                generate_measures()
                status = True

    if st.session_state.edited_measures:
        show_measures_editor()
    return status
