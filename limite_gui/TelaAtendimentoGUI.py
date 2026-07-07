import FreeSimpleGUI as sg
from limite_gui.AbstractTelaGUI import AbstractTelaGUI

class TelaAtendimentoGUI(AbstractTelaGUI):
    def __init__(self, controlador):
        super().__init__()
        self.__controlador = controlador

    def mostrar_menu(self) -> int | str:
        layout = [
            [sg.Text('Controle de Atendimentos', font=("Arial", 18, "bold"), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Button('Incluir Atendimento', size=(25, 2))],
            [sg.Button('Alterar Atendimento', size=(25, 2))],
            [sg.Button('Excluir Atendimento', size=(25, 2))],
            [sg.Button('Listar Atendimentos', size=(25, 2))],
            [sg.Button('Registrar Procedimento', size=(25, 2))],
            [sg.Button('Voltar', key=0, size=(25, 1))]
        ]

        window = sg.Window('Sistema - Atendimentos', layout, size=(500, 480), element_justification="center")
        
        button, values = window.read()
        window.close()

        if button is None or button == 0:
            return 0
            
        return button

    def pegar_dados(self) -> dict:
        layout = [
            [sg.Text('Dados do Atendimento', font=("Arial", 18, "bold"), justification="center", expand_x=True)],
            [sg.Text('Data (DD/MM/AAAA):', size=(20, 1)), sg.InputText(key='data')],
            [sg.Text('Hora Início (HH:MM):', size=(20, 1)), sg.InputText(key='hora_inicio')],
            [sg.Text('Hora Fim (HH:MM):', size=(20, 1)), sg.InputText(key='hora_fim')],
            [sg.Text('Valor (R$):', size=(20, 1)), sg.InputText(key='valor')],
            [sg.Button('Confirmar', key='Confirmar'), sg.Button('Cancelar', key='Cancelar')]
        ]
        
        window = sg.Window('Cadastrar / Alterar Atendimento', layout)
        
        while True:
            button, values = window.read()
            
            if button in (None, 'Cancelar'):
                window.close()
                return None

            data = self.validar_data(values['data'])
            hora_inicio = self.validar_horario(values['hora_inicio'])
            hora_fim = self.validar_horario(values['hora_fim'])
            valor = self.validar_valor(values['valor'])

            if data and hora_inicio and hora_fim and (valor is not None):
                window.close()
                return {
                    "data": data,
                    "hora_inicio": hora_inicio,
                    "hora_fim": hora_fim,
                    "valor": valor
                }
    
    def tabela_atendimentos(self, atendimentos, selecionar=False):
        dados = [[a.data.strftime("%d/%m/%Y"), a.paciente.nome, a.paciente.cpf, a.clinica.nome, a.tipo_atendimento.nome] for a in atendimentos]

        layout = [
            [sg.Table(values=dados,
                      headings=["Data", "Paciente", "CPF", "Clínica", "Tipo"],
                      key="tabela", auto_size_columns=True, justification="left",
                      expand_x=True, expand_y=True, enable_events=True,
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE)]
        ]

        if selecionar:
            layout.append([sg.Button("Selecionar"), sg.Button("Cancelar")])
        else:
            layout.append([sg.Button("Fechar")])

        window = sg.Window("Atendimentos Agendados", layout, size=(800, 400))
        
        while True:
            evento, valores = window.read()
            if evento in (sg.WIN_CLOSED, "Fechar", "Cancelar"):
                window.close()
                return None
            if evento == "Selecionar":
                if not valores["tabela"]:
                    self.mostrar_mensagem("Selecione um atendimento.")
                    continue
                indice = valores["tabela"][0]
                window.close()
                return (atendimentos[indice].paciente.cpf, atendimentos[indice].data)

    def mostrar_atendimento(self, dados_atendimento: dict):
        procs = dados_atendimento.get('procedimentos', [])
        texto_procs = ", ".join([p.descricao for p in procs]) if procs else "Nenhum"

        mensagem = (
            f"DATA: {dados_atendimento['data'].strftime('%d/%m/%Y')}\n"
            f"HORÁRIO: {dados_atendimento['hora_inicio'].strftime('%H:%M')} às {dados_atendimento['hora_fim'].strftime('%H:%M')}\n"
            f"PACIENTE: {dados_atendimento['paciente_nome']} (CPF: {dados_atendimento['paciente_cpf']})\n"
            f"CLÍNICA: {dados_atendimento['clinica_nome']}\n"
            f"PROFISSIONAL: {dados_atendimento['profissional_nome']}\n"
            f"TIPO: {dados_atendimento['tipo_atendimento_nome']}\n"
            f"VALOR: R$ {dados_atendimento['valor']:.2f}\n"
            f"PROCEDIMENTOS: {texto_procs}"
        )
        sg.popup(mensagem, title="Detalhes do Atendimento")

    def mostrar_msg(self, msg: str):
        self.mostrar_mensagem(msg)
