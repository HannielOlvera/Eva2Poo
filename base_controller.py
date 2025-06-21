# src/app/controllers/base_controller.py

from abc import ABC

class BaseController(ABC):
    """
    Controlador base que centraliza el manejo de peticiones a la API
    y el logging de errores. Los controladores específicos pueden
    usar _handle_request para invocar métodos del APIClient de forma
    consistente.
    """

    def _handle_request(self, func, *args, **kwargs):
        """
        Ejecuta la función 'func' con los argumentos proporcionados,
        captura excepciones para logging y retorna el resultado.
        """
        try:
            response = func(*args, **kwargs)
            return self._parse_response(response)
        except Exception as e:
            # Logging centralizado de errores
            print(f"[ERROR] {self.__class__.__name__}: {e}")
            raise

    def _parse_response(self, response):
        """
        Método interno para transformar o validar la respuesta de la API.
        Por defecto devuelve la respuesta tal cual.
        """
        return response

    def get_entities(self):
        """
        Método de conveniencia que pueden implementar los controladores
        que necesiten listar colecciones de entidades (tareas, usuarios, etc.).
        Si no se sobreescribe, lanza NotImplementedError.
        """
        raise NotImplementedError(f"{self.__class__.__name__} no implementó get_entities()")
