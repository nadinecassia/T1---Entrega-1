import FreeSimpleGUI as sg
from limite_gui.AbstractTelaGUI import AbstractTelaGUI

class TelaClinicaGUI(AbstractTelaGUI):
    def __init__(self, controlador):
        super().__init__()
        self.__controlador = controlador

    def mostrar_menu(self) -> int:
        layout = [
            [sg.Text(
                'Cadastro de Clínicas',
                font = ("Arial", 18, "bold"),
                justification = "center",
                expand_x = True
                )],
            [sg.HorizontalSeparator()],
            [sg.Button('Incluir Clínica', size=(25, 2))],
            [sg.Button('Alterar Clínica', size=(25, 2))],
            [sg.Button('Excluir Clínica', size=(25, 2))],
            [sg.Button('Listar Clínicas', size=(25, 2))],
            [sg.Button('Voltar', key=0, size=(25, 1))]
        ]

        window = sg.Window(
            'Sistema de Clínicas',
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
            [sg.Text('Dados da Clínica', 
                     font = ("Arial", 18, "bold"),justification = "center",expand_x = True)],
            [sg.Text('Nome:'), sg.InputText(key='nome')],
            [sg.Text('Descrição:'), sg.InputText(key='descricao')],
            [sg.Text('Cidade:'), sg.InputText(key='cidade')],
            [sg.Text('Horário de abertura (HH:MM):'), sg.InputText(key='horario_aberto')],
            [sg.Text('Horário de fechamento (HH:MM):'), sg.InputText(key='horario_fechado')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        
        window = sg.Window('Cadastrar / Alterar Clínica', layout)
        
        while True:
            button, values = window.read()

            if button in (None, 'Cancelar'):
                window.close()
                return None

            nome = self.validar_texto(values['nome'])
            descricao = self.validar_texto(values['descricao'])
            cidade = self.validar_texto(values['cidade'])
            horario_aberto = self.validar_horario(values['horario_aberto'])
            horario_fechado = self.validar_horario(values['horario_fechado'])

            if nome and descricao and cidade and horario_aberto and horario_fechado:
                window.close()
                return {
                    "nome": nome,
                    "descricao": descricao,
                    "cidade": cidade,
                    "horario_aberto": horario_aberto,
                    "horario_fechado": horario_fechado,
                }

    def mostrar_clinica(self, dados_clinica: dict):
        mensagem = (
            f"NOME DA CLÍNICA: {dados_clinica['nome']}\n"
            f"DESCRIÇÃO: {dados_clinica['descricao']}\n"
            f"CIDADE: {dados_clinica['cidade']}\n"
            f"HORÁRIO DE ABERTURA: {dados_clinica['horario_aberto'].strftime('%H:%M')}\n"
            f"HORÁRIO DE FECHAMENTO: {dados_clinica['horario_fechado'].strftime('%H:%M')}"
        )
        sg.popup(mensagem, title="Detalhes da Clínica")

    def le_texto_obrigatorio(self, mensagem: str):
        while True:
            texto = sg.popup_get_text(mensagem, title="Entrada de Dados")

            if texto is None:
                return None
                
            texto_validado = self.validar_texto(texto)
            if texto_validado:
                return texto_validado

    def mostrar_msg(self, msg: str):
        self.mostrar_mensagem(msg)

    def selecionar(self):
        return self.le_texto_obrigatorio("Digite o nome exato da clínica que deseja selecionar: ")