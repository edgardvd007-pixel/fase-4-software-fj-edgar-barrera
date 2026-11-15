class SoftwareFJError(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""
    pass


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los datos ingresados tienen formato o valores incorrectos."""
    pass


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando falla la creación o validación de un cliente."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando un servicio no existe, está inactivo o no cumple requisitos."""
    pass


class ReservaError(SoftwareFJError):
    """Se lanza cuando ocurre un conflicto o error al gestionar una reserva."""
    pass
