from limite.AbstractTela import AbstractTela

class TelaAtendimento(AbstractTela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostrar_menu(self) -> int:
        print("\n-------- GERENCIAMENTO DE ATENDIMENTOS --------")
        print("1 - Agendar Atendimento (Consulta/Exame)")
        print("2 - Alterar Dados do Atendimento")
        print("3 - Excluir Atendimento")
        print("4 - Listar Atendimentos Agendados")
        print("5 - Registrar Procedimento em um Atendimento")
        print("0 - Voltar")
        
        opcao = self.le_num_inteiro("Escolha a opção: ", [1, 2, 3, 4, 5, 6, 0])
        return opcao

    def pegar_dados(self) -> dict:
        print("\n-------- AGENDAMENTO DE ATENDIMENTO --------")
        

        data_valida = self.le_data("Digite a data do atendimento (DD/MM/AAAA): ")
        horario_inicio = self.le_horario("Digite o horário de início (HH:MM): ")

        while True:
            horario_fim = self.le_horario("Digite o horário de término (HH:MM): ")
            if horario_fim > horario_inicio:
                break
            print("O horário de término deve ser após o horário de início!")

        tipo_atendimento = self.le_texto_obrigatorio("Tipo de atendimento (Consulta, Exame, Retorno, etc.): ")
        valor = self.le_float("Valor base do atendimento (R$): ")

        return {
            "data": data_valida,
            "horario_inicio": horario_inicio,
            "horario_fim": horario_fim,
            "tipo_atendimento": tipo_atendimento,
            "valor": valor
        }

    def mostrar_atendimento(self, dados: dict):
        print("\n================ ATENDIMENTO ================")
        print(f"CLÍNICA: {dados['clinica_nome']} ({dados['clinica_cidade']})")
        print(f"PACIENTE: {dados['paciente_nome']} | CPF: {dados['paciente_cpf']}")
        print(f"PROFISSIONAL: {dados['profissional_nome']} | Registro: {dados['profissional_registro']}")
        print(f"DATA: {dados['data'].strftime('%d/%m/%Y')} | HORÁRIO: {dados['horario_inicio'].strftime('%H:%M')} até {dados['horario_fim'].strftime('%H:%M')}")
        print(f"TIPO: {dados['tipo_atendimento']} | VALOR BASE: R$ {dados['valor']:.2f}")
        print(f"CUSTO DOS PROCEDIMENTOS: R$ {dados['custo_procedimentos']:.2f}")
        print(f"VALOR RESTANTE A PAGAR: R$ {dados['valor_restante']:.2f}")
        print("-" * 45)
        if dados['procedimentos']:
            print("Procedimentos realizados:")
            for p in dados['procedimentos']:
                print(f" -> {p['descricao']} (R$ {p['custo']:.2f})")
        print("=============================================")

    def selecionar(self) -> dict:
        print("\n-------- SELECIONAR ATENDIMENTO --------")
        print("Para localizar o atendimento, informe os dados chave:")
        cpf_paciente = self.le_texto_obrigatorio("CPF do Paciente: ")
        data_valida = self.le_data("Data do atendimento (DD/MM/AAAA): ")
        
        return {"cpf_paciente": cpf_paciente, "data": data_valida}

    def mostrar_msg(self, msg: str):
        print(msg)