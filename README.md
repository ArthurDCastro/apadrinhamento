# Sistema de Apadrinhamento

Este projeto contém dois scripts principais:

- `sorteio.py` → Realiza o sorteio de apadrinhamento.
- `bot.py` → Dispara as mensagens para os veteranos com o resultado do sorteio.

---

## 📦 Requisitos

- Python 3.10 ou superior
- Bibliotecas:
  - pandas

Instalação recomendada:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas
```

---

## 📁 Estrutura esperada

```
apadrinhamento/
├── sorteio.py
├── bot.py
├── data/
│   ├── calouros.csv
│   ├── veteranos.csv
│   └── sorteio_apadrinhamento.csv
```

---

## 📥 Arquivos de entrada

### `data/calouros.csv`

Colunas obrigatórias:

- `GRR`
- `Nome`
- `Genero` (M ou F)

---

### `data/veteranos.csv`

Colunas obrigatórias:

- `Nome`
- `Telefone`
- `Genero`
- `Grupo`
- `Ano`

---

## 🎲 Executando o sorteio

1. Coloque os arquivos `calouros.csv` e `veteranos.csv` dentro da pasta `data/`.
2. Execute:

```bash
python sorteio.py
```

3. O arquivo gerado será:

```
data/sorteio_apadrinhamento.csv
```

---

## 🤖 Executando o envio das mensagens

Após validar o arquivo gerado:

```bash
python bot.py
```

(O funcionamento detalhado do bot está descrito no MANUAL.md)

---

## ⚠️ Observações

- O sorteio prioriza padrinhos/madrinhas do mesmo gênero.
- Caso faltem veteranos, o sistema redistribui com prioridade:
  1. CAAD
  2. PET
  3. Ano mais recente

- Telefones inválidos são sinalizados no terminal.
