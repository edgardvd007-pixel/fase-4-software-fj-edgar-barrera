from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError, ClienteInvalidoError


class EntidadBase(ABC):
    """Clase abstracta base para todas las entidades del sistema Software FJ."""

    def __init__(self, id_entidad):
        if not id_entidad or not str(id_entidad).strip():
            raise DatosInvalidosError("El identificador de la entidad no puede estar vacío.")
        self.__id = str(id_entidad).strip()

    @property
    def id(self):
        return self.__id

    @abstractmethod
    def validar(self):
        """Método abstracto obligatorio para validar la integridad de la entidad."""
        pass

    @abstractmethod
    def obtener_resumen(self):
        """Método abstracto para presentar la información resumida de la entidad."""
        pass


class Cliente(EntidadBase):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""

    def __init__(self, id_cliente, nombre, correo, telefono):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        telefono_limpio = str(valor).strip()
        if not telefono_limpio.isdigit() or len(telefono_limpio) < 7:
            raise ClienteInvalidoError("El teléfono debe contener al menos 7 dígitos numéricos.")
        self.__telefono = telefono_limpio

    def validar(self):
        if not self.__nombre or not self.__correo or not self.__telefono:
            raise ClienteInvalidoError("Todos los campos del cliente son obligatorios.")
        return True

    def obtener_resumen(self):
        return f"Cliente [{self.id}] - {self.__nombre} | Correo: {self.__correo} | Tel: {self.__telefono}"
