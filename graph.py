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
            g.es[nA]['color'] = color
            nA = nA + 1
    


# dados um atributo/resposta e o numero de uma questao cria uma lista de vertices de mesmo atributo (resposta) para dada questao
# para questoes que nao possuem multiplas respostas
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


    for attr in checkBoxes['q7']:
        listVertices(attr, 'q7')

    answers = db.execute(
        """SELECT * FROM resposta WHERE entrevistadoID=(?) ;""", [str(row[0])])

    for answer in answers:
        if(answer[1] != 4 and answer[1] != 6):
            g.vs[nV]['Q' + str(answer[1])] = answer[3]
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

# INSTRUÇOES:
# Para criar arestas no grafo com respostas de questões com multiplas respostas basta utilizar g.vs.select(atributo=True)
# para cada opção da resposta, no caso já existem dicionarios definidos com estas opções e já previamente preenchidos com
# uma lista de vértices nos quais as respostas são true, basta liga-los utilizando a funcao connectVertices, exemplo:
for attr in q7:
    connectVertices(q7[attr], color_dict[attr])
                    # o dicionario color_dict é alterável de acordo com a preferencia do usuario

# Para criar arestas com respostas das demais questoes deve-se utilizar a funcao pronta do igraph "select" pegar os indices
# dos vertices que correspondem a resposta requerida e utilizar novamente a funcao connectVertives, exemplo:

a = g.vs.select(Q2='Redes sociais, amigos, familiares, grupos de whats.')
print(a.indices)

connectVertices(a.indices, 'orange')

layout = g.layout("circle")
igraph.plot(g)

dbConec.close()
