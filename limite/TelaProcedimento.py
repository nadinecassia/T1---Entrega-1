from limite.AbstractTela import AbstractTela

class TelaProcedimento(AbstractTela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostrar_menu(self) -> int:
        print("\n-------- CADASTRO PROCEDIMENTOS --------")
        print("1 - Incluir Procedimento")
        print("2 - Alterar Procedimento")
        print("3 - Excluir Procedimento")
        print("4 - Listar Procedimentos")
        print("0 - Voltar")
        
        opcao = self.le_num_inteiro("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def pegar_dados(self) -> dict:
        print("\n-------- CADASTRAR / ALTERAR PROCEDIMENTO --------")
        descricao = self.le_texto_obrigatorio("Descrição do procedimento: ")
        custo = self.le_float("Custo do procedimento (R$): ")

        return {"descricao": descricao, "custo": custo}

    def mostrar_procedimento(self, dados_procedimento: dict):
        print("PROCEDIMENTO: ", dados_procedimento["descricao"])
        print("CUSTO: R$", f"{dados_procedimento['custo']:.2f}")
        print("PROFISSIONAL RESPONSÁVEL: ", dados_procedimento["profissional_nome"])
        print("-" * 30)

    def selecionar(self) -> str:
        print("\n-------- SELECIONAR PROCEDIMENTO --------")
        descricao = self.le_texto_obrigatorio("Digite a descrição exata do procedimento: ")
        return descricao

    def mostrar_msg(self, msg: str):
        print(msg)