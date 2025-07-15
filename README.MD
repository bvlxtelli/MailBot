
# 📧 **MailBot** *Optimized Python e-mail client*

This module enables sending emails with or without attachments using the Gmail API and Google's OAuth2 authentication. It supports local file attachments, in-memory attachments (`BytesIO`), and multiple PDF files.

---

## 📦 Requirements

🚀 Module Installation

```bash
pip install git+https://github.com/bvlxtelli/MailBot.git
```

Install the dependencies with:

```bash
pip install --upgrade google-api-python-client google-auth google-auth-oauthlib
```

---

## 📁 Expected Structure

The module expects the following Google credential files:

```
credentials/
├── client_secret.json   # provided by Google Cloud
└── token.json           # automatically generated after first login
```

- `client_secret.json`: Download from [console.cloud.google.com](https://console.cloud.google.com/) after creating an OAuth Client ID
- `token.json`: Automatically generated after the authentication flow

---

## 🚀 How to Use

### 1. **Import and login to the Gmail service**

```python
from your_module import login, enviar_email

service = login()
```

---

### 2. **Send a simple email**

```python
enviar_email(
    service=service,
    destinatario="example@domain.com",
    assunto="Test",
    corpo="Hello! This is an email sent via API.",
)
```

---

### 3. **With local attachment**

```python
enviar_email(
    service=service,
    destinatario="example@domain.com",
    assunto="Report",
    corpo="Please find the attachment.",
    caminho_anexo="relatorios/relatorio.pdf"
)
```

---

### 4. **With in-memory attachment (`BytesIO`)**

```python
from io import BytesIO

buffer = BytesIO()
buffer.write(b"Fake PDF content here")  # simulate a PDF
buffer.seek(0)

enviar_email(
    service=service,
    destinatario="example@domain.com",
    assunto="Generated Report",
    corpo="Here is the in-memory PDF.",
    anexo_buffer=buffer,
    nome_anexo="my_file.pdf"
)
```

---

### 5. **With multiple attachments (`dict` of buffers)**

```python
from io import BytesIO

anexos = {
    "file1.pdf": BytesIO(b"content1"),
    "file2.pdf": BytesIO(b"content2"),
}

for buf in anexos.values():
    buf.seek(0)

enviar_email(
    service=service,
    destinatario="example@domain.com",
    assunto="Multiple Reports",
    corpo="Multiple attachments included.",
    multiplos_anexos=anexos
)
```

---

### 6. **Send HTML content (optional)**

```python
enviar_email(
    service=service,
    destinatario="example@domain.com",
    assunto="HTML Email",
    corpo="<h1>Hello!</h1><p>This is an email with <b>HTML</b>.</p>",
    html=True
)
```

---

## 📝 Logs

The module uses `logging` to record important events. To enable logging in your main script:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

---

## ✅ Used Scopes

This module uses the following Gmail API scopes:

- `https://mail.google.com/`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.compose`
- `https://www.googleapis.com/auth/gmail.modify`

---

## 🛡️ Security

- Never share your `client_secret.json` or `token.json`.
- Use environment variables or `.gitignore` to prevent leaking credential files.

---

## 📄 License

Distributed under internal private license. Redistribution or usage without authorization is strictly prohibited.