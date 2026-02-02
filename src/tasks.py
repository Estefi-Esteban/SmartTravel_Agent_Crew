from crewai import Task
from .agents import explorador_agent, logistico_agent, disenador_agent, ocio_agent

# Tarea 1: Investigación General (Vuelos y Hotel)
tarea_investigacion = Task(
    description="""
    Investiga opciones para un viaje a {destino} saliendo desde {origen} por {dias} días.
    1. Busca precio REAL de vuelo ida/vuelta.
    2. Busca precio medio por noche de un hotel de 4 estrellas.
    3. Clima previsto para la fecha próxima.
    """,
    expected_output="Informe con precio del vuelo, precio por noche del hotel y clima.",
    agent=explorador_agent
)

# Tarea 2: Investigación de Ocio y Gastronomía 
tarea_ocio = Task(
    description="""
    Investiga actividades de pago y gastronomía en {destino}:
    1. Encuentra 3 actividades o tours IMPRESCINDIBLES (Museos, Excursiones, Entradas) y sus PRECIOS.
    2. Encuentra 3 restaurantes recomendados (gama media/alta) y el precio medio por persona.
    """,
    expected_output="Lista detallada de 3 actividades y 3 restaurantes con sus precios exactos.",
    agent=ocio_agent
)

# Tarea 3: Cálculo Total
tarea_presupuesto = Task(
    description="""
    Calcula el coste TOTAL del viaje basándote en los informes del explorador y del agente de ocio.
    
    Usa la 'CalculatorTool' para aplicar esta fórmula:
    (Precio_Vuelo) + (Precio_Hotel * {dias}) + (Suma_Precios_Actividades) + (Precio_Medio_Comidas * 2 * {dias})
    
    *Nota: Asume 2 comidas al día por el precio medio encontrado por el agente de ocio.*
    """,
    expected_output="Desglose matemático detallado y la Cifra Final del presupuesto.",
    agent=logistico_agent,
    context=[tarea_investigacion, tarea_ocio]
)

# Tarea 4: Itinerario Final
tarea_itinerario = Task(
    description="""
    1. USA LA TOOL 'FileReadTool' para leer el archivo 'preferencias.txt'.
    2. Crea una GUÍA DE VIAJE PREMIUM para {destino} basada en esas preferencias, el ocio encontrado y el presupuesto.
    
    IMPORTANTE: El formato de salida debe ser MARKDOWN ESTÉTICO siguiendo esta estructura estrictamente:
    
    # ✈️ VIAJE A {destino} - [Estilo de Viaje]
    ---
    
    ## 📊 Resumen del Presupuesto
    (Crea una tabla Markdown con los conceptos: Vuelo, Hotel, Actividades, Comidas, TOTAL)
    
    ## 🍜 Gastronomía y Ocio Recomendado
    *Aquí pon los restaurantes y actividades que encontró el agente de Ocio con sus precios.*
    
    ## 🗓️ Itinerario Día a Día
    ### Día 1: [Título del día]
    * 🌅 Mañana: ...
    * ☀️ Tarde: ...
    * 🌙 Noche: ...
    
    (Repetir para todos los días, integrando las actividades encontradas)
    
    ## 🏨 Alojamiento y Vuelos
    * **Hotel recomendado:** ...
    * **Vuelo:** ...
    
    ## 💡 Consejos Personalizados
    (Basados en las preferencias del cliente leídas del archivo)
    
    ---
    *Plan generado por SmartTravel Agent AI*
    """,
    expected_output="Guía de viaje final en formato Markdown estructurado con tablas, emojis y secciones claras.",
    agent=disenador_agent,
    context=[tarea_investigacion, tarea_ocio, tarea_presupuesto]
)