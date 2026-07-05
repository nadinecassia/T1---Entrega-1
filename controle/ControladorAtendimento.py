from entidade.atendimento import Atendimento
from limite.TelaAtendimento import TelaAtendimento
from datetime import date
from dao.AtendimentoDAO import AtendimentoDAO

class ControladorAtendimento:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__atendimento_dao = AtendimentoDAO()
        self.__tela_atendimento = TelaAtendimento(self)

    @property
    def atendimentos(self):
        return self.__atendimento_dao.get_all()
    
    def atualizar_atendimento_dao(self, atendimento):
        self.__atendimento_dao.update(atendimento)
    
    def iniciar(self):
        self.abrir_tela()

    def incluir_atendimento(self):
        nome_clinica = self.__tela_atendimento.le_texto_obrigatorio("Digite o nome exato da clínica: ")
        clinica = self.__controlador_principal.controlador_clinica.pegar_clinica_por_nome(nome_clinica)
        if not clinica:
            self.__tela_atendimento.mostrar_msg("ERRO: Clínica não cadastrada no sistema!")
            return

        paciente = self.__controlador_principal.controlador_paciente.selecionar_paciente_para_atendimento()
        if not paciente:
            self.__tela_atendimento.mostrar_msg("ERRO: É necessário selecionar um paciente válido!")
            return

        profissional = self.__controlador_principal.controlador_profissional.selecionar_profissional_para_atendimento()
        if not profissional:
            self.__tela_atendimento.mostrar_msg("ERRO: É necessário selecionar um profissional válido!")
            return

        nome_tipo = self.__tela_atendimento.le_texto_obrigatorio("Digite o nome do Tipo de Atendimento: ")
        tipo_atendimento = self.__controlador_principal.controlador_tipo_atendimento.pegar_tipo_por_nome(nome_tipo)
        if not tipo_atendimento:
            self.__tela_atendimento.mostrar_msg("ERRO: Tipo de atendimento não cadastrado!")
            return

        dados_tela = self.__tela_atendimento.pegar_dados()

        if paciente.calcular_idade() < 18:
            self.__tela_atendimento.mostrar_msg(f"O paciente {paciente.nome} tem {paciente.calcular_idade()} anos. Somente maiores de 18 anos podem realizar atendimentos de forma independente!")
            return

        if not clinica.esta_aberta(dados_tela["horario_inicio"], dados_tela["horario_fim"]):
            self.__tela_atendimento.mostrar_msg(f"REJEITADO: Horário fora do funcionamento da clínica!")
            return

        novo_atendimento = Atendimento(
            data=dados_tela["data"],
            horario_inicio=dados_tela["horario_inicio"],
            horario_fim=dados_tela["horario_fim"],
            tipo_atendimento=tipo_atendimento,
            valor=dados_tela["valor"],
            clinica=clinica,
            paciente=paciente,
            profissional=profissional,
        )

        self.__atendimento_dao.add(novo_atendimento)
        self.__tela_atendimento.mostrar_msg("Atendimento agendado com sucesso!")

    def alterar_atendimento(self):
        dados_busca = self.__tela_atendimento.selecionar()
        atendimento = self.__atendimento_dao.get(dados_busca["cpf_paciente"], dados_busca["data"])

        if atendimento is None:
            self.__tela_atendimento.mostrar_msg("ERRO: Atendimento não localizado.")
            return

        novos_dados = self.__tela_atendimento.pegar_dados()

        self.__atendimento_dao.remove(atendimento.paciente.cpf, atendimento.data)

        atendimento.data = novos_dados["data"]
        atendimento.horario_inicio = novos_dados["horario_inicio"]
        atendimento.horario_fim = novos_dados["horario_fim"]
        atendimento.valor = novos_dados["valor"]

        self.__atendimento_dao.add(atendimento)
        self.__tela_atendimento.mostrar_msg("Atendimento alterado com sucesso!")

    def registrar_procedimento_em_atendimento(self):
        dados_busca = self.__tela_atendimento.selecionar()
        atendimento = self.__atendimento_dao.get(dados_busca["cpf_paciente"], dados_busca["data"])

        if atendimento is None:
            self.__tela_atendimento.mostrar_msg("ERRO: Atendimento não localizado!")
            return

        procedimento = self.__controlador_principal.controlador_procedimento.selecionar_procedimento_para_atendimento()
        if procedimento is None:
            return

        atendimento.add_procedimento(procedimento)
        self.__atendimento_dao.update(atendimento)
        self.__tela_atendimento.mostrar_msg(f"Procedimento '{procedimento.descricao}' adicionado!")

    def listar_atendimentos(self):
        atendimentos = self.__atendimento_dao.get_all()
        if not atendimentos:
            self.__tela_atendimento.mostrar_msg("Nenhum atendimento agendado!")
            return

        for a in atendimentos:
            dados = {
                "clinica_nome": a.clinica.nome,
                "clinica_cidade": a.clinica.cidade,
                "paciente_nome": a.paciente.nome,
                "paciente_cpf": a.paciente.cpf,
                "profissional_nome": a.profissional.nome,
                "profissional_registro": a.profissional.registro_profissional,
                "data": a.data,
                "horario_inicio": a.horario_inicio,
                "horario_fim": a.horario_fim,
                "tipo_atendimento": a.tipo_atendimento.nome,
                "valor": a.valor,
                "custo_procedimentos": a.calcular_custo_total_procedimentos(),
                "valor_restante": a.calcular_valor_restante(),
                "procedimentos": [{"descricao": p.descricao, "custo": p.custo} for p in a.procedimentos],
            }
            self.__tela_atendimento.mostrar_atendimento(dados)

    def excluir_atendimento(self):
        dados_busca = self.__tela_atendimento.selecionar()
        atendimento = self.__atendimento_dao.get(dados_busca["cpf_paciente"], dados_busca["data"])

        if atendimento is not None:
            self.__atendimento_dao.remove(atendimento.paciente.cpf, atendimento.data)
            self.__tela_atendimento.mostrar_msg("Atendimento cancelado com sucesso!")
        else:
            self.__tela_atendimento.mostrar_msg("ERRO: Atendimento não localizado.")

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_atendimento,
            2: self.alterar_atendimento,
            3: self.excluir_atendimento,
            4: self.listar_atendimentos,
            5: self.registrar_procedimento_em_atendimento,
            0: self.voltar,
        }
        while True:
            op = self.__tela_atendimento.mostrar_menu()
            if op in lista_opcoes:
                lista_opcoes[op]()
            if op == 0: break

    def voltar(self):
        return
