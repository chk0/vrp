import math
import sys

class VRP:
    def __init__(self, capacity, locations, demands):
        self.capacity = capacity
        self.locations = locations
        self.demands = demands

    def euclidean_distance(self, coord1, coord2):
        return round(math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2))      
      
    def calculate_route_cost(self, route):
        total_distance = 0
        current_node = route[0]

        for next_node in route[1:]:
            total_distance += self.euclidean_distance(self.locations[current_node], self.locations[next_node])
            current_node = next_node
        return total_distance

    def find_nearest_neighbor(self, current_node, unvisited):
        min_distance = float('inf')
        nearest_node = None
        for node in unvisited:
            distance = self.euclidean_distance(self.locations[current_node], self.locations[node])
            if distance < min_distance:
                min_distance = distance
                nearest_node = node
        return nearest_node, min_distance

    def solve(self):
        sorted_customers = sorted(self.demands.keys(), key=lambda x: self.demands[x])

        current_capacity = 0
        current_node = 1
        unvisited = sorted_customers
        routes = []
        route = [current_node]

        while unvisited:
            nearest_node, distance = self.find_nearest_neighbor(current_node, unvisited)
            if self.demands[nearest_node] + current_capacity <= self.capacity:
                route.append(nearest_node)
                current_capacity += self.demands[nearest_node]
                unvisited.remove(nearest_node)
                current_node = nearest_node
            else:
                route.append(1)
                routes.append(route)
                route = [1]
                current_node = 1
                current_capacity = 0

        if route != [1]:
            route.append(1)
            routes.append(route)

        return routes

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 vrp.py <nombre_del_archivo>")
    else:
        file_path = sys.argv[1]

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            capacity = None
            locations = {}
            demands = {}
            current_section = None

            for line in lines:
                if line.startswith("CAPACITY"):
                    capacity = int(line.split()[1])
                elif line.startswith("NODE_COORD_SECTION"):
                    current_section = "NODE_COORD_SECTION"
                elif line.startswith("DEMAND_SECTION"):
                    current_section = "DEMAND_SECTION"
                elif current_section == "NODE_COORD_SECTION":
                    parts = line.split()
                    node = int(parts[0])
                    x, y = map(int, parts[1:])
                    locations[node] = (x, y)
                elif current_section == "DEMAND_SECTION":
                    if line.strip() and line[0].isdigit():
                        node, demand = map(int, line.split())
                        demands[node] = demand

            if capacity is not None and locations and demands:
                vrp = VRP(capacity, locations, demands)
                routes = vrp.solve()

                total_cost = 0
                for i, route in enumerate(routes):
                    cost = vrp.calculate_route_cost(route)
                    total_cost += cost
                    print(f"Ruta {i + 1}: {route} - Costo: {cost}")
                print(f"Costo total de todas las rutas: {total_cost}")
            else:
                print("El archivo no tiene el formato correcto o falta información.")
        except FileNotFoundError:
            print("No se pudo encontrar el archivo.")
