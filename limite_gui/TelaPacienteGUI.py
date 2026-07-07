import FreeSimpleGUI as sg
from limite_gui.AbstractTelaGUI import AbstractTelaGUI


class TelaPacienteGUI(AbstractTelaGUI):
    def __init__(self):
        super().__init__()
        
        layout = [
            [sg.Text(
                "Gerenciamento de Pacientes",
                font = ("Arial", 18, "bold"),
                justification = "center",
                expand_x = True
            )],
        [sg.HorizontalSeparator()],
        [sg.Button("Incluir Paciente", size = (25, 2))],
        [sg.Button("Alterar Paciente", size = (25, 2))],
        [sg.Button("Excluir Paciente", size = (25, 2))],
        [sg.Button("Listar Pacientes", size = (25, 2))],
       
        [sg.Push(), sg.Button("Voltar", size = (10,1))]
        ]

        self.window = sg.Window(
            "Pacientes",
            layout,
            size=(500, 450),
            element_justification="center",
            finalize=True
        )
    
    def mostrar_menu(self):
        evento, valores = self.window.read()

        if evento == sg.WIN_CLOSED:
            return "Voltar"
        
        return evento
    
    def fechar(self):
        self.window.close()
    
    def abrir_janela_cadastro(self, dados_antigos = None):
        if dados_antigos is None:
            nome_padrao = ""
            cpf_padrao = ""
            celular_padrao = ""
            data_padrao = ""
        else:
            nome_padrao = dados_antigos["nome"]
            cpf_padrao = dados_antigos["cpf"]
            celular_padrao = dados_antigos["celular"]
            data_padrao = dados_antigos["data_nascimento"].strftime("%d/%m/%Y")

        layout = [
          [sg.Text("Nome"), sg.Input(default_text=nome_padrao, key="nome")],
        [sg.Text("CPF"), sg.Input(default_text=cpf_padrao, key="cpf")],
        [sg.Text("Celular"), sg.Input(default_text=celular_padrao, key="celular")],
        [sg.Text("Nascimento"), sg.Input(default_text=data_padrao, key="data")],
        [sg.Button("Salvar"), sg.Button("Cancelar")]  
        ]

        window = sg.Window("Cadastrar Paciente", layout)

        while True:
            evento, valores = window.read()

            if evento in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
            
            if evento == "Salvar":
                nome_validado = self.validar_texto(valores["nome"])
                if nome_validado is None:
                    continue
                
                cpf_validado = self.validar_cpf(valores["cpf"])
                if cpf_validado is None:
                    continue

                celular_validado = self.validar_celular(valores["celular"])
                if celular_validado is None:
                    continue

                data_validada = self.validar_data(valores["data"])
                if data_validada is None:
                    continue

                window.close()

                return {
                    "nome": nome_validado,
                    "cpf": cpf_validado,
                    "celular": celular_validado,
                    "data_nascimento": data_validada
                }

