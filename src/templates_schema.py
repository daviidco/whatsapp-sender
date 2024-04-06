from pydantic import BaseModel

class TemplateInsert(BaseModel):
    """Modelo para insertar un nuevo template."""
    template_name: str
    content: str

class TemplateUpdate(BaseModel):
    """Modelo para actualizar un template existente."""
    id: int
    template_name: str
    content: str
