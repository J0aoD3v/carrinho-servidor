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

- `client-side/cliente.py`: Script Python que atua como cliente do sistema. Ele conecta-se ao servidor via TCP para enviar comandos e via UDP para transmitir vídeo da webcam local. Também executa um servidor web Flask para interface de controle e visualização do vídeo em tempo real. Permite enviar comandos ao carrinho e visualizar o log das ações.

- `server-side/servidor.py`: Script Python que atua como servidor do sistema. Ele recebe comandos via TCP e vídeo via UDP do cliente, processando e armazenando os comandos recebidos. Também executa um servidor web Flask para exibir o vídeo recebido do cliente e mostrar o log dos comandos recebidos. Serve como central de controle e monitoramento do carrinho.

- `client-side/`: Pasta com o código do cliente e seus templates web.
- `server-side/`: Pasta com o código do servidor e seus templates web.
- `README.md`: Documentação do projeto.

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

- Windows (PowerShell):
  ```powershell
  python server-side/servidor.py
  ```
- Ubuntu (Bash):
  ```bash
  python3 server-side/servidor.py
  ```

### Cliente (Windows ou Ubuntu/Linux)

- Windows (PowerShell):
  ```powershell
  python client-side/cliente.py
  ```
- Ubuntu (Bash):
  ```bash
  python3 client-side/cliente.py
  ```
