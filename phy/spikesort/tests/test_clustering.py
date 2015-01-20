# -*- coding: utf-8 -*-

"""Tests of sparse matrix structures."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os

import numpy as np
from numpy.testing import assert_array_equal
from pytest import raises

from ...datasets.mock import artificial_spike_clusters
from ..clustering import Clustering


#------------------------------------------------------------------------------
# Tests
#------------------------------------------------------------------------------

def test_clustering():
    clustering = Clustering()

    n_spikes = 1000
    n_clusters = 10
    spike_clusters = artificial_spike_clusters(n_spikes, n_clusters)

    # Instanciate a Clustering instance.
    clustering = Clustering(spike_clusters)
    assert_array_equal(clustering.spike_clusters, spike_clusters)

    # Test cluster labels.
    assert_array_equal(clustering.cluster_labels, np.arange(n_clusters))

    assert clustering.new_cluster_label() == n_clusters
    assert clustering.n_clusters == n_clusters

    assert clustering.cluster_counts.shape[0] == n_clusters
    assert clustering.cluster_counts.sum() == n_spikes

    # Updating a cluster, method 1.
    spike_clusters_new = spike_clusters.copy()
    spike_clusters_new[:10] = 100
    # This automatically updates the Clustering instance.
    clustering.spike_clusters = spike_clusters_new
    assert_array_equal(clustering.cluster_labels,
                       np.r_[np.arange(n_clusters), 100])

    # Updating a cluster, method 2.
    clustering.spike_clusters = spike_clusters
    clustering.spike_clusters[:10] = 100
    # No automatic update (yet?).
    assert_array_equal(clustering.cluster_labels,
                       np.arange(n_clusters))
    # Need to update manually.
    clustering.update()
    assert_array_equal(clustering.cluster_labels,
                       np.r_[np.arange(n_clusters), 100])

    # Not implemented (yet) features.
    with raises(NotImplementedError):
        clustering.cluster_labels = np.arange(n_clusters)
    # Merge.
    with raises(NotImplementedError):
        clustering.merge([2, 3])
    with raises(NotImplementedError):
        clustering.merge([2, 3], 11)
    # Split.
    with raises(NotImplementedError):
        clustering.split([1, 3, 5])
    with raises(NotImplementedError):
        clustering.split([1, 3, 5], 11)
