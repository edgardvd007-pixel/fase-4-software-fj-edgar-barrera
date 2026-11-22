# Importamos ABC y abstractmethod para definir clases base abstractas
from abc import ABC, abstractmethod
# Importamos la excepción personalizada para validar los datos del cliente
from excepciones import DatosInvalidosError


class EntidadBase(ABC):
    # Clase abstracta base que obliga a sus subclases a tener un identificador único

    def __init__(self, id_entidad: str):
        # Valida que el ID no esté vacío ni contenga solo espacios
        if not id_entidad or not id_entidad.strip():
            raise DatosInvalidosError("El identificador de la entidad no puede estar vacío.")
        # Almacena el ID de forma protegida (encapsulamiento)
        self._id_entidad = id_entidad.strip()

    @property
    def id_entidad(self) -> str:
        # Getter que permite consultar el ID sin modificarlo directamente
        return self._id_entidad

    @abstractmethod
    def obtener_resumen(self) -> str:
        # Método abstracto que deberá implementar cada clase hija
        pass


class Cliente(EntidadBase):
    # Clase concreta que representa a un cliente del sistema Software FJ

    def __init__(self, id_cliente: str, nombre: str, documento: str, correo: str):
        # Llama al constructor de EntidadBase para validar y asignar el ID
        super().__init__(id_cliente)
        # Usa los setters definidos abajo para validar cada atributo al crear el objeto
        self.nombre = nombre
        self.documento = documento
        self.correo = correo

    @property
    def nombre(self) -> str:
        # Getter del nombre del cliente
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        # Verifica que el nombre sea una cadena válida con al menos 3 caracteres
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre del cliente debe tener al menos 3 caracteres.")
        # Guarda el nombre limpio de espacios extremos
        self._nombre = valor.strip()

    @property
    def documento(self) -> str:
        # Getter del documento de identidad
        return self._documento

    @documento.setter
    def documento(self, valor: str):
        # Verifica que el documento tenga solo números y mínimo 5 dígitos
        if not isinstance(valor, str) or not valor.strip().isdigit() or len(valor.strip()) < 5:
            raise DatosInvalidosError("El documento debe contener únicamente números (mínimo 5 dígitos).")
        # Guarda el documento validado
        self._documento = valor.strip()

    @property
    def correo(self) -> str:
        # Getter del correo electrónico
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        # Valida estructura básica de correo electrónico (@ y punto)
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        # Normaliza el correo a minúsculas y sin espacios
        self._correo = valor.strip().lower()

    def obtener_resumen(self) -> str:
        # Implementación del método abstracto con los datos formateados del cliente
        return f"Cliente [{self.id_entidad}]: {self.nombre} | Doc: {self.documento} | Email: {self.correo}"
