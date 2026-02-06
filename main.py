import os
from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from src.agents import explorador_agent, logistico_agent, disenador_agent, ocio_agent, llm
from src.tasks import tarea_investigacion, tarea_ocio, tarea_presupuesto, tarea_itinerario

load_dotenv()

def run():
    print("🤖 --- BIENVENIDO A SMARTTRAVEL AGENT --- 🤖")
    
    # --- PASO 1: GENERACIÓN DEL PERFIL (PREFERENCIAS) ---
    print("\n👤 Primero, vamos a configurar tu PERFIL DE VIAJERO personalizado.")
    print("Por favor, responde a estas tres preguntas breves:")
    
    estilo_input = input("1. ¿Cuál es tu estilo de viaje? (Ej: Aventura, Relax, Lujo, Mochilero...): ")
    comida_input = input("2. ¿Qué preferencias de comida tienes? (Ej: Callejera, Vegana, Alta cocina...): ")
    intereses_input = input("3. ¿Tus intereses principales? (Ej: Fotografía, Historia, Fiesta, Museos...): ")

    texto_preferencias = f"""
    PERFIL DEL CLIENTE:
    - Estilo: {estilo_input}
    - Comida: {comida_input}
    - Intereses: {intereses_input}
    """

    try:
        with open('preferencias.txt', 'w', encoding='utf-8') as f:
            f.write(texto_preferencias)
        print("✅ ¡Perfil guardado! Los agentes tendrán en cuenta tus gustos.")
    except Exception as e:
        print(f"⚠️ Advertencia: No se pudo guardar el archivo de preferencias: {e}")

    # --- PASO 2: CONFIGURACIÓN DE LA CREW ---
    print("\n⚙️ Configurando tu equipo de agentes expertos...")
    
    travel_crew = Crew(
        agents=[explorador_agent, ocio_agent, logistico_agent, disenador_agent],
        tasks=[tarea_investigacion, tarea_ocio, tarea_presupuesto, tarea_itinerario],
        # PARA MODO JERARQUICO PONER process=Process.hierarchical y descomentar manager_llm=llm
        process=Process.sequential,
        #manager_llm=llm,
        verbose=True
    )

    # --- PASO 3: DETALLES DEL VIAJE ---
    print("\n📝 Por favor, introduce los detalles logísticos del viaje:")
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
    
    # --- PASO 4: EJECUCIÓN ---
    try:
        resultado = travel_crew.kickoff(inputs=inputs)
        
        nombre_archivo = f"Plan_{destino_input}_desde_{origen_input}.md"
        nombre_archivo = nombre_archivo.replace(" ", "_")
        
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(str(resultado))
            
        print(f"\n✅ ¡Misión cumplida! Tu plan de viaje está listo en: {nombre_archivo}")
        print("¡Disfruta de tu viaje diseñado por IA! 🌍✈️")
        
    except Exception as e:
        print(f"\n❌ Ocurrió un error durante la ejecución: {e}")

if __name__ == "__main__":
    run()