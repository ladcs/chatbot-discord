# Discord Chat Bot + n8n Integration

Este repositório contém um **Discord Bot** integrado com um workflow do **n8n** via webhooks, utilizando Docker e Docker Compose para execução simplificada.

A aplicação permite ao usuário enviar prompts pelo Discord, enviá-los ao n8n, processá-los com um modelo LLM (OpenRouter), retornar a resposta e também informar a quantidade de tokens utilizados.

---

## 📌 **Arquitetura do Projeto**

```
DISCORD_CHAT_BOT/
 ├─ discord_bot/
 │   ├─ src/bot/
 │   │   ├─ main.py
 │   │   ├─ env_loader.py
 │   │   └─ __init__.py
 │   ├─ tests/
 │   │   └─ test_main.py
 │   ├─ .env
 │   ├─ .env.example
 │   ├─ Dockerfile
 │   └─ pyproject.toml
 ├─ docker-compose.yaml
 └─ README.md
```

---

## 🚀 **Como funciona**

### 1. **Usuário envia um comando no Discord**

O bot possui os comandos:

* `/hello` → Envia uma saudação.
* `/prompt <texto>` → Envia o prompt ao workflow principal do n8n.
* `/test <texto>` → Envia ao workflow de teste (`URL_TEST`).

Apenas o usuário autorizado via `USER_ID` pode usar o `/prompt` e `/test`, porém pode-se comentar  as linhas do arquivo main.py:

```py
if str(interaction.user.id) != user_id: # esse if é para restringir o uso do bot pelo id do usuário definido no .env
        await interaction.response.send_message(
            f"sorry {interaction.user.mention}, but I can't pay for all this token :'("
        )
        return
```

para retirar essa restrição.

---

### 2. **Bot envia o prompt ao n8n**

O bot envia via POST JSON contendo:

```json
{
  "prompt": "<texto>",
  "user_id": "...",
  "user_name": "...",
  "guild_id": "...",
  "channel_id": "..."
}
```

---

### 3. **n8n processa o prompt**

O workflow:

* Recebe o webhook
* Processa com **OpenRouter LLM**
* Extrai tokens via código Python interno
* Envia a resposta e depois a contagem de tokens no Discord

O workflow completo está no arquivo:

```
Agente_Simples_Extração_de_Informações.json
```

---

## 🧩 **Configuração do Ambiente**

### 🔑 Como obter sua API Key do OpenRouter

1. Acesse **[https://openrouter.ai](https://openrouter.ai)**
2. Crie uma conta ou faça login
3. Vá em **Dashboard → API Keys**
4. Clique em **Create Key**
5. Copie a chave gerada
6. No n8n, vá em **Credentials → OpenRouter API** e cole a chave

> Alguns modelos podem exigir verificação adicional ou billing habilitado.

### 🤖 Como criar um Bot no Discord

1. Abra o painel: **[https://discord.com/developers/applications](https://discord.com/developers/applications)**
2. Clique em **New Application**
3. Dê um nome e confirme
4. No menu lateral, vá em **Bot**
5. Clique em **Add Bot**
6. Em *Privileged Gateway Intents*, ative:

   * `MESSAGE CONTENT INTENT`
   * `SERVER MEMBERS INTENT` (opcional)
7. Em **Reset Token**, gere o TOKEN do bot e copie
8. No seu `.env` coloque:

```
BOT_TOKEN=seu_token_aqui
```

### 🔗 Como adicionar o bot ao seu servidor

1. Vá em **OAuth2 → URL Generator**
2. Em *Scopes*, selecione:

   * `bot`
   * `applications.commands`
3. Em *Bot Permissions*, selecione:

   * `Send Messages`
   * `Read Message History`
   * `Use Slash Commands`
4. Copie a URL gerada
5. Abra no navegador e selecione o servidor

### 1. Criar arquivo `.env` baseado no `.env.example`

```
BOT_TOKEN=<bot-token-do-discord>
USER_ID=<user-can-use-bot-if-not-commented-if-with-this-restriction>
URL=http://n8n:5678/webhook/aba1a9cf-80c5-4f4a-ad34-9feddc9dd71e
URL_TEST=http://n8n:5678/webhook-test/aba1a9cf-80c5-4f4a-ad34-9feddc9dd71e
```

### 2. Configurar credenciais no n8n

* **Webhook**
* **Discord Bot API**
* **OpenRouter API**

### 3. Importar o workflow no n8n

Use o JSON localizado em:

```
Agente_Simples_Extração_de_Informações.json
```

---

## 🐳 **Rodando com Docker Compose**

Na raiz do projeto:

```bash
docker-compose up -d --build
```

Isso irá subir:

* container do n8n
* container do Discord Bot

Logs do bot:

```bash
docker logs -f discord_bot
```

Acesse o n8n:

```
http://localhost:5678
```

Com tudo isso, o bot vai estar ativo e funcionando!

---

## 🧪 Testes

Os testes ficam em:

```
discord_bot/src/bot/tests/test_main.py
```

Para rodar (no container ou local com dev deps instaladas):

```bash
pytest
```

---

## 🛠️ Tecnologias utilizadas

* **Python 3.11**
* **Discord.py 2.3**
* **Requests**
* **python-dotenv**
* **n8n** (com OpenRouter)
* **Docker & Docker Compose**

---

## 💬 Comandos disponíveis no Discord

| Comando           | Descrição                             |
| ----------------- | ------------------------------------- |
| `/hello`          | Apenas diz hello                      |
| `/prompt <texto>` | Envia um prompt ao workflow principal |
| `/test <texto>`   | Envia ao workflow de teste            |

---

## 📄 **Dockerfile e Estrutura de Build**

O bot é empacotado via `pyproject.toml` e instalado no container Python slim.
A pasta `src` é montada em volume para permitir hot-reload durante desenvolvimento.

---

## 🧰 Erros comuns

### ❌ Webhook não recebe nada

* Verifique se o container se chama `n8n` (como no compose)
* Verifique se o endpoint no `.env` coincide com o caminho do workflow

### ❌ Resposta vem quebrada ou com tokens errados

O bloco Python do n8n deve ser exatamente o fornecido no JSON.

---

## 📜 Licença

**MIT License**.

---

## 🎉 Final

Parabéns por integrar Discord + n8n + OpenRouter com sucesso!
