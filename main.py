import os
from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from src.agents import explorador_agent, logistico_agent, disenador_agent, ocio_agent
from src.tasks import tarea_investigacion, tarea_ocio, tarea_presupuesto, tarea_itinerario

load_dotenv()

def run():
    print("🤖 --- BIENVENIDO A SMARTTRAVEL AGENT --- 🤖")
    print("Configurando tu equipo de agentes expertos...")
    
    # 1. Definir la Crew con los agentes y tareas
    travel_crew = Crew(
        agents=[explorador_agent, ocio_agent, logistico_agent, disenador_agent],
        tasks=[tarea_investigacion, tarea_ocio, tarea_presupuesto, tarea_itinerario],
        process=Process.sequential,
        verbose=True
    )

    # 2. Pedir datos al usuario
    print("\n📝 Por favor, introduce los detalles de tu viaje:")
    origen_input = input("📍 Ciudad de Origen: ")
    destino_input = input("✈️ Ciudad de Destino: ")
    fechas_input = input("📅 Fechas exactas (ej: 10 al 15 de Agosto): ")
    dias_input = input("⏳ Duración (nº de días): ")

    inputs = {
        'origen': origen_input,
        'destino': destino_input,
        'fechas': fechas_input,
        'dias': dias_input
    }

    print("\n🚀 Iniciando la planificación... Los agentes están trabajando.")
    
    # 3. Ejecutar la Crew
    try:
        resultado = travel_crew.kickoff(inputs=inputs)
        
        # 4. Guardar resultado en Markdown estético
        nombre_archivo = f"Plan_{destino_input}_desde_{origen_input}.md"
        nombre_archivo = nombre_archivo.replace(" ", "_")
        
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(str(resultado))
            
        print(f"\n✅ ¡Misión cumplida! Tu plan de viaje está listo en: {nombre_archivo}")
        
    except Exception as e:
        print(f"\n❌ Ocurrió un error durante la ejecución: {e}")

if __name__ == "__main__":
    run()