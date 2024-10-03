from __future__ import annotations

import numpy as np
from scipy.stats import chi2

import nustattools.stats as r


def test_derate_unity_covariance():
    cov = np.eye(7)
    assert (
        np.abs(r.derate_covariance(cov, sigma=1, accuracy=0.001, return_dict={}) - 1.0)
        < 0.01
    )


def test_derate_single_covariance():
    cov = np.array(
        [
            [2.0, 1.0, np.nan, np.nan],
            [1.0, 2.0, np.nan, np.nan],
            [np.nan, np.nan, 3.0, 2.0],
            [np.nan, np.nan, 2.0, 3.0],
        ]
    )
    assert np.abs(r.derate_covariance(cov, sigma=2) - 1.29) < 0.1


def test_derate_known_off_diag():
    cov = np.array(
        [
            [2.0, 0.0, np.nan, 0.0],
            [0.0, 2.0, np.nan, np.nan],
            [np.nan, np.nan, 3.0, 0.0],
            [0.0, np.nan, 0.0, 3.0],
        ]
    )
    assert np.abs(r.derate_covariance(cov, sigma=2) - 1.29) < 0.1


def test_derate_multi_covariance():
    cov1 = np.array(
        [
            [2.0, 1.0, np.nan, np.nan],
            [1.0, 2.0, np.nan, np.nan],
            [np.nan, np.nan, 3.0, 2.0],
            [np.nan, np.nan, 2.0, 3.0],
        ]
    )
    cov2 = np.eye(4)
    cov3 = np.array(
        [
            [2.0, 1.0, 0.0, np.nan],
            [1.0, 2.0, 0.0, np.nan],
            [0.0, 0.0, 3.0, np.nan],
            [np.nan, np.nan, np.nan, 3.0],
        ]
    )
    cov4 = np.zeros((4, 4))
    assert np.abs(r.derate_covariance([cov1, cov2, cov3, cov4], sigma=2) - 1.16) < 0.1


def test_derate_single_covariance_fit():
    cov = np.block(
        [
            [np.eye(5), np.full((5, 5), np.nan)],
            [np.full((5, 5), np.nan), np.eye(5)],
        ]
    )
    A = np.array(
        [
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, -1, 1, -1, 1, -1, 1, -1, 1, -1],
        ],
        dtype=float,
    ).T
    A = A / np.sqrt(np.sum(A**2, axis=0, keepdims=True))
    assert (
        np.abs(r.derate_covariance(cov, jacobian=A, sigma=3, accuracy=0.001) - 1.827)
        < 0.02
    )


def test_derate_multi_covariance_fit():
    cov1 = np.array(
        [
            [2.0, 1.0, np.nan, np.nan],
            [1.0, 2.0, np.nan, np.nan],
            [np.nan, np.nan, 3.0, 2.0],
            [np.nan, np.nan, 2.0, 3.0],
        ]
    )
    cov2 = np.eye(4)
    cov3 = np.array(
        [
            [2.0, 1.0, 0.0, np.nan],
            [1.0, 2.0, 0.0, np.nan],
            [0.0, 0.0, 3.0, np.nan],
            [np.nan, np.nan, np.nan, 3.0],
        ]
    )
    A = np.array(
        [
            [2, 1, 1, 1],
            [1, -1, 1, -1],
        ],
        dtype=float,
    ).T
    A = A / np.sqrt(np.sum(A**2, axis=0, keepdims=True))
    assert (
        np.abs(r.derate_covariance([cov1, cov2, cov3], jacobian=A, sigma=2) - 1.54)
        < 0.1
    )


def test_fitted_fmax():
    fitted = r.FMaxStatistic(k=[7, 13])
    assert fitted.calculate([17, 19]) == 19
    s = fitted([[[17, 19]] * 2] * 3)
    assert np.all(s == 19)
    assert np.all(s.shape == (3, 2))
    assert np.abs(1.0 - fitted.cdf(19.1) - 0.127) < 0.001
    a = np.abs(1.0 - fitted.cdf([[19.1] * 4] * 3) - 0.127)
    assert np.all(a < 0.001)
    assert np.all(a.shape == (3, 4))


def test_pmin_fmax():
    fmax = r.FMaxStatistic(
        k=[7, 13], funcs=[lambda x: chi2(df=7).cdf(x), lambda x: chi2(df=13).cdf(x)]
    )
    assert np.abs(1.0 - fmax([17.03, 19.10]) - 0.02) < 0.01
    assert np.abs(1 - fmax.cdf(1 - 0.02) - 0.034) < 0.01

    qmax = r.QMaxStatistic(k=[7, 13])
    assert np.abs(1.0 - qmax([17.03, 19.10]) - 0.02) < 0.01
    assert np.abs(1 - qmax.cdf(1 - 0.02) - 0.034) < 0.01


def test_optimal_fmax():
    k = [7, 13]
    funcs = []
    for n in k:
        funcs.append(lambda x, df=n: chi2(df=df).logcdf(x) - chi2(df=df).logpdf(x))

    fmax = r.FMaxStatistic(k=k, funcs=funcs)
    assert np.abs(fmax([17.03, 19.10]) - 5.04) < 0.01
    assert np.abs(1 - fmax.cdf(5.04) - 0.038) < 0.001

    optimal = r.OptimalFMaxStatistic(k=k)
    assert np.abs(optimal([17.03, 19.10]) - 5.04) < 0.01
    assert np.abs(1 - optimal.cdf(5.04) - 0.038) < 0.001
    s = np.abs(optimal([[17.03, 19.10]] * 5) - 5.04)
    assert np.all(s < 0.01)
    assert np.all(s.shape == (5,))
