import unittest
from controllers.pagamentos import pagamento_servico, pagamento_repositorio
from datetime import date

class TestPagamento(unittest.TestCase):
    """
    Testes unitários para as operações de pagamentos.
    Inclui criação, edição, listagem e remoção de registros.
    """

    def setUp(self):
        """
        Executa antes de cada teste.
        - Cria um pagamento temporário para uso nos testes.
        """
        self.dados_pagamento = {
            "data_pagamento": str(date.today()),   # formato AAAA-MM-DD
            "valor": 50.0,
            "id_forma_pagamento": 1,  # precisa existir na BD de testes
            "id_reserva": 1           # precisa existir na BD de testes
        }
        sucesso, msg = pagamento_servico.adicionar_pagamento(self.dados_pagamento)
        self.assertTrue(sucesso, f"Falha ao criar pagamento no setUp: {msg}")

        # Buscar o ID gerado
        pagamentos = pagamento_servico.obter_pagamentos()
        self.assertGreater(len(pagamentos), 0, "Nenhum pagamento encontrado após inserção.")
        self.pagamento_id = pagamentos[0]["id"]

    def tearDown(self):
        """
        Executa após cada teste.
        - Remove o pagamento temporário criado no setUp.
        """
        if self.pagamento_id:
            pagamento_repositorio.remover_pagamento_bd(self.pagamento_id)

    def test_editar_pagamento(self):
        """
        Testa a edição de um pagamento existente.
        - Atualiza o valor do pagamento.
        - Verifica se a atualização foi bem-sucedida.
        - Confirma que o valor no banco está correto.
        """
        novos_dados = {
            "id_pagamento": self.pagamento_id,
            "data_pagamento": str(date.today()),
            "valor": 100.0,
            "id_forma_pagamento": 1,
            "id_reserva": 1
        }
        sucesso, msg = pagamento_servico.editar_pagamento(novos_dados)
        self.assertTrue(sucesso, f"Edição de pagamento falhou: {msg}")

        pagamento = pagamento_repositorio.buscar_pagamento_por_id(self.pagamento_id)
        self.assertIsNotNone(pagamento)
        self.assertEqual(pagamento["valor"], 100.0)

    def test_editar_pagamento_inexistente(self):
        """
        Testa edição de um pagamento inexistente.
        - Deve retornar False indicando falha.
        """
        novos_dados = {
            "id_pagamento": 99999,
            "data_pagamento": str(date.today()),
            "valor": 200.0,
            "id_forma_pagamento": 1,
            "id_reserva": 1
        }
        sucesso, msg = pagamento_servico.editar_pagamento(novos_dados)
        self.assertFalse(sucesso, "Deveria falhar ao editar pagamento inexistente.")

    def test_listar_pagamentos(self):
        """
        Testa a listagem de pagamentos.
        - Verifica se o retorno é uma lista.
        - Garante que existe pelo menos um pagamento.
        """
        pagamentos = pagamento_servico.obter_pagamentos()
        self.assertIsInstance(pagamentos, list)
        self.assertGreater(len(pagamentos), 0)

    def test_remover_pagamento(self):
        """
        Testa a remoção de um pagamento.
        - Cria um pagamento temporário.
        - Remove o pagamento e verifica se a remoção foi bem-sucedida.
        """
        dados = {
            "data_pagamento": str(date.today()),
            "valor": 75.0,
            "id_forma_pagamento": 1,
            "id_reserva": 1
        }
        sucesso, msg = pagamento_servico.adicionar_pagamento(dados)
        self.assertTrue(sucesso, f"Falha ao criar pagamento para remoção: {msg}")

        # Buscar o último ID
        pagamentos = pagamento_servico.obter_pagamentos()
        novo_id = pagamentos[0]["id"]

        removido = pagamento_servico.excluir_pagamento(novo_id)
        self.assertTrue(removido, "Remoção de pagamento deveria retornar True")
