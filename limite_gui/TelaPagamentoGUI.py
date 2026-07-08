import FreeSimpleGUI as sg
from limite_gui.AbstractTelaGUI import AbstractTelaGUI


class TelaPagamentoGUI(AbstractTelaGUI):
    def __init__(self, controlador):
        super().__init__()
        self.__controlador = controlador
        
    def mostrar_menu(self):
        layout = [
            [sg.Text(
                "Gerenciamento de Pagamentos",
                font = ("Arial", 18, "bold"),
                justification = "center",
                expand_x = True
            )],
            [sg.HorizontalSeparator()],
            [sg.Button("Incluir Pagamento", size = (25, 2))],
            [sg.Button("Alterar Pagamento", size = (25, 2))],
            [sg.Button("Excluir Pagamento", size = (25, 2))],
            [sg.Button("Listar Pagamentos", size = (25, 2))],
        
            [sg.Push(), sg.Button("Voltar", size = (10,1))]
        ]

        window = sg.Window(
            "Pagamentos",
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
            data_padrao = ""
            valor_pago_padrao = ""
            modalidade_padrao = ""
        
        else:
            data_padrao = dados_antigos["data"].strftime("%d/%m/%Y")
            valor_pago_padrao = str(dados_antigos["valor_pago"])
            modalidade_padrao = dados_antigos["modalidade"]

        layout = [
          [sg.Text("Data do Pagamento"), sg.Input(default_text=data_padrao, key="data")],
        [sg.Text("Valor a ser Pago:"), sg.Input(default_text=valor_pago_padrao, key="valor_pago")],
        [sg.Text("Modo de Pagamento"), sg.Combo(['Dinheiro', 'PIX', 'Cartão de Crédito'],default_value=modalidade_padrao, key="modalidade", readonly=True)],
        [sg.Button("Salvar"), sg.Button("Cancelar")]  
        ]

        window = sg.Window("Cadastrar Pagamento", layout)

        while True:
            evento, valores = window.read()

            if evento in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
            
            if evento == "Salvar":
                data_validada = self.validar_data(valores["data"])
                if data_validada is None:
                    continue
                
                valor_validado = self.validar_valor(valores["valor_pago"])
                if valor_validado is None:
                    continue

                modalidade = valores["modalidade"]
                if not modalidade:
                    self.mostrar_mensagem("Selecione uma modalidade de pagamento.")
                    continue


                window.close()

                return {
                    "data": data_validada,
                    "valor_pago": valor_validado,
                    "modalidade": modalidade,
                }

    def pegar_dados_pix(self):
        layout = [
            [sg.Text("CPF do pagador:"), sg.Input(key="cpf_pagador")],
            [sg.Button("Salvar"), sg.Button("Cancelar")]
        ]
        window = sg.Window("Dados do PIX", layout)

        while True:
            evento, valores = window.read()
            if evento in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
            
            if evento == "Salvar":
                cpf_validado = self.validar_cpf(valores["cpf_pagador"])
                if cpf_validado is None:
                    continue
                window.close()
                return{"cpf_pagador": cpf_validado}
    
    def pegar_dados_cartao(self):
        layout = [
            [sg.Text("Número do Cartão:"), sg.Input(key="numero_cartao")],
            [sg.Text("Bandeira:"), sg.Input(key="bandeira")],
            [sg.Button("Salvar"), sg.Button("Cancelar")]
        ]
        window = sg.Window("Dados do Cartão", layout)
        while True:
            evento, valores = window.read()
            if evento in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
                    
            if evento == "Salvar":
                
                numero = self.validar_texto(valores["numero_cartao"])
                if numero is None:
                    continue
                
                bandeira = self.validar_texto(valores["bandeira"])
                if bandeira is None:
                    continue

                window.close()
                return{"numero_cartao": numero, "bandeira": bandeira}


    def tabela_pagamentos(self, pagamentos, selecionar=False):

        dados = []

        for pagamento in pagamentos:
            dados.append([
                pagamento.codigo,
                pagamento.data.strftime("%d/%m/%Y"),
                f"{pagamento.valor_pago: .2f}",
                self.__controlador.identificar_modalidade(pagamento),
                pagamento.paciente.nome
            ])

        layout = [
            [
                sg.Table(
                    values=dados,
                    headings=[
                        "Número",
                        "Data",
                        "Valor (R$)",
                        "Modalidade",
                        "Paciente"
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
            "Pagamentos",
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
                    self.mostrar_mensagem("Selecione um pagamento.")
                    continue

                indice = valores["tabela"][0]

                window.close()

                return pagamentos[indice].codigo