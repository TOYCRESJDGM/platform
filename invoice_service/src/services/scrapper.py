import requests
from src.utils.settings import URL_SCRAPPER

def call_scrapper(cufe):
    url_scrapper = URL_SCRAPPER
    data = {'cufe': cufe}
    try:
        response = requests.post(url_scrapper, json=data)

        if response.status_code == 200:
            
            datos_respuesta = response.json()
            print("Respuesta del servicio:", datos_respuesta)
        else:
            print("Error al llamar al servicio. Código de estado:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error de conexión:", e)