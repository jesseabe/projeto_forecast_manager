import pandas as pd
import pandera as pa
from pandera import Column
from pandera.typing import DataFrame
from typing import Optional

# Definindo o schema com Pandera
class DataSchema(pa.DataFrameSchema):
    Ano = Column(pa.Int, nullable=False)
    Mes = Column(pa.Int, nullable=False)
    Negocio = Column(pa.String, nullable=False)
    Gerencia = Column(pa.String, nullable=False)
    Tecnologia = Column(pa.String, nullable=False)
    Produto = Column(pa.String, nullable=False)
    Receita_Liquida = Column(pa.Float, nullable=False)

    class Config:
        # Adiciona validações de configuração, caso necessário
        strict = True  # Garante que o DataFrame não terá colunas extra


