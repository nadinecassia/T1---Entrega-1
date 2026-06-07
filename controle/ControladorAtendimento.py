from entidade.atendimento import Atendimento
from limite.TelaAtendimento import TelaAtendimento
from datetime import date, datetime


class ControladorAtendimento:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__atendimentos = []
        self.__tela_atendimento = TelaAtendimento(self)

    @property
    def atendimentos(self):
        return self.__atendimentos

    def iniciar(self):
        self.abrir_tela()

    def incluir_atendimento(self):
        nome_clinica = self.__tela_atendimento.le_texto_obrigatorio(
            "Digite o nome exato da clínica: "
        )
        clinica = (
            self.__controlador_principal
            .controlador_clinica
            .pegar_clinica_por_nome(nome_clinica)
        )
        if not clinica:
            self.__tela_atendimento.mostrar_msg(
                "ERRO: Clínica não cadastrada no sistema!"
            )
            return

        paciente = (
            self.__controlador_principal
            .controlador_paciente
            .selecionar_paciente_para_atendimento()
        )
        if not paciente:
            self.__tela_atendimento.mostrar_msg(
                "ERRO: É necessário selecionar um paciente válido!"
            )
            return

        profissional = (
            self.__controlador_principal
            .controlador_profissional
            .selecionar_profissional_para_atendimento()
        )
        if not profissional:
            self.__tela_atendimento.mostrar_msg(
                "ERRO: É necessário selecionar um profissional válido!"
            )
            return

        nome_tipo = self.__tela_atendimento.le_texto_obrigatorio(
            "Digite o nome do Tipo de Atendimento: "
        )
        tipo_atendimento = (
            self.__controlador_principal
            .controlador_tipo_atendimento
            .pegar_tipo_por_nome(nome_tipo)
        )
        if not tipo_atendimento:
            self.__tela_atendimento.mostrar_msg(
                "ERRO: Tipo de atendimento não cadastrado!"
            )
            return

        dados_tela = self.__tela_atendimento.pegar_dados()

        if paciente.calcular_idade() < 18:
            self.__tela_atendimento.mostrar_msg(
                f"O paciente {paciente.nome} tem {paciente.calcular_idade()} anos. "
                "Somente maiores de 18 anos podem realizar atendimentos "
                "de forma independente!"
            )
            return

        if not clinica.esta_aberta(dados_tela["horario_inicio"],
                                   dados_tela["horario_fim"]):
            self.__tela_atendimento.mostrar_msg(
                f"REJEITADO: Horário fora do funcionamento desta clínica "
                f"({clinica.horario_aberto.strftime('%H:%M')} às "
                f"{clinica.horario_fechado.strftime('%H:%M')})!"
            )
            return

        novo_atendimento = Atendimento(
            data=dados_tela["data"],
            horario_inicio=dados_tela["horario_inicio"],
            horario_fim=dados_tela["horario_fim"],
            tipo_atendimento=tipo_atendimento,
            valor=dados_tela["valor"],
            clinica=clinica,
            paciente=paciente,
            profissional=profissional
        )

        self.__atendimentos.append(novo_atendimento)
        self.__tela_atendimento.mostrar_msg("Atendimento agendado com sucesso!")

    def alterar_atendimento(self):
        if len(self.__atendimentos) == 0:
            self.__tela_atendimento.mostrar_msg("Nenhum atendimento agendado para alterar!")
            return

        dados_busca = self.__tela_atendimento.selecionar()
        atendimento_encontrado = self.__busca_atendimento(
            dados_busca["cpf_paciente"], 
            dados_busca["data"]
        )

        self.__tela_atendimento.mostrar_msg(f"\n--- Digitandos novos dados para o atendimento de {atendimento_encontrado.paciente.nome} ---")
        novos_dados = self.__tela_atendimento.pegar_dados()

        clinica = atendimento_encontrado.clinica
        if not clinica.esta_aberta(novos_dados["horario_inicio"], novos_dados["horario_fim"]):
            self.__tela_atendimento.mostrar_msg(
                f"REJEITADO: Novo horário fora do funcionamento da clínica "
                f"({clinica.horario_aberto.strftime('%H:%M')} às {clinica.horario_fechado.strftime('%H:%M')})!"
            )
            return

        atendimento_encontrado.data = novos_dados["data"]
        atendimento_encontrado.horario_inicio = novos_dados["horario_inicio"]
        atendimento_encontrado.horario_fim = novos_dados["horario_fim"]
        atendimento_encontrado.valor = novos_dados["valor"]

        self.__tela_atendimento.mostrar_msg("Dados do atendimento alterados com sucesso!")

    def __busca_atendimento(self, cpf_paciente: str, data_proc: date):
        for atendimento in self.__atendimentos:
            if (atendimento.paciente.cpf == cpf_paciente and
                    atendimento.data == data_proc):
                return atendimento
        return None

    def registrar_procedimento_em_atendimento(self):
        if len(self.__atendimentos) == 0:
            self.__tela_atendimento.mostrar_msg(
                "Nenhum atendimento agendado para registrar procedimentos!"
            )
            return

        dados_busca = self.__tela_atendimento.selecionar()
        atendimento_encontrado = self.__busca_atendimento(
            dados_busca["cpf_paciente"], 
            dados_busca["data"]
        )

        if atendimento_encontrado is None:
            self.__tela_atendimento.mostrar_msg(
                "ERRO: Atendimento não localizado!"
            )
            return

        procedimento = (
            self.__controlador_principal
            .controlador_procedimento
            .selecionar_procedimento_para_atendimento()
        )
        if procedimento is None:
            self.__tela_atendimento.mostrar_msg(
                "ERRO: Nenhum procedimento válido foi selecionado!"
            )
            return

        atendimento_encontrado.add_procedimento(procedimento)
        self.__tela_atendimento.mostrar_msg(
            f"Procedimento '{procedimento.descricao}' adicionado!"
        )

    def registrar_pagamento_de_atendimento(self):
        if len(self.__atendimentos) == 0:
            self.__tela_atendimento.mostrar_msg(
                "Nenhum atendimento agendado para registrar pagamentos!"
            )
            return

        dados_busca = self.__tela_atendimento.selecionar()
        atendimento_encontrado = self.__busca_atendimento(
            dados_busca["cpf_paciente"], 
            dados_busca["data"]
        )
        
        if atendimento_encontrado is None:
            self.__tela_atendimento.mostrar_msg(
                "ERRO: Atendimento não localizado!"
            )
            return

        valor_restante = atendimento_encontrado.calcular_valor_restante()

        if valor_restante <= 0:
            self.__tela_atendimento.mostrar_msg(
                "Este atendimento já está totalmente quitado!"
            )
            return

        self.__tela_atendimento.mostrar_msg(f"Valor total restante: R$ {valor_restante:.2f}")

        pagamento = (
            self.__controlador_principal
            .controlador_pagamento
            .criar_pagamento_para_atendimento(
                atendimento_encontrado.paciente,
                valor_restante,
                atendimento_encontrado.data
            )
        )

        if pagamento is None:
            self.__tela_atendimento.mostrar_msg(
                "ERRO: Registro de pagamento cancelado!"
            )
            return

        atendimento_encontrado.add_pagamentos(pagamento)
        self.__tela_atendimento.mostrar_msg("Pagamento registrado!")

    def listar_atendimentos(self):
        if len(self.__atendimentos) == 0:
            self.__tela_atendimento.mostrar_msg(
                "Nenhum atendimento agendado até o momento!"
            )
            return

        for atendimento in self.__atendimentos:
            dados = {
                "clinica_nome": atendimento.clinica.nome,
                "clinica_cidade": atendimento.clinica.cidade,
                "paciente_nome": atendimento.paciente.nome,
                "paciente_cpf": atendimento.paciente.cpf,
                "profissional_nome": atendimento.profissional.nome,
                "profissional_registro": (
                    atendimento.profissional.registro_profissional
                ),
                "data": atendimento.data,
                "horario_inicio": atendimento.horario_inicio,
                "horario_fim": atendimento.horario_fim,
                "tipo_atendimento": atendimento.tipo_atendimento.nome,
                "valor": atendimento.valor,
                "custo_procedimentos": (
                    atendimento.calcular_custo_total_procedimentos()
                ),
                "valor_restante": atendimento.calcular_valor_restante(),
                "procedimentos": [
                    {"descricao": p.descricao, "custo": p.custo}
                    for p in atendimento.procedimentos
                ]
            }
            self.__tela_atendimento.mostrar_atendimento(dados)

    def excluir_atendimento(self):
        if len(self.__atendimentos) == 0:
            self.__tela_atendimento.mostrar_msg(
                "Nenhum atendimento cadastrado para excluir!"
            )
            return

        dados_busca = self.__tela_atendimento.selecionar()
        atendimento_encontrado = self.__busca_atendimento(
            dados_busca["cpf_paciente"], 
            dados_busca["data"]
        )

        if atendimento_encontrado is not None:
            self.__atendimentos.remove(atendimento_encontrado)
            self.__tela_atendimento.mostrar_msg(
                "Atendimento cancelado com sucesso!"
            )
        else:
            self.__tela_atendimento.mostrar_msg(
                "ERRO: Atendimento não localizado."
            )

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_atendimento,
            2: self.alterar_atendimento,
            3: self.excluir_atendimento,
            4: self.listar_atendimentos,
            5: self.registrar_procedimento_em_atendimento,
            6: self.registrar_pagamento_de_atendimento,
            0: self.voltar
        }

        while True:
            opcao_escolhida = self.__tela_atendimento.mostrar_menu()
            if opcao_escolhida in lista_opcoes:
                funcao_chosen = lista_opcoes[opcao_escolhida]
                funcao_chosen()
            if opcao_escolhida == 0:
                break

    def voltar(self):
        return