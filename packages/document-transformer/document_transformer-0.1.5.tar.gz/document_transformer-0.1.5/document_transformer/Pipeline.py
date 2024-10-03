# Pipeline.py

from typing import List, Any, Union, get_type_hints, get_origin
from pydantic import BaseModel
from .Document import Document
from .Transformer import DocumentTransformer

class Pipeline(BaseModel):
    transformers: List[DocumentTransformer]
    all_docs: List[Document] = []

    def run(self, input: Union[Document, List[Document]]) -> Union[Document, List[Document]]:
        output = input

        # Inicializamos all_docs y extraemos documentos del input
        self.all_docs.extend(self.process_result(output))

        for transformer in self.transformers:

            if isinstance(output, list):
                # Obtenemos el tipo de entrada que espera el transformador
                input_type = get_type_hints(transformer)['input']
                origin = get_origin(input_type)

                if origin == list:
                    # Si el transformador espera una lista, se la pasamos directamente
                    transformer.input = output
                    output = transformer.run()
                    # self.all_docs.extend(self.process_result(output))
                else:
                    # Si el transformador espera un solo documento, aplicamos la transformación a cada documento
                    transformed_docs = []
                    for doc in output:
                        transformer.input = doc
                        result = transformer.run()
                        transformed_docs.extend(self.process_result(result))
                    output = transformed_docs
            else:
                # Si output es un solo documento, se lo pasamos directamente al transformador
                transformer.input = output
                output = transformer.run()
            
            self.all_docs.extend(self.process_result(output))

        return output


    def process_result(self, result):
        return self._flatten_documents(result)

    def _flatten_documents(self, docs: Any, recursive: bool = True) -> List[Document]:
        flat_list = []
        if isinstance(docs, Document):
            flat_list.append(docs)
            if recursive:
                # Recorremos los campos definidos en el modelo
                for field_name, field in docs.__fields__.items():
                    attr_value = getattr(docs, field_name)
                    if isinstance(attr_value, Document):
                        flat_list.extend(self._flatten_documents(attr_value, recursive=recursive))
                    elif isinstance(attr_value, (list, tuple, set, dict)):
                        # Verificamos si la colección contiene documentos
                        if any(isinstance(item, Document) for item in attr_value):
                            flat_list.extend(self._flatten_documents(attr_value, recursive=recursive))
        elif isinstance(docs, dict):
            for value in docs.values():
                flat_list.extend(self._flatten_documents(value, recursive=recursive))
        elif isinstance(docs, (list, tuple, set)):
            for item in docs:
                if isinstance(item, Document) or isinstance(item, (list, tuple, set, dict)):
                    flat_list.extend(self._flatten_documents(item, recursive=recursive))
        return flat_list

    def get_traces(self):
        # Eliminar duplicados convirtiendo a un conjunto
        return [
            {
                "id": doc.id,
                "path": doc.path,
                "type": type(doc).__name__,
                "childrens": list(doc.childrens),
                "parents": list(doc.parents),
            }
            for doc in self.all_docs
        ]
