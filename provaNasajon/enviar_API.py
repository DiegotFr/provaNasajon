import requests # biblioteca para requisicoes de API
import json # biblioteca para gerenciar arquivos json

# configuracoes
STATS_JSON_FILE = "stats.json"
ACCESS_TOKEN_FILE = "access_token.txt"
PROJECT_FUNCTION_URL = "https://mynxlubykylncinttggu.functions.supabase.co/ibge-submit"

# le o token access gerado la no comeco
with open(ACCESS_TOKEN_FILE, "r", encoding="utf-8") as f:
    ACCESS_TOKEN = f.read().strip()

# le o json de estatisticas corretas geradas
with open(STATS_JSON_FILE, "r", encoding="utf-8") as f:
    stats_payload = json.load(f)

# headers/cabecalhos para a API
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# envio para a API de correcao
try:
    response = requests.post(PROJECT_FUNCTION_URL, headers=headers, json=stats_payload, timeout=15)
    response.raise_for_status()  # Levanta exceção se status != 2xx

    # le a resposta JSON
    result = response.json()
    print("Resposta da API de correção:")
    print(f"User ID: {result.get('user_id')}")
    print(f"Email: {result.get('email')}")
    print(f"Score: {result.get('score')}")
    print(f"Feedback: {result.get('feedback')}")

except requests.exceptions.RequestException as e:
    print("Erro ao enviar para API de correção:", e)
except json.JSONDecodeError:
    print("Erro: resposta da API não está no formato JSON esperado.")