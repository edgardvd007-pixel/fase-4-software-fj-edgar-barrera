from excepciones import (
    SoftwareFJError,
    DatosInvalidosError,
    ClienteInvalidoError,
    ServicioNoDisponibleError,
    ReservaError,
)
from logger import GestorLogs
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva


class SistemaSoftwareFJ:
    """Gestor integral en memoria para clientes, servicios y reservas de Software FJ."""

    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        self.__logger = GestorLogs("eventos_sistema.log")
        self.__logger.registrar_evento("INFO", "Sistema Software FJ inicializado correctamente.")

    def registrar_cliente(self, id_cliente, nombre, correo, telefono):
        try:
            for c in self.__clientes:
                if c.id == str(id_cliente).strip():
                    raise ClienteInvalidoError(f"Ya existe un cliente registrado con ID '{id_cliente}'.")
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
        except SoftwareFJError as error:
            self.__logger.registrar_evento("ERROR", f"Fallo al registrar cliente ({id_cliente}): {error}")
            raise
        else:
            self.__clientes.append(nuevo_cliente)
            self.__logger.registrar_evento("EXITO", f"Cliente registrado: {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente

    def registrar_servicio(self, servicio):
        try:
            for s in self.__servicios:
                if s.id == servicio.id:
                    raise DatosInvalidosError(f"Ya existe un servicio registrado con ID '{servicio.id}'.")
            self.__servicios.append(servicio)
        except SoftwareFJError as error:
            self.__logger.registrar_evento("ERROR", f"Fallo al registrar servicio: {error}")
            raise
        else:
            self.__logger.registrar_evento("EXITO", f"Servicio agregado: {servicio.obtener_resumen()}")
            return servicio

    def buscar_cliente(self, id_cliente):
        try:
            cliente = next((c for c in self.__clientes if c.id == str(id_cliente).strip()), None)
            if cliente is None:
                raise LookupError(f"No se encontró el ID '{id_cliente}' en la lista de clientes.")
            return cliente
        except LookupError as error_interno:
            raise ClienteInvalidoError(
                f"Error de consulta: el cliente '{id_cliente}' no existe en el sistema."
            ) from error_interno

    def buscar_servicio(self, id_servicio):
        try:
            servicio = next((s for s in self.__servicios if s.id == str(id_servicio).strip()), None)
            if servicio is None:
                raise LookupError(f"No se encontró el ID '{id_servicio}' en el catálogo de servicios.")
            return servicio
        except LookupError as error_interno:
            raise ServicioNoDisponibleError(
                f"Error de consulta: el servicio '{id_servicio}' no está registrado."
            ) from error_interno

    def crear_reserva(self, id_reserva, id_cliente, id_servicio, horas, descuento=0.0, incluir_iva=False):
        reserva_creada = None
        try:
            for r in self.__reservas:
                if r.id == str(id_reserva).strip():
                    raise ReservaError(f"El código de reserva '{id_reserva}' ya está en uso.")

            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)
            reserva_creada = Reserva(id_reserva, cliente, servicio, horas, descuento, incluir_iva)
            reserva_creada.confirmar()
        except SoftwareFJError as error:
            detalle_causa = f" | Causa original: {error.__cause__}" if error.__cause__ else ""
            self.__logger.registrar_evento(
                "ERROR", f"Error en reserva '{id_reserva}': {error}{detalle_causa}"
            )
            raise
        else:
            self.__reservas.append(reserva_creada)
            self.__logger.registrar_evento("EXITO", f"Reserva confirmada: {reserva_creada.obtener_resumen()}")
            return reserva_creada
        finally:
            self.__logger.registrar_evento(
                "AUDITORIA", f"Finalizó intento de transacción para reserva '{id_reserva}'."
            )

    def procesar_reserva(self, id_reserva):
        try:
            reserva = next((r for r in self.__reservas if r.id == str(id_reserva).strip()), None)
            if reserva is None:
                raise ReservaError(f"No existe la reserva '{id_reserva}' para procesar.")
            reserva.procesar()
            self.__logger.registrar_evento("EXITO", f"Reserva procesada: {reserva.obtener_resumen()}")
            return reserva
        except SoftwareFJError as error:
            self.__logger.registrar_evento("ERROR", f"No se pudo procesar reserva '{id_reserva}': {error}")
            raise

    def cancelar_reserva(self, id_reserva):
        try:
            reserva = next((r for r in self.__reservas if r.id == str(id_reserva).strip()), None)
            if reserva is None:
                raise ReservaError(f"No existe la reserva '{id_reserva}' para cancelar.")
            reserva.cancelar()
            self.__logger.registrar_evento("EXITO", f"Reserva cancelada: {reserva.obtener_resumen()}")
            return reserva
        except SoftwareFJError as error:
            self.__logger.registrar_evento("ERROR", f"No se pudo cancelar reserva '{id_reserva}': {error}")
            raise

    def mostrar_resumen_general(self):
        print("\n" + "=" * 75)
        print("RESUMEN GENERAL EN MEMORIA - SOFTWARE FJ")
        print("=" * 75)
        print(f"Total Clientes registrados : {len(self.__clientes)}")
        for c in self.__clientes:
            print(f"  * {c.obtener_resumen()}")

        print(f"\nTotal Servicios activos    : {len(self.__servicios)}")
        for s in self.__servicios:
            print(f"  * {s.obtener_resumen()}")

        print(f"\nTotal Reservas en sistema  : {len(self.__reservas)}")
        for r in self.__reservas:
            print(f"  * {r.obtener_resumen()}")
        print("=" * 75 + "\n")


def ejecutar_simulacion():
    """Ejecuta 10 operaciones completas (válidas e inválidas) demostrando tolerancia a fallos."""
    sistema = SistemaSoftwareFJ()
    print("Iniciando simulación de 10 operaciones en Software FJ...\n")

    # Operación 1: Registro de cliente válido
    try:
        c1 = sistema.registrar_cliente("C001", "Laura Gómez", "laura.gomez@empresa.com", "3104567890")
        print(f"[Op 1 - OK] {c1.obtener_resumen()}")
    except SoftwareFJError as e:
        print(f"[Op 1 - ERROR] {e}")

    # Operación 2: Registro de segundo cliente válido
    try:
        c2 = sistema.registrar_cliente("C002", "Carlos Mendoza", "cmendoza@tech.co", "3209876543")
        print(f"[Op 2 - OK] {c2.obtener_resumen()}")
    except SoftwareFJError as e:
        print(f"[Op 2 - ERROR] {e}")

    # Operación 3: Intento de registro de cliente inválido (correo mal formado)
    try:
        sistema.registrar_cliente("C003", "Andrés Ruiz", "correo_sin_arroba.com", "3001112233")
    except SoftwareFJError as e:
        print(f"[Op 3 - Controlado] Error esperado al crear cliente: {e}")

    # Operación 4: Registro de servicios polimórficos (Sala, Equipo, Asesoría)
    try:
        s1 = sistema.registrar_servicio(ReservaSala("S001", "Sala Innovación", 80000, capacidad_personas=25))
        s2 = sistema.registrar_servicio(AlquilerEquipo("S002", "Servidor Portátil GPU", 50000, gama_equipo="profesional"))
        s3 = sistema.registrar_servicio(AsesoriaEspecializada("S003", "Arquitectura Cloud", 120000, area_tecnica="Nube y Redes"))
        s4 = sistema.registrar_servicio(ReservaSala("S004", "Sala Mantenimiento", 60000, capacidad_personas=10, disponible=False))
        print(f"[Op 4 - OK] 4 servicios registrados ({s1.nombre}, {s2.nombre}, {s3.nombre}, {s4.nombre}).")
    except SoftwareFJError as e:
        print(f"[Op 4 - ERROR] {e}")

    # Operación 5: Reserva válida de Sala con descuento e IVA (sobrecarga simulada)
    try:
        r1 = sistema.crear_reserva("R001", "C001", "S001", horas=4, descuento=0.10, incluir_iva=True)
        print(f"[Op 5 - OK] {r1.obtener_resumen()}")
    except SoftwareFJError as e:
        print(f"[Op 5 - ERROR] {e}")

    # Operación 6: Reserva válida de Equipo Profesional sin descuento
    try:
        r2 = sistema.crear_reserva("R002", "C002", "S002", horas=3)
        print(f"[Op 6 - OK] {r2.obtener_resumen()}")
    except SoftwareFJError as e:
        print(f"[Op 6 - ERROR] {e}")

    # Operación 7: Reserva fallida por cliente inexistente (prueba encadenamiento raise ... from)
    try:
        sistema.crear_reserva("R003", "C999", "S003", horas=3)
    except SoftwareFJError as e:
        print(f"[Op 7 - Controlado] {e} | Causa interna: {e.__cause__}")

    # Operación 8: Reserva fallida por servicio no disponible
    try:
        sistema.crear_reserva("R004", "C001", "S004", horas=2)
    except SoftwareFJError as e:
        print(f"[Op 8 - Controlado] Error esperado por disponibilidad: {e}")

    # Operación 9: Reserva fallida por regla de negocio (asesoría requiere mínimo 2 horas)
    try:
        sistema.crear_reserva("R005", "C002", "S003", horas=1)
    except SoftwareFJError as e:
        print(f"[Op 9 - Controlado] Error esperado por horas mínimas: {e}")

    # Operación 10: Procesar reserva R001 y cancelar reserva R002
    try:
        sistema.procesar_reserva("R001")
        sistema.cancelar_reserva("R002")
        print("[Op 10 - OK] Reserva R001 procesada y reserva R002 cancelada correctamente.")
    except SoftwareFJError as e:
        print(f"[Op 10 - ERROR] {e}")

    # Mostrar estado final en memoria
    sistema.mostrar_resumen_general()
    print("Ejecución finalizada. Revisa el archivo 'eventos_sistema.log' generado en la carpeta.")


if __name__ == "__main__":
    ejecutar_simulacion()
