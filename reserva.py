from entidades import EntidadBase, Cliente
from servicios import Servicio
from excepciones import DatosInvalidosError, ReservaError


class Reserva(EntidadBase):
    """Vincula un Cliente con un Servicio, gestionando duración, costo y estado."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, id_reserva, cliente, servicio, horas, descuento=0.0, incluir_iva=False):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva debe asociarse a un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva debe asociarse a un objeto Servicio válido.")
        if horas <= 0:
            raise DatosInvalidosError("La duración de la reserva debe ser mayor a cero horas.")

        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = float(horas)
        self.__descuento = descuento
        self.__incluir_iva = incluir_iva
        self.__estado = "PENDIENTE"
        self.validar()
        self.__costo_total = self.__servicio.calcular_costo(horas, descuento, incluir_iva)

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    def validar(self):
        self.__cliente.validar()
        self.__servicio.validar()
        return True

    def confirmar(self):
        if self.__estado == "CANCELADA":
            raise ReservaError(f"No se puede confirmar la reserva {self.id} porque fue cancelada.")
        self.__estado = "CONFIRMADA"

    def cancelar(self):
        if self.__estado == "PROCESADA":
            raise ReservaError(f"No se puede cancelar la reserva {self.id} porque ya fue procesada.")
        self.__estado = "CANCELADA"

    def procesar(self):
        if self.__estado != "CONFIRMADA":
            raise ReservaError(f"La reserva {self.id} debe estar CONFIRMADA antes de procesarse.")
        self.__estado = "PROCESADA"

    def obtener_resumen(self):
        return (
            f"Reserva [{self.id}] | Estado: {self.__estado} | "
            f"Cliente: {self.__cliente.nombre} | Servicio: {self.__servicio.nombre} "
            f"({self.__horas}h) | Total: ${self.__costo_total:,.2f}"
        )
