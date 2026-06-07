from limite.AbstractTela import AbstractTela


class TelaPrincipal(AbstractTela):
    def __init__(self, controlador):
        super().__init__(controlador)
    
    def mostrar_menu(self) -> int:
        print("\n======== SISTEMA DE ATENDIMENTO DE CLÍNICAS ========")
        print("1 - Gerenciar clínicas")
        print("2 - Gerenciar pacientes")
        print("3 - Gerenciar profissionais")
        print("4 - Gerenciar tipos de atendimento")
        print("5 - Gerenciar procedimentos")
        print("6 - Gerenciar atendimentos")
        print("7 - Gerenciar pagamentos")
        print("8 - Relatórios")
        print("0 - Encerrar sistema")

        opcao = self.le_num_inteiro(
            "Escolha a opção: ",
            [1, 2, 3, 4, 5, 6, 7, 8, 0]
        )

        return opcao