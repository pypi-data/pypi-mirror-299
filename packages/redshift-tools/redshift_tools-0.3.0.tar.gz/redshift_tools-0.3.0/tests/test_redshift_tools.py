# Copyright (C) 2022 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import os

import numpy as np
import PyCosmo
import pytest

import redshift_tools as rt


def _get_abspath(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)


def test_load():
    # test loading from path
    nz, nz_tot = rt.load_bins(_get_abspath("test_bins/example_bins"))
    assert len(nz) == 5

    # test loading from path without nz_tot
    nz, nz_tot = rt.load_bins(_get_abspath("test_bins/example_bins_notot"))
    assert nz_tot is None


def test_lensing_kernel():
    nz, nz_tot = rt.load_bins(_get_abspath("test_bins/example_bins"))

    wz = rt.lensing_kernel(nz)
    assert len(wz) == 5

    wz, wz_tot = rt.lensing_kernel(nz, nz_tot)
    assert len(wz) == 5

    cosmo = PyCosmo.build()
    wz = rt.lensing_kernel(nz, cosmo=cosmo)
    assert len(wz) == 5


def test_create_smail():
    nz, nz_tot = rt.create_bins(5, 0.1 * np.ones(5), redshift_dep=False)
    nz2, nz_tot = rt.create_bins(5, 0.1 * np.ones(5), redshift_dep=True)
    nz3, nz_tot = rt.create_bins(5, 0.1 * np.ones(5), alpha=3, beta=0.5, z0=0.5)
    nz3, nz_tot = rt.create_bins(5, 0.1 * np.ones(5), normalize_bins=False)


def test_create_fu():
    nz, nz_tot = rt.create_bins(
        5, 0.1 * np.ones(5), redshift_dep=False, distribution="fu"
    )
    nz2, nz_tot = rt.create_bins(
        5, 0.1 * np.ones(5), redshift_dep=True, distribution="fu"
    )
    nz3, nz_tot = rt.create_bins(
        5, 0.1 * np.ones(5), distribution="fu", a=0.7, b=8.4, c=0.6, A=1
    )


def test_create_unknown():
    # test that ValueError is raised for unknown distribution
    with pytest.raises(ValueError):
        nz, nz_tot = rt.create_bins(5, 0.1 * np.ones(5), distribution="unknown")


def test_save():
    nz, nz_tot = rt.load_bins(_get_abspath("test_bins/example_bins"))
    rt.create.save_bins(nz, _get_abspath("test_bins/example_bins_save"))
    rt.create.save_bins(nz, _get_abspath("test_bins/example_bins_save"), nz_tot)
    rt.create.save_bins(nz, _get_abspath("test_bins/example_bins_save"), nz_tot)


def test_shift():
    nz, _ = rt.load_bins(_get_abspath("test_bins/example_bins"))
    rt.manipulate.shift(nz, np.array([0.1, -0.1, 0, 0.2, -0.2]))
    nz0 = rt.manipulate.shift(nz, np.zeros(5))
    for i in range(len(nz)):
        assert np.all(nz[i] == nz0[i])


def test_stretch():
    nz, _ = rt.load_bins(_get_abspath("test_bins/example_bins"))
    rt.manipulate.stretch(nz, np.array([1.1, 0.9, 1, 1.2, 0.8]))
    nz1 = rt.manipulate.stretch(nz, np.ones(5), normalize=False)
    for i in range(len(nz)):
        assert np.all(nz[i] == nz1[i])


def test_find_bin_thresholds():
    x = np.random.normal(0, 1, 1000)
    bin_thresholds = rt.catalog.find_bin_thresholds(x, n_bins=4)
    assert len(bin_thresholds) == 5
    assert bin_thresholds[0] == -np.inf
    assert bin_thresholds[-1] == np.inf
    assert bin_thresholds[1] < bin_thresholds[2]
    assert bin_thresholds[2] < bin_thresholds[3]
    assert bin_thresholds[3] < bin_thresholds[4]

    bin_thresholds = rt.catalog.find_bin_thresholds(x, n_bins=4, lower_cut=-1)
    assert len(bin_thresholds) == 6
    assert bin_thresholds[0] == -np.inf
    assert bin_thresholds[-1] == np.inf
    assert bin_thresholds[1] == -1
    assert bin_thresholds[2] < bin_thresholds[3]
    assert bin_thresholds[3] < bin_thresholds[4]

    bin_thresholds = rt.catalog.find_bin_thresholds(x, n_bins=4, upper_cut=1)
    assert len(bin_thresholds) == 6
    assert bin_thresholds[0] == -np.inf
    assert bin_thresholds[-1] == np.inf
    assert bin_thresholds[1] < bin_thresholds[2]
    assert bin_thresholds[2] < bin_thresholds[3]
    assert bin_thresholds[-2] == 1

    bin_thresholds = rt.catalog.find_bin_thresholds(
        x, n_bins=4, lower_cut=-1, upper_cut=1
    )
    assert len(bin_thresholds) == 7
    assert bin_thresholds[0] == -np.inf
    assert bin_thresholds[-1] == np.inf
    assert bin_thresholds[1] == -1
    assert bin_thresholds[-2] == 1
    assert bin_thresholds[2] < bin_thresholds[3]
    assert bin_thresholds[3] < bin_thresholds[4]
    assert bin_thresholds[1] < bin_thresholds[2]
    assert bin_thresholds[3] < bin_thresholds[4]


def test_shift_and_stretch():
    z_bias = np.array([0.1, -0.1, 0, 0.2, -0.2])
    z_sigma = np.array([1.1, 0.9, 1, 1.2, 0.8])
    nz, _ = rt.load_bins(_get_abspath("test_bins/example_bins"))
    nz = rt.manipulate.shift_and_stretch(nz, z_bias, z_sigma)


def test_overlap():
    nz = rt.create_bins(5, 0.1 * np.ones(5), redshift_dep=False)[0]
    ol = rt.manipulate.overlap_all_bins(nz)
    assert len(ol) == 5 + 4 + 3 + 2 + 1


def test_plot():
    nz, nz_tot = rt.load_bins(_get_abspath("test_bins/example_bins"))
    nz2, nz_tot2 = rt.load_bins(_get_abspath("test_bins/example_bins"))
    rt.plot_bins(nz)
    rt.plot_bins([nz, nz2])
    rt.plot_bins(nz, nz_tot)
    rt.plot_bins([nz, nz2], [nz_tot, nz_tot2])
    rt.plot_bins(_get_abspath("test_bins/example_bins"), nz_is_path=True)


def test_plot_bins_2panels():
    nz, nz_tot = rt.load_bins(_get_abspath("test_bins/example_bins"))
    nz2, nz_tot2 = rt.load_bins(_get_abspath("test_bins/example_bins"))

    rt.plot.plot_bins_2panels(nz, nz2)
    rt.plot.plot_bins_2panels(nz, nz2, nz_tot, nz_tot2)
