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
            [sg.Button('Incluir Tipo', key=1, size=(30, 2))],
            [sg.Button('Alterar Tipo', key=2, size=(30, 2))],
            [sg.Button('Excluir Tipo', key=3, size=(30, 2))],
            [sg.Button('Listar Tipos', key=4, size=(30, 2))],
            [sg.Button('Voltar', key=0, size=(30, 1))]
        ]

        window = sg.Window('Sistema - Tipos de Atendimento', layout, size=(400, 380), element_justification="center")
        
        button, values = window.read()
        window.close()

        if button is None:
            return 0
            
        return button

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

    def mostrar_tipo_atendimento(self, dados_tipo: dict):
        mensagem = (
            f"NOME: {dados_tipo['nome']}\n"
            f"DESCRIÇÃO: {dados_tipo['descricao']}"
        )
        sg.popup(mensagem, title="Detalhes do Tipo")

    def selecionar(self) -> str:
        while True:
            texto = sg.popup_get_text("Digite o nome exato do tipo de atendimento:", title="Selecionar Tipo")
            if texto is None:
                return None
            
            texto_validado = self.validar_texto(texto)
            if texto_validado:
                return texto_validado

    def mostrar_msg(self, msg: str):
        self.mostrar_mensagem(msg)