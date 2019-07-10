import numpy as np, random, matplotlib.pyplot as plt, math, time, cProfile, pstats
from io import StringIO

def load_data(file_name): # zwraca listę krotek zawierających wspolrzedne miast
    f = open(file_name, "r")
    city_list = []
    for line in f:
        line = line.split('\t')
        x = int(line[1])
        y = int(line[2].rstrip('\n.'))
        city_list.append((x, y))
    return city_list


def calculate_distance(coords_1, coords_2): # oblicza dystans pomiedzy dwoma krotkami wspolrzednych
    xdis = abs(coords_1[0] - coords_2[0])
    ydis = abs(coords_1[1] - coords_2[1])
    distance = math.sqrt((xdis ** 2) + (ydis ** 2))
    return distance


def create_distances_matrix(city_list): # tworzy macierz zawierajaca odleglosci miedzy wszystkimi miastami
    rows = cols = len(city_list)
    distances = np.zeros((rows, cols))
    for i in range(0, rows):
        for j in range(0, cols):
            distances[i][j] = calculate_distance(city_list[i], city_list[j])
    return distances


class Route:
    def __init__(self, route):
        self.route = route
        self.distance = 0

    def calculate_route_distance(self):
        distance = 0
        for i in range(0, len(self.route)):
            fromCity = self.route[i]
            toCity = None
            if i + 1 < len(self.route):
                toCity = self.route[i + 1]
            else:
                toCity = self.route[0]
            distance += distances[fromCity, toCity]
        self.distance = distance

    def mutate_route(self):
        x = random.randint(0, len(self.route) - 1)
        y = random.randint(0, len(self.route) - 1)
        temp = self.route[x]
        self.route[x] = self.route[y]
        self.route[y] = temp
        self.calculate_route_distance()


def create_route(length):
    r = random.sample(range(length), length)
    route = Route(r)
    route.calculate_route_distance()
    return route


def initial_population(pop_size, cities_count):
    population = []
    for i in range(0, pop_size):
        population.append(create_route(cities_count))
    return population


def selection(current_generation, elite_size, tour_size):
    parents = []
    for i in range(0, elite_size):
        parents.append(current_generation[i])
    for i in range(elite_size, len(current_generation)):
        tour = []
        for j in range(0, tour_size):
            x = random.randint(elite_size, len(current_generation)-1)
            tour.append(current_generation[x])
        tour.sort(key=lambda r: r.distance, reverse=False)
        parents.append(tour[0])
    return parents


def crossover_parents(parent1, parent2):
    child_part1 = []
    child_part2 = []

    x = int(random.random() * len(parent1.route))

    for i in range(0, x):
        child_part1.append(parent1.route[i])

    child_part2 = [item for item in parent2.route if item not in child_part1]

    child = Route(child_part1 + child_part2)
    child.calculate_route_distance()
    return child


def crossover(parents, elite_size):
    children = []
    for i in range (0, elite_size):
        children.append(parents[i])

    length = len(parents) - elite_size
    pool = random.sample(parents, len(parents))

    for i in range(0, length):
        if i+1 < length:
            child = crossover_parents(pool[i], pool[i+1])
        else:
            child = pool[i]
        children.append(child)
    return children


def mutation(generation, mutation_rate):
    mutations_count = round(len(generation) * mutation_rate)
    for i in range(0, mutations_count):
        x = random.randint(0, len(generation)-1)
        generation[x].mutate_route()
    return generation


def next_generation(current_generation):
    tour_size = 5
    elite_size = 10
    parents = selection(current_generation, tour_size, elite_size)
    next_gen = crossover(parents, elite_size)
    mutated = mutation(next_gen, 0.01)
    return mutated


def genetic_algorithm():
    progress = []
    cities_count = len(city_list)
    pop_size = 100
    pop = initial_population(pop_size, cities_count)
    pop.sort(key=lambda r: r.distance, reverse=False)
    progress.append(1/pop[0].distance)
    generations = 100

    best_route = []


    start_time = time.time()


    for i in range (0, generations):
        if i % 10 == 0:
            print('Generation: ' + str(i))

        gen = next_generation(pop)
        gen.sort(key=lambda r: r.distance, reverse=False)
        progress.append(1/gen[0].distance)
        pop = gen
        best_route = gen[0].route

    end_time = time.time()
    plt.figure()
    plt.plot(progress)
    plt.xlabel("Generations")
    plt.ylabel("Score")
    #message = 'Czas wykonania: ' + "{0:.2f}".format(execution_time) + ' s'
    #plt.annotate(message, xy=(0, 1), xytext=(12, -12), va='top', xycoords = 'axes fraction', textcoords = 'offset points')
    #plt.legend()

    plt.show()

    execution_time = end_time - start_time
    print("{0:.2f}".format(execution_time) + ' s')
    return best_route


city_list = load_data('data.txt')
distances = create_distances_matrix(city_list)


cProfile.run('genetic_algorithm()',sort = 'time')
#print(genetic_algorithm())

