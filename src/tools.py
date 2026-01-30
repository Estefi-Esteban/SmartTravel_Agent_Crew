from crewai_tools import SerperDevTool, FileReadTool # <--- Añadimos FileReadTool
from crewai.tools import BaseTool
import os
from dotenv import load_dotenv

load_dotenv()

# --- 1. HERRAMIENTA DE BÚSQUEDA ---
search_tool = SerperDevTool()

# --- 2. HERRAMIENTA DE LECTURA DE ARCHIVOS (NUEVA) ---
file_tool = FileReadTool(file_path='preferencias.txt')

# --- 3. HERRAMIENTA DE CALCULADORA (Tu custom tool) ---
class CalculatorTool(BaseTool):
    name: str = "CalculatorTool"
    description: str = "Calcula operaciones matemáticas. Ej: '200 + 100'."

    def _run(self, operation: str) -> str:
        try:
            return str(eval(operation))
        except Exception as e:
            return "Error de cálculo"

calc_tool = CalculatorTool()