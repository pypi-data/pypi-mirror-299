# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the license found in the LICENSE.txt file in the root
# directory of this source tree.


# =======
# Imports
# =======

import numpy as np
from ..models.util import kl_divergence


# ============
# float to str
# ============

def _float_to_str(x):
    """
    Convert a float number to string with fixed length.
    """

    if x == float('inf'):
        x_str = ' ' * (len(f'{0:0.1f}')) + 'inf'
    elif x == float('-inf'):
        x_str = '-' + ' ' * (len(f'{0:0.1f}') - 1) + 'inf'
    elif np.isnan(x):
        x_str = ' ' * (len(f'{0:0.1f}')) + 'nan'
    else:
        x_str = f'{x:>0.4f}'

    return x_str


# ========
# evaluate
# ========

def evaluate(
        models: list,
        train: bool = False,
        report: bool = True):
    """
    Evaluate models for goodness of fit with respect to training data.

    Parameters
    ----------

    models : list[leaderbot.models.BaseModel]
        A single or a list of models to be evaluated.

        .. note::

            All models should be created using the same dataset to make proper
            comparison.

    train : bool, default=False
        If `True`, the models will be trained. If `False`, it is assumed that
        the models are pre-trained.

    report : bool, default=False
        If `True`, a table of the analysis is printed.

    Returns
    -------

    metrics : dict
        A dictionary containing the following keys and values:

        * ``'name'``: list of names of the models.
        * ``'n_param'``: list of number of parameters of the models.
        * ``'nll'``: list of negative log-likelihood values of the models.
        * ``'jsd'``: list of Jensen-Shannon divergences of the models.
        * ``'kld'``: list of Kullback-Leiber divergences of the models.
        * ``'aic'``: list of Akaike information criterion of the models.
        * ``'bic'``: list of Bayesian information criterion of the models.

    Raises
    ------

    RuntimeError
        if ``train`` is `False` but at least one of the models are not
        pre-trained.

    Examples
    --------

    .. code-block:: python

        >>> import leaderbot as lb

        >>> # Obtain data
        >>> data = lb.data.load()

        >>> # Create models to compare
        >>> model_01 = lb.models.BradleyTerry(data)
        >>> model_02 = lb.models.BradleyTerryScaled(data)
        >>> model_03 = lb.models.BradleyTerryScaledR(data)
        >>> model_04 = lb.models.RaoKupper(data)
        >>> model_05 = lb.models.RaoKupperScaled(data)
        >>> model_06 = lb.models.RaoKupperScaledR(data)
        >>> model_07 = lb.models.Davidson(data)
        >>> model_08 = lb.models.DavidsonScaled(data)
        >>> model_09 = lb.models.DavidsonScaledR(data)

        >>> # Create a list of models
        >>> models = [model_01, model_02, model_03,
        ...           model_04, model_05, model_06,
        ...           model_07, model_08, model_09]

        >>> # Evaluate models
        >>> metrics = lb.evaluate(models, train=True, report=True)

        The above code outputs the following table

        .. literalinclude:: ../_static/data/evaluate.txt
            :language: none
    """

    # Convert a single model to a singleton list
    if not isinstance(models, list):
        models = [models]

    if train:
        for model in models:
            model.train()
    else:
        # Check a model is trained
        for model in models:
            if model.param is None:
                raise RuntimeError('Models are not trained. Set "train" to'
                                   '"True", or pre-train models in advance.')

    # Outputs
    name = []
    n_param = []
    nll = []  # Negative log-likelihood
    cel = []  # Cross-Eentropy loss
    kld = []  # Kullback-Leibler divergence
    jsd = []  # Jensen-Shannon divergence
    aic = []  # Akaike information criterion
    bic = []  # Bayesian information criterion

    for model in models:

        # Model attributes
        name.append(model.__class__.__name__)
        n_param.append(model.n_param)

        # Divergences
        jsd.append(_evaluate_jsd(model))
        kld.append(_evaluate_kld(model))

        # Cross entropy loss
        cel.append(_evaluate_cel(model))

        # Loss with no constraint (just likelihood)
        nll_ = model.loss(return_jac=False, constraint=False)
        nll.append(nll_)

        # Information criteria
        aic.append(_evaluate_aic(model, nll_))
        bic.append(_evaluate_bic(model, nll_))

    # Output
    metrics = {
        'name': name,
        'n_param': n_param,
        'nll': nll,
        'cel': cel,
        'jsd': jsd,
        'kld': kld,
        'aic': aic,
        'bic': bic,
    }

    if report:
        print('+-----------------------+---------+--------+--------+--------+---------+--------+--------+')
        print('| name                  | # param | NLL    | CEL    | AIC    | BIC     | KLD    | JSD %  |')
        print('+-----------------------+---------+--------+--------+--------+---------+--------+--------+')

        for i in range(len(name)):

            name_length = 21
            name_str = name[i]
            if len(name_str) > name_length:
                name_str = name_str[:(name_length - 3)] + '...'
            name_str = name_str.ljust(name_length)

            cel_str = _float_to_str(cel[i])
            kld_str = _float_to_str(kld[i])

            print(f'| {name_str:<21s} '
                  f'| {n_param[i]:>7} '
                  f'| {nll[i]:>0.4f} '
                  f'| {cel_str} '
                  f'| {aic[i]:>0.2f} '
                  f'| {bic[i]:>0.2f} '
                  f'| {kld_str} '
                  f'| {100.0 * jsd[i]:>0.4f} |')

        print('+-----------------------+---------+--------+--------+--------+---------+--------+--------+')

    return metrics


# ============
# evaluate cel
# ============

def _evaluate_cel(model):
    """
    Cross-Entropy Loss.


    Notes
    -----

    When CEL is not inf, its value is exactly identical to NLL.

    The Bradley-Terry models (where no tie is included), the CEL value is non.
    For all other models, CEL and NLL are identical.
    """

    y = model.y
    p_pred = model.infer()

    cel = y * np.log(p_pred)
    cel[y == 0] = 0.0
    cel = -cel.sum() / y.sum()

    return cel


# ============
# evaluate kld
# ============

def _evaluate_kld(model):
    """
    Kullback-Leibler divergence.
    """

    y = model.y
    p_pred = model.infer()

    y_sum = y.sum(axis=1, keepdims=True)
    y_sum[y_sum == 0] = 1.0
    p_obs = y / y_sum

    kld = kl_divergence(p_obs, p_pred)
    kld = kld.sum(axis=1)

    kld = np.mean(kld)
    # kld_mean = np.mean(kld)
    # kld_std = np.std(kld)

    return kld


# ============
# evaluate jsd
# ============

def _evaluate_jsd(model):
    """
    Jensen-Shannon divergence.
    """

    y = model.y
    p_pred = model.infer()

    y_sum = y.sum(axis=1, keepdims=True)
    y_sum[y_sum == 0] = 1.0
    p_obs = y / y_sum
    p_mean = (p_pred + p_obs) / 2.0

    jsd = 0.5 * (kl_divergence(p_obs, p_mean) + kl_divergence(p_pred, p_mean))
    jsd = jsd.sum(axis=1)

    jsd = np.mean(jsd)
    # jsd_mean = np.mean(jsd)
    # jsd_std = np.std(jsd)

    return jsd


# ============
# evaluate aic
# ============

def _evaluate_aic(model, nll):
    """
    Akaike information criterion.
    """

    aic = 2.0 * model.n_param - 2.0 * nll
    return aic


# ============
# evaluate bic
# ============

def _evaluate_bic(model, nll):
    """
    Bayesian information criterion
    """

    x = model.x
    n_samples = x.shape[0]

    bic = model.n_param * np.log(n_samples) - 2.0 * nll
    return bic
