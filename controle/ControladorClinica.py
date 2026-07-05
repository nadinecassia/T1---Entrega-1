from entidade.clinica import Clinica
from limite.TelaClinica import TelaClinica
from dao.ClinicaDAO import ClinicaDAO


class ControladorClinica:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__clinica_dao = ClinicaDAO()
        self.__tela_clinica = TelaClinica(self)

    def iniciar(self):
        self.abrir_tela()

    def pegar_clinica_por_nome(self, nome: str) -> Clinica | None:
        return self.__clinica_dao.get(nome)

    def incluir_clinica(self):
        dados_clinica = self.__tela_clinica.pegar_dados()

        if self.__clinica_dao.get(dados_clinica["nome"]) is not None:
            self.__tela_clinica.mostrar_msg("ERRO: Já existe uma clínica com esse nome!")
            return

        nova_clinica = Clinica(
            dados_clinica["nome"],
            dados_clinica["descricao"],
            dados_clinica["cidade"],
            dados_clinica["horario_aberto"],
            dados_clinica["horario_fechado"],
        )

        self.__clinica_dao.add(nova_clinica)
        self.__tela_clinica.mostrar_msg("Clínica cadastrada com sucesso!")

    def alterar_clinica(self):
        nome_busca = self.__tela_clinica.le_texto_obrigatorio("Digite o nome exato da clínica que deseja alterar: ")

        clinica = self.__clinica_dao.get(nome_busca)
        
        if clinica is None:
            self.__tela_clinica.mostrar_msg("ERRO: Clínica não encontrada.")
            return

        self.__tela_clinica.mostrar_msg("Informe os novos dados da clínica:")
        dados_novos = self.__tela_clinica.pegar_dados()

        if dados_novos["nome"] != nome_busca:
            self.__clinica_dao.remove(nome_busca)

        clinica.nome = dados_novos["nome"]
        clinica.descricao = dados_novos["descricao"]
        clinica.cidade = dados_novos["cidade"]
        clinica.horario_aberto = dados_novos["horario_aberto"]
        clinica.horario_fechado = dados_novos["horario_fechado"]

        self.__clinica_dao.add(clinica)
        
        self.__tela_clinica.mostrar_msg("Clínica alterada com sucesso!")

    def excluir_clinica(self):
        nome = self.__tela_clinica.le_texto_obrigatorio("Digite o nome da clínica que deseja excluir: ")

        clinica = self.__clinica_dao.get(nome)
        
        if clinica is not None:
            self.__clinica_dao.remove(nome)
            self.__tela_clinica.mostrar_msg("Clínica excluída com sucesso!")
        else:
            self.__tela_clinica.mostrar_msg("ERRO: Não existe uma clínica com esse nome!")

    def listar_clinicas(self):
        clinicas = self.__clinica_dao.get_all()
        if len(clinicas) == 0:
            self.__tela_clinica.mostrar_msg("Nenhuma clínica cadastrada até o momento!")
            return

        for clinica in clinicas:
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