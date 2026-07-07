from entidade.TipoAtendimento import TipoAtendimento
from limite_gui.TelaTipoAtendimentoGUI import TelaTipoAtendimentoGUI
from dao.TipoAtendimentoDAO import TipoAtendimentoDAO


class ControladorTipoAtendimento:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__tipo_atendimento_dao = TipoAtendimentoDAO()
        self.__tela_tipo_atendimento = TelaTipoAtendimentoGUI(self)
    
    def iniciar(self):
        self.abrir_tela()
    
    def __gerar_codigo(self) -> int:
        tipos_atendimento = self.__tipo_atendimento_dao.get_all()

        if len(tipos_atendimento) == 0:
            return 1
        
        maior_codigo = 0
        for tipo_atendimento in tipos_atendimento:
            if tipo_atendimento.codigo > maior_codigo:
                maior_codigo = tipo_atendimento.codigo
        
        return maior_codigo + 1

    def pegar_tipo_por_nome(self, nome: str):
        for tipo in self.__tipo_atendimento_dao.get_all():
            if tipo.nome.lower() == nome.lower():
                return tipo
        return None
    
    def incluir_tipo(self):
        dados_tipo = self.__tela_tipo_atendimento.pegar_dados()

        if dados_tipo is None:
            return

        tipo_existente = self.pegar_tipo_por_nome(dados_tipo["nome"])

        if tipo_existente is not None:
            self.__tela_tipo_atendimento.mostrar_msg("Tipo de atendimento já cadastrado")
            return
            
        codigo = self.__gerar_codigo()
        novo_tipo = TipoAtendimento(
            codigo,
            dados_tipo["nome"],
            dados_tipo["descricao"],
        )

        self.__tipo_atendimento_dao.add(novo_tipo)
        self.__tela_tipo_atendimento.mostrar_msg("Tipo de atendimento cadastrado com sucesso!")

    def alterar_tipo_atendimento(self) -> None:
        tipos = self.__tipo_atendimento_dao.get_all()
        if not tipos:
            self.__tela_tipo_atendimento.mostrar_mensagem("Nenhum tipo cadastrado.")
            return

        codigo_busca = self.__tela_tipo_atendimento.tabela_tipos(tipos, selecionar=True)
        if codigo_busca is None:
            return
        
        tipo = self.__tipo_atendimento_dao.get(codigo_busca)
        
        novos_dados = self.__tela_tipo_atendimento.pegar_dados()
        if novos_dados is None:
            return
            
        tipo.nome = novos_dados["nome"]
        tipo.descricao = novos_dados["descricao"]
        
        self.__tipo_atendimento_dao.update(tipo)
        self.__tela_tipo_atendimento.mostrar_mensagem("Tipo de atendimento alterado!")
    
    def excluir_tipo_atendimento(self) -> None:
        tipos = self.__tipo_atendimento_dao.get_all()
        if not tipos:
            self.__tela_tipo_atendimento.mostrar_mensagem("Nenhum tipo cadastrado.")
            return

        codigo_busca = self.__tela_tipo_atendimento.tabela_tipos(tipos, selecionar=True)
        if codigo_busca is None:
            return
        
        self.__tipo_atendimento_dao.remove(codigo_busca)
        self.__tela_tipo_atendimento.mostrar_mensagem("Tipo de atendimento excluído!")
    
    def listar_tipos_atendimento(self) -> None:
        tipos = self.__tipo_atendimento_dao.get_all()
        if not tipos:
            self.__tela_tipo_atendimento.mostrar_mensagem("Nenhum tipo cadastrado.")
            return

        self.__tela_tipo_atendimento.tabela_tipos(tipos, selecionar=False)

    def abrir_tela(self) -> None:
        while True:
            opcao = self.__tela_tipo_atendimento.mostrar_menu()
            if opcao == "Incluir Tipo":
                self.incluir_tipo()
            
            elif opcao == "Alterar Tipo":
                self.alterar_tipo_atendimento()
            
            elif opcao == "Excluir Tipo":
                self.excluir_tipo_atendimento()

            elif opcao == "Listar Tipos":
                self.listar_tipos_atendimento()
            
            elif opcao == "Voltar":
                break
    
    def voltar(self) -> None:
        return