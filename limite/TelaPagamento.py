from limite.AbstractTela import AbstractTela


class TelaPagamento(AbstractTela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostrar_menu(self) -> int:
        print("\n-------- PAGAMENTO --------")
        print("1 - Incluir pagamento")
        print("2 - Alterar pagamento")
        print("3 - Excluir pagamento")
        print("4 - Listar pagamentos")
        print("0 - Voltar")

        opcao = self.le_num_inteiro("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def mostrar_menu_modalidade(self) -> int:
        print("\n-------- MODO DE PAGAMENTO --------")
        print("1 - Dinheiro")
        print("2 - PIX")
        print("3 - Cartão de crédito")

        opcao = self.le_num_inteiro("Escolha a modalidade: ", [1, 2, 3])
        return opcao

    def pegar_dados(self) -> dict:
        print("\n-------- DADOS DO PAGAMENTO --------")
        data = self.le_data("Data do pagamento (DD/MM/YYYY): ")
        valor_pago = self.le_float("Valor pago: ")

        return {
            "data": data,
            "valor_pago": valor_pago,
        }

    def pegar_dados_pix(self) -> dict:
        print("\n-------- DADOS DO PIX --------")
        cpf_pagador = self.le_texto_obrigatorio("CPF do pagador: ")

        return {"cpf_pagador": cpf_pagador}

    def pegar_dados_cartao(self) -> dict:
        print("\n-------- DADOS DO CARTAO --------")
        numero_cartao = self.le_texto_obrigatorio("Número do cartão: ")
        bandeira = self.le_texto_obrigatorio("Bandeira: ")

        return {
            "numero_cartao": numero_cartao,
            "bandeira": bandeira,
        }

    def selecionar_atendimento(self) -> int:
        print("\n-------- SELECIONAR ATENDIMENTO --------")
        indice = self.le_num_inteiro("Digite numero do atendimento: ", None)
        return indice

    def selecionar_pagamento(self) -> int:
        print("\n-------- SELECIONAR PAGAMENTO --------")
        indice = self.le_num_inteiro("Digite número do pagamento: ", None)
        return indice

    def mostrar_pagamento(self, dados_pagamento: dict) -> None:
        print("\nPAGAMENTO")
        print("NÚMERO: ", dados_pagamento["indice"])
        print("MODO DE PAGAMENTO: ", dados_pagamento["modalidade"])
        print("DATA: ", dados_pagamento["data"].strftime("%d/%m/%Y"))
        print("VALOR PAGO: R$", dados_pagamento["valor_pago"])
        print("PACIENTE: ", dados_pagamento["paciente"])
        print("-" * 30)

    def mostrar_atendimento_resumo(self, dados_atendimento: dict) -> None:
        print("\nATENDIMENTO")
        print("NÚMERO: ", dados_atendimento["indice"])
        print("PACIENTE: ", dados_atendimento["paciente"])
        print("PROFISSIONAL: ", dados_atendimento["profissional"])
        print("CLÍNICA: ", dados_atendimento["clinica"])
        print("DATA: ", dados_atendimento["data"].strftime("%d/%m/%Y"))
        print(
            "HORÁRIO: ",
            dados_atendimento["horario_inicio"],
            "-",
            dados_atendimento["horario_fim"],
        )
        print("VALOR RESTANTE: R$", dados_atendimento["valor_restante"])
        print("-" * 30)
