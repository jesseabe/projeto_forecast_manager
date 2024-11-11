import pandas as pd
# Processamento de arquivos CSV

#1. Funcao para ler o arquivo csv
def ler_csv(file):
    df = pd.read_csv(file)
    print(df.head())
    return df

if __name__ == "__main__":
    ler_csv("data/df_re.csv")