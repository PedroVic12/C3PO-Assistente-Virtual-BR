# Guia de Uso da CLI (cli.py)

Este documento explica como usar a ferramenta de linha de comando `cli.py` para gerenciar seu projeto Flask, automatizando a criação de modelos (Models) e controladores (Controllers).

## O que é `cli.py`?

`cli.py` é um script Python que atua como uma interface de linha de comando (CLI) para o seu projeto Flask. Ele utiliza o módulo `argparse` para definir e processar comandos, permitindo que você crie rapidamente a estrutura básica para novas entidades (como usuários, produtos, posts, etc.) em sua aplicação.

Atualmente, `cli.py` oferece os seguintes comandos:

-   `create-model <nome>`: Cria um novo arquivo de modelo (`<nome>_model.py`) na pasta `app/models/`. Este modelo inclui funcionalidades básicas para interagir com um banco de dados SQLite (CRUD - Criar, Ler, Atualizar, Deletar).
-   `create-controller <nome>`: Cria um novo arquivo de controlador (`<nome>_controller.py`) na pasta `app/controllers/`. Este controlador fornece endpoints de API RESTful (GET, POST, PUT, DELETE) para a entidade correspondente, utilizando o modelo criado.

### Como Usar

Para usar `cli.py`, navegue até o diretório raiz do seu projeto no terminal e execute o script com o comando desejado:

```bash
python3 cli.py <comando> <argumentos>
```

**Exemplos:**

-   Para criar um novo modelo chamado `User`:
    ```bash
    python3 cli.py create-model User
    ```
-   Para criar um novo controlador chamado `User`:
    ```bash
    python3 cli.py create-controller User
    ```

## Gerenciando Múltiplos Projetos/Rotas na API

A estrutura atual do seu projeto Flask permite que você crie diversas "entidades" (como `Example`, `Product`, `User`, `Post`, etc.), cada uma com seu próprio modelo e controlador. Cada controlador pode ser visto como um conjunto de rotas relacionadas a uma funcionalidade específica.

Para integrar novas entidades à sua API principal (`main.py`), você precisará:

1.  **Importar o Modelo e o Controlador:** No arquivo `main.py`, adicione as importações para o novo modelo e controlador.
    ```python
    # Exemplo para uma nova entidade 'Post'
    from app.models.post_model import PostModel
    from app.controllers.post_controller import PostController
    ```
2.  **Instanciar o Controlador:** Crie uma instância do novo controlador em `main.py`.
    ```python
    # Exemplo para uma nova entidade 'Post'
    post_controller = PostController()
    ```
3.  **Definir as Rotas da API:** Adicione as rotas (`@app.route`) em `main.py` que direcionarão as requisições para os métodos apropriados do seu novo controlador.
    ```python
    # Exemplo para uma nova entidade 'Post'
    @app.route('/api/posts', methods=['GET'])
    def get_posts():
        return post_controller.get_all()

    @app.route('/api/posts/<int:id>', methods=['GET'])
    def get_post(id):
        return post_controller.get_by_id(id)

    # ... e assim por diante para POST, PUT, DELETE
    ```

Dessa forma, você pode expandir sua API com novas funcionalidades, mantendo as rotas organizadas por entidade. Cada conjunto de rotas para uma entidade pode ser considerado um "mini-projeto" dentro da sua API maior.

## Tarefas Sugeridas para Aprendizado e Expansão

Aqui estão algumas tarefas para você praticar e expandir seu conhecimento usando esta estrutura de API:

1.  **Crie uma Entidade `User`:**
    *   Use `cli.py` para criar um modelo e um controlador para `User`.
    *   Modifique o `UserModel` para incluir campos como `email` (único) e `password` (hash).
    *   Integre as rotas de `User` no `main.py`.
    *   Teste as rotas de `User` usando ferramentas como Postman ou Insomnia.

2.  **Crie uma Entidade `Post` (para um blog):**
    *   Use `cli.py` para criar um modelo e um controlador para `Post`.
    *   Adicione campos como `title`, `content`, `author_id` (chave estrangeira para `User`).
    *   Implemente a lógica para buscar posts por autor.
    *   Integre as rotas de `Post` no `main.py`.

3.  **Implemente Autenticação Básica:**
    *   Adicione um endpoint de login (`/api/login`) que autentique usuários (criados na tarefa 1).
    *   Use JWT (JSON Web Tokens) para proteger algumas rotas (ex: criar/atualizar/deletar posts).

4.  **Adicione Validação de Dados:**
    *   No método `create` e `update` dos seus controladores, adicione validação de dados de entrada (ex: verificar se campos obrigatórios estão presentes, formato de e-mail).

5.  **Refatore Rotas para Blueprints:**
    *   Para projetos maiores, as rotas em `main.py` podem ficar muito extensas. Pesquise sobre "Flask Blueprints" e refatore suas rotas para usar essa funcionalidade, organizando-as em módulos separados (ex: `app/routes/user_routes.py`, `app/routes/product_routes.py`).

Essas tarefas o ajudarão a entender melhor a arquitetura de uma API RESTful com Flask e a utilizar a CLI para acelerar o desenvolvimento.
