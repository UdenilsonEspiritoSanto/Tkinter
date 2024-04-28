# -*- coding: cp1252 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import conexao

tela_cli= tk.Tk()
tela_cli.geometry('970x668+0+0')
#tela_cli.state('zoomed')
#tela_cli.wm_attributes('-fullscreen','true') 
tela_cli['bg'] = "Wheat"

tela_cli.title("Controle Comercial - Cadastro de Clientes")


def limpar():
    txtcodigo.delete(0,"end")
    txtnome.delete(0,"end")
    txttelefone.delete(0,"end")
    txtemail.delete(0,"end")
    txtobservacao.delete("1.0","end")
    txtcodigo.focus_set()

def buscar():
    var_codigo = txtcodigo.get()
 
    con=conexao.conexao()
    sql_txt = f"select codigo,nome,telefone,email,observacao from cliente where codigo = {var_codigo}"
    rs=con.consultar(sql_txt)

    if rs:
    
        limpar()

        txtcodigo.insert(0, rs[0])
        txtnome.insert(0, rs[1])
        txttelefone.insert(0,rs[2])
        txtemail.insert(0,rs[3])
        txtobservacao.insert("1.0",(rs[4]))
    
    else:
        messagebox.showwarning("Aviso", "Codigo nao Encontrado",parent = tela_cli)
        limpar()
        txtcodigo.focus_set()

    con.fechar()
    
def duplo_click(event):
    limpar()
    item = tree.item(tree.selection())
    txtcodigo.insert(0, item['values'][0])
    buscar()

def visualizar():
    con=conexao.conexao()
    sql_txt = f"select * from cliente"
    rs=con.consultar_tree(sql_txt)

    tree.bind("<Double-1>", duplo_click)
    
    for linha in tree.get_children():
        tree.delete(linha)

    
    for linha in rs:
       tree.insert("", tk.END, values=linha)

    con.fechar()

def pesquisar_nome(p):
    con=conexao.conexao()
    sql_txt = f"select * from cliente where nome like '%{p}%'"
    
    rs=con.consultar_tree(sql_txt)

    tree.bind("<Double-1>", duplo_click)
    
    for linha in tree.get_children():
        tree.delete(linha)
    
    for linha in rs:
        tree.insert("", tk.END, values=linha)

    con.fechar()   

    return True
        
def gravar():
    var_codigo = txtcodigo.get()
    var_nome = txtnome.get()
    var_telefone = txttelefone.get()
    var_email = txtemail.get()
    var_observacao = txtobservacao.get("1.0","end")


    con=conexao.conexao()
    #sql_txt = f"select codigo,nome,telefone,email,observacao from cliente where codigo = {var_codigo}"

    #rs=con.consultar(sql_txt)

    #if rs:
    #   sql_text = f"update cliente set nome='{var_nome}',telefone='{var_telefone}',email='{var_email}',observacao='{var_observacao}' where codigo = '{var_codigo}'"
    # else:
    sql_text = f"insert into cliente(nome,telefone,email,observacao) values ('{var_nome}','{var_telefone}','{var_email}','{var_observacao}')"

    print(sql_text)
    if con.gravar(sql_text):
        messagebox.showinfo("Aviso", "Item Gravado com Sucesso", parent = tela_cli)
        limpar()
    else:
        messagebox.showerror("Erro", "Houve um Erro na Gravacao", parent = tela_cli)

    con.fechar()

    visualizar()


def excluir():
    var_del = messagebox.askyesno("Exclusao", "Tem certeza que deseja excluir?", parent = tela_cli)
    if var_del == True:
        var_codigo = txtcodigo.get()

        con=conexao.conexao()
        sql_text = f"delete from cliente where codigo = '{var_codigo}'"
        if con.gravar(sql_text):
              messagebox.showinfo("Aviso", "Item Excluido com Sucesso",parent = tela_cli)
              limpar()
        else:
            messagebox.showerror("Erro", "Houve um Erro na Exclusao",parent = tela_cli)

            
        con.fechar()

        visualizar()
    else:
        limpar()

def menu():
    tela_cli.destroy()




pes_nome = tela_cli.register(func=pesquisar_nome)

lblcodigo = tk.Label(tela_cli, text ="Codigo:", bg="dimgray", fg="white", font=('Calibri', 12), anchor = "w")
lblcodigo.place(x = 50, y = 60, width=80, height = 25)
txtcodigo = tk.Entry(tela_cli, width = 35, font=('Calibri', 12))
txtcodigo.place(x = 150, y = 60, width = 100, height = 25)
txtcodigo.focus_set()


buscabtn = tk.Button(tela_cli, text ="Pesquisar", 
                      bg ='white',foreground='black', font=('Calibri', 12, 'bold'), command = buscar)
buscabtn.place(x = 280, y = 60, width = 90, height = 25)

  
lblnome = tk.Label(tela_cli, text ="Nome:", bg="Peru", fg="white", font=('Calibri', 12, 'bold'), anchor = "w")
lblnome.place(x = 50, y = 100, width=90, height = 40)
#entry = tk.Entry(tela_cli, width = 160, font=('Calibri', 12))
txtnome = tk.Entry(tela_cli, width = 35,font=('Calibri', 20))
txtnome.place(x = 150, y = 100, width = 740, height = 40)


lbltelefone = tk.Label(tela_cli, text ="Telefone:", bg="Peru", fg="white", font=('Calibri', 12, 'bold'), anchor = "w")
lbltelefone.place(x = 50, y = 150, width=90, height = 40)
txttelefone = tk.Entry(tela_cli, width = 35, font=('Calibri', 20))
txttelefone.place(x = 150, y = 150, width = 740, height = 40)

lblemail = tk.Label(tela_cli, text ="E-mail:", bg="Peru", fg="white", font=('Calibri', 12, 'bold'), anchor = "w")
lblemail.place(x = 50, y = 200, width=90, height = 40)
txtemail = tk.Entry(tela_cli, width = 35, font=('Calibri', 20))
txtemail.place(x = 150, y = 200, width = 740, height = 40)

lblobservacao = tk.Label(tela_cli, text ="Observacao:", bg="Peru", fg="white", font=('Calibri', 12, 'bold'), anchor = "w")
lblobservacao.place(x = 50, y = 250, width=90, height = 40)
txtobservacao= tk.Text(tela_cli, font=('Calibri', 14))
txtobservacao.place(x=150, y=250, width=740, height=80)

lbl_pes_nome = tk.Label(tela_cli, text ="Pesquisar por Nome :", bg="Peru", fg="white", font=('Calibri', 12, 'bold'), anchor = "w")
lbl_pes_nome.place(x = 50, y = 390, width=200, height = 25)
txt_pes_nome = tk.Entry(tela_cli, width = 35, font=('Calibri', 12),validate='key', validatecommand=(pes_nome,'%P'))
txt_pes_nome.place(x = 210, y = 390, width = 690, height = 25)

btngravar = tk.Button(tela_cli, text ="Gravar", 
                       bg ='black',foreground='white', font=('Calibri', 12, 'bold'), command = gravar)
btngravar.place(x = 150, y = 350, width = 65)

btnexcluir = tk.Button(tela_cli, text ="Excluir", 
                       bg ='black',foreground='white', font=('Calibri', 12, 'bold'), command = excluir)
btnexcluir.place(x = 250, y = 350, width = 65)

btnlimpar = tk.Button(tela_cli, text ="Limpar", 
                       bg ='black',foreground='white', font=('Calibri', 12, 'bold'), command = limpar)
btnlimpar.place(x = 350, y = 350, width = 65)

btnmenu = tk.Button(tela_cli, text ="Menu",
                       bg ='black',foreground='white', font=('Calibri', 12, 'bold'), command = menu)
btnmenu.place(x = 450, y = 350, width = 65)

style = ttk.Style()
style.configure("mystyle.Treeview", font=("Calibri", 10))
style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

tree = ttk.Treeview(tela_cli, column=("c1", "c2", "c3", "c4", "c5"), show='headings', style="mystyle.Treeview",)

tree.column("#1")
tree.heading("#1", text="Codigo")
tree.column("#1", width = 100, anchor ='c')

tree.column("#2")
tree.heading("#2", text="Nome")
tree.column("#2", width = 200, anchor ='c')

tree.column("#3")
tree.heading("#3", text="Telefone")
tree.column("#3", width = 100, anchor ='w')

tree.column("#4")
tree.heading("#4", text="E-mail")
tree.column("#4", width = 150, anchor ='c')

tree.column("#5")
tree.heading("#5", text="Observacao")
tree.column("#5", width = 300, anchor ='c')

tree.place(x=50,y=420,height=200)

scrollbar = ttk.Scrollbar(tela_cli, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.place(x = 901, y = 420,height=120)

visualizar()

txtcodigo.focus_set()

tela_cli.mainloop()

