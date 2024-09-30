# This file is part of PyCosmo, a multipurpose cosmology calculation tool in Python.
#
# Copyright (C) 2013-2021 ETH Zurich, Institute for Particle and Astrophysics and SIS
# ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Pascal"

import sys

import numpy as np
import pytest

import PyCosmo

"""
Test the NonLinear perturbation module.
"""

RTOL = dict(darwin=1e-5).get(sys.platform, 1e-8)


@pytest.fixture
def halomodel_mw_ps(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_HaloModel_mw_ps_param.ini"))
    yield c.nonlin_pert


@pytest.fixture
def halomodel_st_st(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_HaloModel_st_st_param.ini"))
    yield c.nonlin_pert


@pytest.fixture
def halomodel_ti_ti(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_HaloModel_ti_ti_param.ini"))
    yield c.nonlin_pert


@pytest.fixture
def halomodel_smt_wa(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_HaloModel_smt_wa_param.ini"))
    yield c.nonlin_pert


@pytest.fixture
def halomodel_profile1(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_HaloModel_profile1_param.ini"))
    yield c.nonlin_pert


@pytest.fixture
def hi_halomodel_profile0(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_HI_HaloModel_profile0_param.ini"))
    yield c.nonlin_pert


@pytest.fixture
def hi_halomodel_profile1(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_HI_HaloModel_profile1_param.ini"))
    yield c.nonlin_pert


@pytest.mark.parametrize(
    "model_name",
    [
        "halomodel_mw_ps",
        "halomodel_st_st",
        "halomodel_ti_ti",
        "halomodel_smt_wa",
        "halomodel_profile1",
        "hi_halomodel_profile0",
        "hi_halomodel_profile1",
    ],
)
def test_halomodel_regression(model_name, snapshot, request):
    model = request.getfixturevalue(model_name)
    k_vec = [0.1, 0.3, 0.5, 0.9]
    a_vec = [0.2, 0.5, 1.0]

    pk = model.powerspec_a_k(a_vec, k_vec)
    snapshot.check(pk, atol=0, rtol=RTOL)


def test_halomodel_st_st_regression(halomodel_st_st, snapshot):
    a_vec = [0.2, 0.5, 1.0]

    m_vec = [1e09, 1e10, 1e11, 1e12]

    dn_dm_m = halomodel_st_st.dn_dm_of_m(m_vec, a_vec)
    snapshot.check(dn_dm_m, atol=0, rtol=RTOL)

    sub_dn_dm = halomodel_st_st.subhalos_dn_dm_of_m(subhalo_m_msun=m_vec)
    snapshot.check(sub_dn_dm, atol=0, rtol=RTOL)

    dn_dlnm_m = halomodel_st_st.dn_dlnm_of_m(m_vec, a_vec)
    snapshot.check(dn_dlnm_m, atol=0, rtol=RTOL)

    dn_dlogm_m = halomodel_st_st.dn_dlogm_of_m(m_vec, a_vec)
    snapshot.check(dn_dlogm_m, atol=0, rtol=RTOL)

    nu_vec = [1.3, 1.6, 2.2, 2.9]

    dn_dm_nu = halomodel_st_st.dn_dm_of_nu(nu_vec, a_vec)
    snapshot.check(dn_dm_nu, atol=0, rtol=RTOL)

    dn_dlnm_nu = halomodel_st_st.dn_dlnm_of_nu(nu_vec, a_vec)
    snapshot.check(dn_dlnm_nu, atol=0, rtol=RTOL)

    dn_dlogm_nu = halomodel_st_st.dn_dlogm_of_nu(nu_vec, a_vec)
    snapshot.check(dn_dlogm_nu, atol=0, rtol=RTOL)


def test_halomodel_profile_regressions(
    hi_halomodel_profile0, hi_halomodel_profile1, snapshot
):
    k_vec = [0.1, 0.3, 0.5, 0.9]
    a_vec = [0.2, 0.5, 1.0]

    pk_hi = hi_halomodel_profile0.powerspec_a_k_HI(a_vec, k_vec)
    snapshot.check(pk_hi, atol=0, rtol=RTOL)

    pk_hi = hi_halomodel_profile1.powerspec_a_k_HI(a_vec, k_vec)
    snapshot.check(pk_hi, atol=0, rtol=RTOL)

    mean_temp = hi_halomodel_profile0.mean_hi_temp(a_vec)
    snapshot.check(mean_temp, atol=0, rtol=RTOL)


def test_powerspec_api(halomodel_st_st, hi_halomodel_profile0):
    p1 = halomodel_st_st.powerspec_a_k(
        [0.2, 0.3, 0.5], [0.1, 0.2, 0.5], diag_only=False
    )
    assert p1.shape == (3, 3)
    p2 = halomodel_st_st.powerspec_a_k([0.2, 0.3, 0.5], [0.1, 0.2, 0.5], diag_only=True)
    assert p2.shape == (3,)

    assert np.allclose(np.diag(p1), p2)

    p1 = hi_halomodel_profile0.powerspec_a_k_HI(
        [0.2, 0.3, 0.5], [0.1, 0.2, 0.5], diag_only=False
    )
    assert p1.shape == (3, 3)
    p2 = hi_halomodel_profile0.powerspec_a_k_HI(
        [0.2, 0.3, 0.5], [0.1, 0.2, 0.5], diag_only=True
    )
    assert p2.shape == (3,)

    assert np.allclose(np.diag(p1), p2)
