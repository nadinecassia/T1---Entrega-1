from limite.AbstractTela import AbstractTela

class TelaRelatorio(AbstractTela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostrar_menu(self) -> int:
        print("\n-------- SISTEMA DE RELATÓRIOS ESTATÍSTICOS --------")
        print("1 - Clínicas com Maior Número de Atendimentos")
        print("2 - Atendimentos Mais Caros e Mais Baratos")
        print("3 - Procedimentos Mais Realizados (Populares)")
        print("4 - Procedimentos Mais Caros e Mais Baratos")
        print("0 - Voltar")
        
        opcao = self.le_num_inteiro("Escolha o relatório: ", [1, 2, 3, 4, 0])
        return opcao

    def mostrar_msg(self, msg: str):
        print(msg)

    def exibir_clinicas_mais_atendidas(self, lista_clinicas: list):
        print("\n=== RELATÓRIO: CLÍNICAS COM MAIOR NÚMERO DE ATENDIMENTOS ===")
        for posicao, item in enumerate(lista_clinicas, start=1):
            print(f"{posicao}º Lugar: {item['nome']} | Cidade: {item['cidade']} -> Total: {item['qtd_atendimentos']} atendimentos")
        print("============================================================")

    def exibir_atendimentos_extremos(self, mais_caro: dict, mais_barato: dict):
        print("\n=========== RELATÓRIO: EXTREMOS DE ATENDIMENTOS ===========")
        if mais_caro:
            print(f"ATENDIMENTO MAIS CARO:")
            print(f" -> Paciente: {mais_caro['paciente']} | Data: {mais_caro['data']}")
            print(f" -> Tipo: {mais_caro['tipo']} | Valor Total Real: R$ {mais_caro['valor_total']:.2f}")
        else:
            print("Nenhum atendimento mais caro registrado.")
        print("-" * 60)
        if mais_barato:
            print(f"ATENDIMENTO MAIS BARATO:")
            print(f" -> Paciente: {mais_barato['paciente']} | Data: {mais_barato['data']}")
            print(f" -> Tipo: {mais_barato['tipo']} | Valor Total Real: R$ {mais_barato['valor_total']:.2f}")
        else:
            print("Nenhum atendimento mais barato registrado.")
        print("===========================================================")

    def exibir_procedimentos_populares(self, lista_procedimentos: list):
        print("\n========= RELATÓRIO: PROCEDIMENTOS MAIS REALIZADOS =========")
        for posicao, item in enumerate(lista_procedimentos, start=1):
            print(f"{posicao}º Lugar: '{item['descricao']}' -> Realizado {item['qtd']} vezes")
        print("============================================================")

    def exibir_procedimentos_extremos(self, mais_caro: dict, mais_barato: dict):
        print("\n=========== RELATÓRIO: EXTREMOS DE PROCEDIMENTOS ===========")
        if mais_caro:
            print(f"PROCEDIMENTO MAIS CARO: '{mais_caro['descricao']}' -> Custo: R$ {mais_caro['custo']:.2f}")
        else:
            print("Nenhum procedimento mais caro registrado.")
        print("-" * 60)
        if mais_barato:
            print(f"PROCEDIMENTO MAIS BARATO: '{mais_barato['descricao']}' -> Custo: R$ {mais_barato['custo']:.2f}")
        else:
            print("Nenhum procedimento mais barato registrado.")
        print("===========================================================")