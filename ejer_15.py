# Se requiere implementar un grafo para almacenar las siete maravillas arquitectónicas modernas y 
#naturales del mundo, para lo cual se deben tener en cuenta las siguientes actividades:
# a) de cada una de las maravillas se conoce su nombre, país de ubicación (puede ser más de 
#uno en las naturales) y tipo (natural o arquitectónica);
# b) cada una debe estar relacionada con las otras seis de su tipo, para lo que se debe almacenar 
#la distancia que las separa;
# c) hallar el árbol de expansión mínimo de cada tipo de las maravillas;
# d) determinar si existen países que dispongan de maravillas arquitectónicas y naturales;
# e) determinar si algún país tiene más de una maravilla del mismo tipo;
# f) deberá utilizar un grafo no dirigido.

from lista import Lista as ListaArista
from cola import Cola
from pila import Pila
from heap_min import Heap
from random import randint

class Arista:

    def __init__(self, vertice, peso):
        self.vertice = vertice
        self.peso = peso

    def __str__(self):
        return f"{self.vertice} {self.peso}"

def criterio_comparacion(value, criterio):
    if isinstance(value, (int, str, bool)):
        return value
    else:
        dic_atributos = value.__dict__
        if criterio in dic_atributos:
            return dic_atributos[criterio]
        else:
            print('no se puede ordenar por este criterio')

class Grafo():

    def __init__(self, dirigido=True):
        self.__elements = []
        self.dirigido = dirigido

    def insert_vertice(self, value, criterio=None):
        if len(self.__elements) == 0 or criterio_comparacion(value, criterio) >= criterio_comparacion(self.__elements[-1][0], criterio):
            self.__elements.append([value, ListaArista(), False])
        elif criterio_comparacion(value, criterio) < criterio_comparacion(self.__elements[0][0], criterio):
            self.__elements.insert(0, [value, ListaArista(), False])
        else:
            index = 1
            while criterio_comparacion(value, criterio) >= criterio_comparacion(self.__elements[index][0], criterio):
                index += 1
            self.__elements.insert(index, [value, ListaArista(), False])

    def insert_arist(self, vertice_ori, vertice_des, peso, criterio_vertice=None, criterio_arista='vertice'):
        origen = self.search_vertice(vertice_ori, criterio_vertice)
        destino = self.search_vertice(vertice_des, criterio_vertice)
        if origen is not None and destino is not None:
            self.get_element_by_index(origen)[1].insert(Arista(vertice_des, peso), criterio_arista)
            if not self.dirigido:
                self.get_element_by_index(destino)[1].insert(Arista(vertice_ori, peso), criterio_arista)

    def search_vertice(self, search_value, criterio=None):
        position = None
        first = 0
        last = self.size() - 1
        while (first <= last and position == None):
            middle = (first + last) // 2
            if search_value == criterio_comparacion(self.__elements[middle][0], criterio):
                position = middle
            elif search_value > criterio_comparacion(self.__elements[middle][0], criterio):
                first = middle + 1
            else:
                last = middle - 1
        return position

    def delete_vertice(self, value, criterio=None):
        return_value = None
        pos = self.search_vertice(value, criterio)
        if pos is not None:
            return_value = self.__elements.pop(pos)
            for vertice in self.__elements:
                vertice[1].delete(value, 'vertice')

        return return_value

    def delete_arista(self, origen, destino):
        pos_origen = self.search_vertice(origen)
        if pos_origen is not None:
            ver_origen = self.get_element_by_index(pos_origen)
            delete = ver_origen[1].delete(destino, 'vertice')
            if not self.dirigido:
                pos_destino = self.search_vertice(destino)
                if pos_destino is not None:
                    ver_destino = self.get_element_by_index(pos_destino)
                    ver_destino[1].delete(origen, 'vertice')
            return delete

    def size(self):
        return len(self.__elements)

    def barrido(self):
        for value in self.__elements:
            print(value[0])
            print('Arsitas --------------------')
            value[1].barrido()
            print()
    
    def get_element_by_index(self, index):
        return_value = None
        if index >= 0 and index < self.size():
            return_value = self.__elements[index]
        return return_value

    def is_adyacent(self, origen, destino):
        result = False
        pos_origen = self.search_vertice(origen)
        if pos_origen is not None:
            ver_origen = self.get_element_by_index(pos_origen)
            arista = ver_origen[1].search(destino, 'vertice')
            result = True if arista is not None else False
        return result

    def adyacents(self, origen):
        pos_origen = self.search_vertice(origen)
        if pos_origen is not None:
            ver_origen = self.get_element_by_index(pos_origen)
            ver_origen[1].barrido()

    def mark_as_not_visited(self):
        for vertice in self.__elements:
            vertice[2] = False

    def deep_list(self, poscion=0):
        origen = self.get_element_by_index(poscion)
        if origen is not None:
            if not origen[2]:
                origen[2] = True
                print(origen[0])
                adjacentes = origen[1]
                for index in range(adjacentes.size()):
                    arista = adjacentes.get_element_by_index(index).vertice
                    vertice_adjacente = self.search_vertice(arista)
                    if vertice_adjacente is not None:
                        adjacente = self.get_element_by_index(vertice_adjacente)
                        if not adjacente[2]:
                            self.deep_list(poscion=vertice_adjacente)
                
    def amplitude_list(self, posicion=0):
        origen = self.get_element_by_index(posicion)
        if origen is not None:
            cola_pendientes = Cola()
            cola_pendientes.arrive(origen)
            while not cola_pendientes.size() == 0:
                vertice = cola_pendientes.atention()
                if not vertice[2]:
                    vertice[2] = True
                    print(vertice[0])
                    adjacentes = vertice[1]
                    for index in range(adjacentes.size()):
                        arista = adjacentes.get_element_by_index(index).vertice
                        vertice_adjacente = self.search_vertice(arista)
                        if vertice_adjacente is not None:
                            adjacente = self.get_element_by_index(vertice_adjacente)
                            if not adjacente[2]:
                                cola_pendientes.arrive(adjacente)
            
    def has_path(self, origen, destino, criterio=None):
        result = False
        print(origen)
        origen = self.search_vertice(origen, criterio=criterio)
        if origen is not None:
            vertice_origen = self.get_element_by_index(origen)
            if not vertice_origen[2]:
                vertice_origen[2] = True
                # print(vertice_origen[0])
                adjacentes = vertice_origen[1]
                pos_destino = adjacentes.search(destino, 'vertice')
                if pos_destino is not None:
                    result = True
                    return result
                for index in range(adjacentes.size()):
                    arista = adjacentes.get_element_by_index(index).vertice
                    vertice_adjacente = self.search_vertice(arista, criterio=criterio)
                    if vertice_adjacente is not None:
                        adjacente = self.get_element_by_index(vertice_adjacente)
                        if not adjacente[2]:
                            result = self.has_path(criterio_comparacion(adjacente[0], 'nombre'), destino, criterio=criterio)
        return result
    
mi_grafo = Grafo(dirigido=False)

class Maravilla:
    def __init__(self, nombre, pais, tipo):
        self.nombre = nombre
        self.pais = pais
        self.tipo = tipo
    
    def __str__(self):
        return f'{self.nombre}-{self.pais}-{self.tipo}'

    def paises_con_maravillas(self, tipo):
        paises = set()
        for maravilla in self.vertices:
            if maravilla.tipo == tipo:
                paises.add(maravilla.pais)
        return paises
    
    def paises_con_mas_de_una_maravilla_del_mismo_tipo(self, tipo):
        maravillas_por_pais = {}
        for maravilla in self.vertices:
            if maravilla.tipo == tipo:
                if maravilla.pais in maravillas_por_pais:
                    maravillas_por_pais[maravilla.pais].append(maravilla.nombre)
                else:
                    maravillas_por_pais[maravilla.pais] = [maravilla.nombre]

        paises_con_mas_de_una_maravilla = [pais for pais, maravillas in maravillas_por_pais.items() if len(maravillas) > 1]
        return paises_con_mas_de_una_maravilla

    def kruskal(self):
        def buscar_en_bosque(bosque, buscado):
            for index, arbol in enumerate(bosque):
                print(buscado, arbol)
                if buscado in arbol:
                    return index

        bosque = []
        aristas = Heap()
        for index in range(self.size()):
            vertice = self.get_element_by_index(index)
            bosque.append(criterio_comparacion(vertice[0], 'nombre'))
            aristas_adjacentes = vertice[1]
            for i in range(aristas_adjacentes.size()):
                arista = aristas_adjacentes.get_element_by_index(i)
                aristas.arrive([vertice[0], arista.vertice], arista.peso)

        while len(bosque) > 1 and aristas.size() > 0:
            arista = aristas.atention()
            origen = buscar_en_bosque(bosque, criterio_comparacion(arista[1][0], 'nombre'))
            destino = buscar_en_bosque(bosque, criterio_comparacion(arista[1][1], 'nombre'))
            if origen is not None and destino is not None:
                if origen != destino:
                    if origen > destino:
                        vertice_ori = bosque.pop(origen)
                        vertice_des = bosque.pop(destino)
                    else:
                        vertice_des = bosque.pop(destino)
                        vertice_ori = bosque.pop(origen)

                    if '-' not in vertice_ori and '-' not in vertice_des:
                        bosque.append(f'{vertice_ori}-{vertice_des}-{arista[0]}')
                    elif '-' not in vertice_des:
                        bosque.append(vertice_ori+';'+f'{arista[1][0]}-{vertice_des}-{arista[0]}')
                    elif '-' not in vertice_ori:
                        bosque.append(vertice_des+';'+f'{vertice_ori}-{arista[1][1]}-{arista[0]}')
                    else:
                        bosque.append(vertice_ori+';'+vertice_des+';'+f'{arista[1][0]}-{arista[1][1]}-{arista[0]}')

        return bosque


mi_grafo.insert_vertice(Maravilla("Gran Muralla", 'China', 'arquitectonica'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Machu Picchu", 'Peru', 'arquitectonica'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Chichén Itzá", 'México', 'arquitectónica'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Coliseo Romano", 'Italia', 'arquitectónica'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Cristo Redentor", 'Brasil', 'arquitectónica'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Petra", 'Jordania', 'arquitectónica'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Taj Mahal", 'India', 'arquitectónica'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Bahía de Ha Long", 'Vietnam', 'natural'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Isla Jeju", 'Corea del Sur', 'natural'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Parque Nacional de Komodo", 'Indonesia', 'natural'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Montaña de la Mesa", 'Sudáfrica', 'natural'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Amazonia", 'Varios países', 'natural'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Cataratas del Iguazú", 'Argentina/Brasil', 'natural'),criterio='nombre'),
mi_grafo.insert_vertice(Maravilla("Río Subterráneo de Puerto Princesa", 'Filipinas', 'natural'),criterio='nombre'),

mi_grafo.insert_arista("Chichén Itzá", "Gran Muralla China", 9000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Chichén Itzá", "Petra", 8500,criterio_vertice='nombre'),
mi_grafo.insert_arista("Chichén Itzá", "Taj Mahal", 7500,criterio_vertice='nombre'),
mi_grafo.insert_arista("Coliseo Romano", "Gran Muralla China", 7500,criterio_vertice='nombre'),
mi_grafo.insert_arista("Coliseo Romano", "Cristo Redentor", 4000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Coliseo Romano", "Petra", 11000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Coliseo Romano", "Taj Mahal", 10000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Gran Muralla China", "Cristo Redentor", 9500,criterio_vertice='nombre'),
mi_grafo.insert_arista("Gran Muralla China", "Petra", 11000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Gran Muralla China", "Taj Mahal", 12000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Cristo Redentor", "Petra", 5000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Cristo Redentor", "Taj Mahal", 9000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Petra", "Taj Mahal", 6000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Isla Jeju", "Parque Nacional de Komodo", 2000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Isla Jeju", "Montaña de la Mesa", 9500,criterio_vertice='nombre'),
mi_grafo.insert_arista("Isla Jeju", "Amazonia", 10000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Isla Jeju", "Cataratas del Iguazú", 11000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Isla Jeju", "Río Subterráneo de Puerto Princesa", 12000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Parque Nacional de Komodo", "Montaña de la Mesa", 8000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Parque Nacional de Komodo", "Amazonia", 9500,criterio_vertice='nombre'),
mi_grafo.insert_arista("Parque Nacional de Komodo", "Cataratas del Iguazú", 7000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Parque Nacional de Komodo", "Río Subterráneo de Puerto Princesa", 10000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Montaña de la Mesa", "Amazonia", 7000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Montaña de la Mesa", "Cataratas del Iguazú", 6000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Montaña de la Mesa", "Río Subterráneo de Puerto Princesa", 8000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Amazonia", "Cataratas del Iguazú", 4000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Amazonia", "Río Subterráneo de Puerto Princesa", 6000,criterio_vertice='nombre'),
mi_grafo.insert_arista("Cataratas del Iguazú", "Río Subterráneo de Puerto Princesa", 3500,criterio_vertice='nombre')

# Hallar el arbol de expansión mínima
bosque, acu = mi_grafo.kruskal()
for arbol in bosque:
    print('arbol')
    for nodo in arbol.split(';'):
        print(nodo)
print(f'Distancia total del árbol de expansión mínima: {acu}')

# Determinar si existen países que dispongan de maravillas arquitectónicas y naturales
arq = set()
nat = set()
for maravilla in mi_grafo.__elements:
    if maravilla[0].tipo == 'arquitectonica':
        arq.add(maravilla[0].pais)
    elif maravilla[0].tipo == 'natural':
        nat.add(maravilla[0].pais)

paises_con_arquitectonicas_y_naturales = arq.intersection(nat)
if paises_con_arquitectonicas_y_naturales:
    print(f'Países con maravillas arquitectónicas y naturales: {paises_con_arquitectonicas_y_naturales}')
else:
    print('No hay países con maravillas arquitectónicas y naturales.')

# Determinar si algún país tiene más de una maravilla del mismo tipo
for tipo in ['arquitectonica', 'natural']:
    paises_con_mas_de_una_maravilla = set()
    for maravilla in mi_grafo.__elements:
        if maravilla[0].tipo == tipo:
            paises_con_mas_de_una_maravilla.update(maravilla[0].paises_con_mas_de_una_maravilla_del_mismo_tipo(tipo))
    if paises_con_mas_de_una_maravilla:
        print(f'Países con más de una maravilla {tipo}: {paises_con_mas_de_una_maravilla}')
    else:
        print(f'No hay países con más de una maravilla {tipo}.')
