import csv
import sqlite3

with open('Pesquisa1.csv') as file:
    fileReader = csv.reader(file, delimiter=',')


    dbConec = sqlite3.connect("pesquisaMin.db")
    db = dbConec.cursor()
    
    # db.execute('CREATE TABLE perfilSocioEconomico( id INTEGER PRIMARY KEY AUTOINCREMENT, resposta VARCHAR(100) NOT NULL);')
    # db.execute("""INSERT INTO perfilSocioEconomico (resposta) VALUES ('De R$ 522,50 a R$ 1045,00;');""")
    # db.execute("""INSERT INTO perfilSocioEconomico (resposta) VALUES ('Ate R$ 522,50;');""")
    # db.execute("""INSERT INTO perfilSocioEconomico (resposta) VALUES ('De R$ 1045,00 a R$ 3135,00;');""")
    # db.execute("""INSERT INTO perfilSocioEconomico (resposta) VALUES ('Acima de R$ 3135,00;');""")
  
  
    db.execute('CREATE TABLE questao( id INTEGER PRIMARY KEY AUTOINCREMENT, descricao VARCHAR(100) );')
    db.execute('CREATE TABLE entrevistado(id INTEGER PRIMARY KEY AUTOINCREMENT, data VARCHAR(100) NOT NULL, idade INTEGER NOT NULL, ocupacao VARCHAR(100) NOT NULL, trabalhoEssencial VARCHAR(3) NOT NULL, perfilSocioEconomico VARCHAR(50) NOT NULL);')
    #db.execute('CREATE TABLE entrevistado(id INTEGER PRIMARY KEY AUTOINCREMENT,  data VARCHAR(100) NOT NULL, idade VARCHAR(2) NOT NULL, ocupacao VARCHAR(100) NOT NULL, trabalhoEssencial VARCHAR(3) NOT NULL, perfilSocioEconomicoID INTEGER, FOREIGN KEY (perfilSocioEconomicoID) REFERENCES perfilSocioEconomico(id));')
    db.execute('CREATE TABLE resposta(id INTEGER PRIMARY KEY AUTOINCREMENT, questaoID INTEGER,  entrevistadoID INTEGER, resposta VARCHAR(100) NOT NULL, FOREIGN KEY (questaoID) REFERENCES questao(id), FOREIGN KEY (entrevistadoID) REFERENCES entrevistado(id));')
    
    db.execute("""INSERT INTO questao (descricao) VALUES ('Qual sua idade?');""")
    db.execute("""INSERT INTO questao (descricao) VALUES ('Qual o seu meio principal de informação?');""")
    db.execute("""INSERT INTO questao (descricao) VALUES ('Como está sua rotina? ');""")
    db.execute("""INSERT INTO questao (descricao) VALUES ('Tem usado quais utensílios de prevenção indicados contra o coronavírus?');""")
    db.execute("""INSERT INTO questao (descricao) VALUES ('É a favor do isolamento social para contenção do vírus ? ');""")
    db.execute("""INSERT INTO questao (descricao) VALUES ('Como você está se sentindo neste momento de pandemia?');""")
    db.execute("""INSERT INTO questao (descricao) VALUES ('Qual(is) sua(s) ocupação(ões)? ');""")
    db.execute("""INSERT INTO questao (descricao) VALUES ('É/São em um serviço considerado essencial?');""")
    db.execute("""INSERT INTO questao (descricao) VALUES ('Qual sua renda mensal per capita antes da pandemia do Coronavírus?');""")
    db.execute("""INSERT INTO questao (descricao) VALUES ('Você teve a redução desta renda durante a pandemia? ');""")


    dbConec.commit()
    print( db.lastrowid)

    next(fileReader)

    for row in fileReader:
        try:
            int(row[1]) # para validacao da idade 
            db.execute("""INSERT INTO entrevistado (data, idade, ocupacao, trabalhoEssencial, perfilSocioEconomico) VALUES (?,?,?,?,?);""", (row[0], row[1], row[7], row[8], row[9]))
            idEntrevistado = db.lastrowid
            db.execute("""INSERT INTO resposta (questaoID, entrevistadoID, resposta) VALUES (?,?,?);""", (2, idEntrevistado, row[2]))
            db.execute("""INSERT INTO resposta (questaoID, entrevistadoID, resposta) VALUES (?,?,?);""", (3, idEntrevistado, row[3]))
            db.execute("""INSERT INTO resposta (questaoID, entrevistadoID, resposta) VALUES (?,?,?);""", (4, idEntrevistado, row[4]))
            db.execute("""INSERT INTO resposta (questaoID, entrevistadoID, resposta) VALUES (?,?,?);""", (5, idEntrevistado, row[5]))
            db.execute("""INSERT INTO resposta (questaoID, entrevistadoID, resposta) VALUES (?,?,?);""", (6, idEntrevistado, row[6]))
            db.execute("""INSERT INTO resposta (questaoID, entrevistadoID, resposta) VALUES (?,?,?);""", (10, idEntrevistado, row[10]))
            dbConec.commit()
        except:
            continue
        
    dbConec.close()

