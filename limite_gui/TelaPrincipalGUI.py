import FreeSimpleGUI as sg
from limite_gui.AbstractTelaGUI import AbstractTelaGUI


class TelaPrincipalGUI(AbstractTelaGUI):
    def __init__(self):
        super().__init__()

        layout = [
            [sg.Text(
                "Sistema de Gerenciamento de Clínicas",
                font = ("Arial", 18, "bold"),
                justification = "center",
                expand_x = True
            )],
        [sg.HorizontalSeparator()],
        [sg.Button("Pacientes", size = (25, 2))],
        [sg.Button("Profissionais", size = (25, 2))],
        [sg.Button("Clínicas", size = (25, 2))],
        [sg.Button("Tipos de Atendimento", size = (25, 2))],
        [sg.Button("Procedimentos", size = (25, 2))],
        [sg.Button("Atendimentos", size = (25, 2))],
        [sg.Button("Pagamentos", size = (25, 2))],
        [sg.Button("Relatórios", size = (25, 2))],
       
        [sg.Push(), sg.Button("Sair", size = (10,1))]
        ]

        self.window = sg.Window(
            "Clínica",
            layout,
            element_justification="center",
            finalize=True
        )
    
    def mostrar_menu(self):
        evento, valores = self.window.read()
        if evento == sg.WIN_CLOSED:
            return "Sair"
        return evento
    
    
    def fechar(self):
        self.window.close()