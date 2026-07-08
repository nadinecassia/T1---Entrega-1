from entidade.pagamento import Pagamento
from entidade.pix import Pix
from entidade.dinheiro import Dinheiro
from entidade.cartao import Cartao
from limite_gui.TelaPagamentoGUI import TelaPagamentoGUI
from dao.PagamentoDAO import PagamentoDAO


class ControladorPagamento:
    def __init__(self, controlador_principal) -> None:
        self.__controlador_principal = controlador_principal
        self.__tela_pagamento = TelaPagamentoGUI(self)
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

    def selecionar_atendimento(self):
        atendimentos = self.pegar_atendimentos()

        if len(atendimentos) == 0:
            self.__tela_pagamento.mostrar_mensagem("Nenhum atendimento cadastrado.")
            return None

        return self.__controlador_principal.controlador_atendimento.selecionar_atendimento()


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
        
        dados_pagamento = self.__tela_pagamento.abrir_janela_cadastro()

        if dados_pagamento is None:
            return
        
        if dados_pagamento["data"] > atendimento.data:
            self.__tela_pagamento.mostrar_mensagem(
                "ERRO: O pagamento deve ser realizado até a data do atendimento"
            )
            return

        if dados_pagamento["valor_pago"] > atendimento.calcular_valor_restante():
            self.__tela_pagamento.mostrar_mensagem(
                "ERRO: O valor pago não pode ser maior que o valor restante."
            )  
            return
        
        codigo_novo = self.__gerar_codigo()
        modalidade = dados_pagamento["modalidade"]
        pagamento = None

        if modalidade == "Dinheiro":
            pagamento = Dinheiro(
                codigo_novo,
                dados_pagamento["data"],
                dados_pagamento["valor_pago"],
                atendimento,
            )
        
        elif modalidade == "PIX":
            dados_pix = self.__tela_pagamento.pegar_dados_pix()

            if dados_pix is None:
                return
            
            pagamento = Pix(
                codigo_novo,
                dados_pagamento["data"],
                dados_pagamento["valor_pago"],
                dados_pix["cpf_pagador"],
                atendimento,
            )
        
        elif modalidade == "Cartão de crédito":
            dados_cartao = self.__tela_pagamento.pegar_dados_cartao()

            if dados_cartao is None:
                return
            
            pagamento = Cartao(
                codigo_novo,
                dados_pagamento["data"],
                dados_pagamento["valor_pago"],
                dados_cartao["numero_cartao"],
                dados_cartao["bandeira"],
                atendimento,
            )
        
        if pagamento is not None:
            pagamento.processar_pagamento()
            atendimento.add_pagamentos(pagamento)
            self.__pagamento_dao.add(pagamento)

            self.__tela_pagamento.mostrar_mensagem("Pagamento cadastrado com sucesso!")

    def listar_pagamentos(self) -> None:
        pagamentos = self.__pagamento_dao.get_all()

        if len(pagamentos) == 0:
            self.__tela_pagamento.mostrar_mensagem("Nenhum pagamento cadastrado.")
            return
        
        self.__tela_pagamento.tabela_pagamentos(pagamentos)

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
            self.__tela_pagamento.mostrar_mensagem("Nenhum pagamento cadastrado.")
            return

        codigo = self.__tela_pagamento.tabela_pagamentos(
            self.__pagamento_dao.get_all(),
            selecionar=True
        )
        
        if codigo is None:
            return
        
        pagamento = self.pegar_pagamento_por_codigo(codigo)

        if pagamento is None:
            self.__tela_pagamento.mostrar_mensagem("Pagamento não encontrado.")
            return
        
        dados_antigos = {
            "data": pagamento.data,
            "valor_pago": pagamento.valor_pago,
            "modalidade": self.identificar_modalidade(pagamento)
        }

        novos_dados = self.__tela_pagamento.abrir_janela_cadastro(dados_antigos)

        if novos_dados is None:
            return

        if novos_dados["data"] > pagamento.atendimento.data:
            self.__tela_pagamento.mostrar_mensagem(
                "ERRO: O pagamento deve ser realizado até a data do atendimento."
            )
            return

        valor_maximo_permitido = (
            pagamento.valor_pago + pagamento.atendimento.calcular_valor_restante()
        )

        if novos_dados["valor_pago"] > valor_maximo_permitido:
            self.__tela_pagamento.mostrar_mensagem(
                "ERRO: O novo valor pago ultrapassa o valor restante."
            )
            return
        
        if novos_dados["modalidade"] != self.identificar_modalidade(pagamento):
            self.__tela_pagamento.mostrar_mensagem("Para trocar de modalidade, exclua este pagamento e crie um novo.")
            return

        pagamento.data = novos_dados["data"]
        pagamento.valor_pago = novos_dados["valor_pago"]

        if isinstance(pagamento, Pix):
            dados_pix = self.__tela_pagamento.pegar_dados_pix()
            if dados_pix is None: return
            pagamento.cpf_pagador = dados_pix["cpf_pagador"]

        elif isinstance(pagamento, Cartao):
            dados_cartao = self.__tela_pagamento.pegar_dados_cartao()
            if dados_cartao is None: return
            pagamento.numero_cartao = dados_cartao["numero_cartao"]
            pagamento.bandeira = dados_cartao["bandeira"]

        self.__pagamento_dao.update(pagamento)
        self.__tela_pagamento.mostrar_mensagem("Pagamento alterado com sucesso.")

    def excluir_pagamento(self) -> None:
        if len(self.__pagamento_dao.get_all()) == 0:
            self.__tela_pagamento.mostrar_mensagem("Nenhum pagamento cadastrado.")
            return

        codigo = self.__tela_pagamento.tabela_pagamentos(
            self.__pagamento_dao.get_all(),
            selecionar=True
        )

        if codigo is None:
            return
        
        pagamento = self.pegar_pagamento_por_codigo(codigo)

        if pagamento is None:
            self.__tela_pagamento.mostrar_mensagem("Pagamento não encontrado.")
            return

        self.__pagamento_dao.remove(codigo)

        if pagamento in pagamento.atendimento.pagamentos:
            pagamento.atendimento.pagamentos.remove(pagamento)

        self.__tela_pagamento.mostrar_mensagem("Pagamento removido com sucesso.")

    def abrir_tela(self) -> None:
        while True:
            opcao = self.__tela_pagamento.mostrar_menu()

            if opcao == "Incluir Pagamento":
                self.incluir_pagamento()
            elif opcao == "Alterar Pagamento":
                self.alterar_pagamento()
            elif opcao == "Excluir Pagamento":
                self.excluir_pagamento()
            elif opcao == "Listar Pagamentos":
                self.listar_pagamentos()
            elif opcao == "Voltar":
                break

    def voltar(self) -> None:
        return
