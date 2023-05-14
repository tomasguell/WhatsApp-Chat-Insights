import pandas as pd
from datetime import datetime, time
import re


def obtener_remitentes(df):
    remitentes = df["Remitente"].unique().tolist()
    return remitentes


def leer_chat_whatsapp(archivo):
    # Leer el archivo de texto
    with open(archivo, "r", encoding="utf-8") as file:
        contenido = file.readlines()

    # Extraer información del formato de WhatsApp y crear el DataFrame
    data = []
    for mensaje in contenido:
        # print(mensaje)
        try:
            fecha_hora, contenido = mensaje.split(" - ")
            fecha, hora = fecha_hora.split(", ")
            remitente, mensaje = contenido.split(": ")

            # Convertir la fecha al formato YYYY-MM-DD si viene en formato dd/mm/yyyy o d/m/yy
            if "/" in fecha:
                try:
                    fecha = datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    fecha = datetime.strptime(fecha, "%d/%m/%y").strftime("%Y-%m-%d")

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
                data.append([fecha, hora, remitente, mensaje.strip()])

    # print(data)
    # data = data[3:]

    df = pd.DataFrame(data, columns=["Fecha", "Hora", "Remitente", "Mensaje"])
    print(obtener_remitentes(df))
    print(df)
    return df


def enumerateSenders():
    from .models import Sender

    senders = list(Sender.objects.all())
    for sender in senders:
        print(f"Id: {sender.id} Nombre: {sender.Name}")


"""# Ejemplo de uso
ruta_archivo = "ruta/del/archivo.txt"
df_chat = leer_chat_whatsapp(ruta_archivo)

# Imprimir el DataFrame
print(df_chat)"""
