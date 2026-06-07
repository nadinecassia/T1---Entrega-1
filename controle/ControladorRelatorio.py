from limite.TelaRelatorio import TelaRelatorio


class ControladorRelatorio:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__tela_relatorio = TelaRelatorio(self)

    def iniciar(self):
        self.abrir_tela()

    def clinicas_com_mais_atendimentos(self):
        lista_atendimentos = (
            self.__controlador_principal.controlador_atendimento.atendimentos
        )

        if len(lista_atendimentos) == 0:
            self.__tela_relatorio.mostrar_msg(
                "Não há atendimentos registrados para gerar estatísticas."
            )
            return

        contagem_clinicas = {}
        for atendimento in lista_atendimentos:
            clinica = atendimento.clinica
            if clinica in contagem_clinicas:
                contagem_clinicas[clinica] += 1
            else:
                contagem_clinicas[clinica] = 1

        dados_relatorio = []
        for clinica, qtd in contagem_clinicas.items():
            dados_relatorio.append({
                "nome": clinica.nome,
                "cidade": clinica.cidade,
                "qtd_atendimentos": qtd
            })

        dados_relatorio.sort(key=lambda x: x["qtd_atendimentos"], reverse=True)
        self.__tela_relatorio.exibir_clinicas_mais_atendidas(dados_relatorio)

    def atendimentos_mais_caros_e_mais_baratos(self):
        lista_atendimentos = self.__controlador_principal.controlador_atendimento.atendimentos

        if len(lista_atendimentos) == 0:
            self.__tela_relatorio.mostrar_msg("Não há atendimentos registrados para gerar estatísticas.")
            return

        atendimento_mais_caro = None
        atendimento_mais_barato = None

        for atendimento in lista_atendimentos:
            valor_total = atendimento.valor + atendimento.calcular_custo_total_procedimentos()

            if atendimento_mais_caro is None or valor_total > (atendimento_mais_caro.valor + atendimento_mais_caro.calcular_custo_total_procedimentos()):
                atendimento_mais_caro = atendimento

            if atendimento_mais_barato is None or valor_total < (atendimento_mais_barato.valor + atendimento_mais_barato.calcular_custo_total_procedimentos()):
                atendimento_mais_barato = atendimento

        dados_caro = {
            "paciente": atendimento_mais_caro.paciente.nome,
            "data": atendimento_mais_caro.data.strftime("%d/%m/%Y"),
            "tipo": atendimento_mais_caro.tipo_atendimento.nome,
            "valor_total": atendimento_mais_caro.valor + atendimento_mais_caro.calcular_custo_total_procedimentos()
        }

        dados_barato = {
            "paciente": atendimento_mais_barato.paciente.nome,
            "data": atendimento_mais_barato.data.strftime("%d/%m/%Y"),
            "tipo": atendimento_mais_barato.tipo_atendimento.nome,
            "valor_total": atendimento_mais_barato.valor + atendimento_mais_barato.calcular_custo_total_procedimentos()
        }

        self.__tela_relatorio.exibir_atendimentos_extremos(dados_caro, dados_barato)

    def procedimentos_mais_realizados(self):
        lista_atendimentos = (
            self.__controlador_principal.controlador_atendimento.atendimentos
        )

        if len(lista_atendimentos) == 0:
            self.__tela_relatorio.mostrar_msg(
                "Não há atendimentos com procedimentos para gerar relatórios."
            )
            return

        contagem_procedimentos = {}
        for atendimento in lista_atendimentos:
            for proc in atendimento.procedimentos:
                if proc.descricao in contagem_procedimentos:
                    contagem_procedimentos[proc.descricao] += 1
                else:
                    contagem_procedimentos[proc.descricao] = 1

        if len(contagem_procedimentos) == 0:
            self.__tela_relatorio.mostrar_msg(
                "Nenhum procedimento foi realizado nos atendimentos até agora."
            )
            return

        dados_relatorio = [
            {"descricao": desc, "qtd": qtd}
            for desc, qtd in contagem_procedimentos.items()
        ]
        dados_relatorio.sort(key=lambda x: x["qtd"], reverse=True)

        self.__tela_relatorio.exibir_procedimentos_populares(dados_relatorio)

    def procedimentos_mais_caros_e_mais_baratos(self):
        lista_procedimentos = (
            self.__controlador_principal.controlador_procedimento.procedimentos
        )

        if len(lista_procedimentos) == 0:
            self.__tela_relatorio.mostrar_msg(
                "Não há procedimentos cadastrados no sistema."
            )
            return

        proc_mais_caro = None
        proc_mais_barato = None

        for proc in lista_procedimentos:
            if proc_mais_caro is None or proc.custo > proc_mais_caro.custo:
                proc_mais_caro = proc

            if proc_mais_barato is None or proc.custo < proc_mais_barato.custo:
                proc_mais_barato = proc

        dados_caro = {
            "descricao": proc_mais_caro.descricao,
            "custo": proc_mais_caro.custo
        }
        dados_barato = {
            "descricao": proc_mais_barato.descricao,
            "custo": proc_mais_barato.custo
        }

        self.__tela_relatorio.exibir_procedimentos_extremos(
            dados_caro, dados_barato
        )

    def abrir_tela(self):
        lista_opcoes = {
            1: self.clinicas_com_mais_atendimentos,
            2: self.atendimentos_mais_caros_e_mais_baratos,
            3: self.procedimentos_mais_realizados,
            4: self.procedimentos_mais_caros_e_mais_baratos,
            0: self.voltar
        }

        while True:
            opcao_escolhida = self.__tela_relatorio.mostrar_menu()
            if opcao_escolhida in lista_opcoes:
                funcao_escolhida = lista_opcoes[opcao_escolhida]
                funcao_escolhida()
            if opcao_escolhida == 0:
                break

    def voltar(self):
        return