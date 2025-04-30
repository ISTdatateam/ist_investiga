#05_relato_ia.py
import streamlit as st
from forms.data_form import init_session_fields, get_qm
from ia.questions import InvestigationApp


st.session_state.initial_story = """IDENTIFICACIÓN		1.NOMBRE	MARIA DEL ROSARIO PARRAGUEZ MERINO
		2. RUT	10.965.002-1
		3. EDAD	52 AÑOS
		4.  FECHA ACCIDENTE:	07-11-2024
		5.  HORA ACCIDENTE:	12:30 HRS
		6.  FECHA AVISO ACCIDENTE:	07-11-2024
		7.  SECCIÓN:	PERECIBLES
		8. CARGO:	OPERADORA
		9. ANTIGÜEDAD EN EL CARGO:	11 AÑOS
		10. ZONA DEL CUERPO LESIONADA:	DEDO MEÑIQUE MANO DERECHA
		11. TIPO DE ACCIDENTE: 	GOLPE CONTRA
		12.TAREA REALIZADA:	TRASLADO DE MERCADERIA 
La colaboradora antes individualizada quien se desempeña como operador perecible, se encontraba trasladando jugos a bodega con carro de supermercado cuando, al pasar por pasillo de trastienda, se golpea el dedo meñique de la mano derecha con gaveta de Red Húmeda que se encontraba abierta generándole un corte en la zona antes mencionada. """


def run():
    # Inicializa session_state
    init_session_fields()
    st.header("🧠 Paso 5 – Construcción del relato")

    qm = get_qm()

    # Si no existe relato generado, solicitamos generación
    if not st.session_state.get('relatof'):
        # Incluir inputs de contexto y circunstancias
        st.text_area('Contexto', key='contexto', value=st.session_state.get('contexto',''), height=150)
        st.text_area('Circunstancias', key='circunstancias', value=st.session_state.get('circunstancias',''), height=150)

        st.session_state.initial_story = """IDENTIFICACIÓN		1.NOMBRE	MARIA DEL ROSARIO PARRAGUEZ MERINO
        		2. RUT	10.965.002-1
        		3. EDAD	52 AÑOS
        		4.  FECHA ACCIDENTE:	07-11-2024
        		5.  HORA ACCIDENTE:	12:30 HRS
        		6.  FECHA AVISO ACCIDENTE:	07-11-2024
        		7.  SECCIÓN:	PERECIBLES
        		8. CARGO:	OPERADOR PERECIBLES
        		9. ANTIGÜEDAD EN EL CARGO:	11 AÑOS
        		10. ZONA DEL CUERPO LESIONADA:	DEDO MEÑIQUE MANO DERECHA
        		11. TIPO DE ACCIDENTE: 	GOLPE CONTRA
        		12.TAREA REALIZADA:	TRASLADO DE MERCADERIA 
        La colaboradora antes individualizada quien se desempeña como operador perecible, se encontraba trasladando jugos a bodega con carro de supermercado cuando, al pasar por pasillo de trastienda, se golpea el dedo meñique de la mano derecha con gaveta de Red Húmeda que se encontraba abierta generándole un corte en la zona antes mencionada. """

        if st.button('🧠 Ejecutar IA'):
            # Construir prompt inicial si no está definido
            if not st.session_state.get('initial_story'):
                st.session_state.initial_story = "\n".join([
                    f"Fecha: {st.session_state.fecha_accidente}",
                    f"Hora: {st.session_state.hora_accidente}",
                    f"Actividad: {st.session_state.actividad}",
                    f"Local: {st.session_state.nombre_local}",
                    f"Lugar: {st.session_state.lugar_accidente}",
                    f"Lesión: {st.session_state.naturaleza_lesion}",
                    f"Tarea: {st.session_state.tarea}",
                    f"Operación: {st.session_state.operacion}",
                    f"Contexto: {st.session_state.contexto}",
                    f"Circunstancias: {st.session_state.circunstancias}"
                ])
            # Generar relato inicial por IA
            st.session_state.relatof = qm.generar_pregunta('relato_inicial', st.session_state.initial_story)
            # Marcar inicio de flujo de preguntas
            st.session_state['invest_active'] = True
            st.rerun()
    else:
        if st.session_state.get('invest_active'):
            app = InvestigationApp(st.secrets.get("OPENAI_API_KEY", ""))
            app.run()