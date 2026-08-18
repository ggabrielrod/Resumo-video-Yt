# 🛒 Monitor de Preços com Python

Sistema desenvolvido em **Python** para monitorar automaticamente o preço de um produto no Mercado Livre. O programa realiza consultas periódicas, armazena um histórico dos preços encontrados e envia uma notificação pelo **Telegram** quando o preço atinge ou fica abaixo do valor definido.

## 🚀 Funcionalidades

* 🔎 Consulta automática do preço de um produto.
* ⏰ Verificação periódica em intervalos configuráveis.
* 💰 Definição de um preço-alvo.
* 📊 Armazenamento do histórico de preços em arquivo JSON.
* 📱 Envio de alerta pelo Telegram quando o preço desejado é atingido.
* 📝 Exibição das informações e status das verificações no terminal.

## 🛠️ Tecnologias utilizadas

* **Python 3**
* `Requests` — realização das requisições HTTP.
* `BeautifulSoup4` — extração do preço da página.
* `Schedule` — agendamento das verificações.
* `JSON` — armazenamento do histórico de preços.
* `Telegram Bot API` — envio das notificações.

## 📂 Estrutura do projeto

```text
monitor-precos/
│
├── monitor.py
├── historico_precos.json
├── requirements.txt
└── README.md
```

> O arquivo `historico_precos.json` é criado automaticamente caso ainda não exista.

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone URL_DO_SEU_REPOSITORIO
cd monitor-precos
```

### 2. Instale as dependências

```bash
pip install requests beautifulsoup4 schedule
```

Ou, caso utilize um `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Configure o produto

No arquivo principal, altere as informações conforme necessário:

```python
PRODUTO_URL = "URL_DO_PRODUTO"
PRODUTO_NOME = "Nome do produto"
PRECO_ALVO = 450.00

INTERVALO_HORAS = 3
```

* `PRODUTO_URL` → URL do produto que será monitorado.
* `PRODUTO_NOME` → nome utilizado nas notificações.
* `PRECO_ALVO` → preço máximo desejado.
* `INTERVALO_HORAS` → intervalo entre cada consulta.

## 📱 Configuração do Telegram

Para receber os alertas, é necessário criar um bot no Telegram e configurar o token e o ID do chat.

**Importante:** não coloque seu token diretamente no código antes de publicar o projeto no GitHub.

O ideal é utilizar variáveis de ambiente:

```python
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
```

Depois, configure as variáveis no seu sistema.

### Windows

```powershell
$env:TELEGRAM_TOKEN="SEU_TOKEN"
$env:TELEGRAM_CHAT_ID="SEU_CHAT_ID"
```

## ▶️ Executando o projeto

Execute:

```bash
python monitor.py
```

O programa fará uma primeira consulta imediatamente e depois continuará verificando o preço de acordo com o intervalo configurado.

Exemplo de saída:

```text
Monitorando: Echo Dot
Preço-alvo: R$ 450.00
Checando a cada 3h.

[18/08/2026 13:00] Checando preço...
Preço encontrado: R$ 429.90
Notificação enviada!
```

## 📊 Histórico de preços

Cada consulta realizada é armazenada no arquivo:

```text
historico_precos.json
```

Exemplo:

```json
[
  {
    "data": "18/08/2026 13:00",
    "preco": 429.9
  },
  {
    "data": "18/08/2026 16:00",
    "preco": 439.9
  }
]
```

Isso permite acompanhar a variação do preço ao longo do tempo.

## 🔔 Exemplo de alerta

Quando o preço encontrado for menor ou igual ao preço-alvo, o bot envia uma mensagem semelhante a:

```text
🚨 PROMOÇÃO! Echo Dot
Preço atual: R$ 429.90
Alvo: R$ 450.00

URL do produto
```

## ⚠️ Observações

O projeto utiliza web scraping para obter o preço do produto. Alterações na estrutura HTML do site podem fazer com que o seletor utilizado deixe de encontrar o preço.

O seletor atualmente utilizado é:

```python
SELETOR_PRECO = "span.price"
```

Caso a estrutura da página seja alterada, será necessário atualizar o seletor.

## 🔒 Segurança

Nunca publique no GitHub:

* Tokens de bots.
* Senhas.
* Chaves de API.
* Credenciais pessoais.

Utilize variáveis de ambiente ou um arquivo `.env` que esteja incluído no `.gitignore`.

## 🎯 Objetivo do projeto

Este projeto foi desenvolvido como uma aplicação prática de Python, com foco em:

* Requisições HTTP.
* Web scraping.
* Manipulação de arquivos JSON.
* Automação de tarefas.
* Integração com APIs.
* Agendamento de tarefas.
* Tratamento de exceções.

## 👨‍💻 Autor

**Gabriel Oliveira**

Projeto desenvolvido para prática e demonstração de conhecimentos em **Python, automação e integração com APIs**.
