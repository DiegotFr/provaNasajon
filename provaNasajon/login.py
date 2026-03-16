import requests # biblioteca para requisicoes de API

# URL fornecida para o projeto
SUPABASE_URL = "https://mynxlubykylncinttggu.supabase.co"

# chave publica da API da base fornecida para o projeto
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im15bnhsdWJ5a3lsbmNpbnR0Z2d1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUxODg2NzAsImV4cCI6MjA4MDc2NDY3MH0.Z-zqiD6_tjnF2WLU167z7jT5NzZaG72dWH0dpQW1N-Y"

# URL completa para o login com senha
url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"

# header/cabecalho HTTP da requisicao
# indicando que a aplicacao esta em Json e depois autentica a aplicacao junto a base
headers = {
    "Content-Type": "application/json",
    "apikey": SUPABASE_ANON_KEY
}

# dados do usuario
payload = {
    "email": "diego.floriach@yahoo.com",
    "password": "SUPABASE@1991@999!fjassupa"
}

# envio da requisicao e depois converter em Json
response = requests.post(url, json=payload, headers=headers)

# printa o codigo retornado pelo servidor, podendo ser de sucesso ou de algum erro
print("Status:", response.status_code)

# converte em json de novo
data = response.json()

# printa a resposta da API completa
print("Resposta completa:", data)

# extrai somente o access_token da resposta gerada pela API, que ira ser usado futuramente
access_token = data.get("access_token")

# verifica se foi retornado corretamente o access_token
# exibe o token e o salva em um arquivo .txt local para uso futuro, depois confirma que foi salvo no arquivo
if access_token:

    print("\nAccess Token obtido com sucesso:")
    print(access_token)

    with open("access_token.txt", "w") as f:
        f.write(access_token)

    print("\nToken salvo no arquivo access_token.txt")

else:

    # caso o login falhe ou o token não exista na resposta
    print("\nErro ao obter access_token")