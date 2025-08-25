import unittest
import random
import string
from controllers.cliente import cliente_repositorio

class TestCliente(unittest.TestCase):
    """
    Conjunto de testes unitários para as operações de CRUD de clientes.
    Usa cliente de teste gerado dinamicamente para evitar conflitos.
    """

    def setUp(self):
        """
        Executa antes de cada teste:
        - Gera um cliente de teste com email único.
        - Remove cliente existente com mesmo email (precaução).
        - Adiciona o cliente na base de dados para uso nos testes.
        """
        self.nome = "Teste Cliente"
        sufixo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        self.email = f"teste_{sufixo}@exemplo.com"
        self.telefone = "912345678"
        self.nif = "123456789"

        # Remove cliente existente com mesmo email
        existente = cliente_repositorio.buscar_cliente_por_email(self.email)
        if existente:
            cliente_repositorio.remover_cliente(existente["id"])

        # Adiciona cliente de teste
        sucesso = cliente_repositorio.adicionar_cliente(
            self.nome, self.email, self.telefone, self.nif
        )
        self.assertTrue(sucesso, "Falha ao criar cliente no setUp")

        # Armazena ID do cliente criado
        cliente = cliente_repositorio.buscar_cliente_por_email(self.email)
        self.assertIsNotNone(cliente, "Cliente não encontrado após criação")
        self.cliente_id = cliente["id"]

    def tearDown(self):
        """
        Executa depois de cada teste:
        - Remove o cliente de teste da base de dados.
        """
        if hasattr(self, "cliente_id") and self.cliente_id:
            cliente_repositorio.remover_cliente(self.cliente_id)

    def test_atualizar_cliente(self):
        """
        Testa a atualização de um cliente existente:
        - Altera o nome do cliente.
        - Verifica se a alteração foi persistida na base de dados.
        """
        novo_nome = "Novo Nome"
        sucesso = cliente_repositorio.atualizar_cliente(
            self.cliente_id, novo_nome, self.email, self.telefone, self.nif
        )
        self.assertTrue(sucesso, "Falha ao atualizar cliente")

        # Verifica o cliente atualizado pelo ID
        from controllers.cliente.cliente_repositorio import listar_clientes
        clientes = listar_clientes()
        cliente = next((c for c in clientes if c["id"] == self.cliente_id), None)

        self.assertIsNotNone(cliente, "Cliente não encontrado após atualização")
        self.assertEqual(cliente["nome"], novo_nome)

    def test_listar_clientes(self):
        """
        Testa a listagem de clientes:
        - Verifica se retorna uma lista.
        - Confirma que a lista não está vazia.
        """
        clientes = cliente_repositorio.listar_clientes()
        self.assertIsInstance(clientes, list)
        self.assertGreater(len(clientes), 0)

    def test_atualizar_cliente_inexistente(self):
        """
        Testa atualização de cliente inexistente:
        - Deve retornar False quando tenta atualizar ID inválido.
        """
        resultado = cliente_repositorio.atualizar_cliente(
            99999, "Invalido", "inv@email.com", "999999999", "000000000"
        )
        self.assertFalse(resultado, "Deve falhar ao atualizar cliente inexistente")
