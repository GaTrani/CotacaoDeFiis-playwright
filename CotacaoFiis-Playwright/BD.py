import sqlite3


#CRIAR DATABASE
database = sqlite3.connect('BancoDadosFii.db')
c = database.cursor()

def criarTabela():
    database.execute(''' CREATE TABLE IF NOT EXISTS BDFii(
                            ATIVO VARCHAR(7),
                            DATABA INT NOT NULL,
                            DATAPAGTO INT NOT NULL,
                            COTA FLOAT NOT NULL,
                            PERCENT FLOAT NOT NULL,
                            DIVIDENDO FLOAT NOT NULL) 
                            ''')
    # APRLICA AS ALTERAÇOES NA TABELA
    database.commit()

def inserirat(ATIVO, DATABA, DATAPAGTO, COTA, PERCENT, DIVIDENDO):
    c.execute(''' INSERT into BDFii(ATIVO, DATABA, DATAPAGTO, COTA, PERCENT, DIVIDENDO) VALUES(?, ?, ?, ?, ?, ?)''',
              (ATIVO, DATABA, DATAPAGTO, COTA, PERCENT, DIVIDENDO))
    database.commit()

def deletarat(x):
    c.execute('''delete from BDFii where DATABA=?''', x)
    database.commit()

def lerdadosat():
    c = database.cursor()
    c.execute('''SELECT ATIVO from BDFii''')
    cat = c.fetchall() #pesquisa na tabela inteira os dados
    database.commit()
    return cat
