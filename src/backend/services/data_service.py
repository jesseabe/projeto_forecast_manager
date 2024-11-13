import pandas as pd
import sqlite3
import sqlalchemy
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.backend.services.file_service import ler_xlsx

def csv_to_sql(excel_path, db_path, name):
    df = ler_xlsx(excel_path)

    conn = sqlite3.connect(db_path)
    df.to_sql(name, conn, if_exists='replace', index=False)
    conn.close()
    print("Base salva com sucesso")

    # Apaga o arquivo xlsx
    os.remove(excel_path)
    print("Base salva com sucesso e arquivo Excel removido")

    

if __name__ == "__main__":
    csv_to_sql("data/df_or.xlsx", "data/forecast.db", "orcado")
    csv_to_sql("data/df_re.xlsx", "data/forecast.db", "realizado")