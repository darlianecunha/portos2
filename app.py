import streamlit as st
import pandas as pd

# Caminho do arquivo consolidado
arquivo_path = "movimentacaoportuaria2020_2023.xlsx"

# Carregar cada ano de forma separada, especificando o engine openpyxl
dados_2020 = pd.read_excel(arquivo_path, sheet_name='2020', engine='openpyxl')
dados_2021 = pd.read_excel(arquivo_path, sheet_name='2021', engine='openpyxl')
dados_2022 = pd.read_excel(arquivo_path, sheet_name='2022', engine='openpyxl')
dados_2023 = pd.read_excel(arquivo_path, sheet_name='2023', engine='openpyxl')

# Adicionar uma coluna 'Ano' em cada conjunto de dados
dados_2020['Ano'] = 2020
dados_2021['Ano'] = 2021
dados_2022['Ano'] = 2022
dados_2023['Ano'] = 2023

# Combinar os dados em um único DataFrame
dados = pd.concat([dados_2020, dados_2021, dados_2022, dados_2023])

# Função para calcular o percentual de aumento ou diminuição
def calcular_percentual(ano_anterior, ano_atual):
    return ((ano_atual - ano_anterior) / ano_anterior) * 100 if ano_anterior != 0 else None

# Interface do usuário
st.title("Movimentação Portuária dos Portos Brasileiros (2020-2023)")
porto_escolhido = st.selectbox("Selecione o Porto ou Terminal", sorted(dados['Porto'].unique()))

# Filtrar dados pelo porto selecionado
dados_porto = dados[dados['Porto'] == porto_escolhido]

# Exibir movimentação e cálculos de variação percentual
if not dados_porto.empty:
    st.subheader(f"Movimentação para o Porto: {porto_escolhido}")

    # Exibir a movimentação de cada ano e calcular variação
    dados_anos = dados_porto.groupby('Ano')['Movimentação'].sum().reset_index()
    st.write(dados_anos)

    # Calcular e exibir o percentual de aumento/diminuição
    for i in range(1, len(dados_anos)):
        ano_anterior = dados_anos.loc[i - 1, 'Movimentação']
        ano_atual = dados_anos.loc[i, 'Movimentação']
        percentual = calcular_percentual(ano_anterior, ano_atual)
        st.write(f"Variação de {dados_anos.loc[i-1, 'Ano']} para {dados_anos.loc[i, 'Ano']}: {percentual:.2f}%")

else:
    st.write("Dados não disponíveis para o porto selecionado.")
