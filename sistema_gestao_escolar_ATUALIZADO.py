import psycopg2
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv

# ---------- DATABASE CONFIGURATION ----------
# Coloque a sua senha do PostgreSQL aqui
PSQL_PASS = "886744@Jo_BD"


# ---------- CLASSE DA BASE DE DADOS  ----------
class DatabaseManager:
    def __init__(self):
        self.create_database("alunodb")
        self.connect()
        self.create_table("alunos", "disciplinas", "notas")

    def create_database(self, db):
        try:
            conn = psycopg2.connect(
                dbname="postgres", user="postgres", password=PSQL_PASS, host="localhost"
            )

            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db,))
                    
            if not cur.fetchone():
                cur.execute("CREATE DATABASE alunodb")
                return conn
            
            cur.close()
            conn.close()
        # Controle de exceções do banco de dados
        except psycopg2.DatabaseError as err:
            print(f"Erro de banco de dados ao criar o banco de dados", err)
            
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname="alunodb", user="postgres", password=PSQL_PASS, host="localhost"
            )
            self.cur = self.conn.cursor()
        # Controle de exceções do banco de dados
        except psycopg2.DatabaseError as err:
            print(f"Erro de banco de dados ao criar as tabelas no banco de dados", err)
            
    def create_table(self, table1, table2, table3):
        try:  
            sql_1 = """
                CREATE TABLE IF NOT EXISTS """ + table1 + """ (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL CHECK(nome <> ''),
                    idade INTEGER NOT NULL CHECK(idade >= 0),
                    curso VARCHAR(100) NOT NULL CHECK(curso <> ''),
                    email VARCHAR(100) NOT NULL CHECK(email <> '') UNIQUE,
                    telefone VARCHAR(19) NOT NULL CHECK(telefone <> ''),
                    sexo VARCHAR(1) NOT NULL CHECK(sexo IN ('M', 'F'))
                    )
                    """
            self.cur.execute(sql_1)
                
            sql_2 = """
                CREATE TABLE IF NOT EXISTS """ + table2 + """ (
                        id SERIAL PRIMARY KEY,
                        nome_disciplina VARCHAR(100) NOT NULL CHECK(nome_disciplina <> ''),
                        carga_horaria INTEGER NOT NULL CHECK(carga_horaria > 0),
                        nota REAL CHECK(nota >= 0 AND nota <= 10),
                        nota_corte REAL CHECK(nota_corte >= 0 AND nota_corte <= 10) NOT NULL,
                        valor REAL CHECK(valor >= 1 AND valor <= 1000) NOT NULL,
                        descricao VARCHAR(225)
                    )
                    """
            self.cur.execute(sql_2)
            
            sql_3 = """
                CREATE TABLE IF NOT EXISTS """ + table3 + """ (
                    id SERIAL PRIMARY KEY,
                    nota_1 REAL CHECK(nota_1 >= 0 AND nota_1 <= 10),
                    nota_2 REAL CHECK(nota_2 >= 0 AND nota_2 <= 10),
                    nota_3 REAL CHECK(nota_3 >= 0 AND nota_3 <= 10),
                    status VARCHAR(10) CHECK(status IN ('Aprovado', 'Reprovado')),
                    id_aluno INTEGER NOT NULL,
                    id_disciplina INTEGER NOT NULL,
                    FOREIGN KEY (id_aluno) REFERENCES alunos(id),
                    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id)
                )
                """
            self.cur.execute(sql_3)
                
            self.conn.commit()
            
            print(f"\nTabela '{table1}' criada com sucesso ou já existe no banco de dados!")
            print(f"Tabela '{table2}' criada com sucesso ou já existe no banco de dados!")
            print(f"Tabela '{table3}' criada com sucesso ou já existe no banco de dados!")
            
            # sistema de registro de data e hora das ações sobre o banco de dados
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
                   
    # Controle de exceções do banco de dados
        except psycopg2.DatabaseError as err:
            print(f"Erro de banco de dados ao criar a tabela no banco de dados", err)

    def close(self):
        try:
            if self.cur:
                self.cur.close()
                self.cur = None
            if self.conn:    
                self.conn.close()
                self.conn = None
        except (Exception, psycopg2.Error) as error:
            print("Erro ao fechar conexão", error)
        
# ---------- CREATE ----------
class CreateAluno:
    try:
        def __init__(self, nome, idade, curso, email, telefone, sexo):
            db = DatabaseManager()  
            db.cur.execute(
                "INSERT INTO alunos (nome, idade, curso, email, telefone, sexo) VALUES (%s, %s, %s, %s, %s, %s)",
                (nome, idade, curso, email, telefone, sexo),
            )
            db.conn.commit()
            print("Inserção realizada com sucesso!")
            messagebox.showinfo("Sucesso", "Inserção realizada com sucesso!")
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            messagebox.showinfo("Sucesso", "Data da ação: " + str(dt.strftime('%Y-%m-%d %H:%M:%S')))
            
            db.close()
            
    except (Exception, psycopg2.Error) as error:
            print("Erro ao inserir dados", error)
            messagebox.showerror("Erro", "Erro ao inserir dados", str(error))
                
class CreateDisciplina:
    try:
        def __init__(self, nome_disciplina, carga_horaria, nota, nota_corte, valor, descricao):
            db = DatabaseManager()
            db.cur.execute(
                "INSERT INTO disciplinas (nome_disciplina, carga_horaria, nota, nota_corte, valor, descricao) VALUES (%s, %s, %s, %s, %s, %s)",
                (nome_disciplina, carga_horaria, nota, nota_corte, valor, descricao),
            )
            db.conn.commit()
            print("Inserção realizada com sucesso!")
            messagebox.showinfo("Sucesso", "Inserção realizada com sucesso!")
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            messagebox.showinfo("Sucesso", "Data da ação: " + str(dt.strftime('%Y-%m-%d %H:%M:%S')))
            
            db.close()  
            
    except (Exception, psycopg2.Error) as error:
            print("Erro ao inserir dados", error)
            messagebox.showerror("Erro", "Erro ao inserir dados", str(error))
            
class CreateNota:
    try:
        def __init__(self, nota_1, nota_2, nota_3, status, id_aluno, id_disciplina):
            db = DatabaseManager()
            db.cur.execute(
                "INSERT INTO notas (nota_1, nota_2, nota_3, status, id_aluno, id_disciplina) VALUES (%s, %s, %s, %s, %s, %s)",
                (nota_1, nota_2, nota_3, status, id_aluno, id_disciplina),
            )
            db.conn.commit()
            print("Inserção realizada com sucesso!")
            messagebox.showinfo("Sucesso", "Inserção realizada com sucesso!")
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            messagebox.showinfo("Sucesso", "Data da ação: " + str(dt.strftime('%Y-%m-%d %H:%M:%S')))
            
            db.close()  
            
    except (Exception, psycopg2.Error) as error:
            print("Erro ao inserir dados", error)
            messagebox.showerror("Erro", "Erro ao inserir dados", str(error))
            
# ---------- READ ----------
class ReadAlunos:
    def __init__(self, search_query=None):
        try:
            self.db = DatabaseManager()
            if search_query:
                self.db.cur.execute(
                    "SELECT * FROM alunos WHERE nome ILIKE %s ORDER BY id ASC",
                    ("%" + search_query + "%"),
                )
            else:
                self.db.cur.execute(
                    "SELECT * FROM alunos ORDER BY id ASC"
                )
            self.data = self.db.cur.fetchall()
            self.db.cur.close()
            self.db.close()
            
        except (Exception, psycopg2.Error) as error:
            print("Erro ao selecionar dados", error)
            messagebox.showerror("Erro", f"Erro ao selecionar dados {str(error)}")
            return None
        
    def get_data(self):
        print(dir(self)) 
        return self.data if self.data is not None else []
        
class ReadDisciplinas:
    def __init__(self, search_query=None):
        try:
            self.db = DatabaseManager()
            if search_query:
                self.db.cur.execute(
                    "SELECT * FROM disciplinas WHERE nome ILIKE %s ORDER BY id ASC",
                    ("%" + search_query + "%"),
                )
            else:
                self.db.cur.execute(
                    "SELECT * FROM disciplinas ORDER BY id ASC"
                )
            self.data = self.db.cur.fetchall()
            self.db.cur.close()
            self.db.close()
            
        except (Exception, psycopg2.Error) as error:
            print("Erro ao selecionar dados", error)
            messagebox.showerror("Erro", f"Erro ao selecionar dados {str(error)}")
            return []
        
    def get_data(self):
        if self.data:
            return self.data
        else:
            self.data = []

class ReadNotas:
    def __init__(self, search_query=None):
        try:
            self.db = DatabaseManager()
            if search_query:
                self.db.cur.execute(
                    "SELECT * FROM notas WHERE id_aluno ou id_disciplina ou status ILIKE %s ORDER BY id ASC",
                    ("%" + search_query + "%"),
                )
            else:
                self.db.cur.execute(
                    "SELECT * FROM notas ORDER BY id ASC"
                )
            self.data = self.db.cur.fetchall()
            self.db.cur.close()
            self.db.close()
            
        except (Exception, psycopg2.Error) as error:
            print("Erro ao selecionar dados", error)
            messagebox.showerror("Erro", f"Erro ao selecionar dados {str(error)}")
            return []
            
    def get_data(self):
        if self.data:
            return self.data
        else:
            self.data = []

def ReadNotes_Relation():
    try:
            db = DatabaseManager()
            cur = db.cur
            cur.execute("""
                SELECT A.id, A.nome, N.nota_1, N.nota_2, N.nota_3, N.status, D.id, D.nome_disciplina, D.nota_corte 
                FROM Notas N 
                JOIN Alunos A ON (A.id=N.id_aluno) 
                JOIN Disciplinas D ON (D.id = N.id_disciplina) 
                ORDER BY A.nome, D.nome_disciplina, N.status ASC;
            """)
            registros = cur.fetchall()
            print(registros)
            messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")
            return registros
            
    except (Exception, psycopg2.Error) as error:
               print("Erro ao selecionar dados: ", error)
               messagebox.showerror("Erro", f"Erro ao selecionar dados {str(error)}")
               return []
    finally:
                # Fechamento das conexões
                db.cur.close()
                db.conn.close()
                dt = datetime.now()
                print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    
# ---------- UPDATE ----------
class UpdateAluno:
    try:
        def __init__(self, aluno_id, nome, idade, curso, email, telefone, sexo):
            db = DatabaseManager()
            db.cur.execute(
                "UPDATE alunos SET nome = %s, idade = %s, curso = %s, email = %s, telefone = %s, sexo = %s WHERE id=%s",
                (nome, idade, curso, email, telefone, sexo, aluno_id),
            )
            db.conn.commit()
            print("Atualização realizada com sucesso!")
            dt = datetime.now()
            print(f"\nData e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
            messagebox.showinfo("Sucesso", "Atualização realizada com sucesso! Data: " + str(dt.strftime('%Y-%m-%d %H:%M:%S')))
            db.close()
            
    except (Exception, psycopg2.Error) as error:
            print("Erro ao atualizar dados", error)
            messagebox.showerror("Erro", "Erro ao atualizar dados", str(error))
            
class UpdateDisciplina:
    try:
        def __init__(self, disc_id, nome_disciplina, carga_horaria, nota, nota_corte, valor, descricao):
            db = DatabaseManager()
            db.cur.execute(
                "UPDATE disciplinas SET nome_disciplina = %s, carga_horaria = %s, nota = %s, nota_corte = %s, valor = %s, descricao = %s WHERE id = %s",
                (nome_disciplina, carga_horaria, nota, nota_corte, valor, descricao, disc_id),
            )
            db.conn.commit()
            print("Atualização realizada com sucesso!")
            dt = datetime.now()
            print(f"\nData e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
            messagebox.showinfo("Sucesso", "Atualização realizada com sucesso! Data: " + str(dt.strftime('%Y-%m-%d %H:%M:%S')))
            db.close()
            
    except (Exception, psycopg2.Error) as error:
            print("Erro ao atualizar dados", error)
            messagebox.showerror("Erro", "Erro ao atualizar dados", str(error))
                
class UpdateNota:
    try:
        def __init__(self, nota_id, nota_1, nota_2, nota_3, status, id_aluno, id_disciplina):
            db = DatabaseManager()
            db.cur.execute(
                "UPDATE notas SET nota_1 = %s, nota_2 = %s, nota_3 = %s, status = %s, id_aluno = %s, id_disciplina = %s WHERE id = %s",
                (nota_1, nota_2, nota_3, status, id_aluno, id_disciplina, nota_id),
            )
            db.conn.commit()
            print("Atualização realizada com sucesso!")
            dt = datetime.now()
            print(f"\nData e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
            messagebox.showinfo("Sucesso", "Atualização realizada com sucesso! Data: " + str(dt.strftime('%Y-%m-%d %H:%M:%S')))
            db.close()
            
    except (Exception, psycopg2.Error) as error:
            print("Erro ao atualizar dados", error)
            messagebox.showerror("Erro", "Erro ao atualizar dados", str(error))
                        
# ---------- DELETE ----------
class DeleteAluno:
    try:
        def __init__(self, aluno_id):
            db = DatabaseManager()
            db.cur.execute("DELETE FROM alunos WHERE id=%s", (aluno_id,))
            db.conn.commit()
            print("Exclusão realizada com sucesso!")
            messagebox.showinfo("Sucesso", "Exclusão realizada com sucesso!")
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            messagebox.showinfo("Sucesso", "Data da ação: "+ str(dt.strftime('%Y-%m-%d %H:%M:%S')))
            db.close()
            
    except (Exception, psycopg2.Error) as error:
        print("Erro ao excluir dados", error)
        messagebox.showerror("Erro", "Erro ao excluir dados", str(error))

class DeleteDisciplina:
    try:
        def __init__(self, disc_id):
            db = DatabaseManager()
            db.cur.execute("DELETE FROM alunos WHERE id=%s", (disc_id,))
            db.conn.commit()
            print("Exclusão realizada com sucesso!")
            messagebox.showinfo("Sucesso", "Exclusão realizada com sucesso!")
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            messagebox.showinfo("Sucesso", "Data da ação: "+ str(dt.strftime('%Y-%m-%d %H:%M:%S')))
            db.close()
            
    except (Exception, psycopg2.Error) as error:
        print("Erro ao excluir dados", error)
        messagebox.showerror("Erro", "Erro ao excluir dados", str(error))
        
class DeleteNota:
    try:
        def __init__(self, nota_id):
            db = DatabaseManager()
            db.cur.execute("DELETE FROM alunos WHERE id=%s", (nota_id,))
            db.conn.commit()
            print("Exclusão realizada com sucesso!")
            messagebox.showinfo("Sucesso", "Exclusão realizada com sucesso!")
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            messagebox.showinfo("Sucesso", "Data da ação: "+ str(dt.strftime('%Y-%m-%d %H:%M:%S')))
            db.close()
            
    except (Exception, psycopg2.Error) as error:
        print("Erro ao excluir dados", error)
        messagebox.showerror("Erro", "Erro ao excluir dados", str(error))
                
# ---------- GUI ----------
class AlunoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro e Consulta de Notas de Alunos")
        self.root.geometry("600x400")

        Button(
            root, text="Cadastrar Aluno", command=self.register_window_Aluno, width=30
        ).pack(pady=10)
        Button(root, text="Info. de Alunos", command=self.manage_window_Aluno, width=30).pack(
            pady=10
        )

        Button(
            root, text="Cadastrar Disciplina", command=self.register_window_Disciplina, width=30
        ).pack(pady=10)
        Button(root, text="Info. de Disciplinas", command=self.manage_window_Disciplina, width=30).pack(
            pady=10
        )
        
        Button(
            root, text="Cadastrar Nota", command=self.register_window_Notas, width=30
        ).pack(pady=10)
        Button(root, text="Info. de Notas", command=self.manage_window_Notas, width=30).pack(
            pady=10
        )
        
        Button(
            root, text="Gerar Relatório", command=self.manage_window_Relatorio, width=30
        ).pack(pady=10)
        
    def register_window_Aluno(self):
        win = Toplevel(self.root)
        win.title("Cadastrar Aluno")
        win.geometry("800x400")
        
        Label(win, text="Nome").pack()
        nome = Entry(win)
        nome.pack()

        Label(win, text="Idade").pack()
        idade = Entry(win)
        idade.pack()

        Label(win, text="Curso").pack()
        curso = Entry(win)
        curso.pack()

        Label(win, text="E-mail").pack()
        email = Entry(win)
        email.pack()
        
        Label(win, text="Telefone").pack()
        telefone = Entry(win)
        telefone.pack()
        
        Label(win, text="Gênero").pack()
        sexo = Entry(win)
        sexo.pack()
        
        def submit():
            if nome.get() and idade.get() and curso.get() and email.get() and telefone.get() and sexo.get():
                try:
                    CreateAluno(nome.get(), int(idade.get()), curso.get(), email.get(), telefone.get(), sexo.get())
                    messagebox.showinfo("Success", "Aluno Cadastrado.")
                    win.destroy()

                except ValueError:
                    messagebox.showerror("Error", "Nota precisa ser um número.")
            else:
                messagebox.showerror("Error", "Preencha o formulário inteiro.")

        Button(win, text="Submit", command=submit).pack(pady=10)

    def manage_window_Aluno(self):
        win = Toplevel(self.root)
        win.title("Info. de Alunos")
        win.geometry("1500x400")

        search_var = StringVar()
        search_entry = Entry(win, textvariable=search_var)
        search_entry.pack(side=TOP, fill=X, padx=10, pady=5)

        tree = ttk.Treeview(
            win, columns=("ID", "Nome", "Idade", "Curso", "E-mail", "Telefone", "Gênero"), show="headings"
        )
        for col in ("ID", "Nome", "Idade", "Curso", "E-mail", "Telefone", "Gênero"):
            tree.heading(col, text=col)
        tree.pack(fill=BOTH, expand=True)

        def load_data(search_term=""):
            for row in tree.get_children():
                tree.delete(row)
            alunos = ReadAlunos(search_query=search_term).get_data()
            for aluno in alunos:
                tree.insert("", END, values=aluno)

        def delete_selected():
            selected = tree.focus()
            if selected:
                aluno_id = tree.item(selected)["values"][0]
                DeleteAluno(aluno_id)
                load_data(search_var.get())

        def update_selected():
            selected = tree.focus()
            if not selected:
                return

            values = tree.item(selected)["values"]
            aluno_id, nome_val, idade_val, curso_val, email_val, telefone_val, sexo_val = values

            update_win = Toplevel(win)
            update_win.title("Atualizar Aluno")
            update_win.geometry("800x250")

            Label(update_win, text="Nome").pack()
            nome = Entry(update_win)
            nome.insert(0, nome_val)
            nome.pack()

            Label(update_win, text="Idade").pack()
            idade = Entry(update_win)
            idade.insert(0, idade_val)
            idade.pack()

            Label(update_win, text="Curso").pack()
            curso = Entry(update_win)
            curso.insert(0, curso_val)
            curso.pack()

            Label(update_win, text="E-mail").pack()
            email = Entry(update_win)
            email.insert(0, email_val)
            email.pack()
            
            Label(update_win, text="Telefone").pack()
            telefone = Entry(update_win)
            telefone.insert(0, telefone_val)
            telefone.pack()
            
            Label(update_win, text="Gênero").pack()
            sexo = Entry(update_win)
            sexo.insert(0, sexo_val)
            sexo.pack()
            
            def update():
                try:
                    UpdateAluno(aluno_id, nome.get(), int(idade.get()), curso.get(), email.get(), telefone.get(), sexo.get())
                except ValueError:
                    messagebox.showerror("Error", "Nota precisa ser um número.")

                update_win.destroy()
                load_data(search_var.get())

            Button(update_win, text="Atualizar", command=update).pack(pady=10)

        Button(win, text="Deletar", command=delete_selected).pack(
            side=LEFT, padx=10, pady=10
        )
        Button(win, text="Atualizar", command=update_selected).pack(
            side=LEFT, padx=10, pady=10
        )

        # o lambda event é necessário para o bind funcionar corretamente
        search_entry.bind("<KeyRelease>", lambda event: load_data(search_var.get()))
        load_data()
        
    def register_window_Disciplina(self):
        win = Toplevel(self.root)
        win.title("Cadastrar Disciplina")
        win.geometry("800x400")
        
        Label(win, text="Nome").pack()
        nome = Entry(win)
        nome.pack()

        Label(win, text="Carga Horária").pack()
        carga_horaria = Entry(win)
        carga_horaria.pack()

        Label(win, text="Nota").pack()
        nota = Entry(win)
        nota.pack()

        Label(win, text="Nota de Corte").pack()
        nota_corte = Entry(win)
        nota_corte.pack()
        
        Label(win, text="Valor(R$)").pack()
        valor = Entry(win)
        valor.pack()
        
        Label(win, text="Descrição").pack()
        desc = Entry(win)
        desc.pack()
        
        def submit():
            if nome.get() and carga_horaria.get() and nota.get() and nota_corte.get() and valor.get() and desc.get():
                try:
                    CreateDisciplina(nome.get(), int(carga_horaria.get()), float(nota.get()), float(nota_corte.get()), float(valor.get()), desc.get())
                    messagebox.showinfo("Success", "Disciplina Cadastrado.")
                    win.destroy()

                except ValueError:
                    messagebox.showerror("Error", "Nota precisa ser um número.")
            else:
                messagebox.showerror("Error", "Preencha o formulário inteiro.")

        Button(win, text="Submit", command=submit).pack(pady=10)

    def manage_window_Disciplina(self):
        win = Toplevel(self.root)
        win.title("Info. de Disciplinas")
        win.geometry("1200x400")

        search_var = StringVar()
        search_entry = Entry(win, textvariable=search_var)
        search_entry.pack(side=TOP, fill=X, padx=10, pady=5)

        tree = ttk.Treeview(
            win, columns=("ID", "Nome", "Carga Horária", "Nota", "Nota de Corte", "Valor(R$)", "Descrição"), show="headings"
        )
        for col in ("ID", "Nome", "Carga Horária", "Nota", "Nota de Corte", "Valor(R$)", "Descrição"):
            tree.heading(col, text=col)
        tree.pack(fill=BOTH, expand=True)

        def load_data(search_term=""):
            for row in tree.get_children():
                tree.delete(row)
            disciplinas = ReadDisciplinas(search_query=search_term).get_data()
            for disc in disciplinas:
                tree.insert("", END, values=disc)

        def delete_selected():
            selected = tree.focus()
            if selected:
                disc_id = tree.item(selected)["values"][0]
                DeleteDisciplina(disc_id)
                load_data(search_var.get())

        def update_selected():
            selected = tree.focus()
            if not selected:
                return

            values = tree.item(selected)["values"]
            disc_id, nome_val, c_horaria_val, nota_val, n_corte_val, valor_val, desc_val = values
                
            update_win = Toplevel(win)
            update_win.title("Atualizar Disciplina")
            update_win.geometry("600x250")

            Label(update_win, text="Nome").pack()
            nome = Entry(update_win)
            nome.insert(0, nome_val)
            nome.pack()

            Label(update_win, text="Carga Horária").pack()
            c_horaria = Entry(update_win)
            c_horaria.insert(0, c_horaria_val)
            c_horaria.pack()

            Label(update_win, text="Nota").pack()
            nota = Entry(update_win)
            nota.insert(0, nota_val)
            nota.pack()

            Label(update_win, text="Nota de Corte").pack()
            n_corte = Entry(update_win)
            n_corte.insert(0, n_corte_val)
            n_corte.pack()
            
            Label(update_win, text="Valor(R$)").pack()
            valor = Entry(update_win)
            valor.insert(0, valor_val)
            valor.pack()
            
            Label(update_win, text="Descrição").pack()
            desc = Entry(update_win)
            desc.insert(0, desc_val)
            desc.pack()
            
            def update():
                try:
                    UpdateDisciplina(disc_id, nome.get(), int(c_horaria.get()), float(nota.get()), float(n_corte.get()), float(valor.get()), desc.get())
                except ValueError:
                    messagebox.showerror("Error", "Nota precisa ser um número.")

                update_win.destroy()
                load_data(search_var.get())

            Button(update_win, text="Atualizar", command=update).pack(pady=10)

        Button(win, text="Deletar", command=delete_selected).pack(
            side=LEFT, padx=10, pady=10
        )
        Button(win, text="Atualizar", command=update_selected).pack(
            side=LEFT, padx=10, pady=10
        )

        # o lambda event é necessário para o bind funcionar corretamente
        search_entry.bind("<KeyRelease>", lambda event: load_data(search_var.get()))
        load_data()        

    def register_window_Notas(self):
        win = Toplevel(self.root)
        win.title("Cadastrar Nota")
        win.geometry("800x450")
        
        Label(win, text="1º Nota").pack()
        nota_1 = Entry(win)
        nota_1.pack()

        Label(win, text="2º Nota").pack()
        nota_2 = Entry(win)
        nota_2.pack()

        Label(win, text="3º Nota").pack()
        nota_3 = Entry(win)
        nota_3.pack()

        Label(win, text="Condição do Aluno(a)").pack()
        status = Entry(win, state="disabled", disabledbackground="white")
        status.insert(0, "Aprovado")
        status.pack()
                
        Label(win, text="ID Aluno(a)").pack()
        id_aluno = Entry(win)
        id_aluno.pack()
        
        Label(win, text="ID Disc").pack()
        id_disc = Entry(win)
        id_disc.pack()
        
        def submit():
            if nota_1.get() and nota_2.get() and nota_3.get() and id_aluno.get() and id_disc.get():
                status = (float(nota_1.get()) + float(nota_2.get()) + float(nota_3.get()))
                if status:
                    if status >= 6.0:
                        status = "Aprovado"
                    else:
                        status = "Reprovado"
                try:
                    CreateNota(float(nota_1.get()), float(nota_2.get()), float(nota_3.get()), status, int(id_aluno.get()), int(id_disc.get()))
                    messagebox.showinfo("Success", "Nota Cadastrado.")
                    win.destroy()

                except ValueError:
                    messagebox.showerror("Error", "Nota precisa ser um número.")
            else:
                messagebox.showerror("Error", "Preencha o formulário inteiro.")

        Button(win, text="Submit", command=submit).pack(pady=10)

    def manage_window_Notas(self):
        win = Toplevel(self.root)
        win.title("Info. de Nota")
        win.geometry("1500x400")

        search_var = StringVar()
        search_entry = Entry(win, textvariable=search_var)
        search_entry.pack(side=TOP, fill=X, padx=10, pady=5)

        tree = ttk.Treeview(
            win, columns=("ID", "1º Nota", "2º Nota", "3º Nota", "Condição do Aluno(a)", "ID Aluno(a)", "ID Disc"), show="headings"
        )
        for col in ("ID", "1º Nota", "2º Nota", "3º Nota", "Condição do Aluno(a)", "ID Aluno(a)", "ID Disc"):
            tree.heading(col, text=col)
        tree.pack(fill=BOTH, expand=True)

        def load_data(search_term=""):
            for row in tree.get_children():
                tree.delete(row)
            notas = ReadNotas(search_query=search_term).get_data()
            for nota in notas:
                tree.insert("", END, values=nota)

        def delete_selected():
            selected = tree.focus()
            if selected:
                nota_id = tree.item(selected)["values"][0]
                DeleteNota(nota_id)
                load_data(search_var.get())

        def update_selected():
            selected = tree.focus()
            if not selected:
                return

            values = tree.item(selected)["values"]
            nota_id, nota_1_val, nota_2_val, nota_3_val, status_val, id_aluno_val, id_disc_val = values
                
            update_win = Toplevel(win)
            update_win.title("Atualizar Nota")
            update_win.geometry("1500x250")

            Label(update_win, text="1º Nota").pack()
            nota_1 = Entry(update_win)
            nota_1.insert(0, nota_1_val)
            nota_1.pack()

            Label(update_win, text="2º Nota").pack()
            nota_2 = Entry(update_win)
            nota_2.insert(0, nota_2_val)
            nota_2.pack()

            Label(update_win, text="3º Nota").pack()
            nota_3 = Entry(update_win)
            nota_3.insert(0, nota_3_val)
            nota_3.pack()

            Label(update_win, text="Condição Aluno(a)").pack()
            status = Entry(update_win)
            status.insert(0, status_val)
            status.pack()
            
            Label(update_win, text="ID Aluno(a)").pack()
            id_aluno = Entry(update_win)
            id_aluno.insert(0, id_aluno_val)
            id_aluno.pack()
            
            Label(update_win, text="ID Disciplina").pack()
            id_disc = Entry(update_win)
            id_disc.insert(0, id_disc_val)
            id_disc.pack()
            
            def update():
                try:
                    UpdateNota(nota_id, float(nota_1.get()), float(nota_2.get()), float(nota_3.get()), status.get(), int(id_aluno.get()), int(id_disc.get()))
                except ValueError:
                    messagebox.showerror("Error", "Nota precisa ser um número.")

                update_win.destroy()
                load_data(search_var.get())

            Button(update_win, text="Atualizar", command=update).pack(pady=10)

        Button(win, text="Deletar", command=delete_selected).pack(
            side=LEFT, padx=10, pady=10
        )
        Button(win, text="Atualizar", command=update_selected).pack(
            side=LEFT, padx=10, pady=10
        )

        # o lambda event é necessário para o bind funcionar corretamente
        search_entry.bind("<KeyRelease>", lambda event: load_data(search_var.get()))
        load_data() 
            
    def manage_window_Relatorio(self):
        win = Toplevel(self.root)
        win.title("Info. de Relatório de Notas")
        win.geometry("1200x400")

        search_var = StringVar()
        search_entry = Entry(win, textvariable=search_var)
        search_entry.pack(side=TOP, fill=X, padx=10, pady=5)

        tree = ttk.Treeview(
            win, columns=("ID", "1º Nota", "2º Nota", "3º Nota", "Condição do Aluno(a)", "ID Aluno(a)", "Nome do Aluno(a)", "ID Disc", "Nome da Disciplina"), show="headings"
        )
        for col in ("ID", "1º Nota", "2º Nota", "3º Nota", "Condição do Aluno(a)", "ID Aluno(a)", "Nome do Aluno(a)", "ID Disc", "Nome da Disciplina"):
            tree.heading(col, text=col)
        tree.pack(fill=BOTH, expand=True)

        def load_data(search_term=""):
            for row in tree.get_children():
                tree.delete(row)
            notas = ReadNotes_Relation()
            for nota in notas:
                tree.insert("", END, values=nota)
        
        search_entry.bind("<KeyRelease>", lambda event: load_data(search_var.get()))
        load_data()

        def gerarRelatorioNotas_csv():
            notas = ReadNotes_Relation()
            with open('Relacao_Notas_Alunos.csv', 'w', newline='') as csvfile:
                fieldnames = ['ID', 'Nome', 'Nota 1', 'Nota 2', 'Nota 3', 'Status', 'ID Disciplina', 'Nome Disciplina', 'Nota de Corte']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for nota in notas:
                    writer.writerow({
                        'ID': nota[0],
                        'Nome': nota[1],
                        'Nota 1': nota[2],
                        'Nota 2': nota[3],
                        'Nota 3': nota[4],
                        'Status': nota[5],
                        'ID Disciplina': nota[6],
                        'Nome Disciplina': nota[7],
                        'Nota de Corte': nota[8]
                    })
            print("Relatório de notas gerado com sucesso!")
            return 'Relacao_Notas_Alunos.csv'
        
        Button(win, text="Gerar Relatório", command=gerarRelatorioNotas_csv).pack(side=LEFT, padx=10, pady=5)
            
if __name__ == "__main__":
    root = Tk()
    app = AlunoApp(root)
    root.mainloop()