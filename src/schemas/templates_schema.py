from pydantic import BaseModel


class TemplateSchema(BaseModel):
    """Modelo para de template."""
    id: int
    template_name: str
    content: str


class TemplateInsertSchema(BaseModel):
    """Modelo para insertar un nuevo template."""
    template_name: str
    content: str


class TemplateUpdateSchema(TemplateSchema):
    """Modelo para actualizar un template existente."""
    pass
