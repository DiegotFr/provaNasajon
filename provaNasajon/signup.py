import requests # biblioteca para requisicoes de API

# URL fornecida para o projeto
SUPABASE_URL = "https://mynxlubykylncinttggu.supabase.co"

# chave publica da API da base fornecida para o projeto
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im15bnhsdWJ5a3lsbmNpbnR0Z2d1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUxODg2NzAsImV4cCI6MjA4MDc2NDY3MH0.Z-zqiD6_tjnF2WLU167z7jT5NzZaG72dWH0dpQW1N-Y"

# URL completa
url = f"{SUPABASE_URL}/auth/v1/signup"

# headers/cabecalho para a requisicao HTTP, apikey ira autenticar a requisicao na base
headers = {
    "Content-Type": "application/json",
    "apikey": SUPABASE_ANON_KEY
}

# contem os dados de envio da requisicao
payload = {
    "email": "diego.floriach@yahoo.com",
    "password": "SUPABASE@1991@999!fjassupa",
    "data": {
        "nome": "Diego Floriach"
    }
}

# envia a requisicao ja convertida em json
response = requests.post(url, json=payload, headers=headers)

print("Status:", response.status_code) # printa o codigo que foi retornado pelo servidor, podendo ser codigo de erro ou de sucesso
print("Resposta:", response.json()) # printa a resposta da API, com as informacoes do usuario criado