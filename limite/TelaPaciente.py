from limite.AbstractTela import AbstractTela


class TelaPaciente(AbstractTela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostrar_menu(self) -> int:
        print("\n-------- PACIENTES --------")
        print("1 - Incluir paciente")
        print("2 - Alterar paciente")
        print("3 - Excluir paciente")
        print("4 - Listar pacientes")
        print("0 - Voltar")

        opcao = self.le_num_inteiro("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def pegar_dados(self) -> dict:
        print("\n-------- DADOS DO PACIENTE --------")
        nome = self.le_texto_obrigatorio("Nome: ")
        cpf = self.le_texto_obrigatorio("CPF: ")
        celular = self.le_texto_obrigatorio("Celular: ")
        data_nascimento = self.le_data("Data de nascimento (DD/MM/YYYY): ")

        return {"nome": nome, "cpf": cpf, "celular": celular, "data_nascimento": data_nascimento}

    def mostrar_paciente(self, dados_paciente: dict):
        print("PACIENTE: ", dados_paciente["nome"])
        print("CPF: ", dados_paciente["cpf"])
        print("CELULAR: ", dados_paciente["celular"])
        print("DATA DE NASCIMENTO: ", dados_paciente["data_nascimento"].strftime("%d/%m/%Y"))
        print("IDADE: ", dados_paciente["idade"])
            
        print("-" * 30)

    def selecionar(self) -> str:
        print("\n-------- SELECIONAR PACIENTE --------")
        cpf = self.le_texto_obrigatorio("Digite o cpf do paciente: ")
        return cpf
    
    def mostrar_msg(self, msg: str):
        print(msg)
