from pydantic import BaseModel

class TemplateSchema(BaseModel):
    """Model for a template."""
    id: int
    template_name: str
    content: str


class TemplateInsertSchema(BaseModel):
    """Model for inserting a new template."""
    template_name: str
    content: str


class TemplateUpdateSchema(TemplateSchema):
    """Model for updating an existing template."""
    pass
