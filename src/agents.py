from crewai import Agent, LLM
from .tools import search_tool, calc_tool, file_tool # <--- Importamos la nueva tool
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# 1. EXPLORADOR (Busca datos generales)
explorador_agent = Agent(
    role="Explorador de Destinos",
    goal="Encontrar clima, eventos y precios base en {destino}",
    backstory="Eres un experto rastreador de información turística en tiempo real.",
    tools=[search_tool], 
    verbose=True,
    llm=llm,
    allow_delegation=False
)

# 2. LOGÍSTICO (Calcula números)
logistico_agent = Agent(
    role="Analista de Presupuestos",
    goal="Calcular el coste total exacto usando matemáticas",
    backstory="Eres un contable estricto. Usas la calculadora para dar cifras exactas.",
    tools=[calc_tool], # Solo necesita calcular lo que le den
    verbose=True,
    llm=llm,
    allow_delegation=False
)

# 3. DISEÑADOR (Personaliza el viaje - EL QUE USA LA NUEVA TOOL)
disenador_agent = Agent(
    role="Personal Travel Concierge",
    goal="Diseñar un itinerario ÚNICO basado en las PREFERENCIAS del cliente",
    backstory="""Tu misión es leer el archivo de preferencias del cliente y adaptar 
    toda la información del explorador para crear un viaje a medida. 
    Si al cliente no le gustan los museos, NO pongas museos.""",
    tools=[file_tool], # <--- ¡Aquí está la magia! Lee el archivo local
    verbose=True,
    llm=llm,
    allow_delegation=False
)