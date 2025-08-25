import unittest
from controllers.reservas import reservas_servico
from controllers.reservas import reservas_repositorio

class TestReservasBD(unittest.TestCase):
    """
    Testes unitários para operações de reservas.
    Inclui criação, edição, listagem e remoção de reservas.
    """

    def setUp(self):
        """
        Executa antes de cada teste.
        - Cria uma reserva temporária para uso nos testes.
        """
        self.reserva_dados = {
            "data_inicio": "2025-01-01",
            "data_fim": "2025-01-05",
            "cliente_id": 1,  # assumindo que existe um cliente com ID=1
            "veiculo_id": 1,  # assumindo que existe um veículo com ID=1
            "status": "Confirmada",
            "valor_total": 300.0
        }
        sucesso = reservas_servico.adicionar_reserva_servico(**self.reserva_dados)
        self.assertTrue(sucesso, "Falha ao criar reserva no setUp")

        # Buscar o ID da reserva recém-criada
        reservas = reservas_servico.obter_reservas_servico()
        self.reserva_id = reservas[0]["id"]

    def tearDown(self):
        """
        Executa após cada teste.
        - Remove a reserva temporária criada no setUp.
        """
        reservas_repositorio.remover_reserva_bd(self.reserva_id)

    def test_listar_reservas(self):
        """
        Testa a listagem de reservas.
        - Verifica se o retorno é uma lista.
        - Garante que existe pelo menos uma reserva.
        - Confirma que a reserva criada no setUp está presente.
        """
        reservas = reservas_servico.obter_reservas_servico()
        self.assertIsInstance(reservas, list)
        self.assertGreater(len(reservas), 0)
        self.assertEqual(reservas[0]["id"], self.reserva_id)

    def test_atualizar_reserva(self):
        """
        Testa atualização de uma reserva existente.
        - Modifica datas, estado e valor total.
        - Confirma que a reserva foi atualizada corretamente no banco.
        """
        resultado = reservas_servico.atualizar_reserva_servico(
            self.reserva_id, "2025-01-02", "2025-01-06",
            self.reserva_dados["cliente_id"], self.reserva_dados["veiculo_id"],
            "Cancelada", 350.0
        )
        self.assertTrue(resultado)
        reserva_atualizada = reservas_repositorio.buscar_reserva_por_id(self.reserva_id)
        self.assertEqual(reserva_atualizada["estado"], "Cancelada")
        self.assertEqual(reserva_atualizada["valor_total"], 350.0)

    def test_excluir_reserva(self):
        """
        Testa a exclusão de uma reserva.
        - Cria uma nova reserva temporária apenas para exclusão.
        - Remove a reserva e confirma que não existe mais no banco.
        """
        reservas_servico.adicionar_reserva_servico(
            "2025-02-01", "2025-02-05", 1, 1, "Confirmada", 400.0
        )
        reservas = reservas_servico.obter_reservas_servico()
        nova_id = reservas[0]["id"] if reservas[0]["id"] != self.reserva_id else reservas[1]["id"]

        resultado = reservas_servico.excluir_reserva_servico(nova_id)
        self.assertTrue(resultado)
        reserva_excluida = reservas_repositorio.buscar_reserva_por_id(nova_id)
        self.assertIsNone(reserva_excluida)
