from tkinter import *
from geolocalizacion import obt_clima
from constantes import *
# para crear la imagen final
from PIL import Image, ImageFont, ImageDraw


def obtener_clima_desc(id_clima):
    id_clima = str(id_clima)
    dicc_id_clima_descripcion = {'800':'Cielo despejado.',
                                 '801':'Pocas nubes.',
                                 '802':'Algunas nubes.',
                                 '803':'Cielo Nublado.',
                                 '804':'Cielo Muy Nublado.',
                                 '781':'Tornado.',
                                 '771':'Turbonada.',
                                 '762':'Cenizas Volcánicas.',
                                 '761':'Polvoreda.',
                                 '751':'Arena.',
                                 '741':'Neblina',
                                 '731':'Arena',
                                 '721':'calina.',
                                 '711':'Humo',
                                 '701':'Niebla.',
                                 '622':'Mucha nieve.',
                                 '621':'Mucha nieve.',
                                 '620':'Nieve.',
                                 '616':'Lluvia y Nieve.',
                                 '615':'Poca lluvia y Nieve.',
                                 '613':'Nieve.',
                                 '612':'Nieve.',
                                 '611':'Nieve.',
                                 '602':'Mucha Nieve.',
                                 '601':'Nieve.',
                                 '600':'Nieve.',
                                 '531':'Lluvia irregular.',
                                 '522':'Lluvia intensa.',
                                 '521':'Lluvia intensa.',
                                 '520':'Lluvia un poco intensa.',
                                 '511':'Lluvia Fía.',
                                 '504':'Lluvia Tremenda.',
                                 '503':'Lluvia importante.',
                                 '502':'Lluvia intensa.',
                                 '501':'Lluvia moderada.',
                                 '500':'Llovizna.',
                                 '321':'Llovizna.',
                                 '314':'Llovizna.',
                                 '313':'Llovizna.',
                                 '312':'Llovizna.',
                                 '311':'Llovizna.',
                                 '310':'Llovizna.',
                                 '302':'Llovizna.',
                                 '301':'Llovizna irregular.',
                                 '300':'Llovizna irregular.',
                                 '232':'Alta Tormenta loco.',
                                 '231':'Alta Tormenta loco.',
                                 '230':'Alta Tormenta loco.',
                                 '221':'Tormenta dispersa.',
                                 '212':'Alta Tormenta loco.',
                                 '211':'Alta Tormenta loco.',
                                 '210':'Tormenta liviana.',
                                 '202':'Alta Tormenta con lluvia.',
                                 '201':'Alta Tormenta con lluvia.',
                                 '200':'Alta Tormenta con poca lluvia.',}
    return dicc_id_clima_descripcion[id_clima]                 


def generar_imagen_clima():
    id_clima,clima_visible,descripcion_clima,icono_clima_actual,temp_actual,temp_min,temp_max,humedad,viento,sigla_pais,nombre_localidad,ciudad= obt_clima()

    print(id_clima)
    dicc_incono_fondo = {
        '01d.png': 'dd_R.png',
        '01n.png': 'nd_R.png',
        '02d.png': 'dn_R.png',
        '02n.png': 'nn_R.png',
        '03d.png': 'dn_R.png',
        '03n.png': 'nn_R.png',
        '04d.png': 'muy_nublado_R.png',
        '04n.png': 'muy_nublado_R.png',
        '09d.png': 'dll_R.png',
        '09n.png': 'dll_R.png',
        '10d.png': 'dll_R.png',
        '10n.png': 'dll_R.png',
        '11d.png': 'tormenta_R.png',
        '11n.png': 'tormenta_R.png',
        '13d.png': 'nieve_R.png',
        '13n.png': 'nieve_R.png',
        '50d.png': 'niebla_R.png',
        '50n.png': 'niebla_n_R.png'
    }

    nombre_imagen_icono = f'{icono_clima_actual}.png'

    # determinamos el fondo:
    imagen_fondo_clima = Image.open(CWD + f'imagenes_del_organizador\\{dicc_incono_fondo[nombre_imagen_icono]}')

    # determinamos la imagen del estado del clima:
    img_estado_clima = Image.open(CWD + f'imagenes_del_organizador\\{nombre_imagen_icono}')

    # combinamos ambas imagenes en una nueva.
    x_enfondo = -20
    y_enfondo = -12
    imagen_fondo_clima.paste(img_estado_clima, (x_enfondo, y_enfondo), img_estado_clima)
    imagen_fondo_clima.save(CWD + 'imagenes_del_organizador\\NewImg.png',"PNG")

    # editamos la imagen insertando texto con la info del clima.
    imagen_para_escribir = Image.open(CWD + 'imagenes_del_organizador\\NewImg.png')
    edit_image = ImageDraw.Draw(imagen_para_escribir)


    relacion_temp_C_Y = 20
    relacion_temp_C_X = 15
    fuente_del_texto =ImageFont.truetype(CWD + 'fuentes\\Product Sans Regular.ttf',50)

    nombre_fondo_usado = dicc_incono_fondo[nombre_imagen_icono]
    if nombre_fondo_usado == 'niebla_R.png' or nombre_fondo_usado == 'dn_R.png' or nombre_fondo_usado == 'dll_R.png' or nombre_fondo_usado =='nieve_R.png':
        color_letra = '#F5B041'
    else:
        color_letra = 'white'
        
    # Temperatura actual
    if temp_actual >= 10:
        edit_image.text((260+relacion_temp_C_X, 20+relacion_temp_C_Y), f'{int(temp_actual)}', (color_letra), font=fuente_del_texto)
    else:
        edit_image.text((280+relacion_temp_C_X, 20+relacion_temp_C_Y), f'{int(temp_actual)}', (color_letra), font=fuente_del_texto)

    fuente_del_texto =ImageFont.truetype(CWD + 'fuentes\\Product Sans Regular.ttf',15)
    edit_image.text((315+relacion_temp_C_X, 30+relacion_temp_C_Y), 'ºC', (color_letra), font=fuente_del_texto)

    # descripción del tiempo actual

    texto_a_añadir = obtener_clima_desc(id_clima)
    fuente_del_texto =ImageFont.truetype(CWD + 'fuentes\\Product Sans Regular.ttf',15)
    edit_image.text((100, 6), texto_a_añadir, (color_letra), font=fuente_del_texto)

    # data del tiempo
    texto_a_añadir = f'Tmax. {temp_max:.1f}ºC, Tmin. {temp_min:.1f}ºC\n'+ f'Humedad: {humedad}%.\n' + f'Viento: a {viento} km/h.'
    fuente_del_texto =ImageFont.truetype(CWD + 'fuentes\\Product Sans Regular.ttf',12)
    edit_image.text((100, 26), texto_a_añadir, (color_letra), font=fuente_del_texto)

    # localidad.
    texto_a_añadir = f'{nombre_localidad},\n{ciudad} ,{sigla_pais}'
    fuente_del_texto =ImageFont.truetype(CWD + 'fuentes\\Product Sans Regular.ttf',18)
    edit_image.text((100, 80), texto_a_añadir, (color_letra), font=fuente_del_texto)

    # volvemos a guardar 
    imagen_para_escribir.save(CWD + 'imagenes_del_organizador\\NewImg.png',"PNG")



