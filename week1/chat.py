from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

historial = [{"role": "system", "content": "Eres un asistente un poco imbecil."}]

print("Chat con IA (escribe 'salir' para terminar)")
while True:
    usuario = input("Tú: ")
    if usuario == "salir":
        break
    
    historial.append({"role": "user", "content": usuario})
    
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=1,
        messages=historial
    )
    
    mensaje_ia = respuesta.choices[0].message.content
    historial.append({"role": "assistant", "content": mensaje_ia})
    print(f"IA: {mensaje_ia}\n")