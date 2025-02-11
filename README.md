# Controle Financeiro - Google Sheets & Python

## 📌 Descrição
Este projeto é um **sistema de controle financeiro** desenvolvido em **Python**, integrado ao **Google Sheets** para armazenar e gerenciar transações financeiras, receitas, investimentos e análise de gastos.

## 🔹 Funcionalidades
✅ **Registrar transações** (Receitas e Despesas).  
✅ **Gerenciar investimentos** e acompanhar rentabilidade.  
✅ **Analisar gastos** e identificar áreas de melhoria financeira.  
✅ **Gerar relatórios automáticos no Google Sheets**.  
✅ **Possibilidade de integração com WhatsApp Bot** para registrar despesas via chat.  
✅ **Planejamento para transformar o sistema em um aplicativo mobile**.

---

## 📁 **Estrutura da Planilha**
A planilha contém as seguintes abas:

1️⃣ **Receitas** → Para registrar todas as entradas de dinheiro.  
2️⃣ **Investimentos** → Para acompanhar aplicações financeiras.  
3️⃣ **Análise de Gastos** → Para identificar onde melhorar os gastos.  
4️⃣ **Transações** → Para registrar todas as movimentações financeiras.  

Cada aba tem um **cabeçalho estruturado**, garantindo organização e cálculos automatizados.

---

## 🚀 **Instalação e Configuração**

### 🔹 1️⃣ Requisitos
- Conta no **Google Sheets**.
- Criar um **Projeto no Google Cloud** e ativar as APIs:
  - ✅ **Google Sheets API**
  - ✅ **Google Drive API**
- Criar e baixar uma **chave JSON** da conta de serviço.

### 🔹 1.1 Como Gerar a Chave JSON (Rápido)
1. Acesse [Google Cloud Console](https://console.cloud.google.com/).
2. Vá para **IAM & Admin > Contas de Serviço**.
3. Crie uma nova conta de serviço e conceda permissão **Editor**.
4. Vá até a aba **Chaves**, clique em **Adicionar chave** > **JSON**.
5. O arquivo JSON será baixado automaticamente.
6. Mova esse arquivo para o Google Drive na pasta apropriada.

### 🔹 2️⃣ Configuração do Google Colab

#### **2.1 Montar o Google Drive**
Antes de acessar os arquivos, precisamos montar o Google Drive:

```python
from google.colab import drive
drive.mount('/content/drive')
```

#### **2.2 Definir o Caminho do JSON de Autenticação**
Altere o caminho abaixo conforme a localização do seu arquivo JSON no Google Drive:

```python
path_chave_json = "/content/drive/MyDrive/APIs/sua-chave.json"
```

#### **2.3 Instalar as Bibliotecas Necessárias**
Se ainda não tiver as bibliotecas instaladas, execute o seguinte comando:

```python
!pip install gspread pandas oauth2client
```

#### **2.4 Importar e Configurar a Autenticação**

```python
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(path_chave_json, scope)
client = gspread.authorize(creds)
```

---

## 🔹 **Funcionalidades Implementadas**
### ✅ Criar e Estruturar a Planilha
- Criar abas: "Receitas", "Investimentos", "Análise de Gastos", "Transações".
- Adicionar cabeçalhos padronizados.

### ✅ Registrar e Consultar Dados
- Funções para adicionar **receitas, despesas e investimentos**.
- Cálculo automático de **saldo e análise de gastos**.

### ✅ Criar Interface Mobile
- Planejamento para transformar o sistema em um **app mobile** usando Streamlit ou Kivy.

### ✅ Testes e Otimizações
- Garantir a **conexão com Google Sheets**.
- Criar **botões e menus interativos**.

---

## 🛠 **Próximos Passos**
🚀 Criar a interface para **registrar e visualizar transações**.  
📊 Desenvolver relatórios dinâmicos para análise de gastos.  
📱 Criar um **app mobile** usando Streamlit ou Kivy.  
🤖 Integrar um **bot do WhatsApp** para adicionar despesas via chat.  

---

## 📌 **Autor**
**Desenvolvido por:** **Nathan Thomaz Quintanilha**  
🔗 **LinkedIn:** https://www.linkedin.com/in/nathan-thomaz-devs/  

📌 **Siga o projeto e contribua para melhorias!** 🚀✨

