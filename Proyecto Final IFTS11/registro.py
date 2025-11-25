class Registro(object):
    
    def __init__(self, **kwargs):
        for clave, valor in kwargs.items():
            setattr(self, clave, valor)
    
    def __str__(self):
        atributos = []
        for clave, valor in self.__dict__.items():
            if not clave.startswith('_'): # Excluye atributos internos como _generate_clave
                atributos.append(f"{clave}: {valor}")
        clase = self.__class__.__name__
        return f"<{clase}: {', '.join(atributos)}>"


class Cliente(Registro):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def validar(self):
        if not hasattr(self, 'nombre') or not self.nombre.strip():
            return False
        if hasattr(self, 'dni') and len(self.dni.strip()) != 8:
            return False
        return True
    
    def nombre_completo(self):
        nombre = getattr(self, 'nombre', '').strip()
        apellido = getattr(self, 'apellido', '').strip()
        
        if nombre and apellido:
            return f"{nombre} {apellido}"
        return nombre or "Cliente sin nombre"