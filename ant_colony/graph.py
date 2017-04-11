#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt

from .ant_colony import AntColony


class Node(object):
    """
    Node representation
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, node):
        return sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)


class Graph(object):
    """
    Graph of nodes
    """
    def __init__(self, nodes, alpha=1, beta=3, decay=.2, min_pheromone=.01,
                 deposit=.1, best_deposit=.5):
        self.nodes = nodes
        self.alpha = alpha
        self.beta = beta
        self.decay = decay
        self.min_pheromone = min_pheromone
        self.best_deposit = best_deposit
        self.deposit = deposit
        self._distances = {}
        self._pheromones = {}
        self.total_distances = 0
        for i, node in enumerate(self.nodes):
            for j in range(i):
                distance = node.distance(self.nodes[j])
                self._distances[(i, j)] = distance
                self.total_distances += distance
                self._pheromones[(i, j)] = min_pheromone

    def get_path_distance(self, path):
        """
        Returns total distance along the path
        """
        length = len(path)
        distance = 0
        for i in range(length):
            distance += self.get_distance(path[i], path[(i + 1) % length])
        return distance

    def get_distance(self, i, j):
        """
        Returns distance between two nodes
        """
        return self._distances.get((i, j)) or self._distances.get((j, i))

    def get_pheromone(self, i, j):
        """
        Returns pheromone between two nodes
        """
        return self._pheromones.get((i, j)) or self._pheromones.get((j, i), 0)

    def get_probability(self, i, j):
        """
        Returns probability of going from ith node to the jth
        """
        return (
            (self.get_pheromone(i, j) ** self.alpha) *
            (self.get_distance(i, j) ** -self.beta)
        )

    def local_update_pheromones(self, passes):
        """
        Updates pheromones between nodes locally
        """
        for i, j in passes:
            self._pheromones[(i, j)] *= self.decay
            self._pheromones[(i, j)] += self.deposit

    def update_pheromones(self, ant_colony):
        """
        Updates pheromones between nodes globally
        """
        for node_pair in self._pheromones:
            self._pheromones[node_pair] *= (1 - self.decay)
        for ant in ant_colony.ants:
            distance = self.get_path_distance(ant.path)
            if distance <= ant_colony.min_distance:
                for node_pair in ant.get_passes():
                    self._pheromones[node_pair] += self.best_deposit / distance
        for node_pair in self._pheromones:
            self._pheromones[node_pair] = max(
                self._pheromones[node_pair], self.min_pheromone
            )

    def find_shortest_path(self, n=100, m=10):
        """
        Returns shortest path
        """
        shortest_path = []
        ant_colony = AntColony(m)
        for i in range(n):
            ant_colony.do_cycles(self)
            shortest_path = ant_colony.shortest_path
            self.update_pheromones(ant_colony)
        return shortest_path, ant_colony.min_distance
