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

        if button is None:
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

    def mostrar_procedimento(self, dados_procedimento: dict):
        mensagem = (
            f"PROCEDIMENTO: {dados_procedimento['descricao']}\n"
            f"CUSTO: R$ {dados_procedimento['custo']:.2f}\n"
            f"PROFISSIONAL RESP.: {dados_procedimento.get('profissional_nome', 'Não informado')}"
        )
        sg.popup(mensagem, title="Detalhes do Procedimento")

    def selecionar(self) -> str:
        while True:
            texto = sg.popup_get_text("Digite a descrição exata do procedimento:", title="Selecionar Procedimento")
            if texto is None:
                return None
            
            texto_validado = self.validar_texto(texto)
            if texto_validado:
                return texto_validado

    def mostrar_msg(self, msg: str):
        self.mostrar_mensagem(msg)

    def mostrar_lista(self, procedimentos):
        texto = "--- PROCEDIMENTOS DISPONÍVEIS ---\n\n"
        for p in procedimentos:
            texto += f"-> {p.descricao} (R$ {p.custo:.2f})\n"
        
        sg.popup_scrolled(texto, title="Lista de Procedimentos", size=(40, 10))

    def selecionar_procedimento(self):
        return self.selecionar()

    def selecionar_procedimento_para_remover(self, procedimentos):
        self.mostrar_lista(procedimentos)
        return self.selecionar()