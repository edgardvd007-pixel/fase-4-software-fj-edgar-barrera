# Importamos herramientas para fechas, tipado opcional y clases del dominio
from datetime import datetime
from typing import Optional
from entidades import Cliente
from excepciones import DatosInvalidosError
from servicios import ReservaSala, Servicio


class Reserva:
    # Clase integradora que asocia un Cliente con un Servicio y calcula el valor total

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        cantidad: int,
        descuento: float = 0.0,
        recargo_extra: Optional[float] = None,
        asistentes: Optional[int] = None,
    ):
        # Valida que el código de reserva no sea vacío
        if not id_reserva or not id_reserva.strip():
            raise DatosInvalidosError("El identificador de la reserva es obligatorio.")
        # Valida mediante isinstance que los objetos pertenezcan a las clases esperadas
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Se requiere una instancia válida de Servicio.")

        # Asignación de atributos de la reserva
        self.id_reserva = id_reserva.strip()
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.descuento = descuento
        self.recargo_extra = recargo_extra
        self.asistentes = asistentes
        # Registra la marca de tiempo exacta en que se crea la reserva
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Si el servicio es una sala y se indicó número de asistentes, valida el aforo
        if isinstance(self.servicio, ReservaSala) and self.asistentes is not None:
            self.servicio.validar_asistentes(self.asistentes)

        # Invoca polimórficamente el cálculo del costo según el tipo de servicio
        self.costo_total = self.servicio.calcular_costo(
            self.cantidad,
            descuento=self.descuento,
            recargo_extra=self.recargo_extra,
        )

    def generar_comprobante(self) -> str:
        # Construye y devuelve el resumen textual de la reserva confirmada
        return (
            f"Reserva {self.id_reserva} | Fecha: {self.fecha_registro} | "
            f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre} | "
            f"Cantidad: {self.cantidad} | Total: ${self.costo_total:,.2f}"
        )
