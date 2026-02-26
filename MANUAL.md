# Manual de Execução — Apadrinhamento

Este manual é para rodar o processo completo: **sorteio** + **envio das mensagens** no WhatsApp Web.

---

## 0) Estrutura e arquivos necessários

Na raiz do projeto, você deve ter:

- `sorteio.py`
- `bot.py`
- `masc.txt` (template da mensagem para veteranos do gênero Masculino)
- `fem.txt` (template da mensagem para veteranos do gênero Feminino)
- pasta `data/` com:
  - `calouros.csv`
  - `veteranos.csv`
  - (será gerado) `sorteio_apadrinhamento.csv`

Estrutura recomendada:

```

apadrinhamento/
├── sorteio.py
├── bot.py
├── masc.txt
├── fem.txt
├── whatsapp_profile/        (vai ser criado automaticamente)
└── data/
├── calouros.csv
├── veteranos.csv
└── sorteio_apadrinhamento.csv

```

---

## 1) Preparar o ambiente (uma vez)

### 1.1 Criar e ativar venv

```bash
python -m venv .venv
source .venv/bin/activate
```

### 1.2 Instalar dependências

```bash
pip install pandas selenium
```

### 1.3 Ter o Chrome/Chromium instalado

O `bot.py` usa o Selenium com **Chrome**. Garanta que o navegador está instalado.

> Observação: dependendo do teu setup, pode ser necessário ter o **ChromeDriver** compatível. Se rodar e der erro de driver, o caminho é ajustar isso (a gente documenta conforme o erro que aparecer na sua máquina).

---

## 2) Rodar o sorteio

1. Coloque os CSVs em `data/`:
   - `data/calouros.csv`
   - `data/veteranos.csv`

2. Rode:

```bash
python sorteio.py
```

3. Confirme que foi gerado:

- `data/sorteio_apadrinhamento.csv`

---

## 3) Validar o resultado antes do envio (recomendado)

Abra `data/sorteio_apadrinhamento.csv` e confira rapidamente:

- Todos os calouros aparecem
- A coluna `TelefoneV` está preenchida
- Nomes e GRR estão corretos

Se houver telefone inválido, corrija no `data/veteranos.csv` e rode o `sorteio.py` de novo.

---

## 4) Preparar os templates de mensagem

O `bot.py` lê:

- `masc.txt`
- `fem.txt`

Esses arquivos devem conter placeholders (chaves) no formato do Python `.format()`:

- `{nome_veterano}`
- `{nome_calouro}`
- `{grr_calouro}`

Exemplo simples de `masc.txt`:

```
Oi {nome_veterano}! Tudo bem? Você foi sorteado como padrinho do calouro {nome_calouro} (GRR {grr_calouro}). Bem-vindo ao apadrinhamento!
```

Exemplo simples de `fem.txt`:

```
Oi {nome_veterano}! Tudo bem? Você foi sorteada como madrinha da caloura {nome_calouro} (GRR {grr_calouro}). Bem-vinda ao apadrinhamento!
```

---

## 5) Rodar o bot (envio via WhatsApp Web)

### 5.1 Rodar

```bash
python bot.py
```

### 5.2 Login no WhatsApp Web

- O navegador abrirá o WhatsApp Web.
- Se for a primeira vez, escaneie o QR Code.
- Depois volte no terminal e aperte **Enter** quando estiver logado.

O script usa:

- `--user-data-dir=./whatsapp_profile`

Isso mantém a sessão salva, então **nas próximas execuções geralmente não precisa escanear de novo**.

---

## 6) Durante o envio: o que observar

O bot:

- abre a conversa via link `send?phone=...&text=...`
- espera carregar
- clica no botão de enviar
- imprime logs no terminal

Você verá:

- ✅ Mensagem enviada para X
- ⚠️ Erro ao enviar mensagem para X
- Progresso: `enviadas`, `não enviadas`, `total`

Ao final:

- `🚀 Envio de mensagens concluído!`

---

## 7) Problemas comuns (rápido)

### “Telefone inválido / número errado”

Corrija no `data/veteranos.csv` e rode o `sorteio.py` novamente.

### Não aparece botão de enviar

Pode ser:

- número sem WhatsApp
- WhatsApp Web não carregou direito
- internet lenta (o bot usa `sleep(20)` antes de procurar o botão)

### Selenium/ChromeDriver error

Isso é compatibilidade do driver com o Chrome instalado. Se acontecer, me mande o erro exato que eu te digo o ajuste mais limpo.

---

## 8) Reexecução segura

Se você precisar rodar de novo:

- feche o navegador e rode `python bot.py` novamente
- a pasta `whatsapp_profile/` ajuda a não perder o login
- **recomendo sempre validar o CSV antes**
