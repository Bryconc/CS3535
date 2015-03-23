from __future__ import division

__author__ = 'Brycon'

import numpy as np
import matplotlib.pyplot as plot
import math

DEBUG = False
TEST_ITERATION = 2

C_MAJOR_VECTOR = [0.51, 0.03, 0.12, 0.09, 0.30, 0.19, 0.07, 0.28, 0.09, 0.24, 0.06, 0.00]
C_MINOR_VECTOR = [0.47, 0.06, 0.07, 0.39, 0.03, 0.28, 0.00, 0.30, 0.25, 0.10, 0.06, 0.10]
CHORD_NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
ITERATION_CHECKPOINTS = {25, 100} # Add more checkpoints to create more images (range 0-359)

NEIGHBOR_DECREMENT = 20
MAP_SIZE = 20
INPUT_SIZE = 24
ITERATION_LIMIT = 360
LEARNING_RATE = 0.02

chord_vectors = {}
map_matrix = []
neighbor_radius = MAP_SIZE - 1

def build_chords():
    major_array = np.asarray(C_MAJOR_VECTOR)
    minor_array = np.asarray(C_MINOR_VECTOR)

    for i in range(12):
        chord_vectors[CHORD_NAMES[i] + "M"] = np.roll(major_array, i)

    for i in range(12):
        chord_vectors[CHORD_NAMES[i] + "m"] = np.roll(minor_array, i)


def initialize_map():
    global map_matrix
    map_matrix = [[np.random.uniform(0, 1, 12) for x in range(MAP_SIZE)] for x in range(MAP_SIZE)]


def find_best_match(node):
    min_distance = euclidean_distance(node, map_matrix[0][0])
    node_location = (0, 0)
    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            distance = euclidean_distance(node, map_matrix[i][j])
            if distance < min_distance:
                min_distance = distance
                node_location = (i, j)
    return node_location


def euclidean_distance(vect1, vect2):
    sum_vect = 0
    for i in range(len(vect1)):
        sum_vect += (vect1[i] - vect2[i]) ** 2
    return math.sqrt(sum_vect)


def update_neighbors(node, input, s):
    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            map_matrix[i][j] += neighborhood_function(node, (i, j), s) * LEARNING_RATE * (input - map_matrix[i][j])


def neighborhood_function(bmu, node, iteration):
    return math.e ** -((torus_distance(bmu, node) ** 2) / (2 * (neighbor_deviation(iteration) ** 2)))


# Euclidean distance on a torus.
# Reference: http://stackoverflow.com/questions/2123947/calculate-distance-between-two-x-y-coordinates
def torus_distance(node_1, node_2):
    w = MAP_SIZE
    h = MAP_SIZE
    return math.sqrt(min(abs(node_1[0] - node_2[0]), w - abs(node_1[0] - node_2[0])) ** 2 + min(abs(node_1[1] - node_2[1]), h - abs(node_1[1] - node_2[1])) ** 2)


def neighbor_deviation(iteration):
    return (1 / 3) * (neighbor_radius - (iteration / NEIGHBOR_DECREMENT))


def graph(name, title):
    global map_matrix
    distance_matrix = [[euclidean_distance(map_matrix[i][j], C_MAJOR_VECTOR) for i in range(MAP_SIZE)] for j in range(MAP_SIZE)]

    plot.close()
    plot.imshow(distance_matrix, interpolation="nearest", origin="lower")
    plot_chords()
    plot.title(title)
    plot.colorbar()
    plot.savefig(name + ".png")


def plot_chords():
    for s in chord_vectors.keys():
        closest = find_best_match(chord_vectors[s])
        plot.annotate(s, closest, color="m", fontsize="20")

def main():
    build_chords()
    initialize_map()
    graph("init", "initial")
    from pprint import pprint
    for s in range(1, ITERATION_LIMIT):
        print("Iteration: %d" % s)

        for i in range(INPUT_SIZE):
            from random import choice
            node = choice(chord_vectors.keys())
            closest = find_best_match(chord_vectors[node])
            update_neighbors(closest, chord_vectors[node], s)

        if s in ITERATION_CHECKPOINTS:
            graph("som%d" % s, s)

        if DEBUG and s == TEST_ITERATION:
            pprint(map_matrix[0][0])
            exit()
    graph("final", "final")


if __name__ == '__main__':
    main()