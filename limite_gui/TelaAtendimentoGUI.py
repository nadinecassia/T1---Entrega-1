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
            [sg.Button('Voltar', size=(25, 1))]
        ]

        window = sg.Window(
            'Sistema de Atendimentos',
            layout, size=(500, 480), element_justification="center"
        )
        
        evento, valores = window.read()

        window.close()

        if evento in (sg.WIN_CLOSED, "Voltar"):
            return "Voltar"
            
        return evento
    
    def abrir_janela_cadastro(self, dados_antigos=None):
        data_p = dados_antigos["data"].strftime("%d/%m/%Y") if dados_antigos else ""
        h_inicio_p = dados_antigos["hora_inicio"].strftime("%H:%M") if dados_antigos else ""
        h_fim_p = dados_antigos["hora_fim"].strftime("%H:%M") if dados_antigos else ""
        valor_p = str(dados_antigos["valor"]) if dados_antigos else ""

        layout = [
            [sg.Text('Dados do Atendimento', font=("Arial", 18, "bold"), justification="center", expand_x=True)],
            [sg.Text('Data (DD/MM/AAAA):', size=(20, 1)), sg.InputText(default_text=data_p, key='data')],
            [sg.Text('Hora Início (HH:MM):', size=(20, 1)), sg.InputText(default_text=h_inicio_p, key='hora_inicio')],
            [sg.Text('Hora Fim (HH:MM):', size=(20, 1)), sg.InputText(default_text=h_fim_p, key='hora_fim')],
            [sg.Text('Valor (R$):', size=(20, 1)), sg.InputText(default_text=valor_p, key='valor')],
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
    
    def mostrar_atendimento(self, dados: dict):
        procs = dados.get('procedimentos', [])
        texto_procs = ""
        if procs:
            for p in procs:
                texto_procs += f" -> {p['descricao']} (R$ {p['custo']:.2f})\n"
        else:
            texto_procs = "Nenhum procedimento realizado.\n"

        mensagem = (
            f"DETALHES DO ATENDIMENTO\n\n"
            f"CLÍNICA: {dados['clinica_nome']} ({dados['clinica_cidade']})\n"
            f"PACIENTE: {dados['paciente_nome']} | CPF: {dados['paciente_cpf']}\n"
            f"PROFISSIONAL: {dados['profissional_nome']} | Registro: {dados['profissional_registro']}\n"
            f"DATA: {dados['data'].strftime('%d/%m/%Y')}\n"
            f"HORÁRIO: {dados['horario_inicio'].strftime('%H:%M')} até {dados['horario_fim'].strftime('%H:%M')}\n"
            f"TIPO: {dados['tipo_atendimento_nome']} | VALOR BASE: R$ {dados['valor']:.2f}\n"
            f"CUSTO DOS PROCEDIMENTOS: R$ {dados['custo_procedimentos']:.2f}\n"
            f"VALOR RESTANTE A PAGAR: R$ {dados['valor_restante']:.2f}\n\n"
            f"PROCEDIMENTOS\n"
            f"{texto_procs}"
        )

        sg.popup_scrolled(mensagem, title="Detalhes do Atendimento", size=(60, 15))