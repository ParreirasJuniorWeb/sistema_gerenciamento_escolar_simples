import psycopg2
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# ---------- DATABASE CONFIGURATION ----------
# Coloque a sua senha do PostgreSQL aqui
PSQL_PASS = "admin"


# ---------- CLASSE DA BASE DE DADOS  ----------
class DatabaseManager:
    def __init__(self):
        self.create_database()
        self.connect()
        self.create_table()

    def create_database(self):
        conn = psycopg2.connect(
            dbname="postgres", user="postgres", password=PSQL_PASS, host="localhost"
        )

        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'alunodb'")

        if not cur.fetchone():
            cur.execute("CREATE DATABASE alunodb")

        cur.close()
        conn.close()

    def connect(self):
        self.conn = psycopg2.connect(
            dbname="alunodb", user="postgres", password=PSQL_PASS, host="localhost"
        )
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS alunos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100),
                materia VARCHAR(100),
                nota REAL
            )
        """
        )
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


# ---------- CREATE ----------
class CreateAluno:
    def __init__(self, nome, materia, nota):
        db = DatabaseManager()
        db.cur.execute(
            "INSERT INTO alunos (nome, materia, nota) VALUES (%s, %s, %s)",
            (nome, materia, nota),
        )
        db.conn.commit()
        db.close()


# ---------- READ ----------
class ReadAlunos:
    def __init__(self, search_query=None, offset=0, limit=10):
        self.db = DatabaseManager()
        if search_query:
            self.db.cur.execute(
                "SELECT * FROM alunos WHERE nome ILIKE %s LIMIT %s OFFSET %s",
                ("%" + search_query + "%", limit, offset),
            )
        else:
            self.db.cur.execute(
                "SELECT * FROM alunos ORDER BY id LIMIT %s OFFSET %s", (limit, offset)
            )
        self.data = self.db.cur.fetchall()
        self.db.close()

    def get_data(self):
        return self.data


# ---------- UPDATE ----------
class UpdateAluno:
    def __init__(self, aluno_id, nome, materia, nota):
        db = DatabaseManager()
        db.cur.execute(
            "UPDATE alunos SET nome=%s, materia=%s, nota=%s WHERE id=%s",
            (nome, materia, nota, aluno_id),
        )
        db.conn.commit()
        db.close()


# ---------- DELETE ----------
class DeleteAluno:
    def __init__(self, aluno_id):
        db = DatabaseManager()
        db.cur.execute("DELETE FROM alunos WHERE id=%s", (aluno_id,))
        db.conn.commit()
        db.close()


# ---------- GUI ----------
class AlunoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro e Consulta de Notas de Alunos")
        self.root.geometry("600x400")

        Button(
            root, text="Cadastrar Aluno", command=self.register_window, width=30
        ).pack(pady=10)
        Button(root, text="Info. de Alunos", command=self.manage_window, width=30).pack(
            pady=10
        )

    def register_window(self):
        win = Toplevel(self.root)
        win.title("Cadastrar Aluno")
        win.geometry("300x250")

        Label(win, text="Nome").pack()
        nome = Entry(win)
        nome.pack()

        Label(win, text="Matéria").pack()
        materia = Entry(win)
        materia.pack()

        Label(win, text="Nota").pack()
        nota = Entry(win)
        nota.pack()

        def submit():
            if nome.get() and materia.get() and nota.get():
                try:
                    CreateAluno(nome.get(), materia.get(), float(nota.get()))
                    messagebox.showinfo("Success", "Aluno Cadastrado.")
                    win.destroy()

                except ValueError:
                    messagebox.showerror("Error", "Nota precisa ser um número.")
            else:
                messagebox.showerror("Error", "Preencha o formulário inteiro.")

        Button(win, text="Submit", command=submit).pack(pady=10)

    def manage_window(self):
        win = Toplevel(self.root)
        win.title("Info. de Alunos")
        win.geometry("800x400")

        search_var = StringVar()
        search_entry = Entry(win, textvariable=search_var)

        # Adiciona um texto de placeholder, dentro da capacidade do tkinter Entry
        search_entry.insert(0, "Pesquisar por nome...")
        search_entry.pack(side=TOP, fill=X, padx=10, pady=5)

        tree = ttk.Treeview(
            win, columns=("ID", "Nome", "Matéria", "Nota"), show="headings"
        )
        for col in ("ID", "Nome", "Matéria", "Nota"):
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
            aluno_id, nome_val, materia_val, nota_val = values

            update_win = Toplevel(win)
            update_win.title("Atualizar Aluno")
            update_win.geometry("300x250")

            Label(update_win, text="Nome").pack()
            nome = Entry(update_win)
            nome.insert(0, nome_val)
            nome.pack()

            Label(update_win, text="Matéria").pack()
            materia = Entry(update_win)
            materia.insert(0, materia_val)
            materia.pack()

            Label(update_win, text="Nota").pack()
            nota = Entry(update_win)
            nota.insert(0, nota_val)
            nota.pack()

            def update():
                try:
                    UpdateAluno(aluno_id, nome.get(), materia.get(), float(nota.get()))
                except ValueError:
                    messagebox.showerror("Error", "Nota precisa ser um número.")

                update_win.destroy()
                load_data(search_var.get())

            Button(update_win, text="Atualizar", command=update).pack(pady=10)

        Button(win, text="Deletar", bg="#ed2456", command=delete_selected).pack(
            side=LEFT, padx=10, pady=10
        )
        Button(win, text="Atualizar", command=update_selected).pack(
            side=LEFT, padx=10, pady=10
        )

        # o lambda event é necessário para o bind funcionar corretamente
        search_entry.bind("<KeyRelease>", lambda event: load_data(search_var.get()))
        load_data()


if __name__ == "__main__":
    root = Tk()
    app = AlunoApp(root)
    root.mainloop()
