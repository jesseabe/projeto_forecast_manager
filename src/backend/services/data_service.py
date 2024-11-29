import time
import pandas as pd
import sqlite3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.backend.services.file_service import ler_xlsx, process_forecast_data


def xlsx_to_sql(excel_path, db_path, name):
    try:
        # Verifica se o arquivo existe antes de processar
        if not os.path.exists(excel_path):
            print(f"Aguardando o arquivo {excel_path}...")
            return
        
        df = ler_xlsx(excel_path)
        # Ajustando valores da coluna 'Receita_Liquida'
        df["Receita_Liquida"] = df["Receita_Liquida"].apply(lambda x: 0.00 if x == 0.01 else x)

        conn = sqlite3.connect(db_path)
        df.to_sql(name, conn, if_exists='replace', index=False)
        conn.close()
        print(f"Base '{name}' salva com sucesso no banco de dados")

        # Remove o arquivo processado
        os.remove(excel_path)
        print(f"Arquivo {excel_path} processado e removido")
    except Exception as e:
        print(f"Erro ao processar o arquivo {excel_path}: {e}")


if __name__ == "__main__":
    db_path = "data/forecast.db"
    arquivos = {
        "data/df_or.xlsx": "orcado",
        "data/df_re.xlsx": "realizado",
        "data/forecast.xlsx": None,  # Será processado antes de ser salvo
        "data/forecast_processed.xlsx": "tbforecast"
    }

    print("Monitorando arquivos... Pressione Ctrl+C para sair.")
    try:
        while True:
            for arquivo, tabela in arquivos.items():
                if os.path.exists(arquivo):
                    if arquivo == "data/forecast.xlsx":
                        process_forecast_data(arquivo)
                    elif tabela:
                        xlsx_to_sql(arquivo, db_path, tabela)
            time.sleep(5)  # Intervalo de verificação
    except KeyboardInterrupt:
        print("Monitoramento encerrado.")
