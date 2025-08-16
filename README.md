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
3. Instale as dependências:
   - Com requirements.txt:
     ```powershell
     pip install -r requirements.txt
     ```
     ou
     ```bash
     pip3 install -r requirements.txt
     ```
   - Se não houver requirements.txt:
     ```powershell
     pip install flask opencv-python numpy
     ```
     ou
     ```bash
     pip3 install flask opencv-python numpy
     ```

---

## Como rodar

### Servidor (Ubuntu/Linux)

No diretório `server-side`:

```bash
python3 servidor.py
```

### Cliente (Windows ou Ubuntu/Linux)

No diretório `client-side`:

- Windows (PowerShell):
  ```powershell
  python cliente.py
  ```
- Ubuntu (Bash):
  ```bash
  python3 cliente.py
  ```

Se houver um cliente web:

- Windows (PowerShell):
  ```powershell
  python cliente_web.py
  ```
- Ubuntu (Bash):
  ```bash
  python3 cliente_web.py
  ```

Abra o navegador e acesse o endereço indicado pelo script (ex: http://localhost:porta).
