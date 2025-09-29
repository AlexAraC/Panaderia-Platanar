from django import template             # 1. Importa el módulo de Django para crear filtros y tags personalizados.

register = template.Library()           # 2. Crea un "registro" de filtros que Django reconocerá en los templates.

@register.filter                         # 3. Decorador que indica que la función siguiente será un filtro disponible en templates.
def get_item(dictionary, key):           # 4. Define la función get_item que recibe un diccionario y una clave.                                 
    return dictionary.get(key)           # 6. Devuelve el valor del diccionario correspondiente a la clave. Si no existe, devuelve None.
