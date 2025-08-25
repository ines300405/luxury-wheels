from conexao import conectar_base_dados

def inserir_dados_ficticios() -> None:
    """
    Insere dados fictícios de exemplo nas tabelas da base de dados Luxury Wheels.

    Dados inseridos:
        - utilizadores: admin e gestor.
        - clientes: 3 clientes com dados básicos.
        - veiculos: 20 veículos com diferentes marcas, tipos e categorias.
        - formaspagamento: 4 métodos de pagamento.
        - reservas: 3 reservas de exemplo.
        - pagamentos: 2 pagamentos vinculados a reservas.
        - manutencoes: 3 registros de manutenção de veículos.

    Observações:
        - Os IDs são atribuídos automaticamente pelo AUTOINCREMENT.
        - As datas estão em formato 'YYYY-MM-DD'.
        - Alguns campos têm valores padrão quando não especificados.
    """
    conn = conectar_base_dados()
    cursor = conn.cursor()

    # -------------------- Utilizadores --------------------
    cursor.executemany("""
        INSERT INTO utilizadores (nome, email, senha, perfil) VALUES (?, ?, ?, ?)
    """, [
        ('Admin Master', 'admin@luxurywheels.com', 'senha123', 'admin'),
        ('Gestor Regional', 'gestor@luxurywheels.com', 'senha123', 'gestor')
    ])

    # -------------------- Clientes --------------------
    cursor.executemany("""
        INSERT INTO clientes (nome, email, telefone, nif, data_registo) VALUES (?, ?, ?, ?, ?)
    """, [
        ('João Silva', 'joao.silva@gmail.com', '912345678', '123456789', '2023-12-01 10:15:00'),
        ('Maria Santos', 'maria.santos@gmail.com', '913456789', '987654321', '2024-01-20 14:30:00'),
        ('Carlos Oliveira', 'carlos.oliveira@gmail.com', '914567890', '456789123', '2024-03-05 09:00:00')
    ])

    # -------------------- Veículos --------------------
    cursor.executemany("""
        INSERT INTO veiculos (
            marca, modelo, matricula, ano, km_atual,
            data_ultima_revisao, data_proxima_revisao,
            categoria, transmissao, tipo, lugares, imagem,
            diaria, data_ultima_inspecao, data_proxima_inspecao, estado
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ('Mitsubishi', 'Pajero Sport', 'AA-01-PS', 2021, 48000, '2024-04-15', '2024-10-15',
         'SUV', 'Automática', 'Diesel', 7, 'Mitsubishi_Pajero_sport.jpg', 95.00, '2024-04-15', '2025-04-15', 'disponível'),
        # ... outros veículos omitidos para abreviação ...
        ('Mitsubishi', 'Outlander', 'QQ-17-MO', 2015, 91000, '2024-01-10', '2024-07-10',
         'SUV', 'Automática', 'Diesel', 5, 'Mitsubishi_Outlander_2015.jpg', 70.00, '2024-01-10', '2025-01-10', 'disponível')
    ])

    # -------------------- Formas de pagamento --------------------
    cursor.executemany("""
        INSERT INTO formaspagamento (metodo) VALUES (?)
    """, [
        ('Cartão de Crédito',),
        ('Multibanco',),
        ('Paypal',),
        ('Dinheiro',)
    ])

    # -------------------- Reservas --------------------
    cursor.executemany("""
        INSERT INTO reservas (id_cliente, id_veiculo, data_inicio, data_fim, estado) VALUES (?, ?, ?, ?, ?)
    """, [
        (1, 1, '2024-07-01', '2024-07-10', 'Confirmada'),
        (2, 2, '2024-07-05', '2024-07-12', 'Pendente'),
        (3, 3, '2024-07-03', '2024-07-08', 'Concluída')
    ])

    # -------------------- Pagamentos --------------------
    cursor.executemany("""
        INSERT INTO pagamentos (id_reserva, id_forma_pagamento, valor, data_pagamento) VALUES (?, ?, ?, ?)
    """, [
        (1, 1, 950.00, '2024-07-01'),
        (3, 2, 510.00, '2024-07-03')
    ])

    # -------------------- Manutenções --------------------
    cursor.executemany("""
        INSERT INTO manutencoes (id_veiculo, descricao, data_manutencao, custo) VALUES (?, ?, ?, ?)
    """, [
        (1, 'Mudança de óleo e filtros', '2024-04-15', 120.00),
        (2, 'Revisão geral', '2024-03-10', 200.00),
        (5, 'Substituição de pneus', '2024-06-01', 400.00)
    ])

    # Confirma alterações e fecha conexão
    conn.commit()
    conn.close()
    print("Dados fictícios inseridos com sucesso.")


if __name__ == "__main__":
    inserir_dados_ficticios()
