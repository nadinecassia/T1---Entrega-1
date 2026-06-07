from entidade.clinica import Clinica
from limite.TelaClinica import TelaClinica


class ControladorClinica:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__clinicas = []
        self.__tela_clinica = TelaClinica(self)

    def iniciar(self):
        self.abrir_tela()

    def pegar_clinica_por_nome(self, nome: str):
        for clinica in self.__clinicas:
            if clinica.nome.lower() == nome.lower():
                return clinica
        return None

    def incluir_clinica(self):
        dados_clinica = self.__tela_clinica.pegar_dados()

        for clinica in self.__clinicas:
            if clinica.nome.lower() == dados_clinica["nome"].lower():
                self.__tela_clinica.mostrar_msg(
                    "Já existe uma clínica com esse nome!"
                )
                return

        nova_clinica = Clinica(
            dados_clinica["nome"],
            dados_clinica["descricao"],
            dados_clinica["cidade"],
            dados_clinica["horario_aberto"],
            dados_clinica["horario_fechado"],
        )

        self.__clinicas.append(nova_clinica)
        self.__tela_clinica.mostrar_msg("Clínica cadastrada com sucesso!")

    def alterar_clinica(self):
        nome_busca = self.__tela_clinica.selecionar()

        for clinica in self.__clinicas:
            if clinica.nome.lower() == nome_busca.lower():
                dados_clinica = self.__tela_clinica.pegar_dados()

                clinica.nome = dados_clinica["nome"]
                clinica.descricao = dados_clinica["descricao"]
                clinica.cidade = dados_clinica["cidade"]
                clinica.horario_aberto = dados_clinica["horario_aberto"]
                clinica.horario_fechado = dados_clinica["horario_fechado"]

                self.__tela_clinica.mostrar_msg(
                    "Clínica alterada com sucesso!"
                )
                return

        self.__tela_clinica.mostrar_msg(
            "ERRO: Não existe uma clínica com esse nome!"
        )

    def excluir_clinica(self):
        nome_busca = self.__tela_clinica.selecionar()

        for clinica in self.__clinicas:
            if clinica.nome.lower() == nome_busca.lower():
                self.__clinicas.remove(clinica)
                self.__tela_clinica.mostrar_msg(
                    "Clínica excluída com sucesso!"
                )
                return

        self.__tela_clinica.mostrar_msg(
            "ERRO: Não existe uma clínica com esse nome!"
        )

    def listar_clinicas(self):
        if len(self.__clinicas) == 0:
            self.__tela_clinica.mostrar_msg(
                "Nenhuma clínica cadastrada até o momento!"
            )
            return

        for clinica in self.__clinicas:
            dados = {
                "nome": clinica.nome,
                "descricao": clinica.descricao,
                "cidade": clinica.cidade,
                "horario_aberto": clinica.horario_aberto,
                "horario_fechado": clinica.horario_fechado
            }
            self.__tela_clinica.mostrar_clinica(dados)

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_clinica,
            2: self.alterar_clinica,
            3: self.excluir_clinica,
            4: self.listar_clinicas,
            0: self.voltar
        }

        while True:
            opcao_escolhida = self.__tela_clinica.mostrar_menu()
            if opcao_escolhida in lista_opcoes:
                funcao_escolhida = lista_opcoes[opcao_escolhida]
                funcao_escolhida()
            if opcao_escolhida == 0:
                break

    def voltar(self):
        return