import streamlit as st
from agent import agent_executor
from langchain_core.messages import SystemMessage, HumanMessage

st.set_page_config(
    page_title="Quantitative SAA AI Agent",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Quantitative Strategic Asset Allocation (SAA) Agent")
st.markdown("Plataforma multiagente para simulación estocástica y optimización institucional de portafolios.")

with st.sidebar:
    st.header("Parámetros del Comité")
    horizonte = st.selectbox("Horizonte Temporal (Años)", [3, 5, 10])
    perfil = st.selectbox("Perfil de Riesgo", ["Conservador", "Moderado", "Agresivo"])
    ejecutar = st.button("Ejecutar Análisis Cuantitativo", type="primary")

if ejecutar:
    with st.spinner("El agente autónomo está procesando datos de mercado y ejecutando simulaciones..."):
        prompt = f"Genera un informe SAA técnico para un perfil {perfil} a un horizonte de {horizonte} años. Debes ejecutar la herramienta cuantitativa de simulación obligatoriamente."
        
        try:
            response = agent_executor.invoke({
                "messages": [
                    SystemMessage(content="Eres un Director de Inversiones cuantitativo senior. Analiza los outputs de las herramientas con rigor técnico, emite conclusiones claras y estructúralas bajo estándares de gestión de activos."),
                    HumanMessage(content=prompt)
                ]
            })
            
            st.success("Análisis completado con éxito.")
            
            for message in response["messages"]:
                if message.type == "ai" and message.content:
                    st.markdown(message.content)
                elif message.type == "tool":
                    with st.expander("📊 Datos del Motor Cuantitativo (Tool Output)"):
                        st.code(message.content)
                        
        except Exception as e:
            st.error(f"Error en la ejecución del agente: {str(e)}")
else:
    st.info("Configura los parámetros en la barra lateral y presiona **'Ejecutar Análisis Cuantitativo'**.")
