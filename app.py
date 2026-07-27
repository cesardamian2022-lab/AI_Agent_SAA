import os
import pathlib
import streamlit as st
import importlib.util

groq_spec = importlib.util.find_spec("openai")
if groq_spec is not None:
    openai = importlib.import_module("openai")
else:
    openai = None

def load_dotenv():
    env_path = pathlib.Path(".env")
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        if not line or line.strip().startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if sep != "=":
            continue
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

load_dotenv()

st.set_page_config(
    page_title="SAA AI Agent | Institutional Portfolio Structuring",
    page_icon="💼",
    layout="wide"
)

# Obtenemos la API Key gratuita de Groq
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

if not api_key:
    st.error("No se ha detectado la GROQ_API_KEY. Obtén una gratis en console.groq.com y configúrala.")
    st.stop()

if openai is None:
    st.error("La librería 'openai' no está instalada. Ejecuta: pip install openai")
    st.stop()

# Configuración del cliente apuntando a Groq (Compatible con SDK de OpenAI)
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

st.title("💼 Strategic Asset Allocation (SAA) AI Agent")
st.markdown("Plataforma autónoma para la recomendación y estructuración de carteras institucionales basada en teoría de carteras.")

with st.sidebar:
    st.header("Parámetros del Inversor")
    horizonte = st.selectbox("Horizonte Temporal", ["Corto Plazo (< 3 años)", "Medio Plazo (3-7 años)", "Largo Plazo (> 7 años)"])
    perfil = st.selectbox("Perfil de Riesgo", ["Conservador", "Moderado", "Agresivo", "Dinámico"])
    moneda = st.selectbox("Moneda Base", ["USD", "EUR", "PEN"])
    restricciones = st.text_area("Restricciones Adicionales (Opcional)", "Ej: Sin exposición a renta variable emergente, máximo 15% en alternativos.")
    
    ejecutar = st.button("Generar Propuesta SAA", type="primary")

if ejecutar:
    with st.spinner("Analizando restricciones y calculando asignación óptima..."):
        system_prompt = """
        Eres un Director de Inversiones senior y Arquitecto Cuantitativo especializado en Strategic Asset Allocation (SAA).
        Tu objetivo es proponer una asignación de activos estratégica óptima y robusta (Renta Variable Global, Renta Fija Investment Grade/High Yield, Real Estate/Infrastructure, Cash) 
        alineada estrictamente con el perfil de riesgo, horizonte temporal y moneda base provistos.
        
        Estructura tu respuesta técnica de la siguiente manera:
        1. **Resumen Ejecutivo de la Tesis de Inversión**
        2. **Matriz de Asignación Estratégica (Pesos porcentuales exactos que sumen 100%)**
        3. **Justificación Cuantitativa y Teórica (Diversificación Markowitz / Control de Volatilidad)**
        4. **Monitoreo y Rebalanceo Sugerido**
        """
        
        user_content = f"""
        Genera una propuesta de SAA con las siguientes características:
        - Perfil de Riesgo: {perfil}
        - Horizonte: {horizonte}
        - Moneda Base: {moneda}
        - Restricciones: {restricciones}
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ]
            )
            
            st.success("Propuesta generada con éxito.")
            st.markdown("### Resultados del Análisis SAA")
            st.markdown(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Error al conectar con la API: {str(e)}")
else:
    st.info("Configura los parámetros en la barra lateral y presiona **'Generar Propuesta SAA'** para iniciar el análisis del agente.")
