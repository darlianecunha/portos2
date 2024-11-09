import streamlit as st
import pandas as pd

# Caminho do arquivo consolidado
arquivo_path = "movimentacaoportuaria2020_2023.xlsx"

# Carregar cada ano e renomear as colunas para garantir consistência
dados_2020 = pd.read_excel(arquivo_path, sheet_name='2020', engine='openpyxl').rename(columns={'Carga Movimentada': 'carga', 'Porto': 'porto'})
dados_2021 = pd.read_excel(arquivo_path, sheet_name='2021', engine='openpyxl').rename(columns={'Carga Movimentada': 'carga', 'Porto': 'porto'})
dados_2022 = pd.read_excel(arquivo_path, sheet_name='2022', engine='openpyxl').rename(columns={'Carga Movimentada': 'carga', 'Porto': 'porto'})
dados_2023 = pd.read_excel(arquivo_path, sheet_name='2023', engine='openpyxl').rename(columns={'Carga Movimentada': 'carga', 'Porto': 'porto'})

# Adicionar uma coluna 'Ano' em cada conjunto de dados
dados_2020['Ano'] = 2020
dados_2021['Ano'] = 2021
dados_2022['Ano'] = 2022
dados_2023['Ano'] = 2023

# Combine os dados em um único DataFrame e exiba as colunas para diagnóstico
dados = pd.concat([dados_2020, dados_2021, dados_2022, dados_2023])
st.write("Colunas no DataFrame consolidado:", dados.columns.tolist())

# Introdução e título com azul marinho
st.markdown("<h1 style='color: #002060;'>Movimentação Portuária dos Portos Brasileiros (2020-2023)</h1>", unsafe_allow_html=True)
st.markdown("<p><strong>Ferramenta desenvolvida por Darliane Cunha.</strong> Facilite suas buscas e visualize dados de movimentação portuária dos principais portos e terminais brasileiros!</p>", unsafe_allow_html=True)

# Interface de seleção de porto
porto_escolhido = st.selectbox("Selecione o Porto ou Terminal", sorted(dados['porto'].unique()))

# Filtrar dados pelo porto selecionado
dados_porto = dados[dados['porto'] == porto_escolhido]

# Exibir movimentação e cálculos de variação percentual
if not dados_porto.empty:
    st.markdown(f"<h2 style='color: #002060;'>Movimentação para o Porto: {porto_escolhido}</h2>", unsafe_allow_html=True)

    # Agrupar por 'Ano' e somar a coluna 'carga'
    dados_anos = dados_porto.groupby('Ano')['carga'].sum().reset_index()
    st.write(dados_anos)

    # Calcular e exibir o percentual de aumento/diminuição
    for i in range(1, len(dados_anos)):
        ano_anterior = dados_anos.loc[i - 1, 'carga']
        ano_atual = dados_anos.loc[i, 'carga']
        percentual = ((ano_atual - ano_anterior) / ano_anterior) * 100 if ano_anterior != 0 else None
        st.write(f"Variação de {dados_anos.loc[i-1, 'Ano']} para {dados_anos.loc[i, 'Ano']}: {percentual:.2f}%")

else:
    st.write("Dados não disponíveis para o porto selecionado.")


