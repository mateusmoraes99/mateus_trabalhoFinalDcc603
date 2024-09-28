from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('supermarket.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    conn = sqlite3.connect('supermarket.db')
    cursor = conn.cursor()

    search_query = request.args.get('search', '')
    cor_filtro = request.args.get('cor', '')

    produtos_info = []

    if search_query:
        produtos = cursor.execute("SELECT * FROM produtos WHERE nome LIKE ? OR categoria LIKE ?", 
                                   ('%' + search_query + '%', '%' + search_query + '%')).fetchall()
    else:
        produtos = cursor.execute("SELECT * FROM produtos").fetchall()

    hoje = datetime.now().date()
    validade_limite = hoje + timedelta(days=30)
    estoque_baixo_limite = 20

    for produto in produtos:
        cor = "verde"
        data_validade = datetime.strptime(produto[7], '%Y-%m-%d').date()

        if produto[4] < estoque_baixo_limite:
            cor = "vermelho"
        elif data_validade < validade_limite:
            cor = "amarelo"

        if cor_filtro == '' or cor == cor_filtro:
            produtos_info.append((produto, cor))

    conn.close()
    return render_template('produtos.html', produtos=produtos_info, search_query=search_query, cor_filtro=cor_filtro)

def formatar_preco(preco):
    return f'R$ {preco:,.2f}'

@app.route('/add', methods=['POST'])
def add_product():
    nome = request.form['nome']
    categoria = request.form['categoria']
    preco = request.form['preco']
    quantidade = request.form['quantidade']
    descricao = request.form['descricao']
    data_fabricacao = request.form['data_fabricacao']
    validade = request.form['validade']

    conn = get_db_connection()
    conn.execute('INSERT INTO produtos (nome, categoria, preco, quantidade, descricao, data_fabricacao, validade) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (nome, categoria, preco, quantidade, descricao, data_fabricacao, validade))
    conn.commit()
    conn.close()
    
    return redirect('/')
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        data_fabricacao = request.form['data_fabricacao']
        validade = request.form['validade']
        descricao = request.form['descricao']

        conn.execute('''UPDATE produtos SET nome = ?, categoria = ?, preco = ?, quantidade = ?, 
                        data_fabricacao = ?, validade = ?, descricao = ? WHERE id = ?''',
                     (nome, categoria, preco, quantidade, data_fabricacao, validade, descricao, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_product.html', product=product)

# Rota para remover produto
@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/graficos')
def graficos():
    conn = sqlite3.connect('supermarket.db')
    cursor = conn.cursor()

    

    

    cursor.execute("SELECT preco, quantidade FROM produtos")
    dados_dispersao = cursor.fetchall()
    precos = [row[0] for row in dados_dispersao]
    quantidades = [row[1] for row in dados_dispersao]

    cursor.execute("SELECT data_fabricacao, SUM(quantidade) FROM produtos GROUP BY data_fabricacao")
    dados_area = cursor.fetchall()
    datas_area = [row[0] for row in dados_area]
    quantidades_area = [row[1] for row in dados_area]

    cursor.execute("SELECT preco FROM produtos")
    precos_histograma = cursor.fetchall()
    precos_flat = [row[0] for row in precos_histograma]

    cursor.execute("SELECT nome, (preco * quantidade) as lucro FROM produtos ORDER BY lucro DESC LIMIT 1")
    item = cursor.fetchone()
    item_nome, item_lucro = item[0], item[1] if item else ("N/A", "N/A")

    cursor.execute("SELECT categoria, COUNT(*) FROM produtos GROUP BY categoria")
    dados_pizza = cursor.fetchall()
    categorias = [row[0] for row in dados_pizza]
    quantidades_categoria = [row[1] for row in dados_pizza]

    cursor.execute("SELECT data_fabricacao, AVG(preco) FROM produtos GROUP BY data_fabricacao")
    dados_linha = cursor.fetchall()
    datas_linha = [row[0] for row in dados_linha]
    precos_medios = [row[1] for row in dados_linha]

    cursor.execute("SELECT categoria, SUM(quantidade) FROM produtos GROUP BY categoria")
    dados_barras = cursor.fetchall()
    categorias_barras = [row[0] for row in dados_barras]
    quantidades_barras = [row[1] for row in dados_barras]

    cursor.execute("""
    SELECT nome, categoria, preco, quantidade, (preco * quantidade) as lucro, 
           descricao, data_fabricacao, validade 
    FROM produtos 
    ORDER BY lucro DESC 
    LIMIT 1
     """)
    item = cursor.fetchone()

    if item:
       item_nome, item_categoria, item_preco, item_quantidade, item_lucro, item_descricao, item_data_fabricacao, item_validade = item
    else:
       item_nome, item_categoria, item_preco, item_quantidade, item_lucro, item_descricao, item_data_fabricacao, item_validade = ("N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    # Criando os gráficos
    # Gráfico de Dispersão
    plt.scatter(precos, quantidades, color='blue')
    plt.title('Gráfico de Dispersão: Preço vs Quantidade')
    plt.xlabel('Preço (R$)')
    plt.ylabel('Quantidade')
    img_dispersao = io.BytesIO()
    plt.savefig(img_dispersao, format='png')
    img_dispersao.seek(0)
    img_data_dispersao = base64.b64encode(img_dispersao.getvalue()).decode('utf8')
    plt.close()

    # Gráfico de Área
    plt.fill_between(datas_area, quantidades_area, color='orange', alpha=0.5)
    plt.title('Evolução do Estoque ao Longo do Tempo')
    plt.xlabel('Data de Fabricação')
    plt.ylabel('Quantidade')
    img_area = io.BytesIO()
    plt.savefig(img_area, format='png')
    img_area.seek(0)
    img_data_area = base64.b64encode(img_area.getvalue()).decode('utf8')
    plt.close()

    # Gráfico de Histograma
    plt.hist(precos_flat, bins=10, color='green', edgecolor='black')
    plt.title('Histograma: Distribuição de Preços')
    plt.xlabel('Preço (R$)')
    plt.ylabel('Frequência')
    img_histograma = io.BytesIO()
    plt.savefig(img_histograma, format='png')
    img_histograma.seek(0)
    img_data_histograma = base64.b64encode(img_histograma.getvalue()).decode('utf8')
    plt.close()

    # Gráfico de Pizza
    plt.pie(quantidades_categoria, labels=categorias, autopct='%1.1f%%', startangle=140)
    plt.title('Distribuição de Categorias de Produtos')
    img_pizza = io.BytesIO()
    plt.savefig(img_pizza, format='png')
    img_pizza.seek(0)
    img_data_pizza = base64.b64encode(img_pizza.getvalue()).decode('utf8')
    plt.close()

    # Gráfico de Linhas
    plt.plot(datas_linha, precos_medios, marker='o', color='purple')
    plt.title('Tendência do Preço Médio ao Longo do Tempo')
    plt.xlabel('Data de Fabricação')
    plt.ylabel('Preço Médio (R$)')
    img_linha = io.BytesIO()
    plt.savefig(img_linha, format='png')
    img_linha.seek(0)
    img_data_linha = base64.b64encode(img_linha.getvalue()).decode('utf8')
    plt.close()

    # Gráfico de Barras
    plt.bar(categorias_barras, quantidades_barras, color='cyan')
    plt.title('Quantidade Total por Categoria')
    plt.xlabel('Categoria')
    plt.ylabel('Quantidade')
    img_barras = io.BytesIO()
    plt.savefig(img_barras, format='png')
    img_barras.seek(0)
    img_data_barras = base64.b64encode(img_barras.getvalue()).decode('utf8')
    plt.close()

    conn.close()

    

    return render_template('graficos.html', 
                           img_data_dispersao=img_data_dispersao, 
                           img_data_area=img_data_area, 
                           img_data_histograma=img_data_histograma,
                           img_data_pizza=img_data_pizza,
                           img_data_linha=img_data_linha,
                           img_data_barras=img_data_barras,
                           item_nome=item_nome,
                           item_lucro=item_lucro,
                           item_categoria=item_categoria,
                           item_quantidade=item_quantidade,
                           item_descricao=item_descricao,
                           item_data_fabricacao=item_data_fabricacao,
                           item_validade=item_validade,
                           item_preco=item_preco )

if __name__ == '__main__':
    app.run(debug=True)
