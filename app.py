import os
import pathlib
import streamlit as st
import importlib.util

anthropic_spec = importlib.util.find_spec("anthropic")
if anthropic_spec is not None:
    anthropic = importlib.import_module("anthropic")
else:
    anthropic = None


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

# Carga de variables de entorno locales (si existe .env)
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="SAA AI Agent | Institutional Portfolio Structuring",
    page_icon="💼",
    layout="wide"
)

# Inicialización segura del cliente de Anthropic
api_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", None)

if not api_key:
    st.error("No se ha detectado la ANTHROPIC_API_KEY. Configúrala en el archivo .env o en los secrets de Streamlit Cloud.")
    st.stop()

if anthropic is None:
    st.error("La librería 'anthropic' no está instalada. Ejecuta: pip install anthropic")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

# Interfaz de Usuario
st.title("💼 Strategic Asset Allocation (SAA) AI Agent")
st.markdown("Plataforma autónoma para la recomendación y estructuración de carteras institucionales basada en teoría de carteras.")

with st.sidebar:
    st.header("Parámetros del Inversor")
    horizonte = st.selectbox("Horizonte Temporal", ["Corto Plazo (< 3 años)", "Medio Plazo (3-7 años)", "Largo Plazo (> 7 años)"])
    perfil = st.selectbox("Perfil de Riesgo", ["Conservador", "Moderado", "Agresivo", "Dinámico"])
    moneda = st.selectbox("Moneda Base", ["USD", "EUR", "PEN"])
    restricciones = st.text_area("Restricciones Adicionales (Opcional)", "Ej: Sin exposición a renta variable emergente, máximo 15% en alternativos.")
    
    ejecutar = st.button("Generar Propuesta SAA", type="primary")

# Lógica del Agente
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
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.2,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_content}
                ]
            )
            
            st.success("Propuesta generada con éxito.")
            st.markdown("### Resultados del Análisis SAA")
            st.markdown(response.content[0].text)
            
        except Exception as e:
            st.error(f"Error al conectar con la API de Anthropic: {str(e)}")
else:
    st.info("Configura los parámetros en la barra lateral y presiona **'Generar Propuesta SAA'** para iniciar el análisis del agente.")
