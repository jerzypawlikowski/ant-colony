#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import random


class Ant(object):
    """
    Class representing ant
    """
    def __init__(self, position=0):
        self.path = [position]

    def _go_to_next(self, graph, available):
        """
        Makes ant go to a next node
        """
        if len(available) == 1:
            self.path.append(available.pop())

        if not available:
            return

        total = 0
        probabilities = {}
        for node_index in available:
            probabilities[node_index] = graph.get_probability(
                self.path[-1], node_index
            )
            total += probabilities[node_index]

        threshold = random()
        probability = 0
        for node_index in available:
            probability += probabilities[node_index] / total
            if threshold < probability:
                self.path.append(node_index)
                return
        self.path.append(available.pop())

    def do_cycle(self, graph):
        """
        The ant goes full cycle
        """
        all_nodes = set(range(len(graph.nodes)))
        available = all_nodes - set(self.path)
        counter = 0
        while available:
            counter += 1
            self._go_to_next(graph, available)
            available = all_nodes - set(self.path)

    def get_passes(self):
        """
        Returns list of passes made by the ant
        """
        length = len(self.path)
        return [
            tuple(sorted(
                (self.path[i], self.path[(i + 1) % length]), reverse=True))
            for i in range(length)
        ]

    def get_distance(self, graph):
        """
        Returns distance traveled by the ant
        """
        return graph.get_path_distance(self.path)
