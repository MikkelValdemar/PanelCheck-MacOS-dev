import numpy as np
import pandas as pd
from scipy.stats import f, t
import statsmodels.api as sm
from statsmodels.formula.api import ols


def sensmixed_ver42(frame):
    '''
    # Fmatr, row 1: 3-way: Ass VS Mixed error (Prod*Ass and Rep*Ass) (*1)
    # Fmatr, row 2: 3-way: Prod vs Mixed error (Prod*Ass and Rep*Prod) (*2)
    # Fmatr, row 3: 3-way: Rep vs Mixed error (Prod*Rep and Rep*Ass)
    # Fmatr, row 4: 3-way: Prod*Ass vs. Error
    # Fmatr, row 5: 3-way: Prod*Rep vs. Error
    # Fmatr, row 6: 3-way: Rep*Ass  vs. Error

    # Fmatr, row 7: 2-way: Prod vs Prod*Ass
    # Fmatr, row 8: 2-way: Ass vs Prod*Ass
    # Fmatr, row 9: 2-way: Prod*Ass vs. Error

    # (*1) IF the MS(Rep*Ass) is smaller than MS(E) then MS(Prod*Ass) is used.
    # (*2) IF the MS(Prod*Rep) is smaller than MS(E) then MS(Prod*Ass) is used.

    # Pmatr and Pmatr2 has same structure

    # LSDmatr, row 1: 3-way usual LSD
    # LSDmatr, row 2: 3-way Bonferroni LSD
    # LSDmatr, row 3: 2-way usual LSD
    # LSDmatr, row 4: 2-way Bonferroni LSD
    '''
    # Extract attribute names and number of attributes
    attnames = frame.columns[3:]
    natt = len(attnames)

    # Define factors and levels
    ass = frame.iloc[:, 0].astype('category')
    assnames = ass.cat.categories
    nass = len(assnames)

    prod = frame.iloc[:, 1].astype('category')
    prodnames = prod.cat.categories
    nprod = len(prodnames)

    rep = frame.iloc[:, 2].astype('category')
    repnames = rep.cat.categories
    nrep = len(repnames)

    nrow = frame.shape[0]
    ncol = frame.shape[1]

    # Initialize matrices for storing results
    aovSS = np.zeros((7, natt))

    for i in range(3, ncol):
        X = frame.iloc[:, i]
        model = ols('X ~ C(ass) + C(prod) + C(rep) + C(ass):C(prod) + C(ass):C(rep) + C(prod):C(rep)',
                    data=frame.assign(X=X)).fit()
        aov_table = sm.stats.anova_lm(model, typ=2)
        aovSS[:, i - 3] = aov_table['sum_sq'].values

    aovDF = aov_table['df'].values

    # Initialize matrices for F-values, p-values, and LSD
    Fmatr = np.zeros((9, natt))
    Pmatr = np.zeros((9, natt))
    LSDmatr = np.zeros((4, natt))

    # 2-way analysis
    Fmatr[6, :] = (aovSS[1, :] / aovDF[1]) / (aovSS[3, :] / aovDF[3])
    Fmatr[7, :] = (aovSS[0, :] / aovDF[0]) / (aovSS[3, :] / aovDF[3])
    Fmatr[8, :] = (aovSS[3, :] / aovDF[3]) / (
            (aovSS[2, :] + aovSS[4, :] + aovSS[5, :] + aovSS[6, :]) / (aovDF[2] + aovDF[4] + aovDF[5] + aovDF[6]))
    Pmatr[6, :] = 1 - f.cdf(Fmatr[6, :], aovDF[1], aovDF[3])
    Pmatr[7, :] = 1 - f.cdf(Fmatr[7, :], aovDF[0], aovDF[3])
    Pmatr[8, :] = 1 - f.cdf(Fmatr[8, :], aovDF[3], aovDF[2] + aovDF[4] + aovDF[5] + aovDF[6])

    # 3-way analysis
    Fmatr[0, :] = (aovSS[0, :] / aovDF[0]) / (aovSS[3, :] / aovDF[3])
    for i in range(natt):
        if (aovSS[4, i] / aovDF[4]) > (aovSS[6, i] / aovDF[6]):
            Fmatr[0, i] = (aovSS[0, i] / aovDF[0]) / (
                    (aovSS[3, i]) / (aovDF[3]) + aovSS[4, i] / aovDF[4] - aovSS[6, i] / aovDF[6])

    Fmatr[1, :] = (aovSS[1, :] / aovDF[1]) / (aovSS[3, :] / aovDF[3])
    for i in range(natt):
        if (aovSS[5, i] / aovDF[5]) > (aovSS[6, i] / aovDF[6]):
            Fmatr[1, i] = (aovSS[1, i] / aovDF[1]) / (
                    (aovSS[3, i]) / (aovDF[3]) + aovSS[5, i] / aovDF[5] - aovSS[6, i] / aovDF[6])

    for i in range(natt):
        Fmatr[2, i] = (aovSS[2, i] / aovDF[2]) / (
                (aovSS[4, i]) / (aovDF[4]) + aovSS[5, i] / aovDF[5] - aovSS[6, i] / aovDF[6])

    Fmatr[3, :] = (aovSS[3, :] / aovDF[3]) / (aovSS[6, :] / aovDF[6])
    Fmatr[4, :] = (aovSS[4, :] / aovDF[4]) / (aovSS[6, :] / aovDF[6])
    Fmatr[5, :] = (aovSS[5, :] / aovDF[5]) / (aovSS[6, :] / aovDF[6])

    Pmatr[3, :] = 1 - f.cdf(Fmatr[3, :], aovDF[3], aovDF[6])
    Pmatr[4, :] = 1 - f.cdf(Fmatr[4, :], aovDF[4], aovDF[6])
    Pmatr[5, :] = 1 - f.cdf(Fmatr[5, :], aovDF[5], aovDF[6])

    DFden1 = np.zeros(natt)
    Pmatr[0, :] = 1 - f.cdf(Fmatr[0, :], aovDF[0], aovDF[3])
    for i in range(natt):
        if (aovSS[4, i] / aovDF[4]) > (aovSS[6, i] / aovDF[6]):
            DFden1[i] = (aovSS[3, i] / aovDF[3] + aovSS[4, i] / aovDF[4] - aovSS[6, i] / aovDF[6]) ** 2 / (
                    (aovSS[3, i] ** 2 / aovDF[3] ** 3) + (aovSS[4, i] ** 2 / aovDF[4] ** 3) + (
                    aovSS[6, i] ** 2 / aovDF[6] ** 3)
            )
            Pmatr[0, i] = 1 - f.cdf(Fmatr[0, i], aovDF[0], DFden1[i])

    DFden2 = np.zeros(natt)
    Pmatr[1, :] = 1 - f.cdf(Fmatr[1, :], aovDF[1], aovDF[3])
    for i in range(natt):
        if (aovSS[5, i] / aovDF[5]) > (aovSS[6, i] / aovDF[6]):
            DFden2[i] = (aovSS[3, i] / aovDF[3] + aovSS[5, i] / aovDF[5] - aovSS[6, i] / aovDF[6]) ** 2 / (
                    (aovSS[3, i] ** 2 / aovDF[3] ** 3) + (aovSS[5, i] ** 2 / aovDF[5] ** 3) + (
                    aovSS[6, i] ** 2 / aovDF[6] ** 3)
            )
            Pmatr[1, i] = 1 - f.cdf(Fmatr[1, i], aovDF[1], DFden2[i])

    DFden3 = np.zeros(natt)
    for i in range(natt):
        DFden3[i] = (aovSS[3, i] / aovDF[3] + aovSS[5, i] / aovDF[5] - aovSS[6, i] / aovDF[6]) ** 2 / (
                (aovSS[3, i] ** 2 / aovDF[3] ** 3) + (aovSS[5, i] ** 2 / aovDF[5] ** 3) + (
                aovSS[6, i] ** 2 / aovDF[6] ** 3)
        )
        Pmatr[2, i] = 1 - f.cdf(Fmatr[2, i], aovDF[2], DFden3[i])

    Pmatr2 = Pmatr.copy()
    Pmatr2[Pmatr2 > 0.05] = 4
    Pmatr2[Pmatr2 < 0.001] = 3
    Pmatr2[Pmatr2 < 0.01] = 2
    Pmatr2[Pmatr2 < 0.05] = 1
    Pmatr2[Pmatr2 > 3.5] = 0

    MS = aovSS[3, :] / aovDF[3]

    LSDmatr[2, :] = np.sqrt(2 * MS / (nrep * nass)) * t.ppf(0.975, aovDF[3])
    LSDmatr[3, :] = np.sqrt(2 * MS / (nrep * nass)) * t.ppf(1 - 0.05 / (nprod * (nprod - 1)), aovDF[3])

    LSDmatr[0, :] = LSDmatr[2, :]
    LSDmatr[1, :] = LSDmatr[3, :]

    for i in range(natt):
        if (aovSS[5, i] / aovDF[5]) > (aovSS[6, i] / aovDF[6]):
            MS = aovSS[3, i] / aovDF[3] + aovSS[5, i] / aovDF[5] - aovSS[6, i] / aovDF[6]
            LSDmatr[0, i] = np.sqrt(2 * MS / (nrep * nass)) * t.ppf(0.975, DFden2[i])
            LSDmatr[1, i] = np.sqrt(2 * MS / (nrep * nass)) * t.ppf(1 - 0.05 / (nprod * (nprod - 1)), DFden2[i])

    return Fmatr, Pmatr, Pmatr2, LSDmatr


def sensmixed_no_rep_11(frame):
    attnames = frame.columns[3:]
    natt = len(attnames)

    ass = frame.iloc[:, 0].astype('category')
    assnames = ass.cat.categories
    nass = len(assnames)

    prod = frame.iloc[:, 1].astype('category')
    prodnames = prod.cat.categories
    nprod = len(prodnames)

    rep = frame.iloc[:, 2].astype('category')
    repnames = rep.cat.categories
    nrep = len(repnames)

    nrow = frame.shape[0]
    ncol = frame.shape[1]

    aovSS = np.zeros((3, natt))

    for i in range(3, ncol):
        X = frame.iloc[:, i]
        model = ols('X ~ C(ass) + C(prod)', data=frame.assign(X=X)).fit()
        aov_table = sm.stats.anova_lm(model, typ=2)
        aovSS[:, i - 3] = aov_table['sum_sq'].values

    aovDF = aov_table['df'].values

    Fmatr = np.zeros((2, natt))
    Pmatr = np.zeros((2, natt))
    LSDmatr = np.zeros((2, natt))

    Fmatr[0, :] = (aovSS[0, :] / aovDF[0]) / (aovSS[2, :] / aovDF[2])
    Fmatr[1, :] = (aovSS[1, :] / aovDF[1]) / (aovSS[2, :] / aovDF[2])

    Pmatr[0, :] = 1 - f.cdf(Fmatr[0, :], aovDF[0], aovDF[2])
    Pmatr[1, :] = 1 - f.cdf(Fmatr[1, :], aovDF[1], aovDF[2])

    Pmatr[Pmatr > 0.05] = 4
    Pmatr[Pmatr < 0.001] = 3
    Pmatr[Pmatr < 0.01] = 2
    Pmatr[Pmatr < 0.05] = 1
    Pmatr[Pmatr > 3.5] = 0

    MS = aovSS[2, :] / aovDF[2]

    LSDmatr[0, :] = np.sqrt(2 * MS / (nrep * nass)) * t.ppf(0.975, aovDF[2])
    LSDmatr[1, :] = np.sqrt(2 * MS / (nrep * nass)) * t.ppf(1 - 0.05 / (nprod * (nprod - 1)), aovDF[2])

    return Fmatr, Pmatr, LSDmatr
