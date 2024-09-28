# mateus_trabalhoFinalDcc603
# Controle de Estoque
Este projeto é um sistema de Controle de Estoque desenvolvido em Python utilizando Flask para o backend e SQLite como banco de dados. O sistema permite gerenciar produtos de forma simples e eficiente, com funcionalidades de CRUD (Create, Read, Update, Delete) e alertas automáticos para quando o estoque de um produto estiver baixo.

## Funcionalidades
Cadastro de Produtos: Adicione novos produtos ao sistema, informando nome, preço, quantidade, categoria e data de validade.
Visualização de Produtos: Veja a lista de produtos cadastrados com detalhes como nome, quantidade disponível e validade.
Edição de Produtos: Atualize as informações de qualquer produto cadastrado.
Exclusão de Produtos: Remova produtos do estoque de forma segura.
Alertas de Estoque Baixo: O sistema emite um alerta visual quando a quantidade de um produto está abaixo do limite crítico.

## Tecnologias Utilizadas
Backend: Flask (Python)
Banco de Dados: SQLite
Frontend: HTML5, CSS3 (customizado)
Flask-WTF para tratamento de formulários.
sqlite para interação com o banco de dados.
## Instalação e Configuração
Pré-requisitos
Python 3.12 ou superior
Virtualenv para criação de ambientes virtuai

## Instale as dependências:
    pip install -r requirements.txt
    
### caso não tenha o arquivo supermarket.db execute:
    poputate_db.py
    
## Execute a aplicação:
    python app.py
# Como Usar

## 1. Adicionar um Produto
Vá para a página "Adicionar Produto".
Preencha as informações necessárias (nome, categoria, quantidade, preço, validade).
Clique em "Salvar". O produto será adicionado ao sistema.

## 2. Editar ou Excluir um Produto
Na página principal (lista de produtos), clique em "Editar" ou "Excluir" ao lado do produto que deseja modificar.
Após editar, clique em "Salvar". Para excluir, o sistema pedirá confirmação antes de remover o item.

## 3. Alertas de Estoque
Quando o estoque de um produto estiver abaixo de um limite crítico (definido no código), o sistema destacará o produto em vermelho para chamar a atenção do usuário
