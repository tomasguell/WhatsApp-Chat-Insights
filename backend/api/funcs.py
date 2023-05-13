import pandas as pd


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
            data.append([fecha, hora, remitente, mensaje.strip()])
        except ValueError:
            try:
                print(f"La multilinea es asi: {data[-1][3]} y se le agrega: {mensaje}")

                data[-1][3] = data[-1][3] + mensaje
            except IndexError:
                pass
    # print(data)
    df = pd.DataFrame(data, columns=["Fecha", "Hora", "Remitente", "Mensaje"])

    return df


"""# Ejemplo de uso
ruta_archivo = "ruta/del/archivo.txt"
df_chat = leer_chat_whatsapp(ruta_archivo)

# Imprimir el DataFrame
print(df_chat)"""
