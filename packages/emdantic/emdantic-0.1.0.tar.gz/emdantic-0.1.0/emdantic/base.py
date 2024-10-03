from pydantic import BaseModel


class EmbModel(BaseModel):
    """Embeddable pydantic model"""

    def embed(self):
        """Embed the model"""
        raise NotImplementedError
