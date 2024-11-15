import pandas as pd
import sqlite3
import sqlalchemy
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.backend.services.file_service import ler_xlsx, process_forecast_data


def xlsx_to_sql(excel_path, db_path, name):
    df = ler_xlsx(excel_path)

    conn = sqlite3.connect(db_path)
    df.to_sql(name, conn, if_exists='replace', index=False)
    conn.close()
    print("Base salva com sucesso")

    # Apaga o arquivo xlsx
    os.remove(excel_path)
    print("Base salva com sucesso e arquivo Excel removido")

    

if __name__ == "__main__":
    # xlsx_to_sql("data/df_or.xlsx", "data/forecast.db", "orcado")
    # xlsx_to_sql("data/df_re.xlsx", "data/forecast.db", "realizado")
    process_forecast_data("data/forecast.xlsx")
    xlsx_to_sql("data/forecast_processed.xlsx", "data/forecast.db", "tbforecast")