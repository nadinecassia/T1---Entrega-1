import FreeSimpleGUI as sg
from limite_gui.AbstractTelaGUI import AbstractTelaGUI

class TelaTipoAtendimentoGUI(AbstractTelaGUI):
    def __init__(self, controlador):
        super().__init__()
        self.__controlador = controlador

    def mostrar_menu(self) -> int:
        layout = [
            [sg.Text('Tipos de Atendimento', font=("Arial", 18, "bold"), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Button('Incluir Tipo', size=(30, 2))],
            [sg.Button('Alterar Tipo', size=(30, 2))],
            [sg.Button('Excluir Tipo', size=(30, 2))],
            [sg.Button('Listar Tipos', size=(30, 2))],
            [sg.Button('Voltar', size=(30, 1))]
        ]

        window = sg.Window('Sistema - Tipos de Atendimento', layout, size=(400, 380), element_justification="center")
        
        evento, valores = window.read()

        window.close()

        if evento in (sg.WIN_CLOSED, "Voltar"):
            return "Voltar"
            
        return evento

    def pegar_dados(self) -> dict:
        layout = [
            [sg.Text('Dados do Tipo de Atendimento', font=("Arial", 15, "bold"))],
            [sg.Text('Nome:', size=(10, 1)), sg.InputText(key='nome')],
            [sg.Text('Descrição:', size=(10, 1)), sg.InputText(key='descricao')],
            [sg.Button('Confirmar', key='Confirmar'), sg.Button('Cancelar', key='Cancelar')]
        ]
        
        window = sg.Window('Cadastrar / Alterar Tipo', layout)
        
        while True:
            button, values = window.read()
            
            if button in (None, 'Cancelar'):
                window.close()
                return None

            nome = self.validar_texto(values['nome'])
            descricao = self.validar_texto(values['descricao'])

            if nome and descricao:
                window.close()
                return {"nome": nome, "descricao": descricao}
    
    def tabela_tipos(self, tipos, selecionar=False):
        # A chave no DAO é o código (int)
        dados = [[t.codigo, t.nome, t.descricao] for t in tipos]
        
        layout = [
            [sg.Table(values=dados,
                      headings=["Código", "Nome", "Descrição"],
                      key="tabela", auto_size_columns=True, justification="left",
                      expand_x=True, expand_y=True, enable_events=True,
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE)]
        ]

        if selecionar:
            layout.append([sg.Button("Selecionar"), sg.Button("Cancelar")])
        else:
            layout.append([sg.Button("Fechar")])

        window = sg.Window("Tipos de Atendimento Cadastrados", layout, size=(600, 400))
        
        while True:
            evento, valores = window.read()
            if evento in (sg.WIN_CLOSED, "Fechar", "Cancelar"):
                window.close()
                return None
            if evento == "Selecionar":
                if not valores["tabela"]:
                    self.mostrar_mensagem("Selecione um tipo.")
                    continue
                indice = valores["tabela"][0]
                window.close()
                return tipos[indice].codigo
