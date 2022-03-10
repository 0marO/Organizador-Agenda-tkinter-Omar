
import requests
import geocoder
from geopy.geocoders import Nominatim
import time

# sintaxis para sacar info de data_archivo_json: data_archivo_json[wheather][0][main]  ---->   "Clouds"

def obtener_provincia_con_lat_lng(latitude, longitude, language="en"):
    """Esta función recibe latitud y longitud y devuelve el nombre de la provincia en la que estas"""

    app = Nominatim(user_agent="omar321321")
    # build coordinates string to pass to reverse() function
    coordinates = f"{latitude}, {longitude}"
    # sleep for a second to respect Usage Policy
    #time.sleep(0.03)

    return app.reverse(coordinates, language=language).raw['address']['state']




def obt_clima ():
    g = geocoder.ip('me')

    lat_actual = g.lat
    lng_actual = g.lng
    api_owmap_omar = "http://api.openweathermap.org/data/2.5/weather?lat="+f"{lat_actual}"+"&lon="+ f"{lng_actual}"+"&appid=a6fbfb23b92c72d5288cd277c9598d33"
    data_archivo_json = requests.get(api_owmap_omar).json()

    id_clima = data_archivo_json['weather'][0]['id']
    clima_visible = data_archivo_json['weather'][0]['main']
    descripcion_clima = data_archivo_json['weather'][0]['description']
    icono_clima_actual = data_archivo_json['weather'][0]['icon']
    temp_actual = (data_archivo_json['main']['temp']) - 273.15  # pasado a ºC
    temp_min = (data_archivo_json['main']['temp_min']) - 273.15  # pasado a ºC
    temp_max = (data_archivo_json['main']['temp_max']) - 273.15  # pasado a ºC
    humedad = data_archivo_json["main"]["humidity"]
    viento = data_archivo_json["wind"]['speed']
    sigla_pais = data_archivo_json["sys"]['country']
    nombre_localidad = data_archivo_json['name']
    ciudad = obtener_provincia_con_lat_lng(lat_actual,lng_actual)

    return id_clima,clima_visible,descripcion_clima,icono_clima_actual,temp_actual,temp_min,temp_max,humedad,viento,sigla_pais,nombre_localidad,ciudad


