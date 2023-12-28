# Realiza importações de todas as bibliotecas utilizadas no código
from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import emoji

janela = Tk()

class Funcao(): #Cria uma classe para as funções

    def conectarbd(self): # Cria uma função para conectar ao banco de dados
        self.conn = sqlite3.connect("listas.bd")
        self.cursor = self.conn.cursor(); print("Conectando ao Banco de Dados")

    def desconectarbd(self): # Cria uma função para desconectar ao banco de dados
        self.conn.close(); print ("Desconectando ao Banco de Dados")

    def criartabelas(self): # Cria uma função para criar o banco de dados se caso ele ainda não existir
        self.conectarbd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS listas (
                codigo INTEGER PRIMARY KEY,
                lista_compras CHAR(40) NOT NULL
            );
        """)
        self.conn.commit(); print("Criando Banco de Dados")
        self.desconectarbd()

    def variaveis(self): # Cria uma função para chamar as variaveis da pagina principal
        self.codigolista = self.entrada_codigolista.get()
        self.nomelista = self.entrada_nomelista.get()

    def variaveisCompra(self): # Cria uma função para chamar as variaveis da pagina de Compras
        self.codigolistaCompra = self.entrada_codigolistaCompra.get()
        self.nomeitemCompra = self.entrada_nomeitem.get()
        self.quantidadeCompra = self.entrada_quantidade.get()
        self.valorCompra = self.entrada_valor.get()
        self.concluidoCompra = self.entrada_concluido.get()

    def selecionarLista(self): # Cria uma função para selecionar as listas criadas na pagina principal
        self.listaCompra.delete(*self.listaCompra.get_children())
        self.conectarbd()
        lista = self.cursor.execute("""SELECT codigo, lista_compras FROM listas 
                ORDER BY lista_compras ASC;""")
        for i in lista:
            self.listaCompra.insert("", END, values=i)
        self.desconectarbd()

    def selecionarListaCompra(self): # Cria uma função para selecionar as listas criadas na pagina de Compras
        nome = self.entrada_nomelista.get()
        self.Compra.delete(*self.Compra.get_children())
        self.conectarbd()
        listaCompra = self.cursor.execute(f"SELECT codigoCompras, item, quantidade, valor, concluido, total FROM '{nome}' ORDER BY codigoCompras ASC")
        for i in listaCompra:
            self.Compra.insert("", END, values=i)
        self.desconectarbd()

    def Adicionar(self): # Cria uma função para adicionar uma lista na pagina principal e também cria uma tabela no banco de dados com o nome inserido pelo usuário
        self.variaveis()
        self.conectarbd()
        if self.nomelista:
            nome = self.entrada_nomelista.get()
            self.cursor.execute("INSERT INTO listas (lista_compras) VALUES(?)", (self.nomelista,))
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS "{nome}" (
                                codigoCompras INTEGER PRIMARY KEY,
                                codigo INTEGER,
                                item CHAR,
                                quantidade INT,
                                valor FLOAT,
                                concluido CHAR,
                                total FLOAT,
                                FOREIGN KEY (codigo) REFERENCES listas (codigo)
                                );
                            """); print(f"TABELA '{nome}' CRIADA")
            self.conn.commit()
            self.Limpar()
            messagebox.showinfo("Concluído", "Sua lista foi criada com sucesso")
        else:
            messagebox.showinfo("Erro!", "Insira os dados corretamente")

        self.desconectarbd()
        self.selecionarLista()    

    def AdicionarCompra(self): # Cria uma função para adicionar um item à lista de compras na página de Compras e também inclui esse item na tabela criada no banco de dados
        self.item = self.entrada_nomeitem.get()
        self.quantidade = self.entrada_quantidade.get()
        self.valor = self.entrada_valor.get()
        self.concluido = self.entrada_concluido.get()
        nome = self.entrada_nomelista.get()
        self.conectarbd()
        try:
            quantidade = int(self.quantidade)
            valor = float(self.valor)
            
            if self.item and quantidade and valor and self.concluido:
                total = quantidade * valor
                self.cursor.execute(f'INSERT INTO "{nome}" (item, quantidade, valor, concluido, total) VALUES(?, ?, ?, ?, ?)', (self.item, self.quantidade, self.valor, self.concluido, total))
                self.conn.commit()
                self.LimparCompras()
                self.selecionarListaCompra()
                self.desconectarbd() 
                messagebox.showinfo("Concluído", "Quantidade Cadastrada")
                
            else:
                messagebox.showinfo("Erro!", "Insira os dados corretamente")
        except ValueError:messagebox.showinfo("Erro!", "Insira valores válidos para quantidade e valor")

    def Apagar(self): # Cria uma função para apagar uma lista selecionada na pagina principal e também apaga essa tabela do banco de dados
        self.variaveis()
        self.conectarbd()

        if self.codigolista:
            nome = self.entrada_nomelista.get()
            self.cursor.execute(""" DELETE FROM listas WHERE codigo = ? """, (self.codigolista))
            self.conn.commit()
            self.cursor.execute(f""" DROP TABLE IF EXISTS '{nome}'"""); print(f"TABELA '{nome}' EXCLUIDA")
            self.Limpar()
            self.selecionarLista()
            messagebox.showinfo("Lista Deletada", "A Lista foi deletada com sucesso! ")
            
            self.desconectarbd()  
        else:
            messagebox.showinfo("Erro!", "Selecione uma lista")

    def ApagarCompra(self): # Cria uma função para apagar um item da lista de compras
        codigoCompra = self.entrada_codigolistaCompra.get()
        self.variaveisCompra()
        self.conectarbd()

        if self.codigolista:
            
            nome = self.entrada_nomelista.get()
            self.cursor.execute(f""" DELETE FROM '{nome}' WHERE codigoCompras = ? """, (codigoCompra,))
            self.conn.commit()
            self.LimparCompras()
            self.selecionarListaCompra()
            self.desconectarbd()  
        else:
            messagebox.showinfo("Erro!", "Selecione um Item")

    def Limpar(self): # Cria uma função para limpar as entradas da pagina principal
        self.entrada_codigolista.delete(0, END)
        self.entrada_nomelista.delete(0, END) 

    def LimparCompras(self): # Cria uma função para limpar as entradas da pagina de Compras
        self.entrada_codigolistaCompra.delete(0, END)
        self.entrada_nomeitem.delete(0, END)
        self.entrada_quantidade.delete(0, END)
        self.entrada_valor.delete(0, END)
        self.entrada_concluido.set("Selecione")

    def Alterar(self): # Cria uma função para fazer Alterações da lista criada na pagina principal - também altera o nome da tabela do banco de dados
        self.variaveis()
        self.conectarbd()

        if self.nomelista and self.codigolista:
            self.novatabela = str(simpledialog.askstring('Editar', 'Informe o nome da sua nova tabela'))
            
            if self.novatabela != "":
            
                self.cursor.execute(f"ALTER TABLE '{self.nomelista}' RENAME TO '{self.novatabela}'")
                self.cursor.execute(""" UPDATE listas SET lista_compras=? 
                            WHERE codigo=?""", (self.novatabela, self.codigolista))
                self.Limpar()
                messagebox.showinfo("Lista Editada", "A Lista foi editada com sucesso! ")
            else:
                messagebox.showinfo("Erro!", "Digite o nome da lista")
            
        else:
            messagebox.showinfo("Erro!", "Selecione uma lista")

        self.conn.commit()
        self.desconectarbd()
        self.selecionarLista()

    def AlterarCompra(self): # Cria uma função para fazer Alterações dos itens na pagina de Compras - també altera no banco de dados
        self.variaveisCompra()
        self.conectarbd()
        nome = self.entrada_nomelista.get()
        try:
            quantidade = int(self.quantidadeCompra)
            valor = float(self.valorCompra)

            if self.nomeitemCompra and quantidade and valor and self.concluidoCompra:
                total = quantidade * valor
                self.cursor.execute(f""" UPDATE '{nome}' SET item=?, quantidade=?, valor=?, concluido=?, total=?
                            WHERE codigoCompras = ?""", (self.nomeitemCompra, self.quantidadeCompra, self.valorCompra, self.concluidoCompra, total, self.codigolistaCompra))
           
                self.LimparCompras()
                messagebox.showinfo("Lista Editada", "A Lista foi editada com sucesso! ")
            
            else:
                messagebox.showinfo("Erro!", "Selecione uma lista")
        
        except ValueError:messagebox.showinfo("Erro!", "Insira valores válidos para quantidade e valor")
        
            


        self.conn.commit()
        self.desconectarbd()
        self.selecionarListaCompra()

    def duploClick(self, event): # Cria uma função para utilizar o duplo clique na pagina principal
        self.Limpar()
        self.listaCompra.selection()
        
        for n in self.listaCompra.selection():
            col1, col2 = self.listaCompra.item(n, 'values')
            self.entrada_codigolista.insert(END, col1)
            self.entrada_nomelista.insert(END, col2)

    def duploClickCompras(self, event): # Cria uma função para utilizar o duplo clique na pagina de Compras
        self.LimparCompras()
        self.Compra.selection()

        for n in self.Compra.selection():
            col1, col2, col3, col4, col5, col6 = self.Compra.item(n, 'values')
            self.entrada_codigolistaCompra.insert(END, col1)
            self.entrada_nomeitem.insert(END, col2)
            self.entrada_quantidade.insert(END, col3)
            self.entrada_valor.insert(END, col4)
            self.entrada_concluido.set(col5)

    def Editar(self): #Cria uma função e também uma página de Compras ao clicar em Editar Lista
        nome = self.entrada_nomelista.get() # Armazena o nome da lista selecionada
        self.paginaCompras = Toplevel() # Cria uma pagina
        self.paginaCompras.title(nome) # Insere o titulo com o nome da lista selecionada

        # Seta as configurações da pagina
        self.paginaCompras.resizable(False, True)
        self.paginaCompras.minsize(width=500, height=600)
        self.paginaCompras.maxsize(width=500, height=900)
        self.paginaCompras.configure(background="#4D4D4D")
        self.paginaCompras.grab_set()

        # Cria o bloco principal
        self.blocoCompras1 = Frame(self.paginaCompras, bg="#292929", highlightbackground="black", highlightthickness=3)
        self.blocoCompras1.place(relx=0.02, rely=0.02, relheight=0.45, relwidth=0.96)

        # Cria o Logotipo do bloco principal da página de compras
        self.logoCompra = Label(self.blocoCompras1, text="Shopping", bg="#292929", fg="white", font=('quicksand', 25, ))
        self.logoCompra.place(relx=0.25, rely=0.03)
        self.logoCompra2 = Label(self.blocoCompras1, text="List", bg="#292929", fg="white", font=('quicksand', 20, ))
        self.logoCompra2.place(relx=0.38, rely=0.2)
        self.emojiCompra = Label(self.blocoCompras1, bg="#292929",text=f"{emoji.emojize(":check_box_with_check:")}", font=('quicksand', 60, ))
        self.emojiCompra.place(relx=0.58, rely=0.0)

        # Cria as Entradas da página de compras
        self.codigolistaCompra = Label(self.blocoCompras1, text="Código da Lista", bg="#292929", fg="white", font=('quicksand', 10, ))
        self.codigolistaCompra.place(relx=0.07, rely=0.35)
        self.entrada_codigolistaCompra = Entry(self.blocoCompras1)
        self.entrada_codigolistaCompra.place(relx=0.07, rely=0.43, relwidth=0.24, relheight=0.1)
        self.nomeitem = Label(self.blocoCompras1, text="Item", bg="#292929", fg="white", font=('quicksand', 10, ))
        self.nomeitem.place(relx=0.5, rely=0.35)
        self.entrada_nomeitem = Entry(self.blocoCompras1)
        self.entrada_nomeitem.place(relx=0.4, rely=0.43, relwidth=0.54, relheight=0.1)
        self.quantidade = Label(self.blocoCompras1, text="Quantidade", bg="#292929", fg="white", font=('quicksand', 10, ))
        self.quantidade.place(relx=0.1, rely=0.55)
        self.entrada_quantidade = Entry(self.blocoCompras1)
        self.entrada_quantidade.place(relx=0.07, rely=0.65, relwidth=0.24, relheight=0.1)
        self.valor = Label(self.blocoCompras1, text="Valor", bg="#292929", fg="white", font=('quicksand', 10, ))
        self.valor.place(relx=0.45, rely=0.55)
        self.entrada_valor = Entry(self.blocoCompras1)
        self.entrada_valor.place(relx=0.4, rely=0.65, relwidth=0.24, relheight=0.1)
        self.concluido = Label(self.blocoCompras1, text="Concluido", bg="#292929", fg="white", font=('quicksand', 10, ))
        self.concluido.place(relx=0.75, rely=0.55)
        self.entrada_concluido = StringVar(self.blocoCompras1)
        self.concluidoVar = ("Sim      ", "Não      ")
        self.entrada_concluido.set("Selecione")
        self.selecao = OptionMenu(self.blocoCompras1, self.entrada_concluido, *self.concluidoVar)
        self.selecao.place(relx=0.7, rely=0.65, relwidth=0.28, relheight=0.1)

        # Cria os botões da página de Compras
        self.botaoadicionarCompra = Button(self.blocoCompras1, text="Adicionar", background="#DCB134", bd=3, fg="white", font=('quicksand',11,'bold'), command=self.AdicionarCompra)
        self.botaoadicionarCompra.place(relx=0.07, rely=0.8, relwidth=0.2, relheight=0.125)
        self.botaoalterarCompra = Button(self.blocoCompras1, text="Alterar", background="#DCB134", bd=3, fg="white", font=('quicksand',11,'bold',), command=self.AlterarCompra)
        self.botaoalterarCompra.place(relx=0.3, rely=0.8, relwidth=0.2, relheight=0.125)
        self.botaoapagarCompra = Button(self.blocoCompras1, text="Apagar", background="#DCB134", bd=3, fg="white", font=('quicksand',11,'bold'), command=self.ApagarCompra)
        self.botaoapagarCompra.place(relx=0.53, rely=0.8, relwidth=0.2, relheight=0.125)
        self.botaolimparCompra = Button(self.blocoCompras1, text="Limpar", background="#DCB134", bd=3, fg="white", font=('quicksand',11,'bold'), command=self.LimparCompras)
        self.botaolimparCompra.place(relx=0.76, rely=0.8, relwidth=0.2, relheight=0.125)
       
        #  Cria o bloco da lista da pagina de Compras
        self.blocoCompras2 = Frame(self.paginaCompras, bg="#292929", highlightbackground="black", highlightthickness=3)
        self.blocoCompras2.place(relx=0.02, rely=0.5, relheight=0.45, relwidth=0.96)

        # Cria a exibição das colunas da lista da página de compras
        self.Compra = ttk.Treeview(self.blocoCompras2, height=3, columns=("col0, col1","col2","col3","col4","col5","col6" ))
        self.Compra.heading("#0", text="")
        self.Compra.heading("#1", text="Código Lista")
        self.Compra.heading("#2", text="Item")
        self.Compra.heading("#3", text="Quantidade")
        self.Compra.heading("#4", text="Valor")
        self.Compra.heading("#5", text="Concluido")
        self.Compra.heading("#6", text="Total")
        self.Compra.column("#0", width=0)
        self.Compra.column("#1", width=80)
        self.Compra.column("#2", width=50)
        self.Compra.column("#3", width=100)
        self.Compra.column("#4", width=80)
        self.Compra.column("#5", width=70)
        self.Compra.column("#6", width=100)
        self.Compra.place(relx= 0, rely=0, relheight=1, relwidth=1)
        self.Compra.bind("<Double-1>", self.duploClickCompras)
        self.selecionarListaCompra()
        
class Inicio(Funcao): # Cria uma Classe para a Página Principal

    def __init__(self): # Cria uma função para iniciar as outras funções
        self.janelaPrincipal()
        self.blocoPrincipal()
        self.entradasbloco1()
        self.botoes()
        self.blocoLista()
        self.lista()
        self.criartabelas()
        self.selecionarLista()
        janela.mainloop()

    def janelaPrincipal(self): # Cria uma função para as configurações da Pagina Principal
        self.janelaPrincipal = janela
        self.janelaPrincipal.title("Página Principal")
        self.janelaPrincipal.geometry("500x600")
        self.janelaPrincipal.resizable(False, True)
        self.janelaPrincipal.minsize(width=500, height=600)
        self.janelaPrincipal.maxsize(width=500, height=900)
        self.janelaPrincipal.configure(background="#4D4D4D")
        
    def blocoPrincipal(self): # Cria uma função para o bloco principal
        self.bloco1 = Frame(bg="#292929", highlightbackground="black", highlightthickness=3)
        self.bloco1.place(relx=0.02, rely=0.02, relheight=0.45, relwidth=0.96)
        self.logo = Label(self.bloco1, text="Shopping", bg="#292929", fg="white", font=('quicksand', 25, ))
        self.logo.place(relx=0.25, rely=0.03)
        self.logo2 = Label(self.bloco1, text="List", bg="#292929", fg="white", font=('quicksand', 20, ))
        self.logo2.place(relx=0.38, rely=0.2)
        self.emoji = Label(self.bloco1, bg="#292929",text=f"{emoji.emojize(":check_box_with_check:")}", font=('quicksand', 60, ))
        self.emoji.place(relx=0.58, rely=0.0)

    def entradasbloco1(self): # Cria uma função para as entradas e informações do bloco principal
        self.codigolista = Label(self.bloco1, text="Código", bg="#292929", fg="white", font=('quicksand', 10, ))
        self.codigolista.place(relx=0.1, rely=0.35)
        self.entrada_codigolista = Entry()
        self.entrada_codigolista.place(relx=0.08, rely=0.22, relwidth=0.2, relheight=0.04)
        self.nomelista = Label(self.bloco1, text="Nome da Lista", bg="#292929", fg="white", font=('quicksand', 10, ))
        self.nomelista.place(relx=0.5, rely=0.35)
        self.entrada_nomelista = Entry()
        self.entrada_nomelista.place(relx=0.37, rely=0.22, relwidth=0.5, relheight=0.04)

    def botoes(self): # Cria uma função para os botões do bloco principal
        self.botaoadicionar = Button(self.bloco1, text="Adicionar", background="#DCB134", bd=3, fg="white", font=('quicksand',11,'bold'), command=self.Adicionar)
        self.botaoadicionar.place(relx=0.07, rely=0.63, relwidth=0.2, relheight=0.125)
        self.botaoalterar = Button(self.bloco1, text="Alterar", background="#DCB134", bd=3, fg="white", font=('quicksand',11,'bold'), command=self.Alterar)
        self.botaoalterar.place(relx=0.29, rely=0.63, relwidth=0.2, relheight=0.125)
        self.botaoapagar = Button(self.bloco1, text="Apagar", background="#DCB134", bd=3, fg="white", font=('quicksand',11,'bold'), command=self.Apagar)
        self.botaoapagar.place(relx=0.51, rely=0.63, relwidth=0.2, relheight=0.125)
        self.botaolimpar = Button(self.bloco1, text="Limpar", background="#DCB134", bd=3, fg="white", font=('quicksand',11,'bold'), command=self.Limpar)
        self.botaolimpar.place(relx=0.73, rely=0.63, relwidth=0.2, relheight=0.125)
        self.botaoeditar = Button(self.bloco1, text="Editar Lista", background="#DCB134", bd=3, fg="white", font=('quicksand',11,'bold'), command=self.Editar)
        self.botaoeditar.place(relx=0.29, rely=0.8, relwidth=0.4, relheight=0.125)

    def blocoLista(self): # Cria uma função para o bloco da lista de compras
        self.bloco2 = Frame(bg="#292929", highlightbackground="black", highlightthickness=3)
        self.bloco2.place(relx=0.02, rely=0.5, relheight=0.45, relwidth=0.96)
            
    def lista(self): # Cria uma função para exibir as colunas da lista de compras
        self.listaCompra = ttk.Treeview(self.bloco2, height=3, columns=("col1","col2"))
        self.listaCompra.heading("#0", text="")
        self.listaCompra.heading("#1", text="Código")
        self.listaCompra.heading("#2", text="Nome da Lista")
        self.listaCompra.column("#0", width=1)
        self.listaCompra.column("#1", width=150)
        self.listaCompra.column("#2", width=350)
        self.listaCompra.place(relx= 0, rely=0, relheight=1, relwidth=1)
        self.listaCompra.bind("<Double-1>", self.duploClick)

Inicio() # Inicia o programa