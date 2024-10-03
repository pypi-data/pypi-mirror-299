# Transformer.py

from abc import ABC, abstractmethod
from typing import Any, Optional, Union, List, Dict, Callable
from pydantic import BaseModel
from pathlib import Path
from .Document import Document
import re

class DocumentTransformer(ABC, BaseModel):
    input: Optional[Any] = None  # Puede ser Document, List[Document] o cualquier estructura
    output: Optional[Any] = None
    to: Optional[Union[
        str,
        Path,
        Dict[str, Union[str, Path]],
        Callable[[Document], Optional[Path]]
    ]] = None

    @abstractmethod
    def transformer(self) -> Any:
        pass

    def get_save_path(self, document: Document, index: int = 0) -> Optional[Path]:
        if self.to:
            if callable(self.to):
                return self.to(document)
            elif isinstance(self.to, dict):
                # Determinar el tipo de documento
                doc_type = type(document).__name__
                # Obtener la plantilla de ruta correspondiente
                path_template = self.to.get(doc_type)
                if not path_template:
                    return None  # No se debe guardar este tipo de documento
                # Resolver placeholders en la plantilla
                formatted_path = self._resolve_placeholders(str(path_template), document)
                return Path(formatted_path)
            else:
                # Si 'to' es una cadena o Path
                path_template = str(self.to)
                # Resolver placeholders en la plantilla
                formatted_path = self._resolve_placeholders(path_template, document)
                return Path(formatted_path)
        return None
    
    # Función para resolver placeholders con acceso a atributos anidados
    def _resolve_placeholders(self, template: str, document: Document) -> str:
        pattern = r'\{([^\}]+)\}'

        def get_value(obj, attr_path):
            parts = attr_path.split('.')
            for part in parts:
                if '[' in part and ']' in part:
                    attr, key = re.match(r'([^\[]+)\[([^\]]+)\]', part).groups()
                    obj = getattr(obj, attr)
                    obj = obj[key]
                else:
                    obj = getattr(obj, part)
            return obj

        def replacer(match):
            expression = match.group(1)
            try:
                value = get_value(document, expression)
                return str(value)
            except Exception as e:
                return match.group(0)

        return re.sub(pattern, replacer, template)

    def run(self):
        self.output = self.transformer()
        # Establecer relaciones automáticamente
        self._set_relationships()
        # Guardar documentos si es necesario
        self.save()
        return self.output

    def save(self):
        output_docs = self._flatten_documents(self.output)
        for i, doc in enumerate(output_docs):
            if save_path := self.get_save_path(doc, i):
                doc.save(str(save_path))

    def _set_relationships(self):
        # Obtener documentos de entrada y salida de nivel superior
        input_docs = self._flatten_documents(self.input, recursive=False)
        output_docs = self._flatten_documents(self.output, recursive=False)

        # Establecer relaciones entre documentos de entrada y salida de nivel superior
        for out_doc in output_docs:
            for in_doc in input_docs:
                out_doc.parents.add(in_doc.id)
                in_doc.childrens.add(out_doc.id)

        # Establecer relaciones internas en los documentos de salida
        self._set_internal_relationships(self.output)

    def _flatten_documents(self, docs: Any, recursive: bool = True) -> List[Document]:
        flat_list = []
        if isinstance(docs, Document):
            flat_list.append(docs)
            if recursive:
                # Recorremos los atributos del documento
                for attr_name in vars(docs):
                    if attr_name.startswith('_'):
                        continue  # Saltar atributos privados
                    attr_value = getattr(docs, attr_name)
                    if isinstance(attr_value, Document) or isinstance(attr_value, (list, dict, tuple, set)):
                        flat_list.extend(self._flatten_documents(attr_value, recursive=recursive))
        elif isinstance(docs, dict):
            for value in docs.values():
                flat_list.extend(self._flatten_documents(value, recursive=recursive))
        elif isinstance(docs, (list, tuple, set)):
            for item in docs:
                flat_list.extend(self._flatten_documents(item, recursive=recursive))
        return flat_list


    def _set_internal_relationships(self, docs: Any):
        if isinstance(docs, Document):
            child_docs = []
            for attr_name in vars(docs):
                if attr_name.startswith('_'):
                    continue  # Saltar atributos privados
                attr_value = getattr(docs, attr_name)
                if isinstance(attr_value, Document):
                    child_docs.append(attr_value)
                elif isinstance(attr_value, (list, dict, tuple, set)):
                    child_docs.extend(self._flatten_documents(attr_value))
            for child in child_docs:
                if child.id != docs.id:
                    child.parents.add(docs.id)
                    docs.childrens.add(child.id)
            # Recursividad en los hijos
            for child in child_docs:
                self._set_internal_relationships(child)
        elif isinstance(docs, dict):
            for value in docs.values():
                self._set_internal_relationships(value)
        elif isinstance(docs, (list, tuple, set)):
            for item in docs:
                self._set_internal_relationships(item)
