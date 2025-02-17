from openai import OpenAI
import json
import openai
import os

client = OpenAI(
  api_key=""
)

def compare_profiles(file_name):
    # 2. Carga los archivos JSON
    with open(file_name, 'r', encoding='utf-8') as f:
        profile = json.load(f)

    # 3. Convierte los perfiles a string para incluirlos en el prompt
    profile_str = json.dumps(profile, indent=2, ensure_ascii=False)
    categoria = profile["Categoria"]

    perfiles = {}
    if categoria == "joven":
        ruta = f"perfiles\elder"
    else:
        ruta = f"perfiles\joven"

    for i in range(1,6):
        with open(ruta+f"_{i}.json", 'r', encoding='utf-8') as f:
            candidate_profile = json.load(f)
        candidate_profile_jsn = json.dumps(candidate_profile, indent=2, ensure_ascii=False)

        perfiles[f"cantidato_{i}"] = candidate_profile_jsn

    # 4. Crea el mensaje de sistema (contexto) y el prompt para el usuario

    system_prompt = (
        "Eres un experto analizador en relaciones interpersonales. Te proporcionaré un perfil en formato JSON y lo comparas con los otros perfiles de la variable 'perfiles':"
        "si la variable 'categoria' es joven, los compararas con perfiles de viejos (llamados elders), y el caso opuesto. Tu tarea es compararlos "
        "para determinar si, en función de sus caracteristicas descritas en el perfil, "
        "podrían llevarse bien y lograr una conexion juntos. Detalla que posibles actividades podrian realizar juntos y que temas de conversación tienen en común. En caso la categoría sea joven también detalla algunos datos interesantes de los elders que podrían ser del interés del joven. En caso la categoría sea elder, detalla algunos aspectos que a los elders les atraerían para conocer a los jóvenes. Proporciona un razonamiento claro y conciso. Responde en español."
    )

    user_prompt = (
        f"Aquí está el perfil principal:\n\n"
        f"Perfil {categoria}:\n{profile_str}\n\n"
        f"Aquí están los candidatos:\n{perfiles}\n\n"
        f"Explicame con cuáles de la otra categoría se llevaría mejor puntuandolos del 1 al 100. Siendo 1 que no se llevarian bien entre ellos y 100 que tendrian la posibilidad de llevarse muy bien y realizar varias actividades juntos. Explica tu razonamiento y selecciona los mejores 3." )

    # 5. Llamada a la API de OpenAI usando ChatCompletion (GPT-3.5/4, etc.)
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # o "gpt-4" si tienes acceso, o el modelo que prefieras
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    
    # 6. Devuelve la respuesta del asistente
    return response.choices[0].message.content


if __name__ == "__main__":
    # Asumiendo que "perfil_joven.json" y "perfil_mayor.json" están en la misma carpeta
    result = compare_profiles("perfiles\elder_5.json")
    print("Respuesta del modelo:\n")
    print(result)