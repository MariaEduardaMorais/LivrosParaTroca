# 📚 Sistema de Troca de Livros

Este é um sistema web para troca de livros entre usuários, permitindo cadastro, edição e exclusão de livros, além de registro de resenhas.

## 🚀 Funcionalidades

- 📖 **Cadastro de Livros**: Título, autor, edição e estado de conservação.
- 🔄 **Troca de Livros**: Solicitação e histórico de trocas.
- 📝 **Resenhas**: Registro, edição e exclusão de resenhas associadas aos livros.
- 👤 **Perfis de Usuários**: Histórico de trocas e resenhas.
- 🖥 **Interface Web**: Frontend interativo com design moderno.

## 🛠 Tecnologias Utilizadas

- **Backend**: Flask + SQLAlchemy
- **Frontend**: HTML, CSS e JavaScript
- **Banco de Dados**: SQLite

## 📂 Estrutura do Projeto

```
📦 sistema-troca-livros
├── 📂 static
│   ├── 📄 style.css  # Estilos do frontend
│   ├── 📄 script.js  # Lógica do frontend
├── 📂 templates
│   ├── 📄 index.html  # Página principal
│   ├── 📄 detalhes.html  # Página de detalhes do livro
├── 📂 database
│   ├── 📄 db.sqlite3  # Banco de dados SQLite
├── 📄 app.py  # Aplicação Flask
├── 📄 README.md  # Documentação
```

## 🏁 Como Executar o Projeto

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/seu-usuario/sistema-troca-livros.git
cd sistema-troca-livros
```

### 2️⃣ Crie um ambiente virtual e instale as dependências
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Execute a aplicação
```bash
python app.py
```

### 4️⃣ Acesse no navegador
```
http://127.0.0.1:5000/
```

## 📌 Endpoints da API

### ➕ Adicionar Livro
```http
POST /add
```
**Body JSON:**
```json
{
  "titulo": "Livro Exemplo",
  "autor": "Autor Exemplo",
  "edicao": "1ª",
  "estado": "Bom"
}
```

### 🔄 Editar Livro
```http
PUT /update/<id>
```

### ❌ Excluir Livro
```http
DELETE /delete/<id>
```
