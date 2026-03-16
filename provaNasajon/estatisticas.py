import csv # biblioteca para gerenciar arquivos .csv
import json # biblioteca para gerenciar arquivos json

RESULT_FILE = "resultado.csv"
OUTPUT_JSON_FILE = "stats.json"

# lista de regioes
REGIOES = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

# contadores
total_municipios = 0
total_ok = 0
total_nao_encontrado = 0
total_erro_api = 0
pop_total_ok = 0

# soma e contagem por regiao
regiao_pop = {reg: 0 for reg in REGIOES}
regiao_count = {reg: 0 for reg in REGIOES}

# leitura do csv gerado correto
with open(RESULT_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_municipios += 1
        status = row.get("status", "").upper()
        try:
            pop = int(row.get("populacao_input", 0))
        except:
            pop = 0

        if status == "OK":
            total_ok += 1
            pop_total_ok += pop
            regiao = row.get("regiao", "")
            if regiao in REGIOES:
                regiao_pop[regiao] += pop
                regiao_count[regiao] += 1
        elif status == "NAO_ENCONTRADO":
            total_nao_encontrado += 1
        elif status == "ERRO_API":
            total_erro_api += 1

# calcular medias por regiao
medias_por_regiao = {}
for reg in REGIOES:
    count = regiao_count[reg]
    total = regiao_pop[reg]
    medias_por_regiao[reg] = round(total / count, 2) if count > 0 else 0.0

# montagem do JSON final
stats_json = {
    "stats": {
        "total_municipios": total_municipios,
        "total_ok": total_ok,
        "total_nao_encontrado": total_nao_encontrado,
        "total_erro_api": total_erro_api,
        "pop_total_ok": pop_total_ok,
        "medias_por_regiao": medias_por_regiao
    }
}

# salvar em um arquivo json gerado a ser enviado para API
with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(stats_json, f, ensure_ascii=False, indent=4)

print(f"Arquivo JSON gerado: {OUTPUT_JSON_FILE}")
print(json.dumps(stats_json, indent=4, ensure_ascii=False))