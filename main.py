from crewai import Crew, Process
from src.agents import explorador_agent, logistico_agent, disenador_agent, llm
from src.tasks import tarea_investigacion, tarea_presupuesto, tarea_itinerario
import sys
import os

def generar_preferencias():
    print("\n📝 -- PERFIL DEL VIAJERO --")
    estilo = input("1. ¿Qué estilo de viaje buscas? (Mochilero, Lujo, Aventura...): ")
    comida = input("2. ¿Gustos de comida? (Vegano, Local, Internacional...): ")
    hobbies = input("3. ¿Intereses? (Museos, Trekking, Fiesta, Historia...): ")
    
    contenido = f"""
    PERFIL DEL CLIENTE:
    - Estilo: {estilo}
    - Comida: {comida}
    - Intereses: {hobbies}
    """
    
    with open("preferencias.txt", "w", encoding="utf-8") as f:
        f.write(contenido)
    
    print("✅ Perfil guardado.\n")


# --- Configuración de la Crew ---
travel_crew = Crew(
    agents=[explorador_agent, logistico_agent, disenador_agent],
    tasks=[tarea_investigacion, tarea_presupuesto, tarea_itinerario],
    process=Process.sequential, 
    #manager_llm=llm, 
    verbose=True,
    memory=False,   
    max_rpm=10      
)

def run():
    print("\n✈️  SMART TRAVEL AGENT v3.0 (Full Personalized)")
    print("===============================================")
    
    # 1. Generamos perfil
    generar_preferencias()
    
    # 2. Pedimos datos del viaje
    print("🌍 -- DATOS DEL VIAJE --")
    destino_input = input("¿Destino?: ")
    origen_input = input("¿Ciudad de Origen? (Para vuelos): ")
    dias_input = input("¿Duración (días)?: ")
    
    inputs = {
        'destino': destino_input,
        'origen': origen_input,
        'dias': dias_input
    }
    
    print(f"\n🚀 Iniciando agentes... Buscando vuelos {origen_input} -> {destino_input}")
    
    try:
        resultado = travel_crew.kickoff(inputs=inputs)
        
        nombre_archivo = f"Plan_{destino_input}_desde_{origen_input}.md"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(str(resultado))
            
        print(f"\n✨ ¡PLAN COMPLETADO! Guardado en: {nombre_archivo}")
        print("\n################ RESULTADO ################\n")
        print(resultado)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run()