import pandas as pd
import sqlite3
import sqlalchemy
from src.backend.services.file_service import ler_csv
import os


def csv_to_sql(csv_path, db_path, name):
    df = ler_csv(csv_path)

    conn = sqlite3.connect(db_path)
    df.to_sql(name, conn, if_exists='replace', index=False)
    conn.close()
    print("Base salva com sucesso")

    # Apaga o arquivo CSV
    os.remove(csv_path)
    print("Base salva com sucesso e arquivo CSV removido")

    

if __name__ == "__main__":
    csv_to_sql("data/df_or.csv", "data/orcado.db", "orcado")
    csv_to_sql("data/df_re.csv", "data/realizado.db", "realizado")