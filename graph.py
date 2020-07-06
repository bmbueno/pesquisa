import sqlite3
import igraph

color_dict = {"clt": "pink", "estudante": "red",
              "servidor": "blue", "autônomo": "black", "desempregado": "yellow"}
q4 = {'mascaras': [], 'luvas': [], 'alcoolGel': [],
      'sabao': [], 'nenhumAcesso': [], 'nenhumInteresse': []}
q6 = {'normal': [], 'ansioso': [], 'depressivo': [], 'preocupado': []}
q7 = {'clt': [], 'autônomo': [], 'estudante': [],
      'servidor': [], 'desempregado': []}
checkBoxes = {'q4': q4, 'q6': q6, 'q7': q7}
nV = 0
nA = 0

# dados uma lista de vertices e um atributo cria arestas com este atributo entre cada elemento da lista de vertices
def connectVertices(v, color):
    global nA
    for i in range(1, len(v)):
        for j in range(i-1, -1, -1):
            g.add_edges([(v[i], v[j])])
            # print(str(v[i]) + '  -  ' + str(v[j]))
            # g.es[nA][attr] = True
            g.es[nA]['color'] = color
            nA = nA + 1
        # print(v[i])


# dados um atributo/resposta e o numero de uma questao cria uma lista de vertices de mesmo atributo (resposta) para dada questao
def listVertices(attr, quest):
    if(g.vs[nV][attr]):
        checkBoxes[quest][attr].append(nV)


g = igraph.Graph(0)


dbConec = sqlite3.connect("pesquisaMin.db")
db = dbConec.cursor()

db.execute("""SELECT * FROM entrevistado;""")

entrevistados = db.fetchall()


for row in entrevistados:
    # print(row[0])

    g.add_vertices(1)
    g.vs[nV]['idade'] = row[2]

    g.vs[nV]['clt'] = 'CLT' in row[3]
    g.vs[nV]['estudante'] = 'Estudante' in row[3]
    g.vs[nV]['autônomo'] = 'Autônomo' in row[3]
    g.vs[nV]['servidor'] = 'Servidor' in row[3]
    g.vs[nV]['desempregado'] = 'Desempregado' in row[3]

    g.vs[nV]['8'] = row[4]
    g.vs[nV]['9'] = row[5]
    # g.vs[nV]['essencial'] = 'Sim' in row[4]
    # g.vs[nV]['perfilSocio'] = str(row[5])

    for attr in checkBoxes['q7']:
        listVertices(attr, 'q7')

    answers = db.execute(
        """SELECT * FROM resposta WHERE entrevistadoID=(?) ;""", [str(row[0])])

    for answer in answers:
        if(answer[1] != 4 and answer[1] != 6):
            g.vs[nV][str(answer[1])] = answer[3]
        elif(answer[1] == 4):
            g.vs[nV]['mascaras'] = 'Máscaras' in answer[3]
            g.vs[nV]['luvas'] = 'Luvas' in answer[3]
            g.vs[nV]['alcoolGel'] = 'gel' in answer[3]
            g.vs[nV]['sabao'] = 'Sabão' in answer[3]
            g.vs[nV]['nenhumAcesso'] = 'acesso' in answer[3]
            g.vs[nV]['nenhumInteresse'] = 'interesse' in answer[3]

            for attr in checkBoxes['q4']:
                listVertices(attr, 'q4')
        else:
            g.vs[nV]['normal'] = 'Normal' in answer[3]
            g.vs[nV]['ansioso'] = 'Ansioso' in answer[3]
            g.vs[nV]['depressivo'] = 'Depressivo' in answer[3]
            g.vs[nV]['preocupado'] = 'Preocupado' in answer[3]

            for attr in checkBoxes['q6']:
                listVertices(attr, 'q6')

    nV = nV+1

for attr in q7:
    # print(attr)
    connectVertices(q7[attr], color_dict[attr])


# g.vs["label"] = g.vs['9']
# g.es["label"] = g.es["estudante"]

# print(checkBoxes['q6'])
# print(g.vs['mascaras'])


layout = g.layout("circle")
igraph.plot(g)
# print(db.lastrowid)

dbConec.close()
