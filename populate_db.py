import sqlite3
from faker import Faker
import random

fake = Faker()
conn = sqlite3.connect('supermarket.db')

# Criação da tabela se não existir
conn.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    descricao TEXT,
    data_fabricacao TEXT,
    validade TEXT
)
''')

# Inserir 1000 produtos de exemplo
for _ in range(1000):
    conn.execute('''
        INSERT INTO produtos (nome, categoria, preco, quantidade, descricao, data_fabricacao, validade) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        fake.word().capitalize() + " " + random.choice(['Sabor', 'Tipo', 'Estilo']),
        fake.random_element(elements=('Frutas', 'Laticínios', 'Grãos', 'Bebidas', 'Doces', 'Carnes', 'Pães', 'Condimentos', 'Higiene')),
        round(random.uniform(1.0, 100.0), 2),  # Preço entre 1.0 e 100.0
        random.randint(1, 100),  # Quantidade entre 1 e 100
        fake.text(max_nb_chars=100),  # Descrição
        fake.date_between(start_date='-2y', end_date='today'),  # Data de fabricação
        fake.date_between(start_date='today', end_date='+1y')  # Validade entre hoje e 1 ano após
    ))

conn.commit()
conn.close()

print("Banco de dados preenchido com 1000 produtos.")
