import psycopg2
from datetime import datetime
import pandas as pd

# Coloque a sua senha do PostgreSQL aqui:
PSQL_PASS = "***"

# Classes principais do sistema de gestão escolar:
class AppBD:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.createDataTable("Escola", "Alunos", "Disciplinas", "Notas")
        self.connect_to_db("Escola")

    def create_database_if_not_exists(self, dbname):
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                dbname="postgres",  # Connect to default DB
                user="postgres",
                password=PSQL_PASS,
            )
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
            exists = cur.fetchone()
            if not exists:
                cur.execute(f'CREATE DATABASE "{dbname}"')
                print(f"Banco de dados '{dbname}' criado com sucesso.")
            else:
                print(f"Banco de dados '{dbname}' já existe.")
            cur.close()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print("Erro ao criar banco de dados:", error)

    def createDataTable(self, db, table_1, table_2, table_3):
        try:
            # Abertura de conexão e aquisição de cursor
            self.conn = psycopg2.connect(
                host="localhost",
                port=5432,
                dbname=db,
                user="postgres",
                password=PSQL_PASS,
                sslmode="prefer",
                connect_timeout=10,
            )
            self.cur = self.conn.cursor()
            # Execução de um comando: SELECT... CREATE ...
            comando_1 = f"""CREATE TABLE IF NOT EXISTS {table_1} (
                                matricula SERIAL PRIMARY KEY NOT NULL,
                                nome VARCHAR(255) NOT NULL,
                                idade INTEGER NOT NULL,
                                curso VARCHAR(150) NOT NULL,
                                email VARCHAR(150) NOT NULL,
                                telefone VARCHAR(19) NOT NULL,
                                sexo VARCHAR(1) NOT NULL
                                );"""
            comando_2 = f"""CREATE TABLE IF NOT EXISTS {table_2} (
                                id_disciplina SERIAL PRIMARY KEY NOT NULL,
                                nome_disciplina VARCHAR(150) NOT NULL,
                                nota_corte REAL NOT NULL,
                                valor REAL NOT NULL,
                                descricao VARCHAR(150) NOT NULL,
                                carga_horaria INTEGER NOT NULL
                                );"""

            comando_3 = f"""CREATE TABLE IF NOT EXISTS {table_3} (
                                id_nota SERIAL PRIMARY KEY NOT NULL,
                                nota_1 REAL NOT NULL,
                                nota_2 REAL NOT NULL,
                                nota_3 REAL NOT NULL,
                                media REAL NOT NULL,
                                id_aluno INTEGER NOT NULL,
                                id_disciplina INTEGER NOT NULL,
                                status VARCHAR(60) NOT NULL,
                                FOREIGN KEY (id_aluno) REFERENCES {table_1}(matricula),
                                FOREIGN KEY (id_disciplina) REFERENCES {table_2}(id_disciplina)
                                );"""

            self.cur.execute(comando_1)
            self.cur.execute(comando_2)
            self.cur.execute(comando_3)
            # Efetivação do comando
            self.conn.commit()
            print(
                f"\nTabela criada '{table_1}' com sucesso ou esta tabela já existe no banco da dados!"
            )
            print(
                f"Tabela criada '{table_2}' com sucesso ou esta tabela já existe no banco da dados!"
            )
            print(
                f"Tabela criada '{table_3}' com sucesso ou esta tabela já existe no banco da dados!"
            )
            # sistema de registro de data e hora das ações sobre o banco de dados
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
            # Retornando a conexão
            return self.conn
        # Controle de exceções do banco de dados
        except psycopg2.DatabaseError as err:
            print(f"Erro de banco de dados ao criar a tabela no Banco de Dados: \n", err)

    def connect_to_db(self, db):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                port=5432,
                dbname=db,
                user="postgres",
                password=PSQL_PASS,
                sslmode="prefer",
                connect_timeout=10,
            )
            self.cur = self.conn.cursor()
            # print("\nConexão com o Banco de Dados aberta com sucesso!\n")
            return self.conn
        except (Exception, psycopg2.Error) as error:
            print("Falha ao se conectar ao Banco de Dados", error)

    def selecionar_dados(self, table):
        try:
            self.connect_to_db("Escola")
            comando_SELECAO_TABLE_BD = "SELECT * FROM " + table
            self.cur = self.conn.cursor()
            self.cur.execute(comando_SELECAO_TABLE_BD)
            registros = self.cur.fetchall()
            return registros
        except (Exception, psycopg2.Error) as error:
            print("Erro ao selecionar dados", error)
            return []
        finally:
            # Fechamento das conexões
            self.fechar_conexao()
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}")

    def inserir_dados(self, table, colunas, valores):
        try:
            self.connect_to_db("Escola")
            comando_INSERCAO = f"INSERT INTO {table} ({', '.join(colunas)}) VALUES ({', '.join(['%s'] * len(valores))})"
            self.cur.executemany(comando_INSERCAO, [valores])
            self.conn.commit()
            print("Inserção realizada com sucesso!")
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        except (Exception, psycopg2.Error) as error:
            print("Erro ao inserir dados", error)
        finally:
            # Fechamento das conexões
            self.fechar_conexao()

    def atualizar_dados(self, table, colunas, valores, campo, id):
        try:
            self.connect_to_db("Escola")
            comando_ATUALIZACAO = f"UPDATE {table} SET {', '.join([f'{coluna} = %s' for coluna in colunas])} WHERE {campo} = %s"
            self.cur.execute(comando_ATUALIZACAO, (*valores, id))
            self.conn.commit()
            print("Atualização realizada com sucesso!")
            dt = datetime.now()
            print(f"\nData e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
        except (Exception, psycopg2.Error) as error:
            print("Erro ao atualizar dados", error)
        finally:
            # Fechamento das conexões
            self.fechar_conexao()

    def excluir_dados(self, table, coluna, codigo):
        try:
            self.connect_to_db("Escola")
            comando_DELETE_TABLE_BD = f"DELETE FROM {table} WHERE {coluna} = %s"
            self.cur = self.conn.cursor()
            self.cur.execute(comando_DELETE_TABLE_BD, (codigo,))
            self.conn.commit()
            print("Exclusão realizada com sucesso!")
            dt = datetime.now()
            print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        except (Exception, psycopg2.Error) as error:
            print("Erro ao excluir dados", error)
        finally:
            # Fechamento das conexões
            self.fechar_conexao()

    def fechar_conexao(self):
        """Encapsula o fechamento de conexões ao banco de dados."""
        if self.conn is not None:
            try:
                if self.conn is not None:
                    self.cur.close()
                    self.conn.close()
                # print("Conexão ao banco de dados fechada!")
                self.cur = None
                self.conn = None
                # dt = datetime.now()
                # print(f"Data e Hora da ação: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
            except (Exception, psycopg2.Error) as e:
                print("Erro ao tentar fechar a conexão:", e)
                self.cur = None
                self.conn = None


class Alunos(AppBD):
    def __init__(self, matricula, nome, idade, curso, email, telefone, sexo):
        self.matricula = matricula
        self.nome = nome
        self.idade = idade
        self.curso = curso
        self.email = email
        self.telefone = telefone
        self.sexo = sexo


# Objeto da classe Alunos:
aluno = Alunos(
    22,
    "Jessica Elen",
    24,
    "Engenharia Civil",
    "jessica.elen@gmail.com",
    "(45) 123456789",
    "F",
)

# Cria o banco de dados Escola se não existir
aluno.create_database_if_not_exists("Escola")  

aluno.createDataTable("Escola", "Alunos", "Disciplinas", "Notas")
aluno.connect_to_db("Escola")

# Inserir dados na tabela Alunos através do objeto da classe Alunos:
colunas = ["matricula", "nome", "idade", "curso", "email", "telefone", "sexo"]
valores = [
    str(aluno.matricula),
    str(aluno.nome),
    str(aluno.idade),
    str(aluno.curso),
    str(aluno.email),
    str(aluno.telefone),
    str(aluno.sexo),
]

aluno.inserir_dados("alunos", colunas, valores)
# Exibição dos registros da tabela Aluno no banco de dados MySQL
print(aluno.selecionar_dados("alunos"))

# Atualização dos dados da tabela Aluno no banco de dados MySQL
aluno_2 = Alunos(
    35,
    "Bruna Marcs",
    21,
    "Engenharia de Software",
    "bruna.marcs@gmail.com",
    "(44) 9989454556",
    "F",
)

colunas = ["matricula", "nome", "idade", "curso", "email", "telefone", "sexo"]
valores = [
    str(aluno_2.matricula),
    str(aluno_2.nome),
    str(aluno_2.idade),
    str(aluno_2.curso),
    str(aluno_2.email),
    str(aluno_2.telefone),
    str(aluno_2.sexo),
]

# Inserindo dados no banco de dados
aluno.inserir_dados("alunos", colunas, valores)

# Mostrando todos os registros da tabela Aluno
print(aluno.selecionar_dados("alunos"))


aluno_3 = Alunos(
    65, "Otaviano Luc", 21, "ADS", "otav_luc23.marcs@gmail.com", "(44) 99894555786", "M"
)

colunas = ["matricula", "nome", "idade", "curso", "email", "telefone", "sexo"]
valores = [
    str(aluno_3.matricula),
    str(aluno_3.nome),
    str(aluno_3.idade),
    str(aluno_3.curso),
    str(aluno_3.email),
    str(aluno_3.telefone),
    str(aluno_3.sexo),
]

# Atualizar os dados diretamente no banco de dados PostgreSQL
aluno.atualizar_dados("alunos", colunas, valores, "matricula", aluno_2.matricula)

# Mostrando todos os registros da tabela Aluno
print(aluno.selecionar_dados("alunos"))

# Exclusão dos dados da tabela Aluno no banco de dados MySQL
aluno.excluir_dados("alunos", "matricula", 2)


class Disciplinas(AppBD):
    def __init__(
        self,
        id_disciplina,
        nome_disciplina,
        carga_horaria,
        descricao,
        valor,
        nota_corte,
    ):
        self.id_disciplina = id_disciplina
        self.nome_disciplina = nome_disciplina
        self.carga_horaria = carga_horaria
        self.descricao = descricao
        self.valor = valor
        self.nota_corte = (
            nota_corte  # Nota suficiente para o aluno passar na disciplina
        )


# Objeto da classe Disciplinas:
disciplina = Disciplinas(1, "Matematica", 40, "Equacao do Segundo Grau", 90.87, 6.0)
# print(disciplina.nome_disciplina, disciplina.carga_horaria, disciplina.descricao, disciplina.valor, disciplina.id_disciplina, disciplina.id_curso, disciplina.id_aluno)

# Inserindo dados no banco de dados
colunas = [
    "id_disciplina",
    "nome_disciplina",
    "nota_corte",
    "valor",
    "descricao",
    "carga_horaria",
]

valores = [
    str(disciplina.id_disciplina),
    str(disciplina.nome_disciplina),
    str(disciplina.nota_corte),
    str(disciplina.valor),
    str(disciplina.descricao),
    str(disciplina.carga_horaria),
]

disciplina.inserir_dados("disciplinas", colunas, valores)
# Exibição dos registros da tabela professor no banco de dados MySQL
print(disciplina.selecionar_dados("disciplinas"))

class Notas(AppBD):
    def __init__(
        self,
        id,
        nota_1,
        nota_2,
        nota_3,
        id_aluno,
        id_disciplina,
        media_arit=0,
        soma=0,
        status="",
    ):
        self.id = id
        self.nota_1 = nota_1
        self.nota_2 = nota_2
        self.nota_3 = nota_3
        self.id_aluno = id_aluno
        self.id_disciplina = id_disciplina
        self.media_arit = media_arit
        self.soma = soma
        self.status = status

    def retornarMediaArit(self):
        quant_notas = 3
        self.media_arit = (self.nota_1 + self.nota_2 + self.nota_3) / quant_notas
        return print(self.media_arit)

    def retornarSoma(self):
        self.soma = self.nota_1 + self.nota_2 + self.nota_3
        return print(round(self.soma, 2))

    def retornarStatus(self):
        if self.soma >= 6:
            self.status = "Aluno(a) Aprovado"
            return print(self.status)
        else:
            self.status = "Aluno(a) Reprovado"
            return print(self.status)

    def gerarRelatorioNotas_csv(self):
        # Cria um arquivo csv com as notas dos alunos
        import csv

        with open("notas.csv", "w", newline="") as csvfile:
            fieldnames = [
                "id",
                "nota_1",
                "nota_2",
                "nota_3",
                "media_arit",
                "soma",
                "status",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            notas = self.selecionar_dados("notas")
            for nota in notas:
                writer.writerow(
                    {
                        "id": nota[0],
                        "nota_1": nota[1],
                        "nota_2": nota[2],
                        "nota_3": nota[3],
                        "media_arit": nota[4],
                        "soma": nota[5],
                        "status": nota[7],
                    }
                )


notas = Notas(30, 4.5, 8.9, 5.6, 22, 1, 0, 0, "")
# Inserindo dados no banco de dados

notas.retornarMediaArit()
notas.retornarSoma()
notas.retornarStatus()

colunas = [
    "id_nota",
    "nota_1",
    "nota_2",
    "nota_3",
    "media",
    "id_aluno",
    "id_disciplina",
    "status",
]

valores = [
    str(notas.id),
    str(notas.nota_1),
    str(notas.nota_2),
    str(notas.nota_3),
    str(notas.media_arit),
    str(notas.id_aluno),
    str(notas.id_disciplina),
    str(notas.status),
]

notas.inserir_dados("notas", colunas, valores)
# Exibição dos registros da tabela professor no banco de dados MySQL
print(notas.selecionar_dados("notas"))

notas.gerarRelatorioNotas_csv()  # Gera um arquivo csv com as notas dos alunos

notas.atualizar_dados(
    "notas", colunas, valores, "id_nota", 1
)  # Atualiza os dados da tabela professor no banco de dados MySQL

# Exclusão dos dados da tabela Aluno no banco de dados MySQL
notas.excluir_dados("notas", "id_nota", 1)

# Programa principal
if __name__ == "__main__":
    while True:
        print("\nBem-vindo ao sistema de gerenciamento de Notas dos Alunos!\n")
        print("Escolha uma das seguintes opções:\n")
        print("1 - Inserir dados no banco de dados")
        print("2 - Selecionar dados do banco de dados")
        print("3 - Excluir dados do banco de dados")
        print("4 - Atualizar dados do banco de dados")
        print("5 - Sair do programa")
        escolha = input("Digite o número da opção desejada: ")
        if escolha == "1":
            print("Deseja escolher inserir dados de qual tabela?")
            print("1 - Alunos")
            print("2 - Disciplinas")
            print("3 - Notas")
            escolha_tabela = input("Opção: ")
            if escolha_tabela == "1":
                matricula = int(input("Matrícula do aluno: "))
                nome = input("Nome do aluno: ")
                idade = input("Idade do aluno: ")
                curso = input("Curso do aluno: ")
                email = input("E-mail do aluno: ")
                telefone = input("Telefone do aluno: ")
                genero = input("Gênero do aluno: ")
                aluno = Alunos(matricula, nome, idade, curso, email, telefone, genero)
                colunas = [
                    "matricula",
                    "nome",
                    "idade",
                    "curso",
                    "email",
                    "telefone",
                    "sexo",
                ]
                valores = [
                    str(aluno.matricula),
                    str(aluno.nome),
                    str(aluno.idade),
                    str(aluno.curso),
                    str(aluno.email),
                    str(aluno.telefone),
                    str(aluno.sexo),
                ]
                aluno.inserir_dados("alunos", colunas, valores)
                print(aluno.selecionar_dados("alunos"))
            elif escolha_tabela == "2":
                id_disciplina = int(input("ID da disciplina: "))
                nome_disciplina = input("Nome da disciplina: ")
                carga_horaria = input("Carga horária da disciplina: ")
                descricao = input("Descrição da disciplina: ")
                valor = float(input("Valor da disciplina (R$): "))
                nota_corte = float(input("Nota de corte da disciplina: "))
                disciplina = Disciplinas(
                    id_disciplina,
                    nome_disciplina,
                    carga_horaria,
                    descricao,
                    valor,
                    nota_corte,
                )
                colunas = [
                    "id_disciplina",
                    "nome_disciplina",
                    "nota_corte",
                    "valor",
                    "descricao",
                    "carga_horaria",
                ]
                valores = [
                    str(disciplina.id_disciplina),
                    str(disciplina.nome_disciplina),
                    str(disciplina.nota_corte),
                    str(disciplina.valor),
                    str(disciplina.descricao),
                    str(disciplina.carga_horaria),
                ]
                disciplina.inserir_dados("disciplinas", colunas, valores)
                print(disciplina.selecionar_dados("disciplinas"))
            elif escolha_tabela == "3":
                id_nota = int(input("ID da nota: "))
                nota_1 = float(input("Nota 1: "))
                nota_2 = float(input("Nota 2: "))
                nota_3 = float(input("Nota 3: "))
                id_aluno = int(input("ID do aluno: "))
                id_disciplina = int(input("ID da disciplina: "))
                nota = Notas(
                    id_nota, nota_1, nota_2, nota_3, id_aluno, id_disciplina, 0, 0, ""
                )
                nota.retornarMediaArit()
                nota.retornarSoma()
                nota.retornarStatus()
                colunas = [
                    "id_nota",
                    "nota_1",
                    "nota_2",
                    "nota_3",
                    "media",
                    "id_aluno",
                    "id_disciplina",
                    "status",
                ]
                valores = [
                    str(nota.id),
                    str(nota.nota_1),
                    str(nota.nota_2),
                    str(nota.nota_3),
                    str(nota.media_arit),
                    str(nota.id_aluno),
                    str(nota.id_disciplina),
                    str(nota.status),
                ]
                nota.inserir_dados("notas", colunas, valores)
                print(nota.selecionar_dados("notas"))
            else:
                print("Opção inválida")
                break
        elif escolha == "2":
            print("Deseja escolher MOSTRAR TODOS dados de qual tabela?")
            print("1 - Alunos")
            print("2 - Disciplinas")
            print("3 - Notas")
            escolha_tabela = input("Opção: ")
            if escolha_tabela == "1":
                print(aluno.selecionar_dados("alunos"))
            elif escolha_tabela == "2":
                print(disciplina.selecionar_dados("disciplinas"))
            elif escolha_tabela == "3":
                print(notas.selecionar_dados("notas"))
                print("Deseja salvar dados em um arquivo csv? ")
                escolha_csv = input("Opção: Sim (1) ou Não (2): ")
                if escolha_csv == "1":
                    try:
                        aluno.selecionar_dados("alunos").to_csv(
                            "alunos.csv", index=False
                        )
                        disciplina.selecionar_dados("disciplinas").to_csv(
                            "disciplinas.csv", index=False
                        )
                        notas.selecionar_dados("notas").to_csv("notas.csv", index=False)
                        print("Dados exportados com sucesso!")

                        # Ler dados do arquivo csv
                        dados_alunos = pd.read_csv("alunos.csv")
                        dados_disciplinas = pd.read_csv("disciplinas.csv")
                        dados_notas = pd.read_csv("notas.csv")

                        # Gerar um dataframe de cada tabela seguindo os registros dos arquivos .csv
                        df_alunos = pd.DataFrame(aluno.selecionar_dados("alunos"))
                        df_disciplinas = pd.DataFrame(
                            disciplina.selecionar_dados("disciplinas")
                        )
                        df_notas = pd.DataFrame(notas.selecionar_dados("notas"))

                        # Verificar se os dados do dataframe são iguais aos dados do arquivo csv
                        if dados_alunos.equals(df_alunos):
                            print("Dados do arquivo csv e do dataframe são iguais!")
                        else:
                            print("Dados do arquivo csv e do dataframe são diferentes!")

                        if dados_disciplinas.equals(df_disciplinas):
                            print("Dados do arquivo csv e do dataframe são iguais!")
                        else:
                            print("Dados do arquivo csv e do dataframe são diferentes!")

                        if dados_notas.equals(df_notas):
                            print("Dados do arquivo csv e do dataframe são iguais!")
                        else:
                            print("Dados do arquivo csv e do dataframe são diferentes!")

                    except Exception as e:
                        print(f"Erro ao exportar dados: {e}")
                else:
                    continue
            else:
                print("Opção inválida")
                break
        elif escolha == "3":
            print("Deseja escolher qual tabela para excluir dados?")
            print("1 - Alunos")
            print("2 - Disciplinas")
            print("3 - Notas")
            escolha_tabela = input("Opção: ")
            if escolha_tabela == "1":
                id_aluno = int(input("ID do aluno: "))
                aluno.excluir_dados("alunos", "matricula", id_aluno)
            elif escolha_tabela == "2":
                id_disciplina = int(input("ID da disciplina: "))
                disciplina.excluir_dados("disciplinas", "id_disciplina", id_disciplina)
            elif escolha_tabela == "3":
                id_nota = int(input("ID da nota: "))
                nota.excluir_dados("notas", "id_nota", id_nota)
            else:
                print("Opção inválida")
                break
        elif escolha == "4":
            print("Deseja escolher qual tabela para atualizar dados?")
            print("1 - Alunos")
            print("2 - Disciplinas")
            print("3 - Notas")
            escolha_tabela = input("Opção: ")
            if escolha_tabela == "1":
                matricula = int(input("Matricula antiga do aluno: "))
                matricula_atualizada = input("Nova matricula: ")
                nome_aluno = input("Nome do aluno: ")
                idade_aluno = int(input("Idade do aluno: "))
                curso = input("Curso do aluno: ")
                email = input("E-mail do aluno: ")
                telefone = input("Telefone do aluno: ")
                genero = input("Gênero do aluno: ")
                aluno = Alunos(
                    matricula_atualizada,
                    nome_aluno,
                    idade_aluno,
                    curso,
                    email,
                    telefone,
                    genero,
                )
                colunas = [
                    "matricula",
                    "nome",
                    "idade",
                    "curso",
                    "email",
                    "telefone",
                    "sexo",
                ]
                valores = [
                    str(aluno.matricula),
                    str(aluno.nome),
                    str(aluno.idade),
                    str(aluno.curso),
                    str(aluno.email),
                    str(aluno.telefone),
                    str(aluno.sexo),
                ]
                aluno.atualizar_dados(
                    "aluno", colunas, valores, "matricula", aluno.matricula
                )
            elif escolha_tabela == "2":
                id_disciplina = int(input("ID da disciplina antiga: "))
                id_disciplina_atualizada = int(input("ID da disciplina nova: "))
                nome_disciplina = input("Nome da disciplina: ")
                carga_horaria = input("Carga horária da disciplina: ")
                descricao = input("Descrição da disciplina: ")
                valor = float(input("Valor da disciplina (R$): "))
                nota_corte = float(input("Nota de corte da disciplina: "))
                disciplina = Disciplinas(
                    id_disciplina_atualizada,
                    nome_disciplina,
                    carga_horaria,
                    descricao,
                    valor,
                    nota_corte,
                )
                colunas = [
                    "id_disciplina",
                    "nome_disciplina",
                    "nota_corte",
                    "valor",
                    "descricao",
                    "carga_horaria",
                ]
                valores = [
                    str(disciplina.id_disciplina),
                    str(disciplina.nome_disciplina),
                    str(disciplina.nota_corte),
                    str(disciplina.valor),
                    str(disciplina.descricao),
                    str(disciplina.carga_horaria),
                ]
                disciplina.atualizar_dados(
                    "disciplinas", colunas, valores, "id_disciplina", id_disciplina
                )
                print(disciplina.selecionar_dados("disciplinas"))
            elif escolha_tabela == "3":
                id_nota = int(input("ID da nota antiga do aluno: "))
                id_nota_atualizada = int(input("ID da nota nova do aluno: "))
                nota_1 = float(input("Nota 1: "))
                nota_2 = float(input("Nota 2: "))
                nota_3 = float(input("Nota 3: "))
                id_aluno = int(input("ID do aluno: "))
                id_disciplina = int(input("ID da disciplina: "))
                nota = Notas(
                    id_nota_atualizada,
                    nota_1,
                    nota_2,
                    nota_3,
                    id_aluno,
                    id_disciplina,
                    0,
                    0,
                    "",
                )
                nota.retornarMediaArit()
                nota.retornarSoma()
                nota.retornarStatus()
                colunas = [
                    "id_nota",
                    "nota_1",
                    "nota_2",
                    "nota_3",
                    "media",
                    "id_aluno",
                    "id_disciplina",
                    "status",
                ]
                valores = [
                    str(nota.id),
                    str(nota.nota_1),
                    str(nota.nota_2),
                    str(nota.nota_3),
                    str(nota.media_arit),
                    str(nota.id_aluno),
                    str(nota.id_disciplina),
                    str(nota.status),
                ]
                nota.atualizar_dados("notas", colunas, valores, "id_nota", id_nota)
                print(nota.selecionar_dados("notas"))
            else:
                print("Opção inválida")
                continue
        else:
            print("Fim da execução do programa!")
            break
