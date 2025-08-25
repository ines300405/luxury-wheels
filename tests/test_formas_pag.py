import unittest
from controllers.formas_pagamento import formas_pag_servico
from controllers.formas_pagamento import formas_pag_repositorio

class TestFormasPagamentoBD(unittest.TestCase):
    """
    Testes unitários para as operações de formas de pagamento no banco de dados.
    Inclui criação, listagem, edição, exclusão e exportação para CSV.
    """

    def setUp(self):
        """
        Executa antes de cada teste.
        - Inicializa a tabela de formas de pagamento se necessário.
        - Cria uma forma de pagamento temporária para uso nos testes.
        """
        formas_pag_servico.inicializar_formas_pagamento()
        self.metodo = "Cartão Teste"
        sucesso = formas_pag_servico.adicionar_forma_pagamento(self.metodo)
        self.assertTrue(sucesso, "Falha ao criar forma de pagamento no setUp")
        # Obter o ID da forma criada
        formas = formas_pag_servico.obter_formas_pagamento()
        self.forma_id = formas[-1][0]  # pega a última inserida

    def tearDown(self):
        """
        Executa após cada teste.
        - Remove a forma de pagamento temporária criada no setUp.
        """
        formas_pag_repositorio.remover_forma_pagamento_bd(self.forma_id)

    def test_listar_formas_pagamento(self):
        """
        Testa a listagem de formas de pagamento.
        - Verifica se o resultado é uma lista.
        - Confirma que existe pelo menos uma forma cadastrada.
        - Garante que a forma criada no setUp está presente na lista.
        """
        formas = formas_pag_servico.obter_formas_pagamento()
        self.assertIsInstance(formas, list)
        self.assertGreater(len(formas), 0)
        self.assertIn((self.forma_id, self.metodo), formas)

    def test_editar_forma_pagamento(self):
        """
        Testa a atualização de uma forma de pagamento existente.
        - Altera o nome da forma.
        - Verifica se a atualização foi bem-sucedida.
        - Confirma que o novo nome está correto no banco.
        """
        novo_nome = "Cartão Alterado"
        resultado = formas_pag_servico.editar_forma_pagamento(self.forma_id, novo_nome)
        self.assertTrue(resultado)
        forma_atualizada = formas_pag_repositorio.buscar_forma_pagamento_por_id(self.forma_id)
        self.assertEqual(forma_atualizada["metodo"], novo_nome)

    def test_excluir_forma_pagamento(self):
        """
        Testa a exclusão de uma forma de pagamento.
        - Cria uma nova forma apenas para o teste de exclusão.
        - Executa a exclusão e confirma sucesso.
        - Garante que a forma não existe mais no banco.
        """
        formas_pag_servico.adicionar_forma_pagamento("MB WAY Teste")
        formas = formas_pag_servico.obter_formas_pagamento()
        nova_id = formas[-1][0] if formas[-1][0] != self.forma_id else formas[-2][0]

        resultado = formas_pag_servico.excluir_forma_pagamento(nova_id)
        self.assertTrue(resultado)
        forma_excluida = formas_pag_repositorio.buscar_forma_pagamento_por_id(nova_id)
        self.assertIsNone(forma_excluida)

    def test_exportar_formas_pagamento_para_csv(self):
        """
        Testa a exportação das formas de pagamento para arquivo CSV.
        - Verifica se a função retorna True indicando sucesso.
        """
        resultado = formas_pag_servico.exportar_formas_pagamento_para_csv("test_formas_pagamento.csv")
        self.assertTrue(resultado, "A exportação para CSV deve retornar True")
