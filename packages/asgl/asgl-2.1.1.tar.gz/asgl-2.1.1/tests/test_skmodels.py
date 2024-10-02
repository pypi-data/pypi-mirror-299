import pytest
import numpy as np
from asgl import Regressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error


def test_prepare_data():
    model = Regressor()
    X = np.array([[1, 2], [3, 4]])
    X_prepared, m, group_index = model._prepare_data(X)
    assert X_prepared.shape == (2, 3)  # Adding intercept term
    assert m == 3
    assert group_index is None


# TEST UNPENALIZED ----------------------------------------------------------------------------------------------------


def test_unpenalized_lm():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]

    model = Regressor(model='lm', penalization=None, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Unpenalized lm failure')
    np.testing.assert_array_almost_equal(
        model.intercept_,
        np.array([7.2923]),
        decimal=3,
        err_msg='Unpenalized lm failure')


def test_unpenalized_qr():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]

    model = Regressor(model='qr', penalization=None, quantile=0.8, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([25.92647702, 15.32296485, 26.18622489, 59.82066746,
                  99.17547549, 17.72659176, 11.82218774, 34.74489955, 58.59336065,
                  65.68631127]),
        decimal=3,
        err_msg='Unpenalized qr failure for quantile 0.8')

    model = Regressor(model='qr', penalization=None, quantile=0.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([24.53442726, 15.60297538, 24.87555318, 58.24387077,
                  99.36779578, 15.09292701, 12.15865, 33.94239404, 63.53956298,
                  66.47009116]),
        decimal=3,
        err_msg='Unpenalized qr failure for quantile 0.2')


def test_unpenalized_logit():
    data = np.loadtxt('data_logit.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1].astype('int')

    model = Regressor(model='logit', penalization=None, solver='SCS')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([1.31852718, 1.44379378, -0.8350253,
                  16.70362005, 0.97621178, -37.37958466, -14.11223982,
                  1.41652058, 9.47822006, -15.14141223]),
        decimal=3,
        err_msg='Unpenalized logit failure')


# TEST LASSO PENALIZATION ---------------------------------------------------------------------------------------------


def test_lasso_lm():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]

    model = Regressor(model='lm', penalization='lasso', lambda1=0, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Lasso lm failure for lambda=0')

    model = Regressor(model='lm', penalization='lasso', lambda1=0.1, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.25821113, 15.00872081, 25.33148317, 56.132575,
                  99.34021902, 15.39857671, 10.35704837, 34.86962766, 61.42098122,
                  66.24809898]),
        decimal=3,
        err_msg='Lasso lm failure for lambda=0.1')


def test_lasso_qr():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]

    model = Regressor(model='qr', penalization='lasso', quantile=0.8, lambda1=0, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([25.92647702, 15.32296485, 26.18622489, 59.82066746,
                  99.17547549, 17.72659176, 11.82218774, 34.74489955, 58.59336065,
                  65.68631127]),
        decimal=3,
        err_msg='Lasso qr failure for quantile 0.8 and lambda1=0')

    model = Regressor(model='qr', penalization='lasso', quantile=0.8, lambda1=0.1, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([0., 0., 0., 27.66071305,
                  90.01397685, 0., 0., 21.77214275, 45.01300237,
                  36.34016822]),
        decimal=3,
        err_msg='Lasso qr failure for quantile 0.8 and lambda1=0.1')

    model = Regressor(model='qr', penalization='lasso', quantile=0.2, lambda1=0.1, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([0., 2.37522451, 0.,
                  22.15449983, 77.79554315, 0., 0.,
                  38.65124062, 30.55826802, 29.50093582]),
        decimal=3,
        err_msg='Lasso qr failure for quantile 0.2 and lambda1=0.1')


# TEST RIDGE PENALIZATION ---------------------------------------------------------------------------------------------

def test_ridge_lm():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]

    model = Regressor(model='lm', penalization='ridge', lambda1=0, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Ridge lm failure for lambda=0')

    model = Regressor(model='lm', penalization='ridge', lambda1=0.1, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([18.46772718, 15.2438716, 25.06222985, 50.31818813,
                  89.9845044, 14.03017725, 8.6725918, 33.33322947, 55.33924112,
                  58.02248048]),
        decimal=3,
        err_msg='Ridge lm failure for lambda=0.1')


# TEST GROUP LASSO PENALIZATION ---------------------------------------------------------------------------------------


def test_gl_lm():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='lm', penalization='gl', lambda1=0, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Group lasso lm failure for lambda=0')

    model = Regressor(model='lm', penalization='gl', lambda1=0.1, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.27677831, 15.0266414, 25.33723793, 56.16210945,
                  99.29269691, 15.45069947, 10.37091253, 34.87509388, 61.40852042,
                  66.24043667]),
        decimal=3,
        err_msg='Group lasso lm failure for lambda=0.1')


def test_gl_qr():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='qr', penalization='gl', quantile=0.8, lambda1=0, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([25.92647702, 15.32296485, 26.18622489, 59.82066746,
                  99.17547549, 17.72659176, 11.82218774, 34.74489955, 58.59336065,
                  65.68631127]),
        decimal=3,
        err_msg='Group lasso qr failure for quantile 0.8 and lambda1=0')

    model = Regressor(model='qr', penalization='gl', quantile=0.8, lambda1=0.1, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                  1.33241462e+01, 3.66710686e+01, 4.56237828e+00, 0.00000000e+00,
                  0.00000000e+00, 1.02229130e-04, 1.07166280e-04]),
        decimal=3,
        err_msg='Group lasso qr failure for quantile 0.8 and lambda1=0.1')

    model = Regressor(model='qr', penalization='gl', quantile=0.2, lambda1=0.1, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([0., 0.65037989, 0.62171602,
                  27.42813623, 55.53152069, 7.38334327, 0.,
                  34.14211386, 21.23025218, 30.17858448]),
        decimal=3,
        err_msg='Group lasso qr failure for quantile 0.2 and lambda1=0.1')


# TEST SPARSE GROUP LASSO PENALIZATION --------------------------------------------------------------------------------


def test_sgl_lm():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='lm', penalization='sgl', lambda1=0, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Sparse group lasso lm failure for lambda=0')

    model = Regressor(model='lm', penalization='sgl', lambda1=0.1, alpha=0, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.27677831, 15.0266414, 25.33723793, 56.16210945,
                  99.29269691, 15.45069947, 10.37091253, 34.87509388, 61.40852042,
                  66.24043667]),
        decimal=3,
        err_msg='Sparse group lasso lm failure for lambda=0.1 and alpha=0')

    model = Regressor(model='lm', penalization='sgl', lambda1=0.1, alpha=1, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.25821113, 15.00872081, 25.33148317, 56.132575,
                  99.34021902, 15.39857671, 10.35704837, 34.86962766, 61.42098122,
                  66.24809898]),
        decimal=3,
        err_msg='Sparse group lasso lm failure for lambda=0.1 and alpha=1')

    model = Regressor(model='lm', penalization='sgl', lambda1=0.1, alpha=0.5, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.26750237, 15.01768931, 25.33436154, 56.14735784,
                  99.3164447, 15.42465486, 10.36398602, 34.8723578, 61.41474779,
                  66.24426926]),
        decimal=3,
        err_msg='Sparse group lasso lm failure for lambda=0.1 and alpha=0.5')


def test_sgl_qr():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='qr', penalization='sgl', quantile=0.8, lambda1=0, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([25.92647702, 15.32296485, 26.18622489, 59.82066746,
                  99.17547549, 17.72659176, 11.82218774, 34.74489955, 58.59336065,
                  65.68631127]),
        decimal=3,
        err_msg='Sparse group lasso qr failure for quantile 0.8 and lambda1=0')

    model = Regressor(model='qr', penalization='sgl', quantile=0.8, lambda1=0.1, alpha=0, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                  1.33241462e+01, 3.66710686e+01, 4.56237828e+00, 0.00000000e+00,
                  0.00000000e+00, 1.02229130e-04, 1.07166280e-04]),
        decimal=3,
        err_msg='Sparse group lasso qr failure for quantile 0.8, lambda1=0.1 and alpha=0')

    model = Regressor(model='qr', penalization='sgl', quantile=0.8, lambda1=0.1, alpha=1, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([0., 0., 0., 27.66071305,
                  90.01397685, 0., 0., 21.77214275, 45.01300237,
                  36.34016822]),
        decimal=3,
        err_msg='Sparse group lasso qr failure for quantile 0.8, lambda1=0.1 and alpha=1')

    model = Regressor(model='qr', penalization='sgl', quantile=0.8, lambda1=0.1, alpha=0.5, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([0., 0., 0., 21.95907657,
                  81.32544812, 2.84475096, 0., 20.76154792, 35.57092954,
                  36.05204591]),
        decimal=3,
        err_msg='Sparse group lasso qr failure for quantile 0.8, lambda1=0.1 and alpha=0.5')

    model = Regressor(model='qr', penalization='sgl', quantile=0.2, lambda1=0.1, alpha=0.5, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([0.00000000e+00, 3.97542269e-04, 6.63474565e-04,
                  2.09861368e+01, 6.62803756e+01, 3.97923687e-01, 0.00000000e+00,
                  3.84701424e+01, 2.45480120e+01, 3.01299190e+01]),
        decimal=3,
        err_msg='Sparse group lasso qr failure for quantile 0.2, lambda1=0.1 and alpha=0.5')


# ADAPTIVE LASSO ------------------------------------------------------------------------------------------------------

def test_alasso_lm():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]

    model = Regressor(model='lm', penalization='alasso', lambda1=0, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Adaptive lasso lm failure for lambda=0')

    model = Regressor(model='lm', penalization='alasso', lambda1=0.1, individual_weights=[0] * 10, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Adaptive lasso lm failure for lambda=0.1 and weights=0')

    model = Regressor(model='lm', penalization='alasso', lambda1=0.1, individual_power_weight=0, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.25821113, 15.00872081, 25.33148317, 56.132575,
                  99.34021902, 15.39857671, 10.35704837, 34.86962766, 61.42098122,
                  66.24809898]),
        decimal=3,
        err_msg='Adaptive lasso lm failure for lambda=0.1 and power_weight=0')

    model = Regressor(model='lm', penalization='alasso', lambda1=0.1, weight_technique='pca_pct',
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.40759085, 15.02505376, 25.42714541, 56.26154095,
                  99.31716436, 15.48349891, 10.46980939, 34.88025905, 61.46483173,
                  66.32724564]),
        decimal=3,
        err_msg='Adaptive lasso lm failure for lambda=0.1, weight_technique="pca_pct" and power_weight=1.2')

    model = Regressor(model='lm', penalization='alasso', lambda1=0.1, weight_technique='pca_pct', variability_pct=0.1,
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41947508, 15.12591301, 25.53676036, 56.26451599,
                  99.17162385, 15.56976165, 10.40965701, 34.91913924, 60.40617589,
                  66.2358729]),
        decimal=3,
        err_msg='Adaptive lasso lm failure for lambda=0.1, weight_technique="pca_pct", variability_pct=0.1 and power_weight=1.2')

    model = Regressor(model='lm', penalization='alasso', lambda1=0.1, weight_technique='pca_1',
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.3178, 19.7665, 31.4306, 55.9947, 91.4495, 19.995, 6.3401,
                  37.1303, 2.0283, 61.1574]),
        decimal=3,
        err_msg='Adaptive lasso lm failure for lambda=0.1, weight_technique="pca_1" and power_weight=1.2')

    model = Regressor(model='lm', penalization='alasso', lambda1=0.1, weight_technique='pls_1',
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([0., 15.8424663, 20.7085942,
                  47.99452202, 103.62678229, 10.07182228, 0.37932526,
                  36.87899711, 61.42687489, 65.81253078]),
        decimal=3,
        err_msg='Adaptive lasso lm failure for lambda=0.1, weight_technique="pls_1" and power_weight=1.2')

    model = Regressor(model='lm', penalization='alasso', lambda1=0.1, weight_technique='pls_pct',
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41482334, 15.0351054, 25.42670541, 56.26480226,
                  99.31477567, 15.48593938, 10.47706149, 34.8790109, 61.46425705,
                  66.32666869]),
        decimal=3,
        err_msg='Adaptive lasso lm failure for lambda=0.1, weight_technique="pls_pct" and power_weight=1.2')

    model = Regressor(model='lm', penalization='alasso', lambda1=0.1, weight_technique='unpenalized',
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41482334, 15.0351054, 25.42670541, 56.26480226,
                  99.31477567, 15.48593938, 10.47706149, 34.8790109, 61.46425705,
                  66.32666869]),
        decimal=3,
        err_msg='Adaptive lasso lm failure for lambda=0.1, weight_technique="unpenalized" and power_weight=1.2')

    model = Regressor(model='lm', penalization='alasso', lambda1=0.1, weight_technique='lasso',
                      individual_power_weight=1.2, lambda1_weights=10, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([18.50618959, 15.99793183, 23.00842766,
                  52.68183198, 102.88408418, 14.33748775, 0.,
                  35.57261592, 61.03437244, 65.84201609]),
        decimal=3,
        err_msg='Adaptive lasso lm failure for lambda=0.1, weight_technique="lasso", power_weight=1.2 and lasso_weights=10')


def test_alasso_qr():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]

    model = Regressor(model='qr', penalization='alasso', quantile=0.8, weight_technique='pca_pct', lambda1=0.1,
                      solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([21.98299416, 18.58883895, 24.00320703, 55.48866531,
                  99.26130871, 14.48554396, 9.7589368, 36.5871078, 58.41362123,
                  64.40034079]),
        decimal=3,
        err_msg='Adaptive lasso qr failure for quantile 0.8, weight_technique="pca_pct" and lambda1=0.1')

    model = Regressor(model='qr', penalization='alasso', quantile=0.2, weight_technique='pca_pct', lambda1=0.1,
                      solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.06895887, 13.70817285, 25.1125269,
                  56.67751033, 100.14818519, 14.66378046, 9.83289852,
                  34.53294509, 62.71185356, 67.31032544]),
        decimal=3,
        err_msg='Adaptive lasso qr failure for quantile 0.2, weight_technique="pca_pct" and lambda1=0.1')


# ADAPTIVE RIDGE ------------------------------------------------------------------------------------------------------

def test_aridge_lm():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]

    model = Regressor(model='lm', penalization='aridge', lambda1=0, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Adaptive ridge lm failure for lambda=0')

    model = Regressor(model='lm', penalization='aridge', lambda1=0.1, individual_weights=[0] * 10, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Adaptive ridge lm failure for lambda=0.1 and weights=0')

    model = Regressor(model='lm', penalization='aridge', lambda1=0.1, individual_power_weight=0, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([18.46772718, 15.2438716, 25.06222985, 50.31818813,
                  89.9845044, 14.03017725, 8.6725918, 33.33322947, 55.33924112,
                  58.02248048]),
        decimal=3,
        err_msg='Adaptive ridge lm failure for lambda=0.1 and power_weight=0')

    model = Regressor(model='lm', penalization='aridge', lambda1=0.1, weight_technique='pca_pct',
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([22.98471131, 14.70028341, 25.35506455, 56.01807932,
                  99.41114437, 15.30445687, 10.15810845, 34.91790446, 61.44395258,
                  66.27656906]),
        decimal=3,
        err_msg='Adaptive ridge lm failure for lambda=0.1, weight_technique="pca_pct" and power_weight=1.2')

    model = Regressor(model='lm', penalization='aridge', lambda1=0.1, weight_technique='pca_pct', variability_pct=0.1,
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.2873, 18.7112, 29.5655, 55.7678, 93.5404, 18.5662, 7.6139,
                  36.3732, 19.7147, 62.2061]),
        decimal=3,
        err_msg='Adaptive ridge lm failure for lambda=0.1, weight_technique="pca_pct", variability_pct=0.1 and power_weight=1.2')

    model = Regressor(model='lm', penalization='aridge', lambda1=0.1, weight_technique='pca_1',
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([8.9807, 5.0014, 22.2048, 33.9499, 78.2119, 12.6483, 1.2206,
                  25.3468, 0.5103, 35.8857]),
    decimal=3,
        err_msg='Adaptive ridge lm failure for lambda=0.1, weight_technique="pca_1" and power_weight=1.2')

    model = Regressor(model='lm', penalization='aridge', lambda1=0.1, weight_technique='pls_1',
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([0.2624502, 11.09122486, 16.54176195, 34.80771751,
                  88.67720963, 5.29540699, 0.40226454, 30.5390739, 46.33397339,
                  39.73372401]),
        decimal=3,
        err_msg='Adaptive ridge lm failure for lambda=0.1, weight_technique="pls_1" and power_weight=1.2')

    model = Regressor(model='lm', penalization='aridge', lambda1=0.1, weight_technique='pls_pct',
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.24260219, 14.99870036, 25.31850525, 56.1253754,
                  99.36498975, 15.38625846, 10.33598452, 34.87255987, 61.42942546,
                  66.25610992]),
        decimal=3,
        err_msg='Adaptive ridge lm failure for lambda=0.1, weight_technique="pls_pct" and power_weight=1.2')

    model = Regressor(model='lm', penalization='aridge', lambda1=0.1, weight_technique='unpenalized',
                      individual_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.24260219, 14.99870036, 25.31850525, 56.1253754,
                  99.36498975, 15.38625846, 10.33598452, 34.87255987, 61.42942546,
                  66.25610992]),
        decimal=3,
        err_msg='Adaptive ridge lm failure for lambda=0.1, weight_technique="unpenalized" and power_weight=1.2')

    model = Regressor(model='lm', penalization='aridge', lambda1=0.1, weight_technique='lasso',
                      individual_power_weight=1.2, lambda1_weights=10, solver='CLARABEL')
    model.fit(X, y)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([1.82365801e+01, 1.59339563e+01, 2.28611938e+01,
                  5.25005782e+01, 1.02943320e+02, 1.41203865e+01, 7.15024073e-03,
                  3.55827631e+01, 6.10175767e+01, 6.57531195e+01]),
        decimal=3,
        err_msg='Adaptive ridge lm failure for lambda=0.1, weight_technique="lasso", power_weight=1.2 and lasso_weights=10')


# ADAPTIVE GROUP LASSO ------------------------------------------------------------------------------------------------

def test_agl_lm():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='lm', penalization='agl', lambda1=0, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Adaptive group lasso lm failure for lambda=0')

    model = Regressor(model='lm', penalization='agl', lambda1=0.1, group_weights=[0] * 5, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Adaptive group lasso lm failure for lambda=0.1 and weights=0')

    model = Regressor(model='lm', penalization='agl', lambda1=0.1, group_power_weight=0, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.27677831, 15.0266414, 25.33723793, 56.16210945,
                  99.29269691, 15.45069947, 10.37091253, 34.87509388, 61.40852042,
                  66.24043667]),
        decimal=3,
        err_msg='Adaptive group lasso lm failure for lambda=0.1 and power_weight=0')

    model = Regressor(model='lm', penalization='agl', lambda1=0.1, weight_technique='pca_pct',
                      group_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.40811348, 15.03787478, 25.42532851, 56.26226056,
                  99.31646661, 15.48644655, 10.46922814, 34.87989905, 61.46374758,
                  66.32666011]),
        decimal=3,
        err_msg='Adaptive group lasso lm failure for lambda=0.1, weight_technique="pca_pct" and power_weight=1.2')


def test_agl_qr():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='qr', penalization='agl', quantile=0.8, weight_technique='pca_pct', lambda1=0.1,
                      solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([22.79424377, 18.96442717, 24.65673831, 55.84711541,
                  98.68308529, 14.67274364, 9.53221104, 35.33865081, 57.41022152,
                  64.67356877]),
        decimal=3,
        err_msg='Adaptive group lasso qr failure for quantile 0.8, weight_technique="pca_pct" and lambda1=0.1')

    model = Regressor(model='qr', penalization='agl', quantile=0.2, weight_technique='pca_pct', lambda1=0.1,
                      solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([22.56319979, 14.50549661, 25.96562376, 56.27532891,
                  98.3527059, 15.28195246, 10.47099655, 33.49308075, 62.33930551,
                  64.95028568]),
        decimal=3,
        err_msg='Adaptive group lasso qr failure for quantile 0.2, weight_technique="pca_pct" and lambda1=0.1')


# ADAPTIVE SPARSE GROUP LASSO -----------------------------------------------------------------------------------------

def test_asgl_lm():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='lm', penalization='asgl', lambda1=0, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Adaptive sparse group lasso lm failure for lambda=0')

    model = Regressor(model='lm', penalization='asgl', lambda1=0.1, group_weights=[0] * 5, individual_weights=[0] * 10,
                      solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.41982223, 15.03683211, 25.42968171, 56.26839201, 99.31178417,
                  15.48907319, 10.48258919, 34.87868221, 61.46433177, 66.32752383]),
        decimal=3,
        err_msg='Adaptive sparse group lasso lm failure for lambda=0.1 and weights=0')

    model = Regressor(model='lm', penalization='asgl', lambda1=0.1, alpha=0.5, group_power_weight=0,
                      individual_power_weight=0, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.26751759, 15.01769123, 25.33437106, 56.14736993,
                  99.31644424, 15.42466129, 10.36399787, 34.87235843, 61.41475275,
                  66.24427758]),
        decimal=3,
        err_msg='Adaptive sparse group lasso lm failure for lambda=0.1, alpha=0.5 and power_weight=0')

    model = Regressor(model='lm', penalization='asgl', lambda1=0.1, weight_technique='pca_pct',
                      individual_power_weight=1.2, group_power_weight=1.2, solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([23.40785215, 15.03146436, 25.42623689, 56.26190073,
                  99.31681551, 15.48497273, 10.46951875, 34.88007905, 61.46428965,
                  66.32695287]),
        decimal=3,
        err_msg='Adaptive sparse group lasso lm failure for lambda=0.1, weight_technique="pca_pct" and power_weight=1.2')


def test_asgl_qr():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='qr', penalization='asgl', quantile=0.8, weight_technique='pca_pct', lambda1=0.1, alpha=0.5,
                      solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([22.00090204, 18.58382297, 24.00078222, 55.51157208,
                  99.25845076, 14.49214498, 9.76078433, 36.58435945, 58.40130513,
                  64.40229948]),
        decimal=3,
        err_msg='Adaptive sparse group lasso qr failure for quantile 0.8, weight_technique="pca_pct", lambda1=0.1 and alpha=0.5')

    model = Regressor(model='qr', penalization='asgl', quantile=0.2, weight_technique='pca_pct', lambda1=0.1, alpha=0.5,
                      solver='CLARABEL')
    model.fit(X, y, group_index)
    np.testing.assert_array_almost_equal(
        model.coef_,
        np.array([22.56319952, 14.50549461, 25.9656223, 56.27532967,
                  98.35270706, 15.28195135, 10.4709951, 33.49308079, 62.3393046,
                  64.95028839]),
        decimal=3,
        err_msg='Adaptive sparse group lasso qr failure for quantile 0.2, weight_technique="pca_pct", lambda1=0.1 and alpha=0.5')


# ERROR HANDLING ------------------------------------------------------------------------------------------------------


def test_errors():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='qr', penalization='gl', quantile=0.2, lambda1=0.1, solver='CLARABEL')
    with pytest.raises(ValueError,
                       match="The penalization provided requires fitting the model with a group_index parameter but no group_index was detected."):
        model.fit(X, y)

    model = Regressor(model='aaa', penalization='lasso', quantile=0.2, lambda1=0.1, solver='CLARABEL')
    with pytest.raises(ValueError,
                       match="Invalid value for model parameter."):
        model.fit(X, y)

    model = Regressor(model='lm', penalization='aaa', quantile=0.2, lambda1=0.1, solver='CLARABEL')
    with pytest.raises(ValueError,
                       match="Invalid value for penalization parameter."):
        model.fit(X, y)

    model = Regressor(model='lm', penalization='alasso', quantile=0.1, lambda1=0.1, weight_technique='aaa',
                      solver='CLARABEL')
    with pytest.raises(AttributeError,
                       match="'Regressor' object has no attribute '_waaa'"):
        model.fit(X, y)


# SKLEARN COMPATIBILITY -----------------------------------------------------------------------------------------------


def test_predict():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='lm', penalization='asgl', lambda1=0.1, solver='CLARABEL')
    model.fit(X, y, group_index)
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    np.testing.assert_almost_equal(mse, np.float64(63.11994260430959),
                                   decimal=3,
                                   err_msg='Failed prediction and / or metric computation')


def test_grid_search():
    data = np.loadtxt('data.csv', delimiter=",", dtype=float)
    X = data[:, :-1]
    y = data[:, -1]
    group_index = np.array([1, 2, 2, 3, 3, 3, 4, 5, 5, 5])

    model = Regressor(model='lm', penalization='asgl', solver='CLARABEL')
    param_grid = {'lambda1': [1e-3, 1e-2, 10], 'alpha': [0, 0.5, 1], 'weight_technique': ['pca_pct', 'unpenalized']}
    gscv = GridSearchCV(model, param_grid=param_grid)
    gscv.fit(X, y, **{'group_index': group_index})
    expected_output = {'alpha': 1, 'lambda1': 0.01, 'weight_technique': 'pca_pct'}

    # Assert that the dictionary contains the expected key-value pairs
    for key, value in gscv.best_params_.items():
        assert expected_output.get(key) == value, f"Expected {key} to be {value}, but got {expected_output.get(key)}"


if __name__ == "__main__":
    pytest.main()
