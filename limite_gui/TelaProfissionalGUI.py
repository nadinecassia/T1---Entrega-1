import FreeSimpleGUI as sg
from limite_gui.AbstractTelaGUI import AbstractTelaGUI


class TelaProfissionalGUI(AbstractTelaGUI):
    def __init__(self, controlador):
        super().__init__()
        self.__controlador = controlador
        
    def mostrar_menu(self):
        layout = [
            [sg.Text(
                "Gerenciamento de Profissionais",
                font = ("Arial", 18, "bold"),
                justification = "center",
                expand_x = True
            )],
            [sg.HorizontalSeparator()],
            [sg.Button("Incluir Profissional", size = (25, 2))],
            [sg.Button("Alterar Profissional", size = (25, 2))],
            [sg.Button("Excluir Profissional", size = (25, 2))],
            [sg.Button("Listar Profissionais", size = (25, 2))],
        
            [sg.Push(), sg.Button("Voltar", size = (10,1))]
        ]

        window = sg.Window(
            "Profissionais",
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
            especialidade_padrao = ""
            registro_profissional_padrao = ""
        else:
            nome_padrao = dados_antigos["nome"]
            cpf_padrao = dados_antigos["cpf"]
            celular_padrao = dados_antigos["celular"]
            especialidade_padrao = dados_antigos["especialidade"]
            registro_profissional_padrao = dados_antigos["registro_profissional"]

        layout = [
          [sg.Text("Nome"), sg.Input(default_text=nome_padrao, key="nome")],
        [sg.Text("CPF"), sg.Input(default_text=cpf_padrao, key="cpf")],
        [sg.Text("Celular"), sg.Input(default_text=celular_padrao, key="celular")],
        [sg.Text("Especialidade"), sg.Input(default_text=especialidade_padrao, key="especialidade")],
        [sg.Text("Registro Profissional"), sg.Input(default_text=registro_profissional_padrao, key="registro_profissional")],
        [sg.Button("Salvar"), sg.Button("Cancelar")]  
        ]

        window = sg.Window("Cadastrar Profissional", layout)

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

                especialidade_validada = self.validar_texto(valores["especialidade"])
                if especialidade_validada is None:
                    continue

                registro_profissional_validado = self.validar_registro_profissional(valores["registro_profissional"])
                if registro_profissional_validado is None:
                    continue

                window.close()

                return {
                    "nome": nome_validado,
                    "cpf": cpf_validado,
                    "celular": celular_validado,
                    "especialidade": especialidade_validada,
                    "registro_profissional": registro_profissional_validado
                }
            
    def tabela_profissionais(self, profissionais, selecionar=False):

        dados = []

        for profissional in profissionais:
            dados.append([
                profissional.nome,
                profissional.cpf,
                profissional.celular,
                profissional.especialidade,
                profissional.registro_profissional
            ])

        layout = [
            [
                sg.Table(
                    values=dados,
                    headings=[
                        "Nome",
                        "CPF",
                        "Celular",
                        "Especialidade",
                        "Registro Profissional"
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
            "Profissionais",
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
                    self.mostrar_mensagem("Selecione um profissional.")
                    continue

                indice = valores["tabela"][0]

                window.close()

                return profissionais[indice].cpf