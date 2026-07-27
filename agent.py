import os
import streamlit as st
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from quant_engine import ejecutar_motor_cuantitativo

class SAAParameters(BaseModel):
    perfil: str = Field(description="Perfil de riesgo del inversor")
    horizonte_anos: int = Field(description="Horizonte temporal en años")

@tool("ejecutar_simulacion_portafolio", args_schema=SAAParameters)
def ejecutar_simulacion_portafolio(perfil: str, horizonte_anos: int) -> str:
    """Ejecuta el motor cuantitativo de asignación de activos, descarga precios reales y simula escenarios."""
    if perfil == "Conservador":
        pesos = {"Renta Fija Global": 70, "Cash": 20, "Renta Variable Global": 10}
    elif perfil == "Moderado":
        pesos = {"Renta Fija Global": 45, "Renta Variable Global": 40, "Real Estate / Infra": 10, "Cash": 5}
    else:
        pesos = {"Renta Variable Global": 65, "Alternativos / Commodities": 20, "Renta Fija Global": 15}
        
    resultados = ejecutar_motor_cuantitativo(pesos, horizonte_anos)
    return f"Resultados cuantitativos procesados: {resultados}"

# Obtención de secretos (Soporta entorno local .env y Streamlit Secrets en la nube)
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")

model = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key,
    model="llama-3.3-70b-versatile",
    temperature=0
)

tools = [ejecutar_simulacion_portafolio]
agent_executor = create_react_agent(model, tools)
