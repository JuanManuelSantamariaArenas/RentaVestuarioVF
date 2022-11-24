import sys
from mundo.tienda import Tienda
from mundo.excepciones import *


class Consola:

    def __init__(self):
        self.tienda = Tienda()
        self.tienda.cargar()
        self.opciones = {
            "1": self.registrar_usuario,
            "2": self.mostrar_prendas,
            "3": self.alquilar_prenda,
            "4": self.devolver_prenda,
            "5": self.mostrar_ropa_talla,
            "6": self.mostrar_ropa_color,
            "7": self.mostrar_ropa_clima,
            "8": self.mostrar_planes,
            "9": self.comprar_ropa,
            "10": self.guardar,
            "11": self.cargar,
            "12": self.salir
        }

    def mostar_menu(self):
        print("""
        \n
        BIENVENIDO A RENTUARIO
        |||||||||||||||||||||||||||||||||||
        Menú de opciones:\n
        1. Registrar usuario
        2. Mostrar las prendas
        3. Alquilar prenda
        4. Devolver Prenda
        5. Mostrar prendas según la talla
        6. Mostrar ropa según el color
        7. Mostrar ropa según el clima
        8. Mostrar planes personalizados
        9. Comprar ropa
        10. Guardar
        11. Cargar
        12. Salir
        |||||||||||||||||||||||||||||||||||
        """)

    def ejecutar(self):
        while True:
            self.mostar_menu()
            opcion = input("Seleccione una opción: ")
            accion = self.opciones.get(opcion)
            if accion is not None:
                accion()
            else:
                print(f"INFO: {opcion} NO ES UNA OPCIÓN VÁLIDA")

    def registrar_usuario(self):
        try:
            print("- REGISTRAR USUARIO -")
            cedula = int(input("Ingrese su cedula: "))
            nombre = input("Ingrese su nombre: ")
            correo = input("Ingrese su correo (example@gmail.com): ")
            self.tienda.registrar_usuario(cedula, nombre, correo)
        except ValueError:
            print("INFO: SE INGRESO UN VALOR DIFERENTE A UN NÚMERO, POR FAVOR INGRESE SEGÚN LO SOLICITADO")
        except CorreoInvalidoError:
            print("INFO: SE INGRESÓ UN CORREO INVALIDO")
        except CedulaExistenteError:
            print("INFO: LA CEDULA INGRESADA YA EXISTE EN LA TIENDA")
        except DatosSinIngresarError:
            print("INFO: TODOS LOS DATOS DEBEN SER INGRESADOS")
        else:
            print("INFO: EL REGISTRO FUE UN ÉXITO")

    def mostrar_prendas(self):
        print("\n- CODIGO -- PRENDAS -- TALLA -- COLOR -- CLIMA -- P.Alquiler/dia -- P.Compra")
        lista = list(self.tienda.prendas.values())
        for prenda in lista:
            if prenda.disponibilidad_renta:
                print(prenda)
            else:
                pass

    def alquilar_prenda(self):
        try:
            print("- ALQUILAR PRENDA")
            cedula = int(input("Ingrese su cédula: "))
            codigo = int(input("Ingrese el codigo de la prenda: "))
            tiempo = int(input("Ingrese por tiempo que desea alquilarla: "))
            self.tienda.alquilar_prenda(cedula, codigo, tiempo)
        except ValueError:
            print("INFO: INGRESÓ UNA LETRA EN LUGAR DE UN NÚMERO")
        except PrendaNoDisponibleError:
            print("INFO: LA PRENDA SOLICITADA NO ESTÁ DISPONIBLE")
        except CodigoPrendaInvalidoError:
            print("INFO: EL CÓDIGO INGRESADO ES INVALIDO")
        except UsuarioInexistenteError:
            print("INFO: EL USUARIO INGRESADO NO EXISTE")
        else:
            print("INFO: SE REALIZÓ EL ALQUILER CON ÉXIO")

    def mostrar_planes(self):
        try:
            print("-  PLANES PERSONALIZADOS")
            cedula = int(input("Ingrese su cedula: "))
            plan = self.tienda.mostrar_planes(cedula)
            print(plan)
        except ValueError:
            print("INFO: SE INGRESO UN VALOR DIFERENTE A UN NÚMERO, POR FAVOR INGRESE SEGÚN LO SOLICITADO")

    def mostrar_ropa_clima(self):
        try:
            print("- PRENDAS SEGUN EL CLIMA")
            clima = input("Ingrese el clima que desee: \n  VERANO, INVIERNO O TODOS: ")
            prendas_climas = self.tienda.mostrar_prendas_clima(clima)
            for prendas in prendas_climas:
                print(f"{prendas}")
        except TypeError:
            print("BRO: TYPE ERROR")

    def mostrar_ropa_talla(self):
        try:
            print("- PRENDAS SEGUN LA TALLA")
            talla = input("Ingrese la talla que desee: ")
            prendas_talla = self.tienda.mostrar_prendas_talla(talla)
            for prendas in prendas_talla:
                print(f"{prendas}")
        except TypeError:
            print("BRO: TYPE ERROR")

    def mostrar_ropa_color(self):
        try:
            print("- PRENDAS SEGUN EL COLOR")
            color = input("Ingrese el color que desee: ")
            prendas_color = self.tienda.mostrar_prendas_color(color)
            for prendas in prendas_color:
                print(f"{prendas}")
        except TypeError:
            print("BRO: TYPE ERROR")

    def devolver_prenda(self):
        try:
            print("- DEVOLVER PRENDA")
            cedula = int(input("Ingrese su cedula: "))
            codigo = int(input("Ingrese el codigo de la prenda que desea devolver: "))
            self.tienda.recibir_prenda(cedula, codigo)
        except ValueError:
            print("INFO: SE INGRESO UN VALOR DIFERENTE A UN NÚMERO, POR FAVOR INGRESE SEGÚN LO SOLICITADO")
        except AttributeError:
            print("INFO: SE INGRESÓ UNA CÉDULA QUE NO ESTÁ REGISTRADA, POR ENDE NO EXISTE LA ORDEN")
        except CodigoPrendaInvalidoError:
            print("INFO: NO SE ENCUENTRA UNA PRENDA ALQUILADA POR EL USUARIO CON ESE CÓDIGO")
        except PrendaInexistenteError:
            print("INFO: NO SE ENCUENTRA UNA PRENDA EN LA TIENDA CON ESE CODIGO")
        except UsuarioInexistenteError:
            print("INFO: NO SE ENCUENTRA UN USUARIO CON LA CÉDULA INGRESADA")

    def comprar_ropa(self):
        try:
            print(" - COMPRAR ROPA")
            cedula = int(input("Ingrese su cedula: "))
            codigo = int(input("Ingrese el codigo de la prenda que desea comprar: "))
            self.tienda.vender_prenda(codigo, cedula)
        except ValueError:
            print("INFO: SE INGRESO UN VALOR DIFERENTE A UN NÚMERO, POR FAVOR INGRESE SEGÚN LO SOLICITADO")
        except AttributeError:
            print("INFO: SE INGRESÓ UNA CÉDULA QUE NO ESTÁ REGISTRADA, POR FAVOR REGISTRESE \n"
                  "O SE INGRESÓ UNA PRENDA QUE NO ESTÁ DISPONIBLE, VERIFIQUE LA DISPONIBILIDAD")

    def guardar(self):
        self.tienda.guardar()

    def cargar(self):
        self.tienda.cargar()

    def salir(self):
        print("\nMUCHAS GRACIAS POR USAR LA APLICACIÓN")
        self.tienda.guardar()
        sys.exit(0)
