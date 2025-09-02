from django.shortcuts import render
import requests
import base64
import os
from datetime import datetime
from django.conf import settings

ATRIBUTOS = sorted([
    "5_o_Clock_Shadow", "Arched_Eyebrows", "Attractive", "Bags_Under_Eyes", "Bald", "Bangs",
    "Big_Lips", "Big_Nose", "Black_Hair", "Blond_Hair", "Blurry", "Brown_Hair", "Bushy_Eyebrows",
    "Chubby", "Double_Chin", "Eyeglasses", "Goatee", "Gray_Hair", "Heavy_Makeup", "High_Cheekbones",
    "Male", "Mouth_Slightly_Open", "Mustache", "Narrow_Eyes", "No_Beard", "Oval_Face", "Pale_Skin",
    "Pointy_Nose", "Receding_Hairline", "Rosy_Cheeks", "Sideburns", "Smiling", "Straight_Hair",
    "Wavy_Hair", "Wearing_Earrings", "Wearing_Hat", "Wearing_Lipstick", "Wearing_Necklace",
    "Wearing_Necktie", "Young"
])

# Diccionario de traducción inglés-español para los atributos
ATRIBUTOS_ES = {
    "5_o_Clock_Shadow": "Barba de mediodía",
    "Arched_Eyebrows": "Cejas arqueadas",
    "Attractive": "Atractivo/a",
    "Bags_Under_Eyes": "Ojeras",
    "Bald": "Calvo",
    "Bangs": "Flequillo",
    "Big_Lips": "Labios grandes",
    "Big_Nose": "Nariz grande",
    "Black_Hair": "Cabello negro",
    "Blond_Hair": "Cabello rubio",
    "Blurry": "Borroso",
    "Brown_Hair": "Cabello castaño",
    "Bushy_Eyebrows": "Cejas pobladas",
    "Chubby": "Gordito/a",
    "Double_Chin": "Papada",
    "Eyeglasses": "Gafas",
    "Goatee": "Perilla",
    "Gray_Hair": "Cabello gris",
    "Heavy_Makeup": "Maquillaje abundante",
    "High_Cheekbones": "Pómulos altos",
    "Male": "Hombre",
    "Mouth_Slightly_Open": "Boca entreabierta",
    "Mustache": "Bigote",
    "Narrow_Eyes": "Ojos entrecerrados",
    "No_Beard": "Sin barba",
    "Oval_Face": "Cara ovalada",
    "Pale_Skin": "Piel pálida",
    "Pointy_Nose": "Nariz puntiaguda",
    "Receding_Hairline": "Entradas pronunciadas",
    "Rosy_Cheeks": "Mejillas sonrosadas",
    "Sideburns": "Patillas",
    "Smiling": "Sonriente",
    "Straight_Hair": "Cabello liso",
    "Wavy_Hair": "Cabello ondulado",
    "Wearing_Earrings": "Con pendientes",
    "Wearing_Hat": "Con sombrero",
    "Wearing_Lipstick": "Con lápiz labial",
    "Wearing_Necklace": "Con collar",
    "Wearing_Necktie": "Con corbata",
    "Young": "Joven"
}

def index(request):
    imagenes_generadas = []

    if request.method == "POST":
        seleccionados = request.POST.getlist("atributos")
        prompt = ", ".join(seleccionados)

        rostros_dir = os.path.join(settings.MEDIA_ROOT, "rostros")
        os.makedirs(rostros_dir, exist_ok=True)

        for i in range(3):  # Generar 9 imágenes
            try:
                response = requests.post(
                    "https://2c0070ca1b82.ngrok-free.app/generar/",
                    json={"prompt": prompt}
                )
                if response.status_code == 200:
                    img_base64 = response.json()["imagen"]
                    filename = f"imagen_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{i}.png"
                    filepath = os.path.join(rostros_dir, filename)
                    with open(filepath, "wb") as f:
                        f.write(base64.b64decode(img_base64))
                    imagenes_generadas.append(f"rostros/{filename}")
                else:
                    print("Error en la respuesta del servidor:", response.text)
            except Exception as e:
                print("Error de conexión con el servidor:", str(e))

    atributos_legibles = [(a, ATRIBUTOS_ES.get(a, a.replace("_", " "))) for a in ATRIBUTOS]
    return render(request, "index.html", {"atributos": atributos_legibles, "imagenes_generadas": imagenes_generadas})

def galeria(request):
    rostros_dir = os.path.join(settings.MEDIA_ROOT, "rostros")
    if not os.path.exists(rostros_dir):
        images = []
    else:
        images = [f"rostros/{img}" for img in os.listdir(rostros_dir) if img.endswith('.png') or img.endswith('.jpg')]
    return render(request, "galeria.html", {"images": images})

def landing(request):
    return render(request, "landing.html")