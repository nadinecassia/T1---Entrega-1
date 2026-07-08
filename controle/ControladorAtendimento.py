from entidade.atendimento import Atendimento
from limite_gui.TelaAtendimentoGUI import TelaAtendimentoGUI
from dao.AtendimentoDAO import AtendimentoDAO

class ControladorAtendimento:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__atendimento_dao = AtendimentoDAO()
        self.__tela_atendimento = TelaAtendimentoGUI(self)

    @property
    def atendimentos(self):
        return self.__atendimento_dao.get_all()
    
    def atualizar_atendimento_dao(self, atendimento):
        self.__atendimento_dao.update(atendimento)
    
    def iniciar(self):
        self.abrir_tela()

    def selecionar_atendimento(self):
        atendimentos = self.__atendimento_dao.get_all()

        if not atendimentos:
            self.__tela_atendimento.mostrar_mensagem("Nenhum atendimento cadastrado.")
            return None

        busca = self.__tela_atendimento.tabela_atendimentos(atendimentos, selecionar=True)

        if busca is None:
            return None

        cpf_busca, data_busca = busca
        atendimento = self.__atendimento_dao.get(cpf_busca, data_busca)

        if atendimento is None:
            self.__tela_atendimento.mostrar_mensagem("Erro: Atendimento não encontrado.")
            return None

        return atendimento

    def listar_atendimentos(self):
        atendimentos = self.__atendimento_dao.get_all()
        if not atendimentos:
            self.__tela_atendimento.mostrar_mensagem("Nenhum atendimento agendado!")
            return

        busca = self.__tela_atendimento.tabela_atendimentos(atendimentos, selecionar=True)

        if busca is None:
            return

        cpf_busca, data_busca = busca
        atendimento = self.__atendimento_dao.get(cpf_busca, data_busca)

        if atendimento is None:
            self.__tela_atendimento.mostrar_mensagem("Erro: Atendimento não localizado.")
            return

        dados_detalhados = {
            "clinica_nome": atendimento.clinica.nome,
            "clinica_cidade": atendimento.clinica.cidade,
            "paciente_nome": atendimento.paciente.nome,
            "paciente_cpf": atendimento.paciente.cpf,
            "profissional_nome": atendimento.profissional.nome,
            "profissional_registro": atendimento.profissional.registro_profissional,
            "data": atendimento.data,
            "horario_inicio": atendimento.horario_inicio,
            "horario_fim": atendimento.horario_fim,
            "tipo_atendimento_nome": atendimento.tipo_atendimento.nome,
            "valor": atendimento.valor,
            "custo_procedimentos": atendimento.calcular_custo_total_procedimentos(),
            "valor_restante": atendimento.valor + atendimento.calcular_custo_total_procedimentos(), 
            "procedimentos": [{"descricao": p.descricao, "custo": p.custo} for p in atendimento.procedimentos]
        }

        self.__tela_atendimento.mostrar_atendimento(dados_detalhados)

    def alterar_atendimento(self):
        atendimentos = self.__atendimento_dao.get_all()
        if not atendimentos:
            self.__tela_atendimento.mostrar_mensagem("Nenhum atendimento agendado.")
            return

        busca = self.__tela_atendimento.tabela_atendimentos(atendimentos, selecionar=True)
        if busca is None:
            return

        cpf_busca, data_busca = busca

        atendimento = self.__atendimento_dao.get(cpf_busca, data_busca)

        dados_atuais = {
            "data": atendimento.data,
            "hora_inicio": atendimento.horario_inicio,
            "hora_fim": atendimento.horario_fim,
            "valor": atendimento.valor
        }

        novos_dados = self.__tela_atendimento.abrir_janela_cadastro(dados_antigos=dados_atuais)

        if novos_dados is None: return

        self.__atendimento_dao.remove(atendimento.paciente.cpf, atendimento.data)

        atendimento.data = novos_dados["data"]
        atendimento.horario_inicio = novos_dados["hora_inicio"]
        atendimento.horario_fim = novos_dados["hora_fim"]
        atendimento.valor = novos_dados["valor"]

        self.__atendimento_dao.add(atendimento)
        self.__tela_atendimento.mostrar_mensagem("Atendimento alterado com sucesso!")

    def registrar_procedimento_em_atendimento(self):
        atendimentos = self.__atendimento_dao.get_all()
        if not atendimentos:
            self.__tela_atendimento.mostrar_mensagem("Nenhum atendimento agendado.")
            return

        busca = self.__tela_atendimento.tabela_atendimentos(atendimentos, selecionar=True)
        if busca is None:
            return

        cpf_busca, data_busca = busca

        atendimento = self.__atendimento_dao.get(cpf_busca, data_busca)

        if atendimento is None:
            self.__tela_atendimento.mostrar_mensagem("ERRO: Atendimento não localizado!")
            return

        procedimento = self.__controlador_principal.controlador_procedimento.selecionar_procedimento_para_atendimento()
        if procedimento is None:
            return

        atendimento.add_procedimento(procedimento)
        self.__atendimento_dao.update(atendimento)
        self.__tela_atendimento.mostrar_mensagem(f"Procedimento '{procedimento.descricao}' adicionado!")

    def excluir_atendimento(self):
        atendimentos = self.__atendimento_dao.get_all()
        if not atendimentos:
            self.__tela_atendimento.mostrar_mensagem("Nenhum atendimento agendado.")
            return

        busca = self.__tela_atendimento.tabela_atendimentos(atendimentos, selecionar=True)
        if busca is None:
            return

        cpf_busca, data_busca = busca
        self.__atendimento_dao.remove(cpf_busca, data_busca)
        self.__tela_atendimento.mostrar_mensagem("Atendimento excluído com sucesso!")

    def abrir_tela(self):
        while True:
            opcao = self.__tela_atendimento.mostrar_menu()
            
            if opcao == "Incluir Atendimento":
                self.incluir_atendimento()
            elif opcao == "Alterar Atendimento":
                self.alterar_atendimento()
            elif opcao == "Excluir Atendimento":
                self.excluir_atendimento()
            elif opcao == "Listar Atendimentos":
                self.listar_atendimentos()
            elif opcao == "Registrar Procedimento":
                self.registrar_procedimento_em_atendimento()
            elif opcao == "Voltar":
                break

    def voltar(self):
        return