#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock

from acs.ant import Ant


def test_init():
    ant = Ant(3)
    assert ant.path == [3]


def test_get_distance():
    ant = Ant()
    graph = mock.Mock()
    ant.get_distance(graph)
    graph.get_path_distance.assert_called_with(ant.path)


def test_get_passes():
    ant = Ant()
    ant.path = [1, 4, 3, 5, 2]
    assert ant.get_passes() == [(4, 1), (4, 3), (5, 3), (5, 2), (2, 1)]


def test_go_to_next_single():
    ant = Ant(1)
    ant._go_to_next(graph=None, available=[0])
    assert ant.path == [1, 0]


def test_go_to_next_none():
    ant = Ant(0)
    ant._go_to_next(graph=None, available=[])
    assert ant.path[-1] == 0


def test_go_to_next_random_middle():
    graph = mock.Mock()
    graph.get_probability = lambda i, j: 44
    ant = Ant(0)
    with mock.patch("acs.ant.random") as mocked_random:
        mocked_random.return_value = 0.5
        ant._go_to_next(graph=graph, available=[3, 1, 2])
    mocked_random.assert_called_once()
    assert ant.path[-1] == 1


def test_go_to_next_random_maximum():
    graph = mock.Mock()
    graph.get_probability = lambda i, j: 44
    ant = Ant(0)
    with mock.patch("acs.ant.random") as mocked_random:
        mocked_random.return_value = 1
        ant._go_to_next(graph=graph, available=[2, 1, 3])
    mocked_random.assert_called_once()
    assert ant.path[-1] == 3


def test_do_cycle():
    graph = mock.Mock()
    graph.get_probability = lambda i, j: 44
    graph.nodes = [1, 2, 3, 4]
    ant = Ant(0)
    with mock.patch("acs.ant.random") as mocked_random:
        mocked_random.return_value = 1
        ant.do_cycle(graph)
    mocked_random.assert_has_calls(tuple() * 3)
    assert len(ant.path) == 4
