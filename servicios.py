from abc import abstractmethod
from entidades import EntidadBase
from excepciones import DatosInvalidosError, ServicioNoDisponibleError


class Servicio(EntidadBase):
    """Clase abstracta que modela un servicio ofrecido por Software FJ."""

    def __init__(self, id_servicio, nombre, tarifa_base, disponible=True):
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        if tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser mayor a cero.")
        self.__nombre = nombre.strip()
        self.__tarifa_base = float(tarifa_base)
        self.__disponible = bool(disponible)

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tarifa_base(self):
        return self.__tarifa_base

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, estado):
        self.__disponible = bool(estado)

    def validar(self):
        if not self.__disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.__nombre}' no está disponible actualmente.")
        return True

    @abstractmethod
    def calcular_costo(self, horas, descuento=0.0, incluir_iva=False):
        """
        Calcula el costo del servicio (polimórfico en clases hijas).
        Simula sobrecarga mediante parámetros opcionales (descuento e IVA).
        """
        pass

    def _aplicar_ajustes(self, subtotal, descuento=0.0, incluir_iva=False):
        """Método auxiliar encapsulado para aplicar descuentos e impuestos."""
        if descuento < 0 or descuento > 0.5:
            raise DatosInvalidosError("El descuento debe estar entre 0.0 (0%) y 0.5 (50%).")
        total = subtotal * (1 - descuento)
        if incluir_iva:
            total *= 1.19
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de juntas o capacitación."""

    def __init__(self, id_servicio, nombre, tarifa_base, capacidad_personas, disponible=True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if capacidad_personas <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a cero.")
        self.__capacidad = int(capacidad_personas)

    def calcular_costo(self, horas, descuento=0.0, incluir_iva=False):
        if horas <= 0:
            raise DatosInvalidosError("Las horas de reserva de sala deben ser mayores a cero.")
        subtotal = self.tarifa_base * horas
        if self.__capacidad > 20:
            subtotal *= 1.10
        return self._aplicar_ajustes(subtotal, descuento, incluir_iva)

    def obtener_resumen(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Sala [{self.id}]: {self.nombre} (Capacidad: {self.__capacidad} pers.) - ${self.tarifa_base:,.0f}/h [{estado}]"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""

    def __init__(self, id_servicio, nombre, tarifa_base, gama_equipo, disponible=True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if gama_equipo.lower() not in ("estandar", "profesional"):
            raise DatosInvalidosError("La gama del equipo debe ser 'estandar' o 'profesional'.")
        self.__gama = gama_equipo.lower()

    def calcular_costo(self, horas, descuento=0.0, incluir_iva=False):
        if horas <= 0:
            raise DatosInvalidosError("Las horas de alquiler del equipo deben ser mayores a cero.")
        subtotal = self.tarifa_base * horas
        if self.__gama == "profesional":
            subtotal += 15000
        return self._aplicar_ajustes(subtotal, descuento, incluir_iva)

    def obtener_resumen(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Equipo [{self.id}]: {self.nombre} (Gama {self.__gama}) - ${self.tarifa_base:,.0f}/h [{estado}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica o empresarial."""

    def __init__(self, id_servicio, nombre, tarifa_base, area_tecnica, disponible=True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not area_tecnica or not area_tecnica.strip():
            raise DatosInvalidosError("El área técnica de la asesoría es obligatoria.")
        self.__area_tecnica = area_tecnica.strip()

    def calcular_costo(self, horas, descuento=0.0, incluir_iva=False):
        if horas < 2:
            raise DatosInvalidosError("Las asesorías especializadas requieren un mínimo de 2 horas.")
        subtotal = self.tarifa_base * horas
        return self._aplicar_ajustes(subtotal, descuento, incluir_iva)

    def obtener_resumen(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Asesoría [{self.id}]: {self.nombre} ({self.__area_tecnica}) - ${self.tarifa_base:,.0f}/h [{estado}]"
