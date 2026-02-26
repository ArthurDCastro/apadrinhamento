import pandas as pd
import random
import re

# 📥 Carregar os dados dos CSVs, removendo espaços nos nomes das colunas
calouros_df = pd.read_csv("data/calouros.csv")
veteranos_df = pd.read_csv("data/veteranos.csv")

# 🔍 Depuração: Mostrar nomes reais das colunas
print("Colunas em calouros.csv:", calouros_df.columns.tolist())
print("Colunas em veteranos.csv:", veteranos_df.columns.tolist())

# 🔹 Remover espaços extras dos nomes das colunas
calouros_df.columns = calouros_df.columns.str.strip()
veteranos_df.columns = veteranos_df.columns.str.strip()

# 🔹 Normalizar os valores de gênero (M → Masculino, F → Feminino)
genero_map = {"M": "Masculino", "F": "Feminino"}
if "Genero" in calouros_df.columns:
    calouros_df["Genero"] = calouros_df["Genero"].map(genero_map)
else:
    raise KeyError("A coluna 'Genero' não foi encontrada no arquivo calouros.csv.")

# 📌 Função para limpar e ajustar os números de telefone
def formatar_telefone(numero, nome_veterano):
    numero = re.sub(r"\D", "", str(numero))  # Remove tudo que não for número

    if len(numero) == 11:
        return f"55{numero}"  # Adiciona código do Brasil (55)
    elif len(numero) == 9:
        return f"5541{numero}"  # Adiciona código do Brasil (55) + DDD 41
    else:
        print(f"⚠️ Telefone inválido para {nome_veterano}: {numero}")
        return None  # Retorna None se o número não for corrigível

# Aplicar a formatação no DataFrame de veteranos
veteranos_df["Telefone"] = veteranos_df.apply(lambda row: formatar_telefone(row["Telefone"], row["Nome"]), axis=1)

# 📌 Criar listas separadas por gênero
calouros_masc = calouros_df[calouros_df["Genero"] == "Masculino"].to_dict(orient="records")
calouros_fem = calouros_df[calouros_df["Genero"] == "Feminino"].to_dict(orient="records")

veteranos_masc = veteranos_df[veteranos_df["Genero"] == "Masculino"].to_dict(orient="records")
veteranos_fem = veteranos_df[veteranos_df["Genero"] == "Feminino"].to_dict(orient="records")

# 📌 Função para realizar o sorteio
def sortear_padrinhos(calouros, veteranos):
    resultado = []
    random.shuffle(veteranos)  # Misturar a lista de veteranos

    # 🔹 PRIMEIRA RODADA: Cada calouro recebe um padrinho/madrinha do mesmo gênero
    padrinhos_usados = set()
    for calouro in calouros:
        padrinho = next((v for v in veteranos if v["Nome"] not in padrinhos_usados), None)
        if padrinho:
            padrinhos_usados.add(padrinho["Nome"])
            resultado.append({
                "GRR": calouro["GRR"],
                "Calouro": calouro["Nome"],
                "GeneroC": calouro["Genero"],
                "Veterano": padrinho["Nome"],
                "TelefoneV": padrinho["Telefone"],
                "GeneroV": padrinho["Genero"]
            })
        else:
            break  # Quando acabar os veteranos, sai do loop

    # 🔹 SEGUNDA RODADA: Redistribuir os veteranos seguindo prioridades
    if len(resultado) < len(calouros):  # Se ainda tem calouros sem padrinho/madrinha
        calouros_sem_padrinho = calouros[len(resultado):]
        
        # Ordenar veteranos por prioridade (CAAD > PET > Ano mais recente)
        veteranos.sort(key=lambda v: (v["Grupo"] != "CAAD", v["Grupo"] != "PET", -int(v["Ano"])))

        for calouro in calouros_sem_padrinho:
            padrinho = veteranos.pop(0)  # Pega o primeiro da fila priorizada
            veteranos.append(padrinho)  # Coloca ele no final da fila para balancear
            resultado.append({
                "GRR": calouro["GRR"],
                "Calouro": calouro["Nome"],
                "GeneroC": calouro["Genero"],
                "Veterano": padrinho["Nome"],
                "TelefoneV": padrinho["Telefone"],
                "GeneroV": padrinho["Genero"]
            })

    return resultado

# 🎲 Realizar os sorteios
sorteados_masc = sortear_padrinhos(calouros_masc, veteranos_masc)
sorteados_fem = sortear_padrinhos(calouros_fem, veteranos_fem)

# 📊 Gerar DataFrame final e salvar CSV
sorteio_final = pd.DataFrame(sorteados_masc + sorteados_fem)
sorteio_final.to_csv("data/sorteio_apadrinhamento.csv", index=False)

print("✅ Sorteio concluído! Arquivo salvo como 'sorteio_apadrinhamento.csv'")
