import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox, QAbstractItemView, QInputDialog
from ui.menuPrincipal import *
from ui.dialogoRegistrarUsuario import *
from ui.dialogoMostrarPrendas import *
from ui.dialogoAlquilarPrenda import *
from ui.dialogoComprarPrenda import *
from ui.dialogoDevolverPrenda import *
from mundo.tienda import *


class MainWindowTiendaRopa(QMainWindow, Ui_MenuPrincipal):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MenuPrincipal.__init__(self)
        self.tienda = Tienda()
        self.tienda.cargar()
        self.dialogo_registrar_usuario = DialogoRegistrarUsuario()
        self.dialogo_alquilar_prenda = DialogoAlquilarPrenda()
        self.dialogo_mostrar_prendas = DialogoMostrarPrendas
        self.dialogo_comprar_prenda = DialogoComprarPrenda()
        self.dialogo_devolver_prenda = DialogoDevolverPrenda()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.configurar()

    def configurar(self):

        self.btn_salir.clicked.connect(self.cerrar_app)
        self.btn_registrar_usuario.clicked.connect(self.abrir_dialogo_registrar_usuario)
        self.btn_alquilar_prenda.clicked.connect(self.abrir_dialogo_alquilar_prenda)
        self.btn_comprar_prenda.clicked.connect(self.abrir_dialogo_comprar_prenda)
        self.btn_devolver_prenda.clicked.connect(self.abrir_dialogo_devolver_prenda)
        self.btn_mostrar_prendas.clicked.connect(self.abrir_dialogo_mostrar_prendas)
        self.btn_mostrar_por_talla.clicked.connect(self.mostrar_por_talla)
        self.btn_mostrar_por_clima.clicked.connect(self.mostrar_por_clima)
        self.btn_mostrar_por_color.clicked.connect(self.mostrar_por_color)
        self.btn_mostrar_planes.clicked.connect(self.mostrar_planes)
        self.btn_revisar_pendientes.clicked.connect(self.revisar_pendientes)

    def mostrar_mensaje_error(self, err):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Error")
        msg_box.setText(err.mensaje)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def cerrar_app(self):
        self.tienda.guardar()
        self.destroy()
        sys.exit(0)

    def abrir_dialogo_registrar_usuario(self):
        resp = self.dialogo_registrar_usuario.exec()
        if resp == QDialog.Accepted:
            nombre = self.dialogo_registrar_usuario.le_nombre.text()
            cedula = self.dialogo_registrar_usuario.le_cedula.text()
            correo = self.dialogo_registrar_usuario.le_correo.text()
            try:
                self.tienda.registrar_usuario(cedula, nombre, correo)
            except DatosSinIngresarError as err:
                self.mostrar_mensaje_error(err)
            except CedulaExistenteError as err:
                self.mostrar_mensaje_error(err)
            except CorreoInvalidoError as err:
                self.mostrar_mensaje_error(err)
        self.dialogo_registrar_usuario.limpiar()

    def abrir_dialogo_mostrar_prendas(self):
        prendas = self.obtener_prendas()
        self.dialogo_mostrar_prendas(prendas).exec()

    def obtener_prendas(self) -> list[Prenda]:
        prendas = list(self.tienda.prendas.values())
        prendas_disponibles = []
        for prenda in prendas:
            if prenda.disponibilidad_renta:
                prendas_disponibles.append(prenda)
            else:
                pass
        return prendas_disponibles

    def abrir_dialogo_alquilar_prenda(self):
        resp = self.dialogo_alquilar_prenda.exec()
        if resp == QDialog.Accepted:
            cedula = self.dialogo_alquilar_prenda.le_cedula.text()
            codigo = self.dialogo_alquilar_prenda.le_codigo.text()
            dias = self.dialogo_alquilar_prenda.le_dias.text()
            try:
                self.tienda.alquilar_prenda(cedula, codigo, dias)
            except UsuarioInexistenteError as err:
                self.mostrar_mensaje_error(err)
            except PrendaNoDisponibleError as err:
                self.mostrar_mensaje_error(err)
            except CodigoPrendaInvalidoError as err:
                self.mostrar_mensaje_error(err)
            except DatosSinIngresarError as err:
                self.mostrar_mensaje_error(err)
        self.dialogo_alquilar_prenda.limpiar()

    def abrir_dialogo_comprar_prenda(self):
        resp = self.dialogo_comprar_prenda.exec()
        if resp == QDialog.Accepted:
            cedula = self.dialogo_comprar_prenda.le_cedula.text()
            codigo = self.dialogo_comprar_prenda.le_codigo.text()
            try:
                self.tienda.vender_prenda(cedula, codigo)
            except PrendaNoDisponibleError as err:
                self.mostrar_mensaje_error(err)
            except DatosSinIngresarError as err:
                self.mostrar_mensaje_error(err)
        self.dialogo_comprar_prenda.limpiar()

    def abrir_dialogo_devolver_prenda(self):
        resp = self.dialogo_devolver_prenda.exec()
        if resp == QDialog.Accepted:
            cedula = self.dialogo_devolver_prenda.le_cedula.text()
            codigo = self.dialogo_devolver_prenda.le_codigo.text()
            try:
                self.tienda.recibir_prenda(cedula, codigo)
            except UsuarioInexistenteError as err:
                self.mostrar_mensaje_error(err)
            except PrendaInexistenteError as err:
                self.mostrar_mensaje_error(err)
            except DatosSinIngresarError as err:
                self.mostrar_mensaje_error(err)
        self.dialogo_devolver_prenda.limpiar()

    def abrir_dialogo_mostrar_prendas_atributo(self, atributo: list):
        self.dialogo_mostrar_prendas(atributo).exec()

    def mostrar_por_talla(self):
        talla, ok_pressed = QInputDialog.getItem(self, "Por talla",
                                                 "Seleccione la talla de ropa que desea", ["XS", "S", "XXL", "40", "28",
                                                                                           "42", "M", "38"], 0, False)
        if ok_pressed:
            try:
                lista_talla = self.tienda.mostrar_prendas_talla(talla)
                if lista_talla is not None:
                    self.abrir_dialogo_mostrar_prendas_atributo(lista_talla)
                else:
                    raise PrendaNoDisponibleError
            except PrendaNoDisponibleError as err:
                self.mostrar_mensaje_error(err)

    def mostrar_por_color(self):
        color, ok_pressed = QInputDialog.getItem(self, "Por color", "Seleccione el color de ropa que desea",
                                                 ["Negro", "Azul", "Verde", "Blanco", "Morado"], 0, False)
        if ok_pressed:
            try:
                lista_color = self.tienda.mostrar_prendas_color(color)
                self.abrir_dialogo_mostrar_prendas_atributo(lista_color)
            except PrendaNoDisponibleError as err:
                self.mostrar_mensaje_error(err)

    def mostrar_por_clima(self):
        clima, ok_pressed = QInputDialog.getItem(self, "Por clima", "Seleccione el tipo de clima para el que desea la "
                                                                    "ropa", ["VERANO", "INVIERNO", "TODOS"], 2, False)
        if ok_pressed:
            try:
                lista_clima = self.tienda.mostrar_prendas_clima(clima)
                self.abrir_dialogo_mostrar_prendas_atributo(lista_clima)
            except PrendaNoDisponibleError as err:
                self.mostrar_mensaje_error(err)

    def mostrar_planes(self):
        cedula, ok_pressed = QInputDialog.getInt(self, "Ver planes", "Ingrese su cédula: ", 1, 1)
        try:
            if ok_pressed:
                plan = self.tienda.mostrar_planes(cedula)
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("PLANES PERSONALIZADOS")
                msg_box.setText(plan)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec()
        except UsuarioInexistenteError as err:
            self.mostrar_mensaje_error(err)

    def revisar_pendientes(self):
        self.tienda.revisar_pendientes()
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("INFO")
        msg_box.setText("Se han revisado todos los pendientes.")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()


class DialogoRegistrarUsuario(QDialog, Ui_AgregarUsuario):
    def __init__(self):
        QDialog.__init__(self)
        Ui_AgregarUsuario.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.configurar()

    def configurar(self):
        self.le_cedula.setValidator(QRegExpValidator(QRegExp("\\d{10}"), self.le_cedula))

    def limpiar(self):
        self.le_nombre.clear()
        self.le_correo.clear()
        self.le_cedula.clear()


class DialogoMostrarPrendas(QDialog, Ui_MostrarPrendas):
    def __init__(self, prendas: list):
        QDialog.__init__(self)
        Ui_MostrarPrendas.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.configurar()
        self.mostrar_prendas(prendas)

    def configurar(self):
        table_model = QStandardItemModel()
        table_model.setHorizontalHeaderLabels(["CODE", "PRENDA", "TALLA", "COLOR", "CLIMA", "Renta/dia",
                                               "P.Compra"])
        self.tableView_prendas.setModel(table_model)
        self.tableView_prendas.setColumnWidth(0, 30)
        self.tableView_prendas.setColumnWidth(1, 80)
        self.tableView_prendas.setColumnWidth(2, 40)
        self.tableView_prendas.setColumnWidth(3, 60)
        self.tableView_prendas.setColumnWidth(4, 70)
        self.tableView_prendas.setColumnWidth(5, 65)
        self.tableView_prendas.setColumnWidth(6, 60)
        self.tableView_prendas.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def mostrar_prendas(self, prendas: list[Prenda]):
        model = self.tableView_prendas.model()
        for item in prendas:
            celda_1 = QStandardItem(str(item.codigo))
            celda_2 = QStandardItem(item.nombre)
            celda_3 = QStandardItem(item.talla)
            celda_4 = QStandardItem(item.color)
            celda_5 = QStandardItem(item.clima)
            celda_6 = QStandardItem(str(item.valor_alquiler))
            celda_7 = QStandardItem(str(item.valor_prenda))
            model.appendRow([celda_1, celda_2, celda_3, celda_4, celda_5, celda_6, celda_7])


class DialogoAlquilarPrenda(QDialog, Ui_AlquilarPrenda):
    def __init__(self):
        QDialog.__init__(self)
        Ui_AlquilarPrenda.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.configurar()

    def configurar(self):
        self.le_cedula.setValidator(QRegExpValidator(QRegExp("\\d{10}"), self.le_cedula))
        self.le_codigo.setValidator(QRegExpValidator(QRegExp("\\d{4}"), self.le_codigo))
        self.le_dias.setValidator(QRegExpValidator(QRegExp("\\d{2}"), self.le_dias))

    def limpiar(self):
        self.le_cedula.clear()
        self.le_codigo.clear()
        self.le_dias.clear()


class DialogoComprarPrenda(QDialog, Ui_ComprarPrenda):
    def __init__(self):
        QDialog.__init__(self)
        Ui_ComprarPrenda.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.configurar()

    def configurar(self):
        self.le_cedula.setValidator(QRegExpValidator(QRegExp("\\d{10}"), self.le_cedula))
        self.le_codigo.setValidator(QRegExpValidator(QRegExp("\\d{4}"), self.le_codigo))

    def limpiar(self):
        self.le_cedula.clear()
        self.le_codigo.clear()


class DialogoDevolverPrenda(QDialog, Ui_DevolverPrenda):
    def __init__(self):
        QDialog.__init__(self)
        Ui_DevolverPrenda.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.configurar()

    def configurar(self):
        self.le_cedula.setValidator(QRegExpValidator(QRegExp("\\d{10}"), self.le_cedula))
        self.le_codigo.setValidator(QRegExpValidator(QRegExp("\\d{4}"), self.le_codigo))

    def limpiar(self):
        self.le_codigo.clear()
        self.le_cedula.clear()


class DialogoMostrarPlanes(QDialog, Ui_MostrarPrendas):
    def __init__(self, plan: str):
        QDialog.__init__(self)
        Ui_MostrarPrendas.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.configurar(plan)

    def configurar(self, plan):
        pass
