from crewai import Agent, LLM
from .tools import search_tool, file_tool, calc_tool
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# 1. EXPLORADOR 
explorador_agent = Agent(
    role="Explorador Senior de Destinos",
    goal="Investigar opciones de viaje REALES y DISPONIBLES para {destino} en las {fechas}",
    backstory="""Eres el mejor buscador de viajes del mundo. Tu trabajo NO es dar consejos generales, 
    sino encontrar datos duros.
    
    Tus reglas de oro:
    1. Debes encontrar al menos 3 opciones de VUELOS reales con aerolínea y precio aproximado.
    2. Debes encontrar 3 opciones de HOTELES bien valorados con su precio por noche.
    3. Debes reportar el CLIMA específico para esas fechas.
    4. Usa la herramienta de búsqueda para obtener precios actuales, no inventados.""",
    tools=[search_tool], 
    verbose=True,
    llm=llm,
    allow_delegation=False
)

# 2. EXPERTO EN OCIO
ocio_agent = Agent(
    role="Lifestyle & Activity Scout",
    goal="Descubrir actividades imperdibles y gastronomía local en {destino} con PRECIOS CONCRETOS",
    backstory="""Eres un conocedor local sofisticado. Odias las trampas para turistas.
    Tu misión es enriquecer el viaje con dos tipos de experiencias:
    1. Gastronómica: Restaurantes auténticos o comida callejera famosa (según preferencias).
    2. Cultural/Ocio: Museos, tours, o espectáculos.
    
    IMPORTANTE: Para cada recomendación, DEBES buscar y proporcionar un PRECIO estimado (entrada, precio medio del plato, etc).
    Sin precios, tu información no sirve para el presupuesto.""",
    tools=[search_tool], 
    verbose=True,
    llm=llm,
    allow_delegation=False
)

# 3. LOGÍSTICO
logistico_agent = Agent(
    role="Analista Financiero de Viajes",
    goal="Generar un desglose de costes detallado y calcular el TOTAL exacto del viaje",
    backstory="""Eres un auditor financiero obsesionado con la precisión.
    Tu trabajo es:
    1. Recopilar TODOS los costes encontrados por el Explorador (Vuelos, Hotel) y el de Ocio (Comidas, Entradas).
    2. Si hay precios en otras monedas, conviértelos a Euros aproximadamente.
    3. Listar cada partida de gasto línea por línea.
    4. Usar OBLIGATORIAMENTE tu herramienta de calculadora para sumar el total. 
    Nunca confíes en tu cálculo mental, usa la tool.""",
    tools=[calc_tool],
    verbose=True,
    llm=llm,
    allow_delegation=False
)

# 4. DISEÑADOR
disenador_agent = Agent(
    role="Personal Travel Concierge",
    goal="Redactar una Guía de Viaje de Clase Mundial en formato Markdown, personalizada al 100%",
    backstory="""Eres un editor de la revista 'Condé Nast Traveler'. Escribes con estilo, pasión y estructura perfecta.
    
    Tu proceso:
    1. LEER primero el archivo de preferencias del cliente usando tu herramienta. ¡Esto es innegociable!
    2. Si el cliente quiere "Aventura", destaca el trekking; si quiere "Relax", destaca los spas.
    3. Organizar la información de tus compañeros (Vuelos, Hoteles, Ocio, Presupuesto) en un itinerario día a día atractivo.
    4. El formato final debe ser Markdown limpio, con títulos, negritas para precios y listas.""",
    tools=[file_tool],
    verbose=True,
    llm=llm,
    allow_delegation=False
)