# Document.py

from typing import List, Dict, Any, Optional, Set, ClassVar
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4
from pathlib import Path
from weakref import WeakValueDictionary

class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    path: Optional[str] = None
    data: Any = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    parents: Set[str] = Field(default_factory=set)
    childrens: Set[str] = Field(default_factory=set)
    # Registro de todas las instancias de Document
    _registry: ClassVar[WeakValueDictionary] = WeakValueDictionary()

    def __init__(self, **data):
        super().__init__(**data)
        # Registrar la instancia en el registro
        self._registry[self.id] = self

    @field_validator('path')
    def check_path_exists(cls, value):
        if value:
            path = Path(value)
            if not path.exists():
                raise ValueError(f"El archivo en la ruta '{value}' no existe.")
            return value

    def read(self):
        """
        Método personalizado para leer el archivo. Define self.data.
        """
        if self.path:
            try:
                with open(self.path, 'rb') as file:
                    self.data = file.read()
                    return self
            except Exception as e:
                print(f"Error al leer el archivo: {e}")
                raise e

        raise FileNotFoundError("Defina la ruta del archivo")

    def save(self, path: str):
        self.path = path
        _path = Path(path)
        folder = _path.parent
        folder.mkdir(parents=True, exist_ok=True)
        return self.saver(path)

    def saver(self, path):
        """Clase personalizada para almacenar los datos."""
        with open(path, 'wb') as file:
            file.write(self.data)
        return self

    def append(self, parent: 'Document'):
        # Si se agrega un documento adicional, este será padre
        self.parents.add(parent.id)
        # Y debemos agregar a este como hijo
        parent.childrens.add(self.id)
        # Registrar el padre si no está registrado
        self._registry[parent.id] = parent
        return self.appender(parent)

    def appender(self, parent):
        """Clase que puede sobreescribirse con la lógica personalizada."""
        return self

    def extend(self, parents: List['Document']):
        # Si se agregan documentos adicionales, estos serán padres
        self.parents.update([parent.id for parent in parents])
        # Y debemos agregarlos como hijos
        for parent in parents:
            parent.childrens.add(self.id)
            # Registrar el padre si no está registrado
            self._registry[parent.id] = parent
        return self.extender(parents)

    def extender(self, others):
        """Agrega los contenidos de otros documentos."""
        for other in others:
            self.appender(other)
        return self

    def reset(self):
        self.parents = set()
        self.childrens = set()
        return self

    # Métodos para resolver IDs a instancias de Document
    def get_parents(self) -> Set['Document']:
        return {self._registry[parent_id] for parent_id in self.parents if parent_id in self._registry}

    def get_childrens(self) -> Set['Document']:
        return {self._registry[child_id] for child_id in self.childrens if child_id in self._registry}

    # Sobrescribir __setattr__ para actualizar relaciones
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name not in ('parents', 'childrens', '_registry'):
            self._update_relationships(name, value)

    def _update_relationships(self, name, value):
        if isinstance(value, Document):
            # Establecer relación padre-hijo
            value.parents.add(self.id)
            self.childrens.add(value.id)
            # Registrar el documento relacionado
            self._registry[value.id] = value
        elif isinstance(value, (list, set, tuple)):
            for item in value:
                if isinstance(item, Document):
                    item.parents.add(self.id)
                    self.childrens.add(item.id)
                    self._registry[item.id] = item
        elif isinstance(value, dict):
            for item in value.values():
                if isinstance(item, Document):
                    item.parents.add(self.id)
                    self.childrens.add(item.id)
                    self._registry[item.id] = item
