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
            [sg.Button('Voltar', size=(25, 1))]
        ]

        window = sg.Window(
            'Sistema de Clínicas',
            layout,
            size=(500, 450),
            element_justification="center",
            finalize=True
        )
        
        evento, valores = window.read()

        window.close()

        if evento in (sg.WIN_CLOSED, "Voltar"):
            return "Voltar"
            
        return evento

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

    def tabela_clinicas(self, clinicas, selecionar=False):
        # Transforma a lista de objetos Clinica em uma lista de listas para a tabela
        dados = []
        for c in clinicas:
            dados.append([c.nome, c.descricao, c.cidade, 
                          c.horario_aberto.strftime("%H:%M"), 
                          c.horario_fechado.strftime("%H:%M")])

        layout = [
            [sg.Table(values=dados,
                      headings=["Nome", "Descrição", "Cidade", "Abertura", "Fechamento"],
                      key="tabela",
                      auto_size_columns=True,
                      justification="left",
                      expand_x=True,
                      expand_y=True,
                      enable_events=True,
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE)]
        ]

        if selecionar:
            layout.append([sg.Button("Selecionar"), sg.Button("Cancelar")])
        else:
            layout.append([sg.Button("Fechar")])

        window = sg.Window("Clínicas Cadastradas", layout, size=(700, 400))

        while True:
            evento, valores = window.read()
            if evento in (sg.WIN_CLOSED, "Fechar", "Cancelar"):
                window.close()
                return None

            if evento == "Selecionar":
                if len(valores["tabela"]) == 0:
                    self.mostrar_mensagem("Selecione uma clínica.")
                    continue
                
                indice = valores["tabela"][0]
                window.close()
                return clinicas[indice].nome

