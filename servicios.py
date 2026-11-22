# Importamos herramientas para clases abstractas y tipado opcional
from abc import ABC, abstractmethod
from typing import Optional
# Importamos las excepciones de negocio necesarias
from excepciones import (
    CapacidadExcedidaError,
    DatosInvalidosError,
    DuracionInvalidaError,
    ServicioNoDisponibleError,
)


class Servicio(ABC):
    # Clase abstracta base para todos los servicios ofrecidos por Software FJ

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, disponible: bool = True):
        # Valida que el código y el nombre no estén vacíos
        if not codigo or not codigo.strip():
            raise DatosInvalidosError("El código del servicio es obligatorio.")
        if not nombre or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        # Valida que la tarifa base sea un número positivo
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser un valor numérico mayor a cero.")

        # Asignación de atributos encapsulados
        self._codigo = codigo.strip()
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def codigo(self) -> str:
        # Devuelve el código identificador del servicio
        return self._codigo

    @property
    def nombre(self) -> str:
        # Devuelve el nombre descriptivo del servicio
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        # Devuelve la tarifa base del servicio
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        # Indica si el servicio se encuentra activo para reservas
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        # Actualiza el estado de disponibilidad del servicio
        self._disponible = bool(estado)

    @abstractmethod
    def calcular_costo(self, cantidad: int, descuento: float = 0.0, recargo_extra: Optional[float] = None) -> float:
        # Método polimórfico abstracto con parámetros opcionales (sobrecarga simulada)
        pass

    def _validar_parametros_calculo(self, cantidad: int, descuento: float):
        # Verifica disponibilidad antes de realizar cualquier cálculo
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no se encuentra disponible actualmente.")
        # Valida que la cantidad (horas, días o sesiones) sea mayor a cero
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DuracionInvalidaError("La cantidad o duración debe ser un entero mayor a cero.")
        # Valida que el descuento esté en el rango porcentual permitido [0, 1]
        if not isinstance(descuento, (int, float)) or not (0.0 <= descuento <= 1.0):
            raise DatosInvalidosError("El descuento debe estar entre 0.0 (0%) y 1.0 (100%).")

    def obtener_detalle(self) -> str:
        # Retorna una cadena resumen con el estado del servicio
        estado = "Disponible" if self.disponible else "No disponible"
        return f"[{self.codigo}] {self.nombre} - Tarifa base: ${self.tarifa_base:,.2f} ({estado})"


class ReservaSala(Servicio):
    # Subclase para gestión de alquiler de salas por horas con control de aforo

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, capacidad_maxima: int, disponible: bool = True):
        # Inicializa los atributos heredados de Servicio
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        # Valida que la capacidad máxima sea un entero positivo
        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise DatosInvalidosError("La capacidad máxima de la sala debe ser mayor a cero.")
        self._capacidad_maxima = capacidad_maxima

    @property
    def capacidad_maxima(self) -> int:
        # Devuelve el aforo máximo permitido en la sala
        return self._capacidad_maxima

    def validar_asistentes(self, asistentes: int):
        # Comprueba que los asistentes sean al menos 1 y no superen el aforo máximo
        if not isinstance(asistentes, int) or asistentes <= 0:
            raise DatosInvalidosError("El número de asistentes debe ser mayor a cero.")
        if asistentes > self._capacidad_maxima:
            raise CapacidadExcedidaError(
                f"Aforo excedido en '{self.nombre}': se solicitaron {asistentes} lugares y el máximo es {self._capacidad_maxima}."
            )

    def calcular_costo(self, horas: int, descuento: float = 0.0, recargo_extra: Optional[float] = None) -> float:
        # Ejecuta las validaciones comunes de disponibilidad, duración y descuento
        self._validar_parametros_calculo(horas, descuento)
        # Calcula el subtotal multiplicando tarifa por hora y horas reservadas
        subtotal = self.tarifa_base * horas
        # Aplica el porcentaje de descuento
        total = subtotal * (1 - descuento)
        # Si se envió un recargo opcional (ej. montaje), lo suma al total
        if recargo_extra is not None and recargo_extra > 0:
            total += recargo_extra
        return round(total, 2)


class AlquilerEquipo(Servicio):
    # Subclase para alquiler de equipos tecnológicos por días con seguro opcional

    def __init__(self, codigo: str, nombre: str, tarifa_dia: float, serial: str, disponible: bool = True):
        # Inicializa atributos comunes desde la clase padre Servicio
        super().__init__(codigo, nombre, tarifa_dia, disponible)
        # Valida que el equipo tenga un número de serie asignado
        if not serial or not serial.strip():
            raise DatosInvalidosError("El número de serie del equipo es obligatorio.")
        self._serial = serial.strip()

    @property
    def serial(self) -> str:
        # Devuelve el número de serie del equipo
        return self._serial

    def calcular_costo(self, dias: int, descuento: float = 0.0, recargo_extra: Optional[float] = None) -> float:
        # Valida parámetros de duración y descuento
        self._validar_parametros_calculo(dias, descuento)
        # Calcula el costo base según los días de alquiler
        subtotal = self.tarifa_base * dias
        total = subtotal * (1 - descuento)
        # Suma el seguro o transporte adicional si fue especificado
        if recargo_extra is not None and recargo_extra > 0:
            total += recargo_extra
        return round(total, 2)


class AsesoriaEspecializada(Servicio):
    # Subclase para servicios de consultoría técnica con incremento por modalidad remota

    def __init__(self, codigo: str, nombre: str, tarifa_sesion: float, especialidad: str, disponible: bool = True):
        # Llama al constructor padre
        super().__init__(codigo, nombre, tarifa_sesion, disponible)
        # Valida el área de especialidad del consultor
        if not especialidad or not especialidad.strip():
            raise DatosInvalidosError("La especialidad de la asesoría no puede estar vacía.")
        self._especialidad = especialidad.strip()

    @property
    def especialidad(self) -> str:
        # Devuelve la especialidad técnica
        return self._especialidad

    def calcular_costo(self, sesiones: int, descuento: float = 0.0, recargo_extra: Optional[float] = None) -> float:
        # Valida los parámetros de entrada
        self._validar_parametros_calculo(sesiones, descuento)
        # Aplica un incremento fijo del 10% por soporte documental de asesoría
        subtotal = (self.tarifa_base * sesiones) * 1.10
        total = subtotal * (1 - descuento)
        # Agrega cargos extra opcionales si aplican
        if recargo_extra is not None and recargo_extra > 0:
            total += recargo_extra
        return round(total, 2)
