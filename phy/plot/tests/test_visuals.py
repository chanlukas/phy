# -*- coding: utf-8 -*-

"""Test visuals."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import numpy as np

from ..visuals import (ScatterVisual, PlotVisual, HistogramVisual,
                       LineVisual,
                       )


#------------------------------------------------------------------------------
# Fixtures
#------------------------------------------------------------------------------

def _test_visual(qtbot, c, v, stop=False, **kwargs):
    c.add_visual(v)
    data = v.validate(**kwargs)
    assert v.vertex_count(**data) >= 0
    v.set_data(**kwargs)
    c.show()
    qtbot.waitForWindowShown(c.native)
    if stop:  # pragma: no cover
        qtbot.stop()
    c.close()


#------------------------------------------------------------------------------
# Test scatter visual
#------------------------------------------------------------------------------

def test_scatter_empty(qtbot, canvas):
    _test_visual(qtbot, canvas, ScatterVisual(), x=np.zeros(0), y=np.zeros(0))


def test_scatter_markers(qtbot, canvas_pz):
    c = canvas_pz

    n = 100
    x = .2 * np.random.randn(n)
    y = .2 * np.random.randn(n)

    v = ScatterVisual(marker='vbar')
    c.add_visual(v)
    v.set_data(x=x, y=y)

    c.show()
    qtbot.waitForWindowShown(c.native)

    # qtbot.stop()


def test_scatter_custom(qtbot, canvas_pz):

    n = 100

    # Random position.
    pos = .2 * np.random.randn(n, 2)

    # Random colors.
    c = np.random.uniform(.4, .7, size=(n, 4))
    c[:, -1] = .5

    # Random sizes
    s = 5 + 20 * np.random.rand(n)

    _test_visual(qtbot, canvas_pz, ScatterVisual(),
                 pos=pos, color=c, size=s)


#------------------------------------------------------------------------------
# Test plot visual
#------------------------------------------------------------------------------

def test_plot_empty(qtbot, canvas):
    y = np.zeros((1, 0))
    _test_visual(qtbot, canvas, PlotVisual(),
                 y=y)


def test_plot_0(qtbot, canvas_pz):
    y = np.zeros((1, 10))
    _test_visual(qtbot, canvas_pz, PlotVisual(),
                 y=y)


def test_plot_1(qtbot, canvas_pz):
    y = .2 * np.random.randn(10)
    _test_visual(qtbot, canvas_pz, PlotVisual(),
                 y=y)


def test_plot_2(qtbot, canvas_pz):

    n_signals = 50
    n_samples = 10
    y = 20 * np.random.randn(n_signals, n_samples)

    # Signal colors.
    c = np.random.uniform(.5, 1, size=(n_signals, 4))
    c[:, 3] = .5

    # Depth.
    depth = np.linspace(0., -1., n_signals)

    _test_visual(qtbot, canvas_pz, PlotVisual(),
                 y=y, depth=depth,
                 data_bounds=[-1, -50, 1, 50],
                 color=c)


def test_plot_list(qtbot, canvas_pz):
    y = [np.random.randn(i) for i in (5, 20)]

    c = np.random.uniform(.5, 1, size=(2, 4))
    c[:, 3] = .5

    _test_visual(qtbot, canvas_pz, PlotVisual(),
                 y=y, color=c)


#------------------------------------------------------------------------------
# Test histogram visual
#------------------------------------------------------------------------------

def test_histogram_empty(qtbot, canvas):
    hist = np.zeros((1, 0))
    _test_visual(qtbot, canvas, HistogramVisual(),
                 hist=hist)


def test_histogram_0(qtbot, canvas_pz):
    hist = np.zeros((10,))
    _test_visual(qtbot, canvas_pz, HistogramVisual(),
                 hist=hist)


def test_histogram_1(qtbot, canvas_pz):
    hist = np.random.rand(1, 10)
    _test_visual(qtbot, canvas_pz, HistogramVisual(),
                 hist=hist)


def test_histogram_2(qtbot, canvas_pz):

    n_hists = 5
    hist = np.random.rand(n_hists, 21)

    # Histogram colors.
    c = np.random.uniform(.3, .6, size=(n_hists, 4))
    c[:, 3] = 1

    _test_visual(qtbot, canvas_pz, HistogramVisual(),
                 hist=hist, color=c, ylim=2 * np.ones(n_hists))


#------------------------------------------------------------------------------
# Test line visual
#------------------------------------------------------------------------------

def test_line_empty(qtbot, canvas):
    _test_visual(qtbot, canvas, LineVisual())


def test_line_0(qtbot, canvas_pz):
    y = np.linspace(-.5, .5, 10)
    _test_visual(qtbot, canvas_pz, LineVisual(),
                 y0=y, y1=y, data_bounds=[-1, -1, 1, 1])
