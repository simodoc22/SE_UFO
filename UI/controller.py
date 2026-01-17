import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        set_year = self._model.get_year()
        for i in set_year:
            self._view.dd_year.options.append(ft.DropdownOption(f"{i}"))
            self._view.update()

    def inserisci_forma(self,valore):
        lista_forme= self._model.get_forma(valore)
        for i in lista_forme:
            self._view.dd_shape.options.append(ft.DropdownOption(f"{i}"))
            self._view.update()


    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        valore = self._view.dd_shape.value
        valore2=self._view.dd_year.value
        self._model.crea_grafo(valore,valore2)
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"numero nodi = {self._model.G.number_of_nodes()} numero archi = {self._model.G.number_of_edges()}"))
        for node in self._model.G.nodes():
            conto = 0
            vicini = self._model.G.neighbors(node)
            for i in vicini:
                peso = self._model.G[node][i]['weight']
                conto += peso
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"{node}: {conto}"))
        self._view.update()



    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        self._model.get_best_path()
        lista_best = self._model.lista_best
        tupla_best = self._model.tupla_best
        distanza = self._model.distanza_best
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"distanza percorso massimo = {distanza}"))
        self._view.update()
        for i in tupla_best:
            nodo1 = i[0]
            nodo2= i[1]
            peso = i[2]
            dist= i[3]
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f"{nodo1}-->{nodo2} weight = {peso} distanza = {dist}"))
            self._view.update()