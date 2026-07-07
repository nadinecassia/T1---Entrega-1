import FreeSimpleGUI as sg
from limite_gui.AbstractTelaGUI import AbstractTelaGUI


class TelaPacienteGUI(AbstractTelaGUI):
    def __init__(self, controlador):
        super().__init__()
        self.__controlador = controlador
        
    def mostrar_menu(self):
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

        window = sg.Window(
            "Pacientes",
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
        [sg.Text("Data de Nascimento"), sg.Input(default_text=data_padrao, key="data")],
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
            
    def tabela_pacientes(self, pacientes, selecionar=False):

        dados = []

        for paciente in pacientes:
            dados.append([
                paciente.nome,
                paciente.cpf,
                paciente.celular,
                paciente.data_nascimento.strftime("%d/%m/%Y"),
                paciente.calcular_idade()
            ])

        layout = [
            [
                sg.Table(
                    values=dados,
                    headings=[
                        "Nome",
                        "CPF",
                        "Celular",
                        "Nascimento",
                        "Idade"
                    ],
                    key="tabela",
                    auto_size_columns=True,
                    justification="left",
                    expand_x=True,
                    expand_y=True,
                    enable_events=True,
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE
                )
            ]
        ]

        if selecionar:
            layout.append([
                sg.Button("Selecionar"),
                sg.Button("Cancelar")
            ])
        else:
            layout.append([
                sg.Button("Fechar")
            ])

        window = sg.Window(
            "Pacientes",
            layout,
            size=(900, 400)
        )

        while True:

            evento, valores = window.read()

            if evento in (sg.WIN_CLOSED, "Fechar", "Cancelar"):
                window.close()
                return None

            if evento == "Selecionar":

                if len(valores["tabela"]) == 0:
                    self.mostrar_mensagem("Selecione um paciente.")
                    continue

                indice = valores["tabela"][0]

                window.close()

                return pacientes[indice].cpf
