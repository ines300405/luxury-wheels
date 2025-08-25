import unittest
from controllers.veiculos import veiculos_servico

class TestVeiculo(unittest.TestCase):
    """
    Testes unitários para operações de veículos.
    Inclui criação, listagem, edição e remoção de veículos.
    """

    def setUp(self):
        """
        Executa antes de cada teste.
        - Define um veículo base para teste.
        - Remove veículos existentes com a mesma matrícula para evitar conflitos.
        - Insere o veículo de teste no banco.
        """
        self.dados_base = {
            "marca": "Toyota",
            "modelo": "Corolla",
            "ano": 2020,
            "matricula": "AA-11-BB",
            "categoria": "Sedan",
            "transmissao": "Manual",
            "tipo": "Carro",
            "lugares": 5,
            "imagem": "corolla.png",
            "diaria": 45.0,
            "data_ultima_revisao": "2023-01-01",
            "data_proxima_revisao": "2024-01-01",
            "data_ultima_inspecao": "2023-01-15",
            "data_proxima_inspecao": "2024-01-15",
            "km_atual": 0,
            "estado": "disponível"
        }

        # Remove veículo existente com a mesma matrícula
        veiculos = veiculos_servico.obter_veiculos_servico()
        for v in veiculos:
            if v["matricula"] == self.dados_base["matricula"]:
                veiculos_servico.remover_veiculo_servico(v["id"])

        # Insere veículo base
        self.veiculo_id = veiculos_servico.adicionar_veiculo_servico(**self.dados_base)
        print("DEBUG -> Veículo inserido com ID:", self.veiculo_id)
        self.assertIsNotNone(self.veiculo_id, "Falha ao inserir veículo de teste no setUp")

    def tearDown(self):
        """
        Executa após cada teste.
        - Remove o veículo de teste criado no setUp.
        """
        if self.veiculo_id:
            veiculos_servico.remover_veiculo_servico(self.veiculo_id)

    def test_listar_veiculos(self):
        """
        Testa a listagem de veículos.
        - Verifica se o retorno é uma lista.
        - Garante que existe pelo menos um veículo.
        """
        veiculos = veiculos_servico.obter_veiculos_servico()
        self.assertIsInstance(veiculos, list)
        self.assertGreater(len(veiculos), 0)

    def test_adicionar_veiculo(self):
        """
        Testa a adição de um novo veículo.
        - Cria um veículo com matrícula única.
        - Verifica se a inserção foi bem-sucedida.
        - Remove o veículo criado após o teste.
        """
        novo_dados = self.dados_base.copy()
        novo_dados["marca"] = "Honda"
        novo_dados["modelo"] = "Civic"
        novo_dados["matricula"] = "CC-22-DD"

        veiculos = veiculos_servico.obter_veiculos_servico()
        for v in veiculos:
            if v["matricula"] == novo_dados["matricula"]:
                veiculos_servico.remover_veiculo_servico(v["id"])

        novo_id = veiculos_servico.adicionar_veiculo_servico(**novo_dados)
        self.assertIsNotNone(novo_id)
        veiculos_servico.remover_veiculo_servico(novo_id)

    def test_editar_veiculo(self):
        """
        Testa a edição de um veículo existente.
        - Atualiza diária e km do veículo.
        - Confirma se a atualização foi aplicada corretamente.
        """
        dados_atualizados = self.dados_base.copy()
        dados_atualizados["diaria"] = 60.0
        dados_atualizados["km_atual"] = 15000

        atualizado = veiculos_servico.atualizar_veiculo_servico(self.veiculo_id, **dados_atualizados)
        print("DEBUG -> Resultado atualização:", atualizado)
        self.assertTrue(atualizado, "Atualização falhou: veículo não encontrado ou dados inválidos")

        veiculos = veiculos_servico.obter_veiculos_servico()
        veiculo_atualizado = next((v for v in veiculos if v["id"] == self.veiculo_id), None)
        print("DEBUG -> Veículo atualizado:", veiculo_atualizado)

        self.assertIsNotNone(veiculo_atualizado)
        self.assertAlmostEqual(float(veiculo_atualizado["diaria"]), 60.0)
        self.assertEqual(int(veiculo_atualizado["km_atual"]), 15000)

    def test_remover_veiculo(self):
        """
        Testa a remoção de um veículo.
        - Cria um veículo temporário.
        - Remove o veículo e verifica se a exclusão foi bem-sucedida.
        """
        novo_dados = self.dados_base.copy()
        novo_dados["matricula"] = "EE-33-FF"

        veiculos = veiculos_servico.obter_veiculos_servico()
        for v in veiculos:
            if v["matricula"] == novo_dados["matricula"]:
                veiculos_servico.remover_veiculo_servico(v["id"])

        novo_id = veiculos_servico.adicionar_veiculo_servico(**novo_dados)
        removido = veiculos_servico.remover_veiculo_servico(novo_id)
        self.assertTrue(removido)

    def test_editar_veiculo_inexistente(self):
        """
        Testa atualização de veículo inexistente.
        - Deve retornar False ao tentar editar um veículo com ID inválido.
        """
        dados_invalidos = self.dados_base.copy()
        dados_invalidos["marca"] = "Invalido"
        resultado = veiculos_servico.atualizar_veiculo_servico(99999, **dados_invalidos)
        self.assertFalse(resultado)
