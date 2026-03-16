import requests # biblioteca para requisicoes de API
import csv # biblioteca para gerenciar arquivos .csv
import difflib # biblitoeca padrao para comparacoes

# arquivos
ENRICHED_FILE = "enriched_municipios.csv"
RESULT_FILE = "resultado.csv"

# URL da API do IBGE a ser utilizada
IBGE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

# leitura dos municipios enriquecidos
municipios_ibge = {}

with open(ENRICHED_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # dados corrigidos
        nome_input = row.get("municipio_input", "").strip()
        pop_input = int(row.get("populacao_input", 0))
        nome_ibge = row.get("municipio_ibge", "").strip()
        uf = row.get("uf", "").strip()
        regiao = row.get("regiao", "").strip()
        id_ibge = row.get("id_ibge", "").strip()
        status = row.get("status", "").strip()
        motivo = row.get("motivo", "").strip()

        # se nome_ibge vazio, tentar correcao simples com difflib para comparacao com semelhantes
        if not nome_ibge or status != "OK":
            # busca match proximo
            # removendo acentos e coisas simples
            try:
                resp = requests.get(IBGE_URL, timeout=10)
                resp.raise_for_status()
                lista_municipios = resp.json()
            except:
                lista_municipios = []

            nomes_oficiais = [m["nome"].lower() for m in lista_municipios]
            match = difflib.get_close_matches(nome_input.lower(), nomes_oficiais, n=1, cutoff=0.8)
            if match:
                # Encontrou match
                mun = next((m for m in lista_municipios if m["nome"].lower() == match[0]), None)
                if mun:
                    nome_ibge = mun["nome"]
                    uf = mun["microrregiao"]["mesorregiao"]["UF"]["sigla"]
                    regiao = mun["microrregiao"]["mesorregiao"]["UF"]["regiao"]["nome"]
                    id_ibge = str(mun["id"])
                    status = "OK"
                    motivo = "corrigido"
            else:
                if status != "OK":
                    status = status or "NAO_ENCONTRADO"
                    motivo = motivo or "nao encontrado no IBGE"

        # --- Consolidar duplicados usando municipio_ibge como chave ---
        if nome_ibge in municipios_ibge:
            # Soma populações, mantém status OK
            prev = municipios_ibge[nome_ibge]
            municipios_ibge[nome_ibge]["populacao_input"] += pop_input
            municipios_ibge[nome_ibge]["status"] = "OK"  # consolidado
            # UF, regiao, id_ibge mantidos do primeiro registro
        else:
            municipios_ibge[nome_ibge] = {
                "municipio_input": nome_input,
                "populacao_input": pop_input,
                "municipio_ibge": nome_ibge,
                "uf": uf,
                "regiao": regiao,
                "id_ibge": id_ibge,
                "status": status,
                "motivo": motivo
            }

# --- Escreve resultado consolidado ---
with open(RESULT_FILE, "w", encoding="utf-8", newline="") as f:
    fieldnames = ["municipio_input", "populacao_input", "municipio_ibge", "uf", "regiao", "id_ibge", "status", "motivo"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for mun in municipios_ibge.values():
        writer.writerow(mun)

print(f"Arquivo resultado consolidado gerado: {RESULT_FILE}")