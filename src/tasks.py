from crewai import Task
from .agents import explorador_agent, logistico_agent, disenador_agent, ocio_agent

# Tarea 1: Investigación Completa (Vuelos + Hotel + Transporte Local + Eventos)
tarea_investigacion = Task(
    description="""
    Eres el encargado de la logística base para un viaje a {destino} desde {origen} en las fechas: {fechas} ({dias} días).
    
    ESTA ES LA PARTE CRÍTICA (Se realista):
    1. **Vuelos (CRUCIAL):** - Busca vuelos IDA Y VUELTA directos o con escalas cortas.
       - Prioriza aerolíneas confiables (Ej: Iberia, British Airways, Lufthansa, Air France) o Low-Cost con maleta incluida.
       - IGNORA precios gancho tipo "desde 10€". Busca un precio MEDIO realista para esas fechas (temporada alta).
       - Escribe en el informe: "Aerolínea recomendada: X, Precio aprox: Y €".
       
    2. **Alojamiento:** Busca hoteles de 4 estrellas céntricos (Puntuación superior a 8/10). Da el precio TOTAL por las {dias} noches.
    
    3. **Transporte Local:** Investiga PRECIOS de Metro, Uber/Taxi aeropuerto-centro y tarjetas turísticas.
    
    4. **Agenda Cultural:** Busca "Events in {destino} {fechas}". 
    
    5. **Clima:** Previsión detallada.
    """,
    expected_output="Informe realista con vuelos de aerolíneas reconocidas (ida/vuelta), hotel 4* y transporte.",
    agent=explorador_agent
)

# Tarea 2: Ocio y Rutas
tarea_ocio = Task(
    description="""
    Tu misión es llenar {dias} días de contenido. NO te limites a 3 cosas.
    
    1. Busca al menos 10 Puntos de Interés (Monumentos, Museos, Parques, Barrios de moda).
    2. Busca 5 Restaurantes/Cafeterías con encanto (desayuno, comida, cena).
    3. Agrupa estos lugares por ZONAS GEOGRÁFICAS para que el itinerario tenga sentido (ej: Día 1 Zona Centro, Día 2 Zona Sur).
    4. Consigue los PRECIOS de las entradas de los sitios principales.
    """,
    expected_output="Lista extensa de actividades agrupadas por zonas y restaurantes con precios.",
    agent=ocio_agent,
    context=[tarea_investigacion]
)

# Tarea 3: Presupuesto Detallado
tarea_presupuesto = Task(
    description="""
    Calcula el presupuesto TOTAL riguroso.
    
    Usa la 'CalculatorTool'.
    Desglose necesario:
    - Vuelos
    - Alojamiento (Total por todas las noches)
    - Transporte (30€/día x persona aprox si no tienes datos exactos)
    - Comidas (Calcula 50€/día x persona media)
    - Actividades (Suma las entradas encontradas)
    
    Calcula el TOTAL FINAL.
    """,
    expected_output="Tabla de costes desglosada línea por línea y suma final.",
    agent=logistico_agent,
    context=[tarea_investigacion, tarea_ocio]
)

# Tarea 4: Guía Final
tarea_itinerario = Task(
    description="""
    Usa la 'FileReadTool' para leer 'preferencias.txt'.
    
    Genera la GUÍA DE VIAJE DEFINITIVA. Actúa como un Travel Blogger experto y carismático.
    Tu objetivo es vender la experiencia. Escribe con detalle, no hagas listas secas.
    
    REGLAS DE ORO PARA EL ITINERARIO:
    1. Debes cubrir TODOS los {dias} días.
    2. Para CADA día, debes estructurar: MAÑANA, COMIDA, TARDE y NOCHE.
    3. Describe el ambiente, no solo el nombre del sitio. (Ej: "Pasea por el mercado de Camden mientras huele a comida callejera...").
    
    ESTRUCTURA DE SALIDA (MARKDOWN):
    
    # ✈️ LA GRAN AVENTURA EN {destino} ({fechas})
    
    ## 💰 Tu Presupuesto Detallado
    (Tabla completa del agente logístico)
    
    ## 🚕 Moverse como un Local
    (Información de transporte del explorador)
    
    ## 🗺️ ITINERARIO DÍA A DÍA (DETALLADO)
    
    ### 📅 DÍA 1: [Ponle un Título Épico, ej: "Aterrizaje y primera toma de contacto"]
    * 🌅 **09:00 - Mañana:** [Describe qué hacer, qué ver y por qué mola].
    * 🍽️ **14:00 - Dónde comer:** [Recomendación del agente de ocio].
    * ☀️ **16:00 - Tarde:** [Siguiente actividad o paseo por barrio].
    * 🌙 **21:00 - Noche:** [Plan nocturno: cena, paseo o mirador].
    
    (REPITE ESTA ESTRUCTURA EXACTA PARA LOS {dias} DÍAS. ¡NO RESUMAS!)
    
    ## 🎒 Consejos Finales y Maleta
    * Tips de visado, enchufes y ropa.
    
    ---
    *Planificado por tu Agente IA de Viajes*
    """,
    expected_output="Guía Markdown MUY extensa, descriptiva y detallada día a día.",
    agent=disenador_agent,
    context=[tarea_investigacion, tarea_ocio, tarea_presupuesto]
)