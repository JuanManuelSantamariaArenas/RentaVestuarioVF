import re
import smtplib
import pickle
import datetime
from typing import Optional

from mundo.excepciones import *


class Prenda:

    def __init__(self, codigo: int, nombre: str, talla: str, color: str,
                 clima: str, valor_prenda: int, valor_alquiler: int):
        self.codigo = codigo
        self.nombre = nombre
        self.disponibilidad_renta = True
        self.talla = talla
        self.color = color
        self.clima = clima
        self.valor_prenda = valor_prenda
        self.valor_alquiler = valor_alquiler
        self.rentas_mes = 0

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} - {self.talla} - {self.color} - {self.clima} - {self.valor_alquiler} " \
               f"- {self.valor_prenda}"

    def esta_disponible(self) -> bool:
        if self.disponibilidad_renta:
            return True
        else:
            return False


class Renta:

    def __init__(self, prenda: Prenda, tiempo: int, entregar_prenda: bool, estado: bool, fecha: datetime):
        self.tiempo = tiempo
        self.prenda = prenda
        self.entregar_prenda = entregar_prenda
        self.estado = estado
        self.fecha = fecha


class Usuario:

    def __init__(self, cedula: int, nombre: str, correo: str):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.numero_rentas = 0
        self.deuda = 0
        self.orden: dict[int:list] = {}
        self.rentas: list[Renta] = []

    def __str__(self):
        return f"cedula: {self.cedula}"

    def crear_orden(self, prenda: Prenda, tiempo: int):
        fecha = datetime.date.today()
        alquiler = Renta(prenda, tiempo, entregar_prenda=True, estado=True, fecha=fecha)
        self.rentas.append(alquiler)
        self.orden[self.cedula] = self.rentas
        self.numero_rentas += 1
        self.deuda = (prenda.valor_alquiler * int(tiempo)) + self.deuda


class Tienda:
    PLANBASICO = "Plan Básico: 3 Prendas por 30 días"
    PLANCIRCULAR = "Plan Circular: 5 Prendas por 30 días"
    PLANMAXIPRO = "Plan MaxiPro: 8 Prendas por 60 días"

    def __init__(self):
        self.prendas: dict[int: Prenda] = {}
        self.usuarios: dict[int: Usuario] = {}

    def registrar_ropa(self):
        """
        p1 = Prenda(1, "Buso", "S", "Negro", "INVIERNO", 40000, 100)
        p2 = Prenda(2, "Pantaloneta", "28", "Azul", "VERANO", 10000, 40)
        p3 = Prenda(3, "Corbata", "XXL", "Negro", "TODOS", 20000, 120)
        p4 = Prenda(4, "Sandalias", "40", "Verde", "VERANO", 15000, 65)
        p5 = Prenda(5, "Sombrero", "M", "Blanco", "VERANO", 35000, 96)
        p6 = Prenda(6, "Botas", "38", "Azul", "INVIERNO", 50000, 114)
        p7 = Prenda(7, "Guantes", "XS", "Negro", "INVIERNO", 4000, 20)
        p8 = Prenda(8, "Tenis", "42", "Morado", "TODOS", 120000, 354)
        self.prendas[p1.codigo] = p1
        self.prendas[p2.codigo] = p2
        self.prendas[p3.codigo] = p3
        self.prendas[p4.codigo] = p4
        self.prendas[p5.codigo] = p5
        self.prendas[p6.codigo] = p6
        self.prendas[p7.codigo] = p7
        self.prendas[p8.codigo] = p8

        self.registrar_usuario(1, "Juan Manuel", "juanmanuelsantamariaarenas01@gmail.com")
        self.registrar_usuario(2, "Matías Yepes", "matius@gmail.com")
        self.registrar_usuario(3, "Juan Fernando", "juanfer@gmail.com")
        self.registrar_usuario(4, "Luis Cardona", "luisacardona@gmail.com")
        self.registrar_usuario(5, "Jesús Alvira", "jesusalvira20@gmail.com")

        # self.alquilar_prenda(1, 4, 32)
        """
        """
        user=self.buscar_usuario(1)
        renta=user.orden[1]
        renta.estado = False
        print(self.prendas[4])
        """

    def buscar_usuario(self, cedula: int) -> Optional[Usuario]:
        for usuario in self.usuarios.values():
            if usuario.cedula == cedula:
                return usuario
        return None

    def buscar_prenda(self, codigo: int) -> Optional[Prenda]:
        for prenda in self.prendas.values():
            if prenda.codigo == codigo:
                return prenda
        return None

    def mostrar_prendas_clima(self, clima: str) -> list[Prenda]:
        ropa = list(self.prendas.values())
        ropa_clima = []
        for prenda in ropa:
            if prenda.esta_disponible():
                if prenda.clima == clima:
                    ropa_clima.append(prenda)
        if len(ropa_clima) > 0:
            return ropa_clima
        else:
            raise PrendaNoDisponibleError(f"No se encontró una prenda disponible con el clima: {clima}")

    def mostrar_prendas_talla(self, talla: str) -> list[Prenda]:
        ropa = list(self.prendas.values())
        ropa_talla = []
        for prenda in ropa:
            if prenda.esta_disponible():
                if prenda.talla == talla:
                    ropa_talla.append(prenda)
        if len(ropa_talla) > 0:
            return ropa_talla
        else:
            raise PrendaNoDisponibleError(f"No se encontró una prenda disponible con la talla: {talla}")

    def mostrar_prendas_color(self, color: str) -> list[Prenda]:
        ropa = list(self.prendas.values())
        ropa_color = []
        for prenda in ropa:
            if prenda.esta_disponible():
                if prenda.color == color:
                    ropa_color.append(prenda)
        if len(ropa_color) > 0:
            return ropa_color
        else:
            raise PrendaNoDisponibleError(f"No se encontró una prenda disponible con el color: {color}")

    def alquilar_prenda(self, cedula: int, codigo: int, tiempo: int):
        """El tiempo es en días"""
        if cedula != "" and codigo != "" and tiempo != "":
            prenda = self.buscar_prenda(int(codigo))
            if prenda is not None:
                if prenda.esta_disponible():
                    usuario = self.buscar_usuario(int(cedula))
                    if usuario is not None:
                        usuario.crear_orden(prenda, tiempo)
                        prenda.disponibilidad_renta = False
                        # print(f"{usuario.nombre}, tu deuda es de {usuario.deuda} mil pesos") #-----------------> Add
                    else:
                        raise UsuarioInexistenteError(f"No se encontró un usuario con la cédula: {cedula}")
                else:
                    raise PrendaNoDisponibleError(f"La prenda: {prenda.nombre} no está disponible en éste momento")
            else:
                raise CodigoPrendaInvalidoError(f"No se encontró una prenda con el código: {codigo}")
        else:
            raise DatosSinIngresarError(f"Tienes que ingresar todos los datos solicitados")

    def mostrar_planes(self, cedula: int):
        plan = ""
        usuario = self.buscar_usuario(int(cedula))
        if usuario is not None:
            if usuario.numero_rentas < 5:
                plan = f"{usuario.nombre}: NO PUEDES ACCEDER A NINGÚN PLAN PERSONALIZADO"
            elif usuario.numero_rentas >= 5 & usuario.numero_rentas < 10:
                plan = f"{usuario.nombre}: EL PLAN AL QUE PUEDES ACCEDER ES {Tienda.PLANBASICO}"
            elif usuario.numero_rentas >= 10 & usuario.numero_rentas < 15:
                plan = f"{usuario.nombre}: EL PLAN AL QUE PUEDES ACCEDER ES {Tienda.PLANCIRCULAR}"
            elif usuario.numero_rentas >= 15:
                plan = f"{usuario.nombre}: EL PLAN AL QUE PUEDES ACCEDER ES {Tienda.PLANMAXIPRO}"
            return plan
        else:
            raise UsuarioInexistenteError(f"No se encontró un usuario con la cédula: {cedula}")

    def hay_usuario(self, cedula: int):
        for cedula_usuario in self.usuarios.keys():
            if cedula_usuario == cedula:
                return True
        return False

    def registrar_usuario(self, cedula: int, nombre: str, correo: str):
        if cedula != "" and nombre != "" and correo != "":
            if self.es_correo_valido(correo):
                if not self.hay_usuario(int(cedula)):
                    self.usuarios[int(cedula)] = Usuario(int(cedula), nombre, correo)
                else:
                    raise CedulaExistenteError(f"La cédula {cedula} ya está registrada")
            else:
                raise CorreoInvalidoError(f"El correo {correo} es inválido")
        else:
            raise DatosSinIngresarError(f"Tienes que ingresar todos los datos solicitados")

    def vender_prenda(self, cedula: int, codigo: int):
        if cedula != "" and codigo != "":
            prenda = self.buscar_prenda(int(codigo))
            usuario = self.buscar_usuario(int(cedula))
            if prenda.esta_disponible():
                usuario.deuda += prenda.valor_prenda
                self.prendas.pop(prenda.codigo)
            else:
                raise PrendaNoDisponibleError(f"La prenda: {prenda} no está disponible en el momento")
        else:
            raise DatosSinIngresarError(f"Tienes que ingresar todos los datos solicitados")

    def recibir_prenda(self, cedula: int, codigo: int):
        if cedula != "" and codigo != "":
            usuario = self.buscar_usuario(int(cedula))
            if usuario is not None:
                prenda = self.buscar_prenda(int(codigo))
                if prenda is not None:
                    for renta in usuario.rentas:
                        if renta.prenda.codigo == int(codigo):
                            # renta.estado = False #-----------------> Add
                            if renta.estado:
                                prenda.disponibilidad_renta = True
                                usuario.rentas.remove(renta)
                            else:
                                usuario.deuda += prenda.valor_prenda
                                self.prendas.pop(int(codigo))
                        else:
                            pass
                else:
                    raise PrendaInexistenteError(f"No se encontró una prenda con el codigo: {codigo}")
            else:
                raise UsuarioInexistenteError(f"No se encontró un usuario con la cedula {cedula}")
        else:
            raise DatosSinIngresarError(f"Tienes que ingresar todos los datos solicitados")

    def es_correo_valido(self, correo: str):
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        return re.match(expresion_regular, correo) is not None

    def enviar_correo(self, correo: str, asunto: str):
        cr = correo
        message = 'Subject: {}'.format(asunto)
        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.starttls()
        server.login("juanfgomez6@gmail.com", "Nacional6.")
        server.sendmail("juanfgomez6@gmail.com", cr, message)
        server.quit()

    def notificar_estado_prenda(self):
        usuarios = self.usuarios.values()
        for usuario in usuarios:
            if len(usuario.rentas) > 0:
                for renta in usuario.rentas:
                    if renta.entregar_prenda:
                        correo = usuario.correo
                        asunto = "PRENDA LISTA PARA RECOGER"
                        self.enviar_correo(correo, asunto)

    def es_tiempo(self, fecha: datetime, tiempo: int):
        ahora = datetime.date.today()
        resta = ahora - fecha
        resta = resta.days
        diferencia = resta - int(tiempo)
        if diferencia <= 2:
            return True
        else:
            return False

    def recordatorio_devolucion(self):
        usuarios = self.usuarios.values()
        for usuario in usuarios:
            if len(usuario.rentas) > 0:
                for renta in usuario.rentas:
                    if self.es_tiempo(renta.fecha, renta.tiempo):
                        correo = usuario.correo
                        cr = str(correo)
                        self.enviar_correo(cr, "La prenda debe ser entregada")

    def revisar_pendientes(self):
        self.notificar_estado_prenda()
        self.recordatorio_devolucion()

    def guardar(self):
        with open("historial.txt", "wb") as file:
            pickle.dump(self, file)

    def cargar(self):
        with open("historial.txt", "rb") as file:
            t = pickle.load(file)
            self.usuarios = t.usuarios
            self.prendas = t.prendas
