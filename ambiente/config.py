import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

# Caminho para acessar a chave JSON (deve estar na mesma pasta do app.py ou definir caminho correto)
DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script
path_chave_json = os.path.join(DIR_ATUAL, "chave.json")  # Caminho correto do JSON


def config_ambiente():
    """
    Configura a conexão com o Google Sheets e verifica a necessidade de configuração inicial.
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    if not os.path.exists(path_chave_json):
        st.error("❌ Chave JSON não encontrada! Certifique-se de que 'chave.json' está no diretório correto.")
        return None

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(path_chave_json, scope)
        client = gspread.authorize(creds)
        st.success("✅ Conexão bem-sucedida com Google Sheets!")

        # ✅ Se ainda não configurou a planilha nesta sessão, configura agora
        if not st.session_state.get("planilha_configurada", False):
            criar_abas_e_cabecalhos(client, "Controle Financeiro")
            st.session_state["planilha_configurada"] = True  # Marca como configurada

        config_print()
        return client

    except Exception as e:
        st.error(f"❌ Erro ao conectar com Google Sheets: {e}")
        return None


def criar_abas_e_cabecalhos(client, nome_planilha):
    """
    Configura as abas e cabeçalhos na planilha do Google Sheets (somente na primeira execução).
    """
    try:
        spreadsheet = client.open(nome_planilha)

        abas_e_cabecalhos = {
            "Receitas": ["Data", "Descrição", "Valor", "Meio de Pagamento", "Categoria"],
            "Despesas": ["Data", "Descrição", "Valor", "Meio de Pagamento", "Categoria"],
            "Transações": ["Data", "Descrição", "Valor", "Forma de Pagamento", "Categoria", "Tipo"],
            "Investimentos": ["Ativo", "Valor Investido", "Rentabilidade", "Valor Atual", "Data de Compra", "Data de Venda"],
            "Análise de Gastos": ["Mês/Ano", "Categoria", "Total Gasto", "Média Mensal", "Percentual do Total", "Recomendação"]
        }

        abas_existentes = {sheet.title for sheet in spreadsheet.worksheets()}

        # Criar abas que não existem
        for aba, cabecalho in abas_e_cabecalhos.items():
            if aba not in abas_existentes:
                spreadsheet.add_worksheet(title=aba, rows="100", cols="10")
                sheet = spreadsheet.worksheet(aba)
                sheet.append_row(cabecalho)
                st.success(f"📂 Aba '{aba}' criada e cabeçalho adicionado!")

        # Corrigir cabeçalhos das abas existentes (somente se houver erro)
        for aba, cabecalho in abas_e_cabecalhos.items():
            sheet = spreadsheet.worksheet(aba)
            dados = sheet.get_all_values()

            if not dados or dados[0] != cabecalho:
                sheet.update(range_name='A1', values=[cabecalho])
                st.warning(f"⚠️ Cabeçalho da aba '{aba}' atualizado.")

        st.success("✅ Planilha configurada corretamente!")

    except Exception as e:
        st.error(f"❌ Erro ao configurar a planilha: {e}")


def config_print():
    """
    Configurações para exibição de DataFrames no Streamlit.
    """
    pd.set_option("display.colheader_justify", "left")  # Alinha cabeçalhos à esquerda
    pd.set_option("display.width", 200)  # Ajusta a largura máxima da tela
    pd.set_option("display.max_columns", None)  # Mostra todas as colunas sem quebrar
