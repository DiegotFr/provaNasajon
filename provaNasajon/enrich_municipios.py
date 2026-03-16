import requests # biblioteca para requisicoes de API
import csv # biblioteca para gerenciar arquivos .csv
import unicodedata # biblioteca para gerenciar caracteres e fazer normalizacao dos dados

# URL da API de municípios do IBGE
IBGE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

# arquivo de entrada a ser lido
INPUT_FILE = "input.csv"

# arquivo a ser gerado
OUTPUT_FILE = "enriched_municipios.csv"

# funcao para normalizar nomes de municipios
def normalize(text):
    if not text:
        return ""
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))  # remove acentos
    # remove caracteres que nao sao letras, numeros ou espacos
    text = "".join(c for c in text if c.isalnum() or c.isspace())
    return text.strip()

# funcao para buscar municipios do IBGE e organizar em dicionario
def fetch_ibge():
    try:
        response = requests.get(IBGE_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        municipios = {}

        for m in data:
            try:
                nome = m.get("nome", "")
                microrregiao = m.get("microrregiao")
                if not microrregiao:
                    continue
                mesorregiao = microrregiao.get("mesorregiao")
                if not mesorregiao:
                    continue
                uf_info = mesorregiao.get("UF")
                if not uf_info:
                    continue
                regiao_info = uf_info.get("regiao")
                if not regiao_info:
                    continue

                uf = uf_info.get("sigla", "")
                regiao = regiao_info.get("nome", "")
                id_ibge = m.get("id", "")

                key = normalize(nome)
                if key not in municipios:
                    municipios[key] = []

                municipios[key].append({
                    "municipio_ibge": nome,
                    "uf": uf,
                    "regiao": regiao,
                    "id_ibge": id_ibge
                })

            except Exception as e:
                # para algum registro incompleto a ser ignorado
                print(f"Registro incompleto ignorado: {m.get('nome', 'SEM NOME')} - {e}")
                continue

        return municipios

    except Exception as e:
        print("Erro ao acessar API do IBGE:", e)
        return None

# funcao principal que enriquece os municipios
def enrich_data(input_file, output_file):
    municipios_ibge = fetch_ibge()
    if municipios_ibge is None:
        print("Não foi possível obter dados do IBGE. Abortando.")
        return

    resultados = []

    with open(input_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            municipio_input = row["municipio"]
            populacao_input = row["populacao"]

            municipio_ibge = uf = regiao = id_ibge = ""
            status = ""

            key = normalize(municipio_input)

            try:
                matches = municipios_ibge.get(key, [])
                if len(matches) == 0:
                    status = "NAO_ENCONTRADO"
                elif len(matches) > 1:
                    status = "AMBIGUO"
                else:
                    info = matches[0]
                    municipio_ibge = info["municipio_ibge"]
                    uf = info["uf"]
                    regiao = info["regiao"]
                    id_ibge = info["id_ibge"]
                    status = "OK"
            except Exception as e:
                # qualquer problema aqui marca NAO_ENCONTRADO
                print(f"Erro ao processar {municipio_input}: {e}")
                status = "NAO_ENCONTRADO"

            resultados.append({
                "municipio_input": municipio_input,
                "populacao_input": populacao_input,
                "municipio_ibge": municipio_ibge,
                "uf": uf,
                "regiao": regiao,
                "id_ibge": id_ibge,
                "status": status
            })

    # grava resultados em CSV
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["municipio_input", "populacao_input", "municipio_ibge", "uf", "regiao", "id_ibge", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in resultados:
            writer.writerow(r)

    print(f"Arquivo enriquecido gerado: {output_file}")

    # estatisticas basicas do arquivo gerado
    total = len(resultados)
    total_ok = sum(1 for r in resultados if r["status"] == "OK")
    total_nao_encontrado = sum(1 for r in resultados if r["status"] == "NAO_ENCONTRADO")
    total_erro_api = sum(1 for r in resultados if r["status"] == "ERRO_API")
    total_ambiguo = sum(1 for r in resultados if r["status"] == "AMBIGUO")

    print(f"Total de registros processados: {total}")
    print(f"Status OK: {total_ok}")
    print(f"Status NAO_ENCONTRADO: {total_nao_encontrado}")
    print(f"Status ERRO_API: {total_erro_api}")
    print(f"Status AMBIGUO: {total_ambiguo}")

if __name__ == "__main__":
    enrich_data(INPUT_FILE, OUTPUT_FILE)

"""
O arquivo aqui gerado ainda nao e o resultado.csv propriamente dito, por enquanto, ele somente faz a requisicao com a API do IBGE, e mostra o que encontrou com base na tabela atual,
sem modificar nada ainda, somente para verificar se esta funcionando tudo corretamente, ou seja, a API, os status tratados, se a normalizacao esta sendo feita corretamente, etc
O arquivo gerado somente retrata a logica do codigo e ainda nao e o resultado.csv final corrigido
"""