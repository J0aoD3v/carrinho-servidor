# Carrinho Servidor

## Estrutura do Projeto

```
carrinho-servidor/
│
├── client-side/
│   ├── cliente.py
│   └── templates/
│       └── index.html
│
├── server-side/
│   ├── servidor.py
│   └── templates/
│       └── servidor_index.html
│
└── README.md
```

### Descrição

- `client-side/`: Código do cliente (Windows ou Ubuntu/Linux)
- `server-side/`: Código do servidor (Ubuntu/Linux)
- `README.md`: Documentação

---

## Instalação

**Pré-requisito:** Python 3.x

1. Clone o repositório:

```bash
git clone https://github.com/J0aoD3v/carrinho-servidor
cd carrinho-servidor
```

2. (Opcional) Crie e ative um ambiente virtual:
   - Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - Ubuntu (Bash):
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Ative o ambiente virtual (caso ainda não tenha ativado) e instale as dependências:
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```
   - Ubuntu (Bash):
     ```bash
     source venv/bin/activate
     pip3 install -r requirements.txt
     ```

---

## Como rodar

### Servidor (Windows ou Ubuntu/Linux)

No diretório `server-side`:

- Windows (PowerShell):
  ```powershell
  python server-side/servidor.py
  ```
- Ubuntu (Bash):
  ```bash
  python3 server-side/servidor.py
  ```

### Cliente (Windows ou Ubuntu/Linux)

No diretório `client-side`:

- Windows (PowerShell):
  ```powershell
  python client-side/cliente.py
  ```
- Ubuntu (Bash):
  ```bash
  python3 client-side/cliente.py
  ```
