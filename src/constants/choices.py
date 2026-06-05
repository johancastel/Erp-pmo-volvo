# src/constants/choices.py

TECNICOS_OPCIONES = sorted([
    "Juan Camilo Diaz", "Diego Vargas", "Yeudy Lopez", "Jose Gil", "Manuel Rodriguez",
    "Santiago Acosta", "Adolfo Abello", "Antonio Robayo", "Cristian Caicedo", "Jefferson Stiven Gutierrez",
    "Jhon Cardenas", "Jorge Guerra", "Jhoston Harry Roa", "Juan Ramos", "Sebastian Moreno",
    "Manuel Cortes", "Wilmer Ferreira", "Daniel Aldana", "Edwin Gonzalez", "Harnold Guerra",
    "Jose Luis Rodrigez", "Andres Felipe Gomez", "Cristian Ayure", "Camilo Monsalve", "Brandon Castellanos",
    "Yesid Nava", "Oscar Sanchez", "Julian Lopez", "Carlos Aristizabal", "Bryan Orobajo",
    "Carlos Luque", "Ginna Salcedo", "Muguel Cucanchon", "Milton Fonseca", "Juan Ladino",
    "David Martinez", "Yeifer Cruz", "Wilmer Joya Prieto", "Alejandro Contraras", "Daniel Sepulveda",
    "Darwin Barreto", "Jefer Pinzon", "Maicol Carrion", "Fabian Andres Reyes Gomez", "Nixon Salgado",
    "Roger David Rayo", "Juan Camilo Lagunas", "Jair Morales", "Juan Jimenez", "Julian Suarez",
    "Yojans Sebastian Roncancio", "Johan Salcedo", "Cristian Hernandez", "William Guerrero", "Jose Castiblanco"
])

CHECKLIST_SI_NO = ["", "SI", "NO"]
CHECKLIST_SI_NO_NA = ["", "SI", "NO", "N/A"]
INSUMOS_CHOICES = ["", "NO", "N/A"]

import json
import os

_dir = os.path.dirname(os.path.abspath(__file__))
_json_path = os.path.join(_dir, "observaciones.json")
try:
    with open(_json_path, "r", encoding="utf-8") as f:
        OBSERVACIONES_OPCIONES = json.load(f)
except Exception:
    OBSERVACIONES_OPCIONES = []

