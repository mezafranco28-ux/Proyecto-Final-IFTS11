from registro import Registro 

class Transforma(object):
    
    def __init__(self, atributos, tipo_registro=None):
        self.keys = [k.strip() for k in atributos] 
        self.tipo_registro = tipo_registro or Registro 

    def toDict(self, values):
        if len(values) != len(self.keys):
            return None
        
        datos = {}
        for k, v in zip(self.keys, values):
            datos[k] = v.strip()
            
        return datos
    
    def toObject(self, values):
        datos = self.toDict(values)
        if datos is None:
            return None

        try:
            obj = self.tipo_registro(**datos)
            if hasattr(obj, 'validar') and not obj.validar():
                return None 
            return obj
        except Exception as e:
            return None