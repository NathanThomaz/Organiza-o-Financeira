import streamlit as st
from ambiente.config import config_ambiente
from funcoes.google_sheets import (
    adicionar_transacao,
    visualizar_transacoes,
    atualizar_analise_gastos,
    importar_transacoes_csv
)

# 🔹 Ajusta o layout da página para expandir um pouco a largura
st.set_page_config(layout="centered", page_title="Controle Financeiro")

# 🔹 CSS Customizado para aumentar levemente a largura do conteúdo
st.markdown(
    """
    <style>
        .main-container {
            max-width: 85%;  /* Aumenta um pouco a largura sem ocupar toda a tela */
            margin-left: auto;
            margin-right: auto;
        }
        .block-container {
            max-width: 85% !important;  /* Ajusta a área do conteúdo */
        }
        .stDataFrame {
            width: 100% !important;
        }
        .stSelectbox, .stTextInput, .stNumberInput {
            width: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Conectar ao Google Sheets
st.sidebar.title("📌 Configuração do Sistema")
client = config_ambiente()
NOME_PLANILHA = "Controle Financeiro"

# 🔹 Criar Menu no Sidebar
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio("Escolha uma opção:", ["Visão Geral", "Adicionar Transação", "Visualizar Transações", "Análise de Gastos", "Importar Transações (CSV)"])

# 🔹 Opções do Menu
if client:
    if menu == "Visão Geral":
        st.subheader("📊 Bem-vindo a parte de Controle Financeiro!")
        st.write("Use as opções do menu lateral para gerenciar suas transações.")

    elif menu == "Adicionar Transação":
        adicionar_transacao(client, NOME_PLANILHA)

    elif menu == "Visualizar Transações":
        visualizar_transacoes(client, NOME_PLANILHA)

    elif menu == "Análise de Gastos":
        atualizar_analise_gastos(client, NOME_PLANILHA)

    elif menu == "Importar Transações (CSV)":
        importar_transacoes_csv()