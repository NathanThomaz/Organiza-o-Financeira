import os
import gspread
import pandas as pd
import streamlit as st
from pynubank import Nubank
from oauth2client.service_account import ServiceAccountCredentials

# 🔹 Configuração do Google Sheets
def conectar_google_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("ambiente/chave.json", scope)
    client = gspread.authorize(creds)
    return client

# 🔹 Conectar ao Nubank
def conectar_nubank():
    nu = Nubank()
    
    # Credenciais do Nubank
    CPF = "SEU_CPF"
    SENHA = "SUA_SENHA"
    CERTIFICADO = "ambiente/certificado_nubank.p12"  # Caminho do certificado
    
    if not os.path.exists(CERTIFICADO):
        st.error("❌ Certificado Nubank não encontrado. Gere o certificado no app Nubank!")
        return None
    
    nu.authenticate_with_cert(CPF, SENHA, CERTIFICADO)
    return nu

# 🔹 Buscar transações do Nubank
def obter_transacoes_nubank(nu):
    try:
        transacoes = nu.get_account_statements()  # Obtém os extratos da conta
        return transacoes
    except Exception as e:
        st.error(f"❌ Erro ao buscar transações do Nubank: {e}")
        return None

# 🔹 Evitar transações duplicadas
def remover_duplicatas(dados_novos, dados_existentes):
    """ 
    Compara as transações novas com as existentes na planilha para evitar duplicação.
    """
    df_existente = pd.DataFrame(dados_existentes[1:], columns=dados_existentes[0]) if len(dados_existentes) > 1 else pd.DataFrame()
    
    # Se a planilha estiver vazia, retorna todos os novos dados
    if df_existente.empty:
        return dados_novos
    
    transacoes_existentes = set(df_existente["Descrição"] + df_existente["Data"] + df_existente["Valor"])  # Combinação única
    
    # Filtrar apenas transações novas
    transacoes_filtradas = [t for t in dados_novos if (t[1] + t[0] + t[2]) not in transacoes_existentes]
    
    return transacoes_filtradas

# 🔹 Atualizar Planilha com as transações do Nubank
def atualizar_planilha_nubank():
    st.info("🔄 Buscando transações do Nubank...")

    client = conectar_google_sheets()
    nu = conectar_nubank()
    
    if not nu:
        return
    
    transacoes = obter_transacoes_nubank(nu)
    
    if not transacoes:
        return

    planilha = client.open("Controle Financeiro")  
    sheet = planilha.worksheet("Transações")  

    dados_existentes = sheet.get_all_values()
    
    dados_novos = []
    
    for t in transacoes:
        # Ajustar valores conforme o formato correto
        valor_formatado = f"R$ {abs(t['amount']) / 100:.2f}".replace(".", ",")  # Formato R$ 0,00
        tipo_transacao = "Receita" if t["amount"] > 0 else "Despesa"  # Define se é Receita ou Despesa
        categoria = "Outros"  # Se não houver categoria, definir como "Outros"

        dados_novos.append([
            t["time"][:10],  # 📅 Data da transação (YYYY-MM-DD)
            t["title"],  # 📝 Descrição
            valor_formatado,  # 💰 Valor formatado corretamente
            "Nubank",  # 💳 Meio de pagamento fixo como Nubank
            categoria,  # 🏷️ Categoria (se não houver, definir como "Outros")
            tipo_transacao  # 🔄 Tipo (Receita ou Despesa)
        ])

    # Remover transações duplicadas antes de adicionar na planilha
    transacoes_filtradas = remover_duplicatas(dados_novos, dados_existentes)

    if transacoes_filtradas:
        sheet.append_rows(transacoes_filtradas)
        st.success("✅ Transações do Nubank adicionadas com sucesso!")
    else:
        st.warning("⚠️ Nenhuma nova transação encontrada. Nenhuma atualização feita.")

# 🔹 Streamlit para Importação manual
if st.sidebar.button("📥 Importar Transações do Nubank"):
    atualizar_planilha_nubank()
