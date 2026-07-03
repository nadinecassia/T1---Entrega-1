from entidade.pagamento import Pagamento
from entidade.pix import Pix
from entidade.dinheiro import Dinheiro
from entidade.cartao import Cartao
from limite.TelaPagamento import TelaPagamento
from dao.PagamentoDAO import PagamentoDAO


class ControladorPagamento:
    def __init__(self, controlador_principal) -> None:
        self.__controlador_principal = controlador_principal
        self.__tela_pagamento = TelaPagamento(self)
        self.__pagamento_dao = PagamentoDAO()

    def iniciar(self) -> None:
        self.abrir_tela()

    def __gerar_codigo(self) -> int:
        pagamentos = self.__pagamento_dao.get_all()

        if len(pagamentos) == 0:
            return 1
        
        maior_codigo = 0
        for pagamento in pagamentos:
            if pagamento.codigo > maior_codigo:
                maior_codigo = pagamento.codigo
        
        return maior_codigo + 1

    def pegar_atendimentos(self) -> list:
        return self.__controlador_principal.controlador_atendimento.atendimentos

    def listar_atendimentos_para_pagamento(self) -> None:
        atendimentos = self.pegar_atendimentos()

        if len(atendimentos) == 0:
            self.__tela_pagamento.mostrar_msg("Nenhum atendimento cadastrado.")
            return

        for indice, atendimento in enumerate(atendimentos):
            dados_atendimento = {
                "indice": indice,
                "paciente": atendimento.paciente.nome,
                "profissional": atendimento.profissional.nome,
                "clinica": atendimento.clinica.nome,
                "data": atendimento.data,
                "horario_inicio": atendimento.horario_inicio,
                "horario_fim": atendimento.horario_fim,
                "valor_restante": atendimento.calcular_valor_restante(),
            }

            self.__tela_pagamento.mostrar_atendimento_resumo(dados_atendimento)

    def selecionar_atendimento(self):
        atendimentos = self.pegar_atendimentos()

        if len(atendimentos) == 0:
            self.__tela_pagamento.mostrar_msg("Nenhum atendimento cadastrado.")
            return None

        self.listar_atendimentos_para_pagamento()

        indice = self.__tela_pagamento.selecionar_atendimento()

        if indice < 0 or indice >= len(atendimentos):
            self.__tela_pagamento.mostrar_msg("Atendimento inválido.")
            return None

        return atendimentos[indice]

    def criar_pagamento_para_atendimento(self, atendimento):
        dados_pagamento = self.__tela_pagamento.pegar_dados()

        if dados_pagamento["data"] > atendimento.data:
            self.__tela_pagamento.mostrar_msg(
                "ERRO: O pagamento deve ser realizado até a data do atendimento."
            )
            return None

        if dados_pagamento["valor_pago"] > atendimento.calcular_valor_restante():
            self.__tela_pagamento.mostrar_msg(
                "ERRO: O valor pago não pode ser maior que o valor restante."
            )
            return None

        codigo_novo = self.__gerar_codigo()
        modalidade = self.__tela_pagamento.mostrar_menu_modalidade()

        if modalidade == 1:
            pagamento = Dinheiro(
                codigo_novo,
                dados_pagamento["data"],
                dados_pagamento["valor_pago"],
                atendimento,
            )

        elif modalidade == 2:
            dados_pix = self.__tela_pagamento.pegar_dados_pix()

            pagamento = Pix(
                codigo_novo,
                dados_pagamento["data"],
                dados_pagamento["valor_pago"],
                dados_pix["cpf_pagador"],
                atendimento,
            )

        else:
            dados_cartao = self.__tela_pagamento.pegar_dados_cartao()

            pagamento = Cartao(
                codigo_novo,
                dados_pagamento["data"],
                dados_pagamento["valor_pago"],
                dados_cartao["numero_cartao"],
                dados_cartao["bandeira"],
                atendimento,
            )

        return pagamento

    def remover_pagamento_do_atendimento(self, atendimento) -> None:
        pagamentos_para_remover = []

        for pagamento in self.__pagamento_dao.get_all():
            if pagamento.atendimento == atendimento:
                pagamentos_para_remover.append(pagamento)

        for pagamento in pagamentos_para_remover:
            self.__pagamento_dao.remove(pagamento.codigo)

    def incluir_pagamento(self) -> None:
        atendimento = self.selecionar_atendimento()

        if atendimento is None:
            return

        pagamento = self.criar_pagamento_para_atendimento(atendimento)

        if pagamento is None:
            return

        pagamento.processar_pagamento()

        atendimento.add_pagamentos(pagamento)
        self.__pagamento_dao.add(pagamento)

        self.__tela_pagamento.mostrar_msg("Pagamento cadastrado com sucesso.")

    def listar_pagamentos(self) -> None:
        if len(self.__pagamento_dao.get_all()) == 0:
            self.__tela_pagamento.mostrar_msg("Nenhum pagamento cadastrado.")
            return

        for pagamento in self.__pagamento_dao.get_all():
            dados_pagamento = {
                "codigo": pagamento.codigo,
                "modalidade": self.identificar_modalidade(pagamento),
                "data": pagamento.data,
                "valor_pago": pagamento.valor_pago,
                "paciente": pagamento.paciente.nome,
            }

            self.__tela_pagamento.mostrar_pagamento(dados_pagamento)

    def pegar_pagamento_por_codigo(self, codigo: int) -> Pagamento | None:
        return self.__pagamento_dao.get(codigo)

    def identificar_modalidade(self, pagamento) -> str:
        if isinstance(pagamento, Dinheiro):
            return "Dinheiro"

        if isinstance(pagamento, Pix):
            return "PIX"

        if isinstance(pagamento, Cartao):
            return "Cartão de crédito"

        return "Pagamento"

    def alterar_pagamento(self) -> None:
        if len(self.__pagamento_dao.get_all()) == 0:
            self.__tela_pagamento.mostrar_msg("Nenhum pagamento cadastrado.")
            return

        self.listar_pagamentos()

        codigo = self.__tela_pagamento.selecionar_pagamento()
        pagamento = self.pegar_pagamento_por_codigo(codigo)

        if pagamento is None:
            self.__tela_pagamento.mostrar_msg("Pagamento não encontrado.")
            return

        dados_pagamento = self.__tela_pagamento.pegar_dados()

        if dados_pagamento["data"] > pagamento.atendimento.data:
            self.__tela_pagamento.mostrar_msg(
                "ERRO: O pagamento deve ser realizado até a data do atendimento."
            )
            return

        valor_maximo_permitido = (
            pagamento.valor_pago + pagamento.atendimento.calcular_valor_restante()
        )

        if dados_pagamento["valor_pago"] > valor_maximo_permitido:
            self.__tela_pagamento.mostrar_msg(
                "ERRO: O novo valor pago ultrapassa o valor restante."
            )
            return

        pagamento.data = dados_pagamento["data"]
        pagamento.valor_pago = dados_pagamento["valor_pago"]

        if isinstance(pagamento, Pix):
            dados_pix = self.__tela_pagamento.pegar_dados_pix()
            pagamento.cpf_pagador = dados_pix["cpf_pagador"]

        elif isinstance(pagamento, Cartao):
            dados_cartao = self.__tela_pagamento.pegar_dados_cartao()
            pagamento.numero_cartao = dados_cartao["numero_cartao"]
            pagamento.bandeira = dados_cartao["bandeira"]

        self.__pagamento_dao.update(pagamento)
        self.__tela_pagamento.mostrar_msg("Pagamento alterado com sucesso.")

    def excluir_pagamento(self) -> None:
        if len(self.__pagamento_dao.get_all()) == 0:
            self.__tela_pagamento.mostrar_msg("Nenhum pagamento cadastrado.")
            return

        self.listar_pagamentos()

        codigo = self.__tela_pagamento.selecionar_pagamento()
        pagamento = self.pegar_pagamento_por_codigo(codigo)

        if pagamento is None:
            self.__tela_pagamento.mostrar_msg("Pagamento não encontrado.")
            return

        self.__pagamento_dao.remove(codigo)

        if pagamento in pagamento.atendimento.pagamentos:
            pagamento.atendimento.pagamentos.remove(pagamento)

        self.__tela_pagamento.mostrar_msg("Pagamento removido com sucesso.")

    def abrir_tela(self) -> None:
        lista_opcoes = {
            1: self.incluir_pagamento,
            2: self.alterar_pagamento,
            3: self.excluir_pagamento,
            4: self.listar_pagamentos,
            0: self.voltar,
        }

        continua = True

        while continua:
            opcao_escolhida = self.__tela_pagamento.mostrar_menu()

            funcao_escolhida = lista_opcoes[opcao_escolhida]

            if opcao_escolhida == 0:
                continua = False

            funcao_escolhida()

    def voltar(self) -> None:
        return
