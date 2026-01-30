from crewai import Task
from .agents import explorador_agent, logistico_agent, disenador_agent

# Tarea 1: Investigación (Añadimos el origen)
tarea_investigacion = Task(
    description="""
    Investiga un viaje a {destino} saliendo desde {origen} por {dias} días.
    1. Clima previsto para la próxima temporada.
    2. 3 Eventos culturales/sociales.
    3. Buscar precios de vuelos (ruta {origen} - {destino}) y hotel medio.
    """,
    expected_output="Informe con clima, eventos y precios base de vuelos y hoteles.",
    agent=explorador_agent
)

# Tarea 2: Cálculo (Igual, pero ahora el precio de vuelo será más preciso)
tarea_presupuesto = Task(
    description="""
    Basado en el informe del explorador:
    1. Toma el precio del vuelo ({origen} -> {destino}) y el precio del hotel por noche.
    2. USA LA HERRAMIENTA 'CalculatorTool' para: (Precio_Hotel * {dias}) + Precio_Vuelo.
    3. Dame el cálculo desglosado.
    """,
    expected_output="Cifra exacta del presupuesto total calculado.",
    agent=logistico_agent,
    context=[tarea_investigacion]
)

# Tarea 3: Personalización (Sin cambios, usa las preferencias)
tarea_itinerario = Task(
    description="""
    1. USA LA TOOL 'FileReadTool' para leer el archivo 'preferencias.txt'.
    2. Crea un itinerario para {destino} respetando esas preferencias.
    3. Incluye el presupuesto total calculado.
    """,
    expected_output="Guía de viaje final personalizada y presupuestada.",
    agent=disenador_agent,
    context=[tarea_investigacion, tarea_presupuesto]
)