# 📰 Near News - Privacy News Aggregator in Python

This is a local project that automatically collects news from various RSS feeds about digital privacy and security, displaying them in a lightweight web interface using Python and Flask.

## ✅ Funcionalidades

- **Coleta de Feeds RSS:** Adicione e gira múltiplos feeds RSS através de uma interface web.
- **Filtros por Palavras-chave:** Os artigos são filtrados por um conjunto de palavras-chave configuráveis.
- **Interface Web Simples:** Inclui pesquisa de artigos e gestão de feeds.
- **Atualização Automática:** Um agendador atualiza os feeds a cada hora.
- **Banco de Dados SQLite:** Persistência de dados simples e eficaz.

---

## 🖥️ Como executar localmente

### Pré-requisitos
- Python 3.10+ instalado.

### Passos

1.  **Clone o repositório e navegue para a pasta:**
    ```bash
    git clone https://github.com/your-username/near-news.git
    cd near-news
    ```

2.  **(Recomendado) Crie e ative um ambiente virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # No Windows: .venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicialize a base de dados:**
    ```bash
    python database.py
    ```
    Este comando irá criar o ficheiro `news.db` e popular a tabela de feeds com fontes de notícias iniciais.

5.  **(Opcional) Popule a base de dados com as notícias mais recentes imediatamente:**
    Se não quiser esperar pela atualização automática, pode executar o parser manualmente.
    ```bash
    python news_parser.py
    ```

6.  **Execute a aplicação:**
    ```bash
    python app.py
    ```
    A aplicação estará disponível em `http://127.0.0.1:5000`.

### Gestão da Aplicação

-   **Parar a aplicação:**
    Pressione `Ctrl+C` no terminal onde a aplicação está a ser executada.

-   **Fazer reset à base de dados:**
    Para apagar todos os artigos e feeds, apague o ficheiro `news.db` e reinicialize a base de dados.
    ```bash
    rm news.db
    python database.py
    ```

---

## 📁 Estrutura do projeto
```
/
|-- app.py                # Aplicação principal Flask com as rotas
|-- config.py             # Ficheiro de configuração centralizado
|-- database.py           # Configuração e inicialização da base de dados (SQLAlchemy)
|-- news_parser.py        # Script para buscar e analisar notícias dos feeds RSS
|-- scheduler.py          # Módulo de agendamento de tarefas (APScheduler)
|-- requirements.txt      # Lista de dependências Python
|-- templates/
|   |-- index.html        # Template para a página principal (feed de notícias)
|   |-- feeds.html        # Template para a página de gestão de feeds
|-- static/
|   |-- style.css         # Folha de estilos CSS
|-- news.db               # Base de dados SQLite (criada após a inicialização)