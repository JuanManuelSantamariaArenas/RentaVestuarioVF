class AlquilerRopaError(Exception):
    def __init__(self, msg: str):
        self.mensaje = msg


class CorreoInvalidoError(AlquilerRopaError):
    def __init__(self, msg):
        super().__init__(msg)


class CedulaExistenteError(AlquilerRopaError):
    def __init__(self, msg):
        super().__init__(msg)


class UsuarioInexistenteError(AlquilerRopaError):
    def __init__(self, msg):
        super().__init__(msg)


class CodigoPrendaInvalidoError(AlquilerRopaError):
    def __init__(self, msg):
        super().__init__(msg)


class PrendaClimaNoDisponibleError(AlquilerRopaError):
    def __init__(self, msg):
        super().__init__(msg)


class ClimaIncorrectoError(AlquilerRopaError):
    def __init__(self, msg):
        super().__init__(msg)


class PrendaNoDisponibleError(AlquilerRopaError):
    def __init__(self, msg):
        super().__init__(msg)


class PrendaInexistenteError(AlquilerRopaError):
    def __init__(self, msg):
        super().__init__(msg)


class DatosSinIngresarError(AlquilerRopaError):
    def __init__(self, msg):
        super().__init__(msg)

