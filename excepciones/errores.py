class FoodStoreError(Exception):
    """Excepción base de todos los errores de negocio de Food Store."""


class EntidadNoEncontradaError(FoodStoreError):
    """El id buscado no existe o corresponde a una entidad eliminada."""


class DatoInvalidoError(FoodStoreError):
    """Un dato ingresado no cumple el formato o la regla esperada."""


class PrecioInvalidoError(DatoInvalidoError):
    """El precio ingresado es inválido (por ejemplo, negativo)."""


class StockInsuficienteError(FoodStoreError):
    """La cantidad pedida supera el stock disponible del producto."""


class DuplicadoError(FoodStoreError):
    """Ya existe una entidad con ese dato único (mail, nombre de categoría)."""


class OperacionNoPermitidaError(FoodStoreError):
    """La operación solicitada viola una regla de negocio."""


class CredencialesInvalidasError(FoodStoreError):
    """El mail o la contraseña no coinciden, o el usuario está eliminado."""
