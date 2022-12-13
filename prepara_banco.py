import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='88428666'
        )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)


cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `projetos`;")

cursor.execute("CREATE DATABASE `projetos`;")

cursor.execute("USE `projetos`;")

TABLES = {}
TABLES['Projetos'] = ('''
      CREATE TABLE `Projetos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `linguagem` varchar(40) NOT NULL,
      `descricao` varchar(50) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')



usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Felipe", "Bipe", generate_password_hash("04061999").decode('utf-8')),
      ("Lucas", "Luly", generate_password_hash("08071991").decode('utf-8')),
      ("Julia", "Juju", generate_password_hash("09072001").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from projetos.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

projetos_sql = 'INSERT INTO projetos (nome, linguagem, descricao) VALUES (%s, %s, %s)'
projetos = [
    ('Site Flask', 'Python', 'Web Development'),
    ('Pandas', 'Python', 'Datascience'),
    ('Django', 'Python', 'Web Development')

]

cursor.executemany(projetos_sql, projetos)
print(' -------------  Projetos:  -------------')
for projeto in cursor.fetchall():
    print(projeto[1])


conn.commit()
cursor.close()
conn.close()