from entidade.TipoAtendimento import TipoAtendimento
from limite.TelaTipoAtendimento import TelaTipoAtendimento

class ControladorTipoAtendimento:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__tipos_atendimento = []
        self.__tela_tipo_atendimento = TelaTipoAtendimento(self)
    
    def iniciar(self):
        self.abrir_tela()

    def pegar_tipo_por_nome(self, nome: str):
        for tipo in self.__tipos_atendimento:
            if tipo.nome.lower() == nome.lower():
                return tipo
        return None
    
    def incluir_tipo(self):
        dados_tipo = self.__tela_tipo_atendimento.pegar_dados()
        tipo_existente = self.pegar_tipo_por_nome(dados_tipo["nome"])

        if tipo_existente is not None:
            self.__tela_tipo_atendimento.mostrar_msg("Tipo de atendimento já cadastrado")
            return
            
        novo_tipo = TipoAtendimento(
            dados_tipo["nome"],
            dados_tipo["descricao"],
        )

        self.__tipos_atendimento.append(novo_tipo)
        self.__tela_tipo_atendimento.mostrar_msg("Tipo de atendimento cadastrado com sucesso!")

    def alterar_tipo_atendimento(self) -> None:
        self.listar_tipos_atendimento()
        nome = self.__tela_tipo_atendimento.selecionar()
        tipo = self.pegar_tipo_por_nome(nome)

        if tipo is None:
            self.__tela_tipo_atendimento.mostrar_msg("Tipo de atendimento não encontrado.")
            return
        
        novos_dados = self.__tela_tipo_atendimento.pegar_dados()
        tipo.nome = novos_dados["nome"]
        tipo.descricao = novos_dados["descricao"]
        self.__tela_tipo_atendimento.mostrar_msg("Tipo de atendimento alterado com sucesso.")
    
    def excluir_tipo_atendimento(self) -> None:
        self.listar_tipos_atendimento()
        nome = self.__tela_tipo_atendimento.selecionar()
        tipo = self.pegar_tipo_por_nome(nome)

        if tipo is None:
            self.__tela_tipo_atendimento.mostrar_msg("Tipo de atendimento não encontrado.")
            return
        
        self.__tipos_atendimento.remove(tipo)
        self.__tela_tipo_atendimento.mostrar_msg("Tipo de atendimento excluído com sucesso.")
    
    def listar_tipos_atendimento(self) -> None:
        if len(self.__tipos_atendimento) == 0:
            self.__tela_tipo_atendimento.mostrar_msg("Nenhum tipo de atendimento cadastrado.")
            return
        
        for tipo in self.__tipos_atendimento:
            dados_tipo = {"nome": tipo.nome, "descricao": tipo.descricao}
            self.__tela_tipo_atendimento.mostrar_tipo_atendimento(dados_tipo)

    def abrir_tela(self) -> None:
        lista_opcoes = {
            1: self.incluir_tipo,
            2: self.alterar_tipo_atendimento,
            3: self.excluir_tipo_atendimento,
            4: self.listar_tipos_atendimento,
            0: self.voltar
        }

        while True:
            opcao_escolhida = self.__tela_tipo_atendimento.mostrar_menu()
            
            if opcao_escolhida == 0:
                break
                
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()
    
    def voltar(self) -> None:
        return