#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock

from acs.ant_colony import AntColony


def test_reset_ants():
    ant_colony = AntColony(m=3)
    graph = mock.Mock()
    graph.nodes = [0] * 5
    with mock.patch("acs.ant_colony.randint") as mocked_randint:
        ant_colony.reset_ants(graph=graph)

    mocked_randint.assert_has_calls((
        mock.call(0, 4), mock.call(0, 4), mock.call(0, 4)
    ))


def test_do_cycles():
    graph = mock.Mock()
    graph.nodes = [0] * 5
    ant_colony = AntColony(m=3)

    def mock_reset_ants(graph):
        for i in range(ant_colony.m):
            mocked_ant = mock.Mock()
            mocked_ant.path = [0] * 5
            mocked_ant.get_distance.return_value = 5
            ant_colony.ants.append(mocked_ant)

    ant_colony.reset_ants = mock_reset_ants
    ant_colony.do_cycles(graph=graph)
    for ant in ant_colony.ants:
        ant.do_cycle.assert_called_once_with(graph=graph)
