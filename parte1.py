import os
import json
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(
  api_key=""
)

class Convertidor_txt_json(BaseModel):
    Categoria: str
    Nombre: str
    Edad: int
    Personalidad: str
    Intereses: str
    Valores: str
    Estilo_de_vida: str
    Comunicacion: str
    Deportes: str
    Hobbies: str

# Nombre del archivo de entrada (definir manualmente o recibir como argumento)
filename = "perfiles_en_texto\Valeria Gómez.txt"  # Cambia esto por el nombre del archivo deseado

# Leer el contenido del archivo TXT
with open(filename, "r", encoding="utf-8") as file:
    texto = file.read()

completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure. Provide the information in spanish. Category has to be either 'elder' or 'joven' based on the age"},
        {"role": "user", "content": texto,}
    ],
    response_format=Convertidor_txt_json,
)

data_en_json = completion.choices[0].message.parsed

# Determinar la categoría
categoria = "elder" if data_en_json.Categoria.lower() == "elder" else "joven"

# Crear carpeta si no existe
os.makedirs("perfiles", exist_ok=True)

# Contar archivos existentes de la misma categoría
existing_files = [f for f in os.listdir("perfiles") if f.startswith(categoria)]
nuevo_numero = len(existing_files) + 1

# Nombre del archivo JSON
json_filename = f"perfiles/{categoria}_{nuevo_numero}.json"

# Guardar JSON en el archivo
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(data_en_json.dict(), json_file, ensure_ascii=False, indent=4)

print(f"Perfil guardado en {json_filename}")