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

    def incluir_atendimento(self):
        clinica = self.__controlador_principal.controlador_clinica.selecionar_clinica_por_tabela()
        if clinica is None: 
            return 

        paciente = self.__controlador_principal.controlador_paciente.selecionar_paciente_para_atendimento()
        if paciente is None:
            return

        profissional = self.__controlador_principal.controlador_profissional.selecionar_profissional_para_atendimento()
        if profissional is None:
            return

        tipo_atendimento = self.__controlador_principal.controlador_tipo_atendimento.selecionar_tipo_por_tabela()
        if tipo_atendimento is None:
            return

        dados_tela = self.__tela_atendimento.abrir_janela_cadastro()
        if dados_tela is None: 
            return

        if paciente.calcular_idade() < 18:
            self.__tela_atendimento.mostrar_mensagem(f"O paciente {paciente.nome} tem {paciente.calcular_idade()} anos. Somente maiores de 18 anos podem realizar atendimentos de forma independente!")
            return

        if not clinica.esta_aberta(dados_tela["hora_inicio"], dados_tela["hora_fim"]):
            self.__tela_atendimento.mostrar_mensagem(f"REJEITADO: Horário fora do funcionamento da clínica!")
            return

        novo_atendimento = Atendimento(
            data=dados_tela["data"],
            horario_inicio=dados_tela["hora_inicio"],
            horario_fim=dados_tela["hora_fim"],
            tipo_atendimento=tipo_atendimento,
            valor=dados_tela["valor"],
            clinica=clinica,
            paciente=paciente,
            profissional=profissional,
        )

        self.__atendimento_dao.add(novo_atendimento)
        self.__tela_atendimento.mostrar_mensagem("Atendimento agendado com sucesso!")

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

    def listar_atendimentos(self):
        atendimentos = self.__atendimento_dao.get_all()
        if not atendimentos:
            self.__tela_atendimento.mostrar_mensagem("Nenhum atendimento agendado!")
            return

        self.__tela_atendimento.tabela_atendimentos(atendimentos, selecionar=False)

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