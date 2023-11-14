# Implementar sobre un grafo no dirigido los algoritmos necesario para dar solución a las siguientes tareas:
# a) cada vértice representar un ambiente de una casa: cocina, comedor, cochera, quincho, 
#baño 1, baño 2, habitación 1, habitación 2, sala de estar, terraza, patio;
# b) cargar al menos tres aristas a cada vértice, y a dos de estas cárguele cinco, el peso de la arista es la distancia entre los ambientes, se debe cargar en metros;
# c) obtener el árbol de expansión mínima y determine cuantos metros de cables se necesitan 
#para conectar todos los ambientes;
# d) determinar cuál es el camino más corto desde la habitación 1 hasta la sala de estar para 
#determinar cuántos metros de cable de red se necesitan para conectar el router con el 
#Smart Tv

class Arista:
    def __init__(self, inicio, fin, peso):
        self.inicio = inicio
        self.fin = fin
        self.peso = peso

class Grafo:
    def __init__(self):
        self.vertices = set()
        self.aristas = []

    def agregar_vertice(self, vertice):
        self.vertices.add(vertice)

    def agregar_arista(self, inicio, fin, peso):
        arista = Arista(inicio, fin, peso)
        self.aristas.append(arista)

    def obtener_adyacentes(self, vertice):
        adyacentes = []
        for arista in self.aristas:
            if arista.inicio == vertice:
                adyacentes.append(arista.fin)
            elif arista.fin == vertice:
                adyacentes.append(arista.inicio)
        return adyacentes

    def obtener_peso(self, inicio, fin):
        for arista in self.aristas:
            if (arista.inicio == inicio and arista.fin == fin) or (arista.inicio == fin and arista.fin == inicio):
                return arista.peso
        return None

    def arbol_expansion_minima(self):
        arbol = Grafo()
        if not self.aristas:
            return arbol
        
        aristas_ordenadas = sorted(self.aristas, key=lambda x: x.peso)

        arbol_vertices = set()

        arbol.agregar_vertice(aristas_ordenadas[0].inicio)
        arbol_vertices.add(aristas_ordenadas[0].inicio)

        while len(arbol_vertices) < len(self.vertices):
            for arista in aristas_ordenadas:
                if arista.inicio in arbol_vertices and arista.fin not in arbol_vertices:
                    arbol.agregar_vertice(arista.fin)
                    arbol_vertices.add(arista.fin)
                    arbol.agregar_arista(arista.inicio, arista.fin, arista.peso)
                    break
                elif arista.fin in arbol_vertices and arista.inicio not in arbol_vertices:
                    arbol.agregar_vertice(arista.inicio)
                    arbol_vertices.add(arista.inicio)
                    arbol.agregar_arista(arista.inicio, arista.fin, arista.peso)
                    break

        return arbol

    def calcular_longitud_cables(self):
        longitud_total = 0
        arbol = self.arbol_expansion_minima()
        for arista in arbol.aristas:
            longitud_total += arista.peso
        return longitud_total

    def camino_mas_corto(self, inicio, fin):
        if inicio not in self.vertices or fin not in self.vertices:
            return None

        distancia = {v: float('inf') for v in self.vertices}
        distancia[inicio] = 0
        visitados = set()

        while visitados != self.vertices:
            vertice_actual = min(set(distancia.keys()) - visitados, key=lambda x: distancia[x])
            visitados.add(vertice_actual)

            for vecino in self.obtener_adyacentes(vertice_actual):
                peso_arista = self.obtener_peso(vertice_actual, vecino)
                if distancia[vecino] > distancia[vertice_actual] + peso_arista:
                    distancia[vecino] = distancia[vertice_actual] + peso_arista

        return distancia[fin]

grafo = Grafo()

# a) Agregar vértices (ambientes de la casa)
ambientes = ["cocina", 
             "comedor", 
             "cochera", 
             "quincho", 
             "baño1", 
             "baño2", 
             "habitacion1", 
             "habitacion2", 
             "sala_estar", 
             "terraza", 
             "patio"]

for ambiente in ambientes:
    grafo.agregar_vertice(ambiente)

# b) Agregar aristas con pesos (distancias en metros)
aristas = [("cocina", "comedor", 5), 
           ("cocina", "cochera", 8), 
           ("cocina", "baño1", 10),
           ("comedor", "quincho", 6), 
           ("comedor", "habitacion1", 5), 
           ("cochera", "habitacion2", 7),
           ("baño1", "baño2", 3), 
           ("habitacion1", "habitacion2", 4), 
           ("sala_estar", "terraza", 2),
           ("patio", "terraza", 9), 
           ("habitacion1", "sala_estar", 8)]

for arista in aristas:
    grafo.agregar_arista(arista[0], arista[1], arista[2])

# c) Obtener el árbol de expansión mínima y determinar la longitud de los cables
arbol_exp_minima = grafo.arbol_expansion_minima()
longitud_cables = grafo.calcular_longitud_cables()
print(f"Longitud total de cables para conectar todos los ambientes: {longitud_cables} metros")

# d) Determinar el camino más corto desde habitacion1 hasta sala_estar
inicio = "habitacion1"
fin = "sala_estar"
camino_corto = grafo.camino_mas_corto(inicio, fin)
print(f"El camino más corto desde {inicio} hasta {fin} es de {camino_corto} metros")
