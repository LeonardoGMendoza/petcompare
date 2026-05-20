# 🐾 PetCompare — Automação e Dashboard

PetCompare é um sistema corporativo no nicho Pet, combinando **RPA, Web Scraping e API REST**, para buscar, agrupar e exibir os melhores preços de serviços (Hotéis, Creches e Pet Sitters).

## 🚀 Arquitetura do Projeto

* **Backend API**: Python (FastAPI + SQLAlchemy) conectado ao PostgreSQL.
* **Scraping Bots**: Selenium, Requests, BeautifulSoup (para varrer DogHero, Google Maps, etc).
* **RPA Bots**: PyAutoGUI e pywinauto para automação de desktop e preenchimento de sistemas locais.
* **Data Processing**: Pandas para limpeza, agregação e exportação em Excel/CSV.
* **Frontend**: HTML/CSS/JS (Vanilla) com design Premium Dark Mode (Estilo Trivago).
* **Agendamento**: APScheduler para rodar robôs automaticamente de madrugada.

## 🛠️ Requisitos

* Python 3.10+
* Google Chrome instalado (para o Selenium)
* PostgreSQL rodando localmente ou no servidor (veja o `.env`)

## ⚙️ Instalação Local

1. Clone o repositório ou baixe os arquivos.
2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Renomeie o arquivo `.env.example` para `.env` e preencha suas configurações do banco de dados (Host, Senha, User).

## 🏃 Como Rodar a API

Para subir a API localmente:
```bash
python run.py
```
A API estará disponível em: `http://localhost:8001`
* Documentação Swagger: `http://localhost:8001/docs`

## 🐳 Como Rodar no Servidor (Docker)

Se você for subir no seu servidor Ubuntu (187.77.32.137):
```bash
docker-compose up -d --build
```
Isso vai subir um container com o PostgreSQL e outro com a API FastAPI na porta 8001.

## 🎨 Como Acessar o Dashboard (Site)

Basta abrir o arquivo `dashboard/index.html` diretamente no seu navegador, ou hospedá-lo em qualquer servidor web (como Nginx ou Apache) apontando para a pasta `dashboard`.

## 🤖 Como os Robôs funcionam

Os módulos estão divididos em:
* `bots/scraping/`: Contém os robôs que buscam em sites na internet usando Selenium.
* `bots/rpa/`: Contém robôs que controlam mouse e teclado.

Para integrar um robô, você deve importá-lo no `api/routes/jobs.py` e chamar o método `schedule_daily_scraping` localizado em `scheduler/task_scheduler.py`.
