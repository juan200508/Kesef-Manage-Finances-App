"""Excepciones propias del dominio de la aplicación.

Estas excepciones son lanzadas por la capa de servicios (app/services/)
y no dependen de FastAPI ni de HTTPException — se traducen a respuestas
HTTP en la capa de routers (app/api/routers/), donde cada una se mapea
al status code correspondiente.
"""


class AppException(Exception):
    #Excepción base de la que heredan todas las excepciones de negocio.

    def __init__(self, message: str = "Something went wrong"):
        self.message = message
        super().__init__(self.message)


class NotFoundError(AppException):
    #Base para cualquier caso de 'recurso no encontrado
    def __init__(self, resource_name: str, resource_id: str | None = None):
        self.resource_name = resource_name
        self.resource_id = resource_id
        message = f"{resource_name} not found"
        if resource_id:
            message += f" (id: {resource_id})"
        super().__init__(message)


class ConfigurationError(AppException):
    # Base para errores de configuración del sistema, no causados por el usuario.
    # Ej: falta un dato que el sistema debería tener sembrado (seed) de antemano
    def __init__(self, message: str = "Error in the system config"):
        super().__init__(message)


# --- Excepciones específicas: Category ---

class CategoryNotFoundError(NotFoundError):
    def __init__(self, category_id: str | None = None):
        super().__init__(resource_name="Category", resource_id=category_id)


class DefaultCategoryNotConfiguredError(ConfigurationError):
    # Se lanza si la categoría global 'Otros' no existe cuando se necesita
    # para reasignar movimientos de una categoría eliminada
    def __init__(self, category_name: str = "Otros"):
        super().__init__(
            message=f"The backup category '{category_name}' is not config in the system"
        )