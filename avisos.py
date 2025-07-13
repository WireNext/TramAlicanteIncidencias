import requests
from bs4 import BeautifulSoup
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.tramalacant.es/wp-content/themes/metrovalencia/functions/ajax-no-wp.php"

payload = {
    "action": "formularios_ajax",
    "data": "action=comprobar-usuario&lang=es"
}

try:
    response = requests.post(url, data=payload, verify=False)  # <- Aquí
    response.raise_for_status()
    json_data = response.json()
    html_alertas = json_data.get("htmlAlertas", "")

    soup = BeautifulSoup(html_alertas, "html.parser")

    avisos = []

    for alerta in soup.select(".feed-noticias.alerta-general"):
        lineas = alerta.select(".linea img")
        lineas_texto = [img['alt'] for img in lineas]
        texto_alerta = alerta.select_one(".noticia-min span").get_text(strip=True)
        avisos.append({
            "lineas_afectadas": lineas_texto,
            "texto_alerta": texto_alerta
        })

    with open("avisos_tramalacant.json", "w", encoding="utf-8") as f:
        json.dump(avisos, f, ensure_ascii=False, indent=4)

    print(f"{len(avisos)} avisos guardados en avisos_tramalacant.json")

except Exception as e:
    print("Error al obtener o procesar los avisos:", e)
