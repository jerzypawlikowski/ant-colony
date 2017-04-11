#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock

from acs.graph import Graph, Node


def test_node_distance():
    node_1 = Node(x=0, y=3)
    node_2 = Node(x=4, y=0)
    assert node_1.distance(node=node_2) == 5


def test_get_pheromone():
    nodes = [Node(x=0, y=1), Node(x=1, y=0), Node(x=0, y=0)]
    graph = Graph(nodes)
    assert graph.get_pheromone(0, 1) == graph.min_pheromone


def test_get_path_distance():
    nodes = [Node(x=0, y=0), Node(x=0, y=1), Node(x=1, y=1), Node(x=1, y=0)]
    graph = Graph(nodes)
    assert graph.get_path_distance([0, 1, 2, 3]) == 4


def test_get_probability_zero():
    nodes = [Node(x=0, y=0), Node(x=0, y=1), Node(x=1, y=1), Node(x=1, y=0)]
    graph = Graph(nodes, alpha=1, beta=2, min_pheromone=0.1)
    assert abs(graph.get_probability(0, 2) - 0.05) < 0.1 ** 6


def test_local_update():
    nodes = [Node(x=0, y=0), Node(x=0, y=1), Node(x=1, y=1), Node(x=1, y=0)]
    graph = Graph(nodes)
    graph.local_update_pheromones([(3, 2), (2, 1), (1, 0), (3, 0)])
    assert graph.get_pheromone(3, 1) == graph.min_pheromone
    assert graph.get_pheromone(2, 3) > graph.min_pheromone


def test_global_update():
    nodes = [Node(x=0, y=0), Node(x=0, y=1), Node(x=1, y=1), Node(x=1, y=0)]
    graph = Graph(nodes)

    ant_colony = mock.Mock(min_distance=4)
    ant_colony.ants = [
        mock.Mock(
            path=[0, 1, 2, 3],
            get_passes=lambda: [(1, 0), (2, 1), (3, 2), (3, 0)]
        ),
        mock.Mock(path=[0, 2, 3, 1])
    ]

    graph.update_pheromones(ant_colony=ant_colony)
    assert graph.get_pheromone(3, 1) < graph.get_pheromone(2, 3)


def test_find_shortest_path():
    nodes = [Node(x=0, y=0), Node(x=0, y=1), Node(x=1, y=1), Node(x=1, y=0)]
    graph = Graph(nodes)

    assert graph.find_shortest_path()[1] == 4
