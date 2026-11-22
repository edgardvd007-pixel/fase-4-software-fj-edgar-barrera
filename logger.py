# Importamos datetime para sellar cada registro con fecha y hora exacta
from datetime import datetime
# Importamos la excepción personalizada para fallos de escritura en disco
from excepciones import RegistroLogError


class GestorLogs:
    # Clase encargada de persistir eventos de auditoría, éxito y error en un archivo .log

    def __init__(self, ruta_archivo: str = "eventos_sistema.log"):
        # Define el nombre del archivo de salida
        self.ruta_archivo = ruta_archivo

    def registrar_evento(self, nivel: str, operacion: str, mensaje: str):
        # Genera la marca de tiempo actual
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Formatea la línea de registro con nivel, operación y descripción
        linea = f"[{timestamp}] [{nivel.upper()}] [{operacion}] - {mensaje}\n"
        try:
            # Abre el archivo en modo 'append' ('a') con codificación UTF-8 para no sobrescribir historial
            with open(self.ruta_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except OSError as exc:
            # Si falla la escritura en disco, encadena el error hacia nuestra excepción personalizada
            raise RegistroLogError(f"No se pudo escribir en el archivo de log '{self.ruta_archivo}'.") from exc
