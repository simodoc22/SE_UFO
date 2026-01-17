from database.dao import DAO
from datetime import datetime
import networkx as nx
from geopy import distance
class Model:
    def __init__(self):
        self.Dao = DAO()
        self.lista_avvistamenti= self.Dao.read_sighting()
        self.G = nx.Graph()
        self.dizionario_stati = {}
        self.stati = self.Dao.read_state()
        for i in self.stati:
            self.dizionario_stati[i.id]=i
        self.dizionario_avvistamenti_per_paese= {}
        self.lista_best = []
        self.tupla_best= []
        self.distanza_best= 0



    def get_year(self):
        insieme = set()
        for i in self.lista_avvistamenti:
            date = i.s_datetime
            if i.s_datetime.year <=2014 and i.s_datetime.year>=1910:
                insieme.add(i.s_datetime.year)
        lista = []
        for i in insieme:
            lista.append(i)

        return sorted(lista)

    def get_forma(self,value):
        insieme  =set()
        for i in self.lista_avvistamenti:
            if i.s_datetime.year == int(value):
                insieme.add(i.shape)
        lista=[]
        for i in insieme:
            lista.append(i)

        return lista

    def crea_grafo(self,shape,anno):
        self.calcola_avvistamenti(shape,anno)
        for i in self.stati:
            self.G.add_node(i.id)
        stati_confinanti = self.Dao.read_neighbors()
        for i in stati_confinanti:
            stato1= i[0]
            stato2= i[1]
            if stato1 != stato2:
                peso = self.search_peso(stato1, stato2)
                self.G.add_edge(stato1,stato2,weight=peso)


    def search_peso(self,stato1,stato2):
        conto = 0
        conto1=0
        conto2=0
        try:
            conto1= self.dizionario_avvistamenti_per_paese[stato1.lower()]
        except KeyError:
            pass
        try:
            conto2= self.dizionario_avvistamenti_per_paese[stato2.lower()]
        except KeyError:
            pass
        conto = conto1 + conto2
        return conto


    def calcola_avvistamenti(self,shape,anno):
        for i in self.lista_avvistamenti:
            stato_id = i.state
            if i.s_datetime.year==int(anno) and i.shape==shape:
                if stato_id not in self.dizionario_avvistamenti_per_paese:
                    self.dizionario_avvistamenti_per_paese[stato_id]=1
                else:
                    self.dizionario_avvistamenti_per_paese[stato_id]+=1

    def get_best_path(self):
        for node in self.G.nodes():
            distanza = 0
            lista_parziale = []
            tupla_parziale =[]
            starting_node = node
            peso_precedente=0
            self.ricorsione(distanza,lista_parziale,tupla_parziale,starting_node,peso_precedente)




    def ricorsione(self,distanza,lista_parziale,tupla_parziali,starting_node,peso_precedente):


        lista_parziale.append(starting_node)

        vicini = list(self.G.neighbors(starting_node))
        if self.controllo_vicini(vicini,starting_node,peso_precedente,lista_parziale):
            if distanza>self.distanza_best:
                self.lista_best=lista_parziale.copy()
                self.distanza_best=distanza
                self.tupla_best=tupla_parziali.copy()
                return

        else:
            for i in vicini:
                peso = self.G[i][starting_node]['weight']
                if peso<= peso_precedente or i in lista_parziale:
                    continue
                lista_parziale.append(i)
                dist= distance.geodesic((self.dizionario_stati[starting_node].lat, self.dizionario_stati[starting_node].lng), (self.dizionario_stati[i].lat, self.dizionario_stati[i].lng)).km
                distanza1= distanza+dist
                tupla_parziali.append((starting_node,i,peso,dist))
                self.ricorsione(distanza1,lista_parziale,tupla_parziali,i,peso)
            lista_parziale.pop()
            tupla_parziali.pop()

    def controllo_vicini(self,vicini,staring_node,peso_precedente,lista_parziale):
        lista = []
        for i in vicini:
            peso = self.G[i][staring_node]['weight']
            if peso>peso_precedente and i not in lista_parziale:
                lista.append(i)
        if len(lista)==0:
            return True
        else:
            return False






























