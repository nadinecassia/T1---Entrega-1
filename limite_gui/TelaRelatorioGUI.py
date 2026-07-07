import FreeSimpleGUI as sg
from limite_gui.AbstractTelaGUI import AbstractTelaGUI

class TelaRelatorioGUI(AbstractTelaGUI):
    def __init__(self, controlador):
        super().__init__()
        self.__controlador = controlador

    def mostrar_menu(self) -> int:
        layout = [
            [sg.Text('Relatórios Estatísticos', font=("Arial", 18, "bold"), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Button('Clínicas com Maior Número de Atendimentos', key=1, size=(45, 2))],
            [sg.Button('Atendimentos Mais Caros e Mais Baratos', key=2, size=(45, 2))],
            [sg.Button('Procedimentos Mais Realizados (Populares)', key=3, size=(45, 2))],
            [sg.Button('Procedimentos Mais Caros e Mais Baratos', key=4, size=(45, 2))],
            [sg.Button('Voltar', key=0, size=(45, 1))]
        ]

        window = sg.Window('Sistema - Relatórios', layout, size=(500, 380), element_justification="center")
        
        button, values = window.read()
        window.close()

        if button is None:
            return 0
            
        return button

    def mostrar_msg(self, msg: str):
        self.mostrar_mensagem(msg)

    def exibir_clinicas_mais_atendidas(self, lista_clinicas: list):
        texto = "=== RELATÓRIO: CLÍNICAS COM MAIOR NÚMERO DE ATENDIMENTOS ===\n\n"
        for posicao, item in enumerate(lista_clinicas, start=1):
            texto += f"{posicao}º Lugar: {item['nome']} | Cidade: {item['cidade']} -> Total: {item['qtd_atendimentos']} atendimentos\n"

        sg.popup_scrolled(texto, title="Relatório de Clínicas", size=(60, 15), font=("Helvetica", 11))

    def exibir_atendimentos_extremos(self, mais_caro: dict, mais_barato: dict):
        texto = "=========== RELATÓRIO: EXTREMOS DE ATENDIMENTOS ===========\n\n"
        if mais_caro:
            texto += "ATENDIMENTO MAIS CARO:\n"
            texto += f" -> Paciente: {mais_caro['paciente']} | Data: {mais_caro['data']}\n"
            texto += f" -> Tipo: {mais_caro['tipo']} | Valor Total Real: R$ {mais_caro['valor_total']:.2f}\n\n"
        else:
            texto += "Nenhum atendimento mais caro registrado.\n\n"
            
        texto += "-" * 60 + "\n\n"
        
        if mais_barato:
            texto += "ATENDIMENTO MAIS BARATO:\n"
            texto += f" -> Paciente: {mais_barato['paciente']} | Data: {mais_barato['data']}\n"
            texto += f" -> Tipo: {mais_barato['tipo']} | Valor Total Real: R$ {mais_barato['valor_total']:.2f}\n"
        else:
            texto += "Nenhum atendimento mais barato registrado.\n"
            
        sg.popup_scrolled(texto, title="Atendimentos Extremos", size=(60, 15), font=("Helvetica", 11))

    def exibir_procedimentos_populares(self, lista_procedimentos: list):
        texto = "========= RELATÓRIO: PROCEDIMENTOS MAIS REALIZADOS =========\n\n"
        for posicao, item in enumerate(lista_procedimentos, start=1):
            texto += f"{posicao}º Lugar: '{item['descricao']}' -> Realizado {item['qtd']} vezes\n"
            
        sg.popup_scrolled(texto, title="Procedimentos Populares", size=(60, 15), font=("Helvetica", 11))

    def exibir_procedimentos_extremos(self, mais_caro: dict, mais_barato: dict):
        texto = "=========== RELATÓRIO: EXTREMOS DE PROCEDIMENTOS ===========\n\n"
        if mais_caro:
            texto += f"PROCEDIMENTO MAIS CARO: '{mais_caro['descricao']}' -> Custo: R$ {mais_caro['custo']:.2f}\n\n"
        else:
            texto += "Nenhum procedimento mais caro registrado.\n\n"
            
        texto += "-" * 60 + "\n\n"
        
        if mais_barato:
            texto += f"PROCEDIMENTO MAIS BARATO: '{mais_barato['descricao']}' -> Custo: R$ {mais_barato['custo']:.2f}\n"
        else:
            texto += "Nenhum procedimento mais barato registrado.\n"

        sg.popup_scrolled(texto, title="Procedimentos Extremos", size=(60, 15), font=("Helvetica", 11))