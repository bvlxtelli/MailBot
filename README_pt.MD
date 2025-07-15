# 📧 **MailBot** *Cliente Python para e-mails otimizado*

Este módulo permite o envio de e-mails com ou sem anexos usando a API do Gmail com autenticação OAuth2 do Google. É compatível com envio de anexos locais, anexos em memória (`BytesIO`) e múltiplos arquivos PDF.

---

## 📦 Requisitos

🚀 Instalação do módulo

```bash
pip install git+https://github.com/bvlxtelli/MailBot.git
```

Instale as dependências com:

```bash
pip install --upgrade google-api-python-client google-auth google-auth-oauthlib
```

---

## 📁 Estrutura esperada

O módulo espera os arquivos de credenciais do Google:

```
credentials/
├── client_secret.json   # fornecido pelo Google Cloud
└── token.json           # gerado automaticamente após o primeiro login
```

- `client_secret.json`: Baixe em [console.cloud.google.com](https://console.cloud.google.com/) ao criar um OAuth Client ID
- `token.json`: Gerado automaticamente após o fluxo de autenticação

---

## 🚀 Como usar

### 1. **Importe e faça login no serviço do Gmail**

```python
from seu_modulo import login, enviar_email

service = login()
```

---

### 2. **Envie um e-mail simples**

```python
enviar_email(
    service=service,
    destinatario="exemplo@dominio.com",
    assunto="Teste",
    corpo="Olá! Esse é um e-mail enviado via API.",
)
```

---

### 3. **Com anexo local**

```python
enviar_email(
    service=service,
    destinatario="exemplo@dominio.com",
    assunto="Relatório",
    corpo="Segue em anexo.",
    caminho_anexo="relatorios/relatorio.pdf"
)
```

---

### 4. **Com anexo em memória (`BytesIO`)**

```python
from io import BytesIO

buffer = BytesIO()
buffer.write(b"PDF fake aqui")  # simule um PDF
buffer.seek(0)

enviar_email(
    service=service,
    destinatario="exemplo@dominio.com",
    assunto="Relatório Gerado",
    corpo="Segue o PDF em memória.",
    anexo_buffer=buffer,
    nome_anexo="meu_arquivo.pdf"
)
```

---

### 5. **Com múltiplos anexos (`dict` com buffers)**

```python
from io import BytesIO

anexos = {
    "arquivo1.pdf": BytesIO(b"conteudo1"),
    "arquivo2.pdf": BytesIO(b"conteudo2"),
}

for buf in anexos.values():
    buf.seek(0)

enviar_email(
    service=service,
    destinatario="exemplo@dominio.com",
    assunto="Múltiplos relatórios",
    corpo="Segue mais de um anexo.",
    multiplos_anexos=anexos
)
```

---

### 6. **Enviar conteúdo HTML (opcional)**

```python
enviar_email(
    service=service,
    destinatario="exemplo@dominio.com",
    assunto="E-mail com HTML",
    corpo="<h1>Olá!</h1><p>Este é um e-mail com <b>HTML</b>.</p>",
    html=True
)
```

---

## 📝 Logs

O módulo usa `logging` para registrar eventos importantes. Para ativar logs no seu script principal:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

---

## ✅ Escopos utilizados

Este módulo usa os seguintes escopos da API Gmail:

- `https://mail.google.com/`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.compose`
- `https://www.googleapis.com/auth/gmail.modify`

---

## 🛡️ Segurança

- Nunca compartilhe seu `client_secret.json` ou `token.json`.
- Use variáveis de ambiente ou `gitignore` para evitar vazamento dos arquivos de credenciais.

---

## 📄 Licença

Distribuído sob a licença privada interna. Qualquer redistribuição e utilização sem autorização é estritamente proibida.