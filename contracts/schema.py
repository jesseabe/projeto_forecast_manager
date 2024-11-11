from typing import Optional
from pydantic import BaseModel, PositiveFloat
from enum import Enum
from datetime import date

class rename_columns(str, Enum):
    Ano = "Ano",
    Mes = "Mes"
    Negocio = "Negocio"
    Gerencia = "Gerencia"
    Tecnologia = "Tecnologia"
    Produto = "Produto"
    Rec_Liq = "Receita Liquida"

    class config:
        strict = True
        coerce = True


class dataschema(BaseModel):
    Ano: str
    Mes: str
    Negocio: str
    Gerencia: str
    Tecnologia: str
    Produto: str
    Rec_Liq: float
