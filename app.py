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
dados_2020['Ano'] = "2020"
dados_2021['Ano'] = "2021"
dados_2022['Ano'] = "2022"
dados_2023['Ano'] = "2023"

# Combine os dados em um único DataFrame
dados = pd.concat([dados_2020, dados_2021, dados_2022, dados_2023])

# Interface do usuário
st.title("Movimentação Portuária dos Portos Brasileiros (2020-2023)")
porto_escolhido = st.selectbox("Selecione o Porto ou Terminal", sorted(dados['porto'].unique()))

# Filtrar dados pelo porto selecionado
dados_porto = dados[dados['porto'] == porto_escolhido]

# Exibir movimentação e cálculos de variação percentual
if not dados_porto.empty:
    st.subheader(f"Movimentação para o Porto: {porto_escolhido}")

    # Agrupar por 'Ano' e somar a coluna 'carga'
    dados_anos = dados_porto.groupby('Ano')['carga'].sum().reset_index()
    
    # Formatar valores de carga e ano para o padrão brasileiro, sem casas decimais
    dados_anos['carga'] = dados_anos['carga'].map("{:,.0f}".format).str.replace(",", "X").str.replace(".", ",").str.replace("X", ".")

    # Aplicar estilização ao DataFrame
    styled_dados_anos = dados_anos.style.set_properties(**{
        'background-color': '#add8e6',  # Azul claro
        'color': 'black',               # Texto preto
        'width': '200px'                # Largura das colunas
    })

    # Exibir DataFrame estilizado
    st.dataframe(styled_dados_anos)

    # Calcular e exibir o percentual de aumento/diminuição
    for i in range(1, len(dados_anos)):
        ano_anterior = float(dados_anos.loc[i - 1, 'carga'].replace(".", "").replace(",", "."))
        ano_atual = float(dados_anos.loc[i, 'carga'].replace(".", "").replace(",", "."))
        percentual = ((ano_atual - ano_anterior) / ano_anterior) * 100 if ano_anterior != 0 else None
        st.write(f"Variação de {dados_anos.loc[i-1, 'Ano']} para {dados_anos.loc[i, 'Ano']}: {percentual:.2f}%")

else:
    st.write("Dados não disponíveis para o porto selecionado.")

# Adicionar a fonte no final da aplicação
st.write("Fonte: Estatístico Aquaviário ANTAQ. Dados obtidos em nov/24.")

