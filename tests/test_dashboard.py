import unittest
from controllers.dashboard import dashboard_servico

class TestDashboard(unittest.TestCase):
    """
    Conjunto de testes unitários para os serviços do dashboard.
    Verifica métricas como total de clientes, veículos disponíveis,
    reservas ativas e receita total de pagamentos.
    """

    def test_obter_total_clientes(self):
        """
        Testa a função que retorna o total de clientes.
        - Verifica se o valor não é None.
        - Confirma que é um inteiro.
        - Garante que não é negativo.
        """
        total = dashboard_servico.obter_total_clientes()
        self.assertIsNotNone(total, "O total de clientes não deve ser None")
        self.assertIsInstance(total, int, "O resultado deve ser um inteiro")
        self.assertGreaterEqual(total, 0, "O total de clientes não pode ser negativo")

    def test_obter_total_veiculos_disponiveis(self):
        """
        Testa a função que retorna o total de veículos disponíveis.
        - Verifica se o valor não é None.
        - Confirma que é um inteiro.
        - Garante que não é negativo.
        """
        total = dashboard_servico.obter_total_veiculos_disponiveis()
        self.assertIsNotNone(total, "O total de veículos não deve ser None")
        self.assertIsInstance(total, int, "O resultado deve ser um inteiro")
        self.assertGreaterEqual(total, 0, "O total de veículos disponíveis não pode ser negativo")

    def test_obter_total_reservas_ativas(self):
        """
        Testa a função que retorna o total de reservas ativas.
        - Verifica se o valor não é None.
        - Confirma que é um inteiro.
        - Garante que não é negativo.
        """
        total = dashboard_servico.obter_total_reservas_ativas()
        self.assertIsNotNone(total, "O total de reservas não deve ser None")
        self.assertIsInstance(total, int, "O resultado deve ser um inteiro")
        self.assertGreaterEqual(total, 0, "O total de reservas ativas não pode ser negativo")

    def test_calcular_receita_total_pagamentos(self):
        """
        Testa a função que calcula a receita total de pagamentos.
        - Verifica se o valor não é None.
        - Confirma que é numérico (int ou float).
        - Garante que não é negativo.
        """
        receita = dashboard_servico.calcular_receita_total_pagamentos()
        self.assertIsNotNone(receita, "A receita total não deve ser None")
        self.assertIsInstance(receita, (int, float), "O resultado deve ser numérico")
        self.assertGreaterEqual(receita, 0.0, "A receita total não pode ser negativa")

    def test_obter_reservas_agrupadas_por_mes(self):
        """
        Testa a função que agrupa reservas por mês.
        - Verifica se o resultado é uma lista.
        - Para cada item, confere se contém as chaves 'mes' e 'total'.
        - Garante tipos corretos e valores não negativos.
        """
        reservas = dashboard_servico.obter_reservas_agrupadas_por_mes()
        self.assertIsInstance(reservas, list, "O resultado deve ser uma lista")

        if reservas:  # Só valida conteúdo se existir resultado
            for item in reservas:
                self.assertIn("mes", item, "Cada item deve conter a chave 'mes'")
                self.assertIn("total", item, "Cada item deve conter a chave 'total'")
                self.assertIsInstance(item["mes"], str, "O campo 'mes' deve ser string (YYYY-MM)")
                self.assertIsInstance(item["total"], int, "O campo 'total' deve ser inteiro")
                self.assertGreaterEqual(item["total"], 0, "O total de reservas por mês não pode ser negativo")
