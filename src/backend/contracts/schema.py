import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema
from typing import Optional

# Definindo o schema com Pandera
class DataSchema(pa.SchemaModel):
    Ano: int
    Mes: int
    Negocio: str
    Gerencia: str
    Tecnologia: str
    Produto: str
    Receita_Liquida: float

    class Config:
        # Adiciona validações de configuração, caso necessário
        strict = True  # Garante que o DataFrame não terá colunas extra

