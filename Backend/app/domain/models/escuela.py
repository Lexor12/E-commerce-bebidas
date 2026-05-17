from dataclasses import dataclass
from typing import Optional

@dataclass
class Escuela:
    id_escuela: Optional[int] # Debido a que aqui podemos crear nuevas instancias, podemos crear nuevas escuelas, y como aun no tienen ID, cuando se manden, el sistema detectara esto y le asignara un ID
    nombre: str
    ubicacion: str
    nivel_academico: str
    telefono: str
    estatus: bool = True