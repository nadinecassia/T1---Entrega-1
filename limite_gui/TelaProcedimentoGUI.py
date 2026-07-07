import FreeSimpleGUI as sg
from limite_gui.AbstractTelaGUI import AbstractTelaGUI

class TelaProcedimentoGUI(AbstractTelaGUI):
    def __init__(self, controlador):
        super().__init__()
        self.__controlador = controlador

    def mostrar_menu(self) -> int:
        layout = [
            [sg.Text('Cadastro de Procedimentos', font=("Arial", 18, "bold"), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Button('Incluir Procedimento', size=(25, 2))],
            [sg.Button('Alterar Procedimento', size=(25, 2))],
            [sg.Button('Excluir Procedimento', size=(25, 2))],
            [sg.Button('Listar Procedimentos', size=(25, 2))],
            [sg.Button('Voltar', key=0, size=(25, 1))]
        ]

        window = sg.Window(
            'Sistema de Procedimentos',
            layout,
            size=(500, 450),
            element_justification="center",
            finalize=True
        )
        
        button, values = window.read()
        window.close()

        if button is None or button == 0:
            return 0
            
        return button

    def pegar_dados(self) -> dict:
        layout = [
            [sg.Text(
                'Dados do Procedimento',
                font = ("Arial", 18, "bold"),justification = "center",
                expand_x = True)],
            [sg.Text('Descrição:'), sg.InputText(key='descricao')],
            [sg.Text('Custo (R$):'), sg.InputText(key='custo')],
            [sg.Button('Confirmar', key='Confirmar'), sg.Button('Cancelar', key='Cancelar')]
        ]
        
        window = sg.Window('Cadastrar / Alterar Procedimento', layout)
        
        while True:
            button, values = window.read()
            
            if button in (None, 'Cancelar'):
                window.close()
                return None

            descricao = self.validar_texto(values['descricao'])
            custo = self.validar_valor(values['custo'])
            
            if descricao and custo is not None:
                window.close()
                return {"descricao": descricao, "custo": custo}

    def tabela_procedimentos(self, procedimentos, selecionar=False):
        dados = [[p.descricao, f"R$ {p.custo:.2f}", p.profissional.nome] for p in procedimentos]

        layout = [
            [sg.Table(values=dados,
                      headings=["Descrição", "Custo", "Profissional"],
                      key="tabela", auto_size_columns=True, justification="left",
                      expand_x=True, expand_y=True, enable_events=True,
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE)]
        ]

        if selecionar:
            layout.append([sg.Button("Selecionar"), sg.Button("Cancelar")])
        else:
            layout.append([sg.Button("Fechar")])

        window = sg.Window("Procedimentos Cadastrados", layout, size=(700, 400))
        
        while True:
            evento, valores = window.read()
            if evento in (sg.WIN_CLOSED, "Fechar", "Cancelar"):
                window.close()
                return None
            if evento == "Selecionar":
                if not valores["tabela"]:
                    self.mostrar_mensagem("Selecione um procedimento.")
                    continue
                indice = valores["tabela"][0]
                window.close()
                return procedimentos[indice].descricao

    def mostrar_procedimento(self, dados_procedimento: dict):
        mensagem = (
            f"PROCEDIMENTO: {dados_procedimento['descricao']}\n"
            f"CUSTO: R$ {dados_procedimento['custo']:.2f}\n"
            f"PROFISSIONAL RESP.: {dados_procedimento.get('profissional_nome', 'Não informado')}"
        )
        sg.popup(mensagem, title="Detalhes do Procedimento")

    def mostrar_msg(self, msg: str):
        self.mostrar_mensagem(msg)
