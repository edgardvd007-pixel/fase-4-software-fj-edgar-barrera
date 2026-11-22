# Módulo que define la jerarquía de excepciones personalizadas para el sistema Software FJ

class SoftwareFJError(Exception):
    # Clase base para todas las excepciones de negocio del sistema
    pass


class DatosInvalidosError(SoftwareFJError):
    # Se lanza cuando un atributo (nombre, correo, documento o tarifa) tiene formato inválido
    pass


class CapacidadExcedidaError(SoftwareFJError):
    # Se lanza cuando la cantidad de asistentes supera el aforo máximo permitido de una sala
    pass


class DuracionInvalidaError(SoftwareFJError):
    # Se lanza cuando las horas o días de reserva son menores o iguales a cero
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    # Se lanza cuando se intenta procesar un servicio o equipo inactivo o sin stock
    pass


class RegistroLogError(SoftwareFJError):
    # Se lanza si ocurre un error de entrada/salida al escribir en el archivo eventos_sistema.log
    pass
