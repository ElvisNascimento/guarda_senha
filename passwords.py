import sqlite3

conn = sqlite3.connect('passwords.db')

cursor = conn.cursor()

MASTER_PASSWORD = "123456"

senha = input("Insira sua senha master: ")
if senha != MASTER_PASSWORD:
    print("Senha Invalida Encerrando ... ")
    exit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS master (
    username TEXT NOT NULL,
    master_password TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
''')

def menu():
    print("******************************")
    print("* i : inserir nova senha     *")
    print("* l : listar serviços salvos *")
    print("* r : recuperar uma senha    *")
    print("* s : sair                   *")
    print("******************************")

def get_password(service):
    cursor.execute(f'''
        SELECT username, password FROM users
        WHERE service = '{service}'    
    ''')

    if cursor.rowcount == 0:
        print("Serviço não cadastrado (use 'l' para verificar os serviços).")
    else:
        for user in cursor.fetchall():
            print(user)

def insert_service(conn, service, username, password):
    # Verifica se o serviço já existe no banco de dados
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    if cursor.fetchone():
        print(f"O usuario {username} já está cadastrado.")
        return

    # Insere o novo registro no banco de dados
    cursor.execute(f"INSERT INTO users (service, username, password) VALUES ('{service}', '{username}', '{password}')")
    conn.commit()
    print(f"Senha do usuario {username} no serviço {service} cadastrada com sucesso.")

def show_services():
    cursor.execute('''
        SELECT service FROM users;
    ''')
    for service in cursor.fetchall():
        print (service)

while True:
    menu()
    op = input("O que deseja fazer? ")
    if op not in ['l', 'i', 'r', 's']:
        print("Opcao invalida!")
        continue
    if op == 's':
        break

    if op == 'i':
        service = input('Qual o nome do serviço? ')
        username = input('Qual o nome do usuario? ')
        password = input('Qual a senha ? ')
        insert_service(conn, service, username, password)

    if op == 'l':
        show_services()

    if op == 'r':
        service = input('Qual o serviço que voce quer ver a senha? ')
        get_password(service)

conn.close()
