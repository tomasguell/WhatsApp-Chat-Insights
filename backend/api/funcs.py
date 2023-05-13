import pandas as pd
from datetime import datetime, time
import re


def leer_chat_whatsapp(archivo):
    # Leer el archivo de texto
    with open(archivo, "r", encoding="utf-8") as file:
        contenido = file.readlines()

    # Extraer información del formato de WhatsApp y crear el DataFrame
    data = []
    for mensaje in contenido:
        try:
            fecha_hora, contenido = mensaje.split(" - ")
            fecha, hora = fecha_hora.split(", ")
            remitente, mensaje = contenido.split(": ")

            fecha = datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")

            try:
                hora = re.sub(
                    r"[^\d:]", "", hora
                )  # Eliminar caracteres especiales excepto dígitos y ":"
                hora = datetime.strptime(hora, "%H:%M").strftime("%H:%M:%S")
            except Exception:
                print("Error al analizar la hora")
                continue
            data.append([fecha, hora, remitente, mensaje.strip()])
        except ValueError:
            try:
                data[-1][3] = data[-1][3] + mensaje
            except IndexError:
                pass

    data = data[:3]
    df = pd.DataFrame(data, columns=["Fecha", "Hora", "Remitente", "Mensaje"])
    return df


"""# Ejemplo de uso
ruta_archivo = "ruta/del/archivo.txt"
df_chat = leer_chat_whatsapp(ruta_archivo)

# Imprimir el DataFrame
print(df_chat)"""
