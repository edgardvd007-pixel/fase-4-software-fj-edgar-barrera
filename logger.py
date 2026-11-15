from datetime import datetime


class GestorLogs:
    """Clase encargada de registrar eventos y errores en un archivo de texto plano."""

    def __init__(self, nombre_archivo="eventos_sistema.log"):
        self.__nombre_archivo = nombre_archivo

    def registrar_evento(self, tipo, mensaje):
        """Escribe una línea con fecha, hora, tipo de evento y detalle en el archivo log."""
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{fecha_hora}] [{tipo.upper()}] {mensaje}\n"
        try:
            with open(self.__nombre_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except OSError as error:
            print(f"Advertencia: No se pudo escribir en el archivo de logs: {error}")
