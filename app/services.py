import os,logging, base64
from PIL import Image, ImageDraw, ImageFont # type: ignore


logging.basicConfig(
    filename = os.path.abspath("logs/output.log"), 
    level=logging.DEBUG,  # Define el nivel de los logs (INFO, DEBUG, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Switch:
    @staticmethod
    def verificar_tipo_doc(data):
        print("Realizando servicio de creacion de imagenes")
        logging.info("Realizando servicio de creacion de pdf")
        if data["tipo"] == "cotizar_vuelo":
            return Imagen.cotizar_vuelos(data)
        elif data["tipo"] == "hola":
            return Imagen.generar_adendum(data)
        elif data["tipo"] == "hola":
            return Imagen.cotizar_vuelos(data)
        else:
            return {"estado": False, "mensaje": "No se reconoce el tipo de archivo"}

   
class Imagen:
    @staticmethod
    def cotizar_vuelos(data):
        if data:
            ruta_plantilla = os.path.abspath("plantilla/plantilla.jpg")
            ruta_imagen_generada = os.path.abspath("plantilla/vuelos.jpg")
            imagen_original = Image.open(ruta_plantilla)
            imagen_copia = imagen_original.copy()
            imagen_copia.save(ruta_imagen_generada)
            Imagen.colocar_texto_a_imagen(data["ida_fecha"],(170,105),ruta_imagen_generada,ruta_imagen_generada,15)
            imagen_pequena = Imagen.sacar_logo_aereolina(data["aereolina_codigo"])
            Imagen.colocar_imagen_pequena(imagen_pequena, (33,20), ruta_imagen_generada, ruta_imagen_generada,90,40)
            Imagen.colocar_texto_a_imagen(data["aereolina_nombre"],(120,30),ruta_imagen_generada,ruta_imagen_generada,15)
            Imagen.colocar_texto_a_imagen(data["vuelta_fecha"],(170,315),ruta_imagen_generada,ruta_imagen_generada,15)
            texto_ida = data["codigo_salida"] + "-" + data["codigo_destino"]
            Imagen.colocar_texto_a_imagen(texto_ida,(700,20),ruta_imagen_generada,ruta_imagen_generada,15)
            texto_vuelta = data["codigo_destino"] + "-" + data["codigo_salida"]
            Imagen.colocar_texto_a_imagen(texto_vuelta,(700,35),ruta_imagen_generada,ruta_imagen_generada,15)
            altura = 147
            for index, vuelo in enumerate(data["vuelos_ida"]):
                if index<3:
                    idVuelo = "I"+str(index+1)
                    Imagen.colocar_texto_a_imagen(idVuelo,(96,altura),ruta_imagen_generada,ruta_imagen_generada,13)
                    texto_horas = data["codigo_salida"]+": "+vuelo["hora_salida"]+" ---> "+data["codigo_destino"]+": "+vuelo["hora_llegada"]
                    Imagen.colocar_texto_a_imagen(texto_horas,(144,altura),ruta_imagen_generada,ruta_imagen_generada,15)
                    Imagen.colocar_texto_a_imagen(vuelo["duracion"],(500,altura),ruta_imagen_generada,ruta_imagen_generada,15)
                    ruta_personal = Imagen.sacar_equipaje("personal",vuelo["equipaje_personal"])
                    ruta_carry = Imagen.sacar_equipaje("carry",vuelo["equipaje_carry"])
                    ruta_bodega = Imagen.sacar_equipaje("bodega",vuelo["equipaje_bodega"])
                    Imagen.colocar_imagen_pequena(ruta_personal, (700,altura-3), ruta_imagen_generada, ruta_imagen_generada,18,18)
                    Imagen.colocar_imagen_pequena(ruta_carry, (720,altura-4), ruta_imagen_generada, ruta_imagen_generada,20,20)
                    Imagen.colocar_imagen_pequena(ruta_bodega, (740,altura-4), ruta_imagen_generada, ruta_imagen_generada,20,20)
                    altura = altura +52
            altura = 355
            for index, vuelo in enumerate(data["vuelos_vuelta"]):
                if index<3:
                    idVuelo = "v"+str(index+1)
                    Imagen.colocar_texto_a_imagen(idVuelo,(96,altura),ruta_imagen_generada,ruta_imagen_generada,13)
                    texto_horas = data["codigo_salida"]+": "+vuelo["hora_salida"]+" ---> "+data["codigo_destino"]+": "+vuelo["hora_llegada"]
                    Imagen.colocar_texto_a_imagen(texto_horas,(144,altura),ruta_imagen_generada,ruta_imagen_generada,15)
                    Imagen.colocar_texto_a_imagen(vuelo["duracion"],(500,altura),ruta_imagen_generada,ruta_imagen_generada,15)
                    ruta_personal = Imagen.sacar_equipaje("personal",vuelo["equipaje_personal"])
                    ruta_carry = Imagen.sacar_equipaje("carry",vuelo["equipaje_carry"])
                    ruta_bodega = Imagen.sacar_equipaje("bodega",vuelo["equipaje_bodega"])
                    Imagen.colocar_imagen_pequena(ruta_personal, (700,altura-3), ruta_imagen_generada, ruta_imagen_generada,18,18)
                    Imagen.colocar_imagen_pequena(ruta_carry, (720,altura-4), ruta_imagen_generada, ruta_imagen_generada,20,20)
                    Imagen.colocar_imagen_pequena(ruta_bodega, (740,altura-4), ruta_imagen_generada, ruta_imagen_generada,20,20)
                    altura = altura +52
            imagen_base64 = Imagen.convertir_imagen_a_base64(ruta_imagen_generada)
            if imagen_base64:
                return {"estado": True, "mensaje": "Imagen generada correctamente", "imagen": imagen_base64}  
            else:
                return {"estado": False, "mensaje": "No se ha podido generar Imagen"}  
        else:
            return {"estado": False, "mensaje": "No hay datos en el body"}  
        

    @staticmethod
    def convertir_imagen_a_base64(ruta_imagen):
        try:
            # Abrir la imagen en modo binario
            with open(ruta_imagen, "rb") as imagen:
                # Leer los datos binarios de la imagen
                datos_imagen = imagen.read()
                # Convertir los datos binarios a Base64
                base64_imagen = base64.b64encode(datos_imagen).decode("utf-8")
            return base64_imagen
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return False


    
    @staticmethod
    def colocar_texto_a_imagen(texto,coordenadas,ruta_imagen, ruta_salida,fuente):
        try:
            # Cargar la imagen
            imagen = Image.open(ruta_imagen)

            # Crear un objeto de dibujo
            draw = ImageDraw.Draw(imagen)

            # Configurar la fuente (asegúrate de que "arial.ttf" esté disponible en tu sistema)
            fuente = ImageFont.truetype("arial.ttf", fuente)

            # Dibujar el texto en las coordenadas especificadas
            draw.text(coordenadas, texto, fill="black", font=fuente)

            # Guardar la imagen modificada
            imagen.save(ruta_salida)
            return True
        except Exception as e:
            print(f"Ocurrió un error: {e}") 
            return False



    @staticmethod
    def sacar_logo_aereolina(aereolina):
        if aereolina == "AV" or aereolina == '2K':
            return os.path.abspath("img/aereolinas_logos/avianca.png")
        elif aereolina == 'CM':
            return os.path.abspath("img/aereolinas_logos/copa.png")
        elif aereolina == 'DL':
            return os.path.abspath("img/aereolinas_logos/delta.png")        
        elif aereolina == 'B6':
            return os.path.abspath("img/aereolinas_logos/jet.png")
        elif aereolina == 'LA':
            return os.path.abspath("img/aereolinas_logos/latam.png")
        elif aereolina == 'AA':
            return os.path.abspath("img/aereolinas_logos/american.png")
        

    @staticmethod
    def sacar_equipaje(tipo,id):
        if tipo == "personal":
            if id == "1":
                return os.path.abspath("img/equipaje/si_personal.png")
            else:
                return os.path.abspath("img/equipaje/no_personal.png")
        elif tipo == 'carry':
            if id == "1":
                return os.path.abspath("img/equipaje/si_carry.png")
            else:
                return os.path.abspath("img/equipaje/no_carry.png")
        elif tipo == 'bodega':
            if id == "1":
                return os.path.abspath("img/equipaje/si_bodega.png")
            else:
                return os.path.abspath("img/equipaje/no_bodega.png")       
        




    @staticmethod
    def colocar_imagen_pequena(imagen_pequena, coordenadas, ruta_imagen, ruta_salida, ancho_pequena, alto_pequena):
        try:
            # Cargar la imagen de fondo
            imagen_grande = Image.open(ruta_imagen)
            
            # Crear una nueva imagen blanca del mismo tamaño que la imagen de fondo
            fondo_blanco = Image.new("RGB", imagen_grande.size, (255, 255, 255))
            
            # Pegar la imagen grande en el fondo blanco
            fondo_blanco.paste(imagen_grande, (0, 0))
            
            # Cargar la imagen pequeña
            imagen_pequena = Image.open(imagen_pequena)
            
            # Redimensionar la imagen pequeña al tamaño especificado
            imagen_pequena = imagen_pequena.resize((ancho_pequena, alto_pequena), Image.LANCZOS)  # Cambiado de ANTIALIAS a LANCZOS
            
            # Pegar la imagen pequeña en el fondo blanco en las coordenadas deseadas
            fondo_blanco.paste(imagen_pequena, coordenadas, 
                            imagen_pequena.convert("RGBA").getchannel("A") if imagen_pequena.mode == 'RGBA' else None)
            
            # Guardar la imagen resultante
            fondo_blanco.save(ruta_salida)            
        except Exception as e:
            print(f"Ocurrió un error: {e}")
