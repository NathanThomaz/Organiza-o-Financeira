import gspread
import streamlit as st
from datetime import datetime
import pandas as pd

# Listas de categorias padronizadas
CATEGORIAS_RECEITAS = ["Salário", "Freelance", "Aluguel", "Investimentos", "Reembolso", "Outros"]
CATEGORIAS_DESPESAS = ["Alimentação", "Transporte", "Moradia", "Saúde", "Lazer", "Educação", "Compras", "Assinaturas", "Dívidas", "Outros"]

# Formas de pagamento aceitas
FORMAS_PAGAMENTO = ["Pix", "Ted", "Boleto", "Dinheiro"]

def adicionar_transacao(client, nome_planilha):
    """
    Adiciona uma transação na aba 'Transações' e também na respectiva aba de acordo com seu tipo (Receita ou Despesa).
    """

    # Abrir a planilha
    spreadsheet = client.open(nome_planilha)

    st.subheader("📝 Adicionar Nova Transação")

    # Escolher um tipo de transação
    tipo = st.radio("Selecione o tipo de transação:", ["Receita", "Despesa"])

    # Inserir valor da transação
    valor = st.number_input("Valor (R$):", min_value=0.01, format="%.2f")

    # Inserir descrição da transação
    descricao = st.text_input("Descrição da transação:")

    # Inserir data (padrão: hoje)
    data = st.date_input("Data da transação:", value=datetime.today())

    # Inserir forma de pagamento
    forma_pgt = st.selectbox("Forma de pagamento:", FORMAS_PAGAMENTO)

    # Escolher categoria da transação
    categorias = CATEGORIAS_RECEITAS if tipo == "Receita" else CATEGORIAS_DESPESAS
    categoria = st.selectbox("Categoria da transação:", categorias)

    # Botão para adicionar transação
    if st.button("Adicionar Transação"):
        try:
            # Formatar valores corretamente
            valor_formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            data_formatada = data.strftime("%d-%m-%Y")

            # Dados formatados para inserção na aba "Transações"
            dados_transacao = [data_formatada, descricao, valor_formatado, forma_pgt, categoria, tipo]
            dados_aba_correta = [data_formatada, descricao, valor_formatado, forma_pgt, categoria]

            # Adiciona sempre na aba "Transações"
            sheet_transacoes = spreadsheet.worksheet("Transações")
            sheet_transacoes.append_row(dados_transacao)

            # Adiciona também na aba correta (Receitas ou Despesas)
            aba_destino = "Receitas" if tipo == "Receita" else "Despesas"
            sheet_destino = spreadsheet.worksheet(aba_destino)
            sheet_destino.append_row(dados_aba_correta)

            # Exibir mensagem de sucesso
            st.success(f"✅ Transação adicionada com sucesso na aba '{aba_destino}'!")

            # Exibir resumo da transação
            st.write("📌 **Resumo da Transação:**")
            st.write(f"- **Tipo:** {tipo}")
            st.write(f"- **Valor:** R$ {valor_formatado}")
            st.write(f"- **Descrição:** {descricao}")
            st.write(f"- **Data:** {data_formatada}")
            st.write(f"- **Forma de Pagamento:** {forma_pgt}")
            st.write(f"- **Categoria:** {categoria}")

        except Exception as e:
            st.error(f"❌ Erro ao adicionar transação: {e}")


def visualizar_transacoes(client, nome_planilha):
    """
    Exibe as transações da aba 'Transações' no Streamlit.
    Permite ao usuário visualizar todas as transações ou aplicar múltiplos filtros.
    """
    try:
        # Abrir a planilha e acessar a aba "Transações"
        spreadsheet = client.open(nome_planilha)
        sheet = spreadsheet.worksheet("Transações")

        # Obter os dados da planilha
        dados = sheet.get_all_values()

        # Verificar se há transações registradas
        if len(dados) <= 1:
            st.warning("📂 Nenhuma transação encontrada.")
            return

        # Criar DataFrame a partir dos dados
        cabecalho = dados[0]  # Primeira linha (nomes das colunas)
        transacoes = dados[1:]  # Dados das transações
        df = pd.DataFrame(transacoes, columns=cabecalho)

        # Converter a coluna 'Valor' corretamente
        df["Valor"] = df["Valor"].str.replace("R$ ", "").str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)

        # Criar sidebar para filtros
        st.sidebar.header("🔍 Filtros de Pesquisa")

        # Selecionar filtros
        data_filtro = st.sidebar.text_input("📅 Filtrar por Data (DD-MM-YYYY)")
        descricao_filtro = st.sidebar.text_input("📂 Filtrar por Descrição")
        valor_filtro = st.sidebar.number_input("💰 Filtrar por Valor", min_value=0.0, step=0.01, format="%.2f")
        tipo_filtro = st.sidebar.selectbox("📄 Filtrar por Tipo", ["Todos", "Receita", "Despesa"])
        forma_pgt_filtro = st.sidebar.selectbox("💳 Filtrar por Forma de Pagamento", ["Todos", "Pix", "Ted", "Boleto", "Dinheiro"])

        # Aplicar filtros ao DataFrame
        if data_filtro:
            df = df[df["Data"] == data_filtro]
        if descricao_filtro:
            df = df[df["Descrição"].str.contains(descricao_filtro, case=False, na=False)]
        if valor_filtro > 0:
            df = df[df["Valor"] == valor_filtro]
        if tipo_filtro != "Todos":
            df = df[df["Tipo"] == tipo_filtro]
        if forma_pgt_filtro != "Todos":
            df = df[df["Forma de Pagamento"] == forma_pgt_filtro]

        # Exibir resultados
        if df.empty:
            st.warning("❌ Nenhuma transação encontrada com os filtros aplicados.")
        else:
            # Formatar valores para exibição correta
            df["Valor"] = df["Valor"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

            st.subheader("📊 Transações Filtradas")
            st.dataframe(df)

            # Calcular e exibir o valor total das transações filtradas
            total_valor = df["Valor"].str.replace("R$ ", "").str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float).sum()
            total_valor_formatado = f"R$ {total_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            st.info(f"💰 **Valor Total das Transações Filtradas:** {total_valor_formatado}")

    except Exception as e:
        st.error(f"❌ Erro ao visualizar transações: {e}")


def atualizar_analise_gastos(client, nome_planilha):
    """
    Gera os cálculos de análise de gastos a partir da aba 'Transações' e grava os resultados na aba 'Análise de Gastos'.
    Permite visualizar os resultados com filtros aplicáveis no Streamlit.
    """
    try:
        # Abrir a planilha e acessar as abas necessárias
        spreadsheet = client.open(nome_planilha)
        sheet_transacoes = spreadsheet.worksheet("Transações")
        sheet_analise = spreadsheet.worksheet("Análise de Gastos")

        # Obter os dados da aba "Transações"
        dados_transacoes = sheet_transacoes.get_all_values()

        # Verificar se há transações registradas
        if len(dados_transacoes) <= 1:
            st.warning("📂 Nenhuma transação encontrada para análise.")
            return

        # Criar DataFrame com os dados das transações
        cabecalho = dados_transacoes[0]
        transacoes_df = pd.DataFrame(dados_transacoes[1:], columns=cabecalho)

        # Converter valores numéricos corretamente (tratando erros de conversão)
        transacoes_df["Valor"] = (
            transacoes_df["Valor"]
            .str.replace("R$ ", "")
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )

        # Converter para número corretamente e tratar erros
        transacoes_df["Valor"] = pd.to_numeric(transacoes_df["Valor"], errors="coerce")
        transacoes_df.loc[:, "Valor"] = transacoes_df["Valor"].fillna(0)  # ✅ Isso resolve o problema

        # Extrair "Mês/Ano" da coluna "Data"
        transacoes_df["Mês/Ano"] = pd.to_datetime(transacoes_df["Data"], format="%d-%m-%Y").dt.strftime("%m/%Y")

        # Separar apenas as despesas (excluir receitas)
        despesas_df = transacoes_df[transacoes_df["Tipo"] == "Despesa"]

        # Se não houver despesas, exibir alerta
        if despesas_df.empty:
            st.warning("💰 Nenhuma despesa registrada. Seus gastos estão zerados!")
            return

        # Agrupar por Mês/Ano e Categoria e calcular Total Gasto e Média Mensal
        analise_gastos_df = despesas_df.groupby(["Mês/Ano", "Categoria"]).agg(
            Total_Gasto=("Valor", "sum"),
            Media_Mensal=("Valor", "mean")
        ).reset_index()

        # Calcular percentual do total para cada categoria dentro de cada Mês/Ano
        total_por_mes = analise_gastos_df.groupby("Mês/Ano")["Total_Gasto"].transform("sum")
        analise_gastos_df["Percentual_do_Total"] = (analise_gastos_df["Total_Gasto"] / total_por_mes) * 100

        # Gerar recomendações baseadas no percentual gasto
        def gerar_recomendacao(percentual):
            if percentual > 50:
                return "Alto gasto! Considere cortar despesas supérfluas."
            elif percentual > 30:
                return "Gasto considerável. Analise se pode economizar."
            else:
                return "Gasto saudável. Continue monitorando."

        analise_gastos_df["Recomendação"] = analise_gastos_df["Percentual_do_Total"].apply(gerar_recomendacao)

        # Substituir valores NaN e infinitos antes da exibição
        analise_gastos_df.replace([float("inf"), float("-inf")], 0, inplace=True)
        analise_gastos_df.fillna(0, inplace=True)

        # Converter valores numéricos para string antes da exibição (evita erro de JSON)
        analise_gastos_df["Total_Gasto"] = analise_gastos_df["Total_Gasto"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        analise_gastos_df["Media_Mensal"] = analise_gastos_df["Media_Mensal"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        analise_gastos_df["Percentual_do_Total"] = analise_gastos_df["Percentual_do_Total"].apply(lambda x: f"{x:.2f}%")

        # Atualizar os dados na aba "Análise de Gastos"
        sheet_analise.clear()
        sheet_analise.append_row(["Mês/Ano", "Categoria", "Total Gasto", "Média Mensal", "Percentual do Total", "Recomendação"])
        sheet_analise.append_rows(analise_gastos_df.values.tolist())

        st.success("✅ Análise de Gastos atualizada com sucesso!")

        # Filtros para visualização
        st.subheader("🔍 Filtros para Análise")
        mes_filtro = st.selectbox("📅 Selecione um mês/ano:", ["Todos"] + analise_gastos_df["Mês/Ano"].unique().tolist())
        categoria_filtro = st.selectbox("📂 Selecione uma categoria:", ["Todas"] + analise_gastos_df["Categoria"].unique().tolist())

        df_filtrado = analise_gastos_df.copy()

        if mes_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Mês/Ano"] == mes_filtro]
        if categoria_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria_filtro]

        # Exibir os resultados
        if df_filtrado.empty:
            st.warning("❌ Nenhum dado encontrado para os filtros aplicados.")
        else:
            st.subheader("📊 Análise de Gastos")
            st.dataframe(df_filtrado)

    except Exception as e:
        st.error(f"❌ Erro ao analisar os gastos: {e}")


def importar_transacoes_csv():
    """
    Permite ao usuário carregar um arquivo CSV com transações e processa os dados antes de adicioná-los à planilha.
    """
    st.subheader("📥 Importar Transações do CSV")
    uploaded_file = st.file_uploader("Selecione um arquivo CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
    # Definir categorias conhecidas com base em palavras-chave
    categorias_map = {
        "Alimentação": ["restaurant", "food", "bar", "cafe", "lanches", "tortas", "pizzaria", "padaria", "burguer", "mcdonalds"],
        "Saúde": ["farmacia", "droga", "pacheco", "saude", "clinic"],
        "Transporte": ["uber", "99pop", "gasolina", "posto", "combustivel"],
        "Lazer": ["netflix", "spotify", "cinema", "teatro", "viagem"],
        "Educação": ["curso", "escola", "faculdade", "canva"],
        "Compras": ["shopping", "loja", "mercado", "amazon", "magalu", "casas bahia"],
        "Assinaturas": ["prime video", "disney", "globo play", "hbo", "quinto andar"],
        "Moradia": ["aluguel", "condominio", "energia", "internet", "claro", "vivo", "tim", "oi"],
        "Outros": []
    }

    # Função para mapear a categoria com base no título
    def definir_categoria(title):
        title_lower = title.lower()
        for categoria, palavras in categorias_map.items():
            if any(palavra in title_lower for palavra in palavras):
                return categoria
        return "Outros"

    # Ajustar DataFrame conforme necessário
    df["Categoria"] = df["title"].apply(definir_categoria)
    df["Data"] = pd.to_datetime(df["date"]).dt.strftime("%d-%m-%Y")
    df["Descrição"] = df["title"]
    df["Valor"] = df["amount"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    df["Forma de Pagamento"] = "Cartão de Crédito"
    df["Tipo"] = "Despesa"

    # Selecionar apenas as colunas no formato correto para a planilha
    df_final = df[["Data", "Descrição", "Valor", "Forma de Pagamento", "Categoria", "Tipo"]]

    # Exibir o DataFrame processado
    st.dataframe(df_final)
    st.success("✅ Transações processadas com sucesso!")