from tkinter import *
from tkinter import ttk
import sqlite3

def criar_labela():

    conexao = sqlite3.connect('produtos.db')
    c = conexao.cursor()

    c.execute(''' CREATE TABLE IF NOT EXISTS produtos (
        
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        fabricacao TEXT,
        estado TEXT NOT NULL,
        comentario text   )
    ''')

    conexao.commit()
    conexao.close()
criar_labela()    

def click(event):
    limpar_tela()
    lista_produto.selection()

    for n in lista_produto.selection():
        col1,col2,col3,col4,col5 = lista_produto.item(n, 'values')
        caixa_nome.insert(END, col1)
        caixa_categoria.insert(END, col2)
        caixa_fabricacao.insert(END, col3)
        caixa_estado.insert(END, col4)
        caixa_comentario.insert(END, col5)

def menus():
    barramenu = Menu(janela)
    janela.config(menu=barramenu)
    menu1 = Menu(barramenu)

    def sair(): janela.destroy()
    
    barramenu.add_cascade(label= 'Opções', menu=menu1)

    menu1.add_command(label='Sair', command=sair)

janela = Tk()
janela.title('Cadastro de Produtos')
janela.geometry("950x300")
janela.configure(background='#DEDEDE')
janela.resizable(False, False)

frame_esquerda = Frame(janela, width=250, height=400, bg='#8000FF')
frame_esquerda.grid(row=0, column=0)
frame_direita = Frame(janela, width=700, height=400, bg='#9FDFFB')
frame_direita.grid(row=0, column=1)


lista_produto = ttk.Treeview(frame_direita, height=1, columns=('col0','col1','col2','col3','col4','col5', 'col6'))

lista_produto.heading('#0', text='')
lista_produto.heading('#1', text='ID')
lista_produto.heading('#2', text='Nome')
lista_produto.heading('#3', text='Categoria')
lista_produto.heading('#4', text='Fabricação')
lista_produto.heading('#5', text='Estado')
lista_produto.heading('#6', text='Comentario')

lista_produto.column("#0", width=0)
lista_produto.column("#1", width=1)
lista_produto.column("#2", width=100)
lista_produto.column("#3", width=100)
lista_produto.column("#4", width=100)
lista_produto.column("#5", width=125)
lista_produto.column("#6", width=170)

lista_produto.place(relx=0.05, rely=0.1, relwidth=0.90, relheight=0.55)
barra_rolagem = Scrollbar(frame_direita, orient='vertical')
lista_produto.configure(yscrollcommand=barra_rolagem.set)
barra_rolagem.place(relx=0.053, rely=0.105, relwidth=0.025 , relheight=0.542)
lista_produto.bind('<Double-Button-1>', click)

def cadastrar_produtos():
    con = sqlite3.connect('produtos.db')
    cursor = con.cursor()
    cursor.execute(" INSERT INTO produtos VALUES (:id, :nome, :categoria, :fabricacao, :estado, :comentario)",
            {   
                'id':None,
                'nome':caixa_nome.get(),
                'categoria':caixa_categoria.get(),
                'fabricacao': caixa_fabricacao.get(),
                'estado': caixa_estado.get(),
                'comentario': caixa_comentario.get()
            } )

    con.commit()
    con.close()
    select_info()
    limpar_tela()

def select_info():
    lista_produto.delete(*lista_produto.get_children())
    con = sqlite3.connect('produtos.db')
    cursor = con.cursor()
    lista = cursor.execute("SELECT id ,nome, categoria, fabricacao, estado, comentario FROM produtos ")
    for i in lista:
        lista_produto.insert("", END, values=i)
    
    con.close()
select_info()

def excluir_produto():

    item_selecionado = lista_produto.focus()
    conteudo = (lista_produto.item(item_selecionado))
    item = conteudo['values']
    lista_produto.delete(item_selecionado)
    con = sqlite3.connect('produtos.db')
    cursor = con.cursor()
    cursor.execute(f"DELETE FROM produtos WHERE id= {item[0]}")
    con.commit()
    con.close()
    select_info()

def atualizarfuncao():
    excluir_produto()
    cadastrar_produtos()

#------------------Label----------------
titulo = Label(frame_esquerda, text='Cadastro de Produtos', bg='#8000FF', font= 14, fg='white')
titulo.place(x=10, y=20)

nome = Label(frame_esquerda, text='Nome', bg='#8000FF', fg='white')
nome.place(x=10, y=40)
caixa_nome = Entry(frame_esquerda ,width=35, justify='left')
caixa_nome.place(x=10, y=60)

categoria = Label(frame_esquerda, text='Categoria', bg='#8000FF', fg='white')
categoria.place(x=10, y=80)
caixa_categoria = Entry(frame_esquerda ,width=35, justify='left')
caixa_categoria.place(x=10, y=100)

fabricacao = Label(frame_esquerda, text='Fabricação', bg='#8000FF', fg='white')
fabricacao.place(x=10, y=120)
caixa_fabricacao = Entry(frame_esquerda ,width=35, justify='left')
caixa_fabricacao.place(x=10, y=140)

estado = Label(frame_esquerda, text='Estado', bg='#8000FF', fg='white')
estado.place(x=10, y=160)
caixa_estado = Entry(frame_esquerda ,width=35, justify='left')
caixa_estado.place(x=10, y=180)

comentario = Label(frame_esquerda, text='Comentario', bg='#8000FF', fg='white')
comentario.place(x=10, y=200)
caixa_comentario = Entry(frame_esquerda ,width=35, justify='left')
caixa_comentario.place(x=10, y=220)

#---------------Botões----------------------
inserir = Button(frame_esquerda, text='Inserir', bg= 'green', fg= 'white', command = cadastrar_produtos)
inserir.place(x= 10, y=250)
atualizar = Button(frame_esquerda, text='Atualizar', bg='blue', fg='white', command = atualizarfuncao)
atualizar.place(x= 89, y=250)
excluir = Button(frame_esquerda, text='Excluir', bg='red', fg='white', command = excluir_produto)
excluir.place(x= 183, y=250)

def limpar_tela():
    caixa_nome.delete(0, END),
    caixa_categoria.delete(0, END),
    caixa_fabricacao.delete(0, END),
    caixa_estado.delete(0, END),
    caixa_comentario.delete(0, END)

if __name__ == '__main__':
    menus()
    janela.mainloop()
    
    