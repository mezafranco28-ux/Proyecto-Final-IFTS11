from datetime import datetime, date, time
from registro import Registro 

class Turno(Registro):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dt_fecha_hora = None
    
    def validar(self) -> bool:
        if not hasattr(self, 'fecha') or not hasattr(self, 'hora'):
            return False
            
        try:
            fecha_str = self.fecha.strip()
            hora_str = self.hora.strip()
            
            fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y").date()
            hora_obj = datetime.strptime(hora_str, "%H:%M").time()
            
            self.dt_fecha_hora = datetime.combine(fecha_obj, hora_obj)
            return True
        except:
            return False

    def __lt__(self, other):
        if not self.dt_fecha_hora or not other.dt_fecha_hora:
             self.validar()
             other.validar()
             
             if not self.dt_fecha_hora or not other.dt_fecha_hora:
                 return False 
                 
        return self.dt_fecha_hora < other.dt_fecha_hora