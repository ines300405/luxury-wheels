from conexao import conectar_base_dados

def criar_tabelas() -> None:
    """
    Cria todas as tabelas necessárias para a aplicação Luxury Wheels.

    Tabelas criadas:
        - utilizadores: gestão de utilizadores do sistema (admin ou gestor).
        - clientes: registo de clientes da empresa.
        - veiculos: inventário de veículos com informações completas.
        - formaspagamento: métodos de pagamento disponíveis.
        - reservas: reservas feitas pelos clientes.
        - pagamentos: pagamentos realizados por reservas.
        - manutencoes: registo de manutenções realizadas nos veículos.

    Observações:
        - Usa FOREIGN KEYS para garantir integridade referencial.
        - Tabelas só são criadas se não existirem.
    """
    conn = conectar_base_dados()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS utilizadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        perfil TEXT DEFAULT 'gestor'  -- Pode ser 'admin' ou 'gestor'
    );

    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE,
        telefone TEXT,
        nif TEXT,
        data_registo TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT,
        modelo TEXT,
        matricula TEXT UNIQUE,
        ano INTEGER,
        km_atual INTEGER,
        data_ultima_revisao TEXT,
        data_proxima_revisao TEXT,
        categoria TEXT,
        transmissao TEXT,
        tipo TEXT,
        lugares INTEGER,
        imagem TEXT,
        diaria REAL,
        data_ultima_inspecao TEXT,
        data_proxima_inspecao TEXT,
        estado TEXT DEFAULT 'disponível'  -- Ex: disponível, alugado, em manutenção
    );

    CREATE TABLE IF NOT EXISTS formaspagamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metodo TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_veiculo INTEGER,
        data_inicio TEXT,
        data_fim TEXT,
        estado TEXT DEFAULT 'Pendente',  -- Confirmada, Concluída, Pendente, Cancelada
        FOREIGN KEY (id_cliente) REFERENCES clientes(id),
        FOREIGN KEY (id_veiculo) REFERENCES veiculos(id)
    );

    CREATE TABLE IF NOT EXISTS pagamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_reserva INTEGER,
        id_forma_pagamento INTEGER,
        valor REAL,
        data_pagamento TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (id_reserva) REFERENCES reservas(id),
        FOREIGN KEY (id_forma_pagamento) REFERENCES formaspagamento(id)
    );

    CREATE TABLE IF NOT EXISTS manutencoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_veiculo INTEGER,
        descricao TEXT,
        data_manutencao TEXT,
        custo REAL,
        FOREIGN KEY (id_veiculo) REFERENCES veiculos(id)
    );
    """)

    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso.")


if __name__ == "__main__":
    criar_tabelas()
