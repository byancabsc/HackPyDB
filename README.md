# 🛡️ HackPyDB – Plataforma Educativa de SQL Injection

**HackPyDB** é uma aplicação web vulnerável criada para fins **educacionais**, com o objetivo de ensinar e praticar **SQL Injection (SQLi)** nos três principais sistemas de gerenciamento de banco de dados:

- ✅ **MySQL**
- ✅ **PostgreSQL**
- ✅ **Microsoft SQL Server (MSSQL)**

> ⚠️ **Atenção**: Esta plataforma foi criada com intenções **didáticas** e **legais**. Utilize-a apenas em ambientes controlados, locais e com permissão explícita.

---

## 🚀 Funcionalidades Atuais

- 🔓 Página de login vulnerável a SQLi (Login Bypass)
- 🔍 Formulários de pesquisa com campos injetáveis
- 🧪 Diferentes bancos de dados para testar comportamentos variados
- 🔌 API simples e modular para expansão futura

---

## 📦 Instalação (Modo Local)

### Requisitos
- Python 3.8+
- Pip
- MySQL, PostgreSQL e MSSQL instalados localmente ou via Docker (em breve: suporte via `docker-compose`)
- Virtualenv (opcional)

### Passos

```bash
git clone https://github.com/gabrielwonheld/hackpydb
cd hackpydb

# Ativando ambiente virtual (opcional)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalando dependências
pip install -r requirements.txt

# Rodando a aplicação
python app.py
