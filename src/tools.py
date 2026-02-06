from crewai_tools import SerperDevTool, FileReadTool
from crewai.tools import BaseTool, tool
import os
from dotenv import load_dotenv

load_dotenv()

# --- 1. HERRAMIENTA DE BÚSQUEDA ---
search_tool = SerperDevTool()

# --- 2. HERRAMIENTA DE LECTURA DE ARCHIVOS ---
file_tool = FileReadTool(file_path='preferencias.txt')

# --- 3. HERRAMIENTA DE CALCULADORA ---
@tool("CalculatorTool")
def calc_tool(operation: str) -> str:
    """
    Realiza calculos matematicos. La entrada debe ser una expresion matematica 
    simple en formato string, por ejemplo: '200*7' o '5000/2'.
    """
    try:
        return str(eval(operation))
    except Exception as e:
        return f"Error al calcular: {str(e)}"
