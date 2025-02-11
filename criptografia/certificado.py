import requests

url = "https://prod-s0-webapp-proxy.nubank.com.br/api/discovery"

response = requests.get(url)

if response.status_code == 200:
    print("✅ Conexão bem-sucedida com a API do Nubank!")
else:
    print(f"❌ Erro {response.status_code}: A API do Nubank pode estar bloqueando seu IP.")
