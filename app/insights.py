"""Derived descriptive comparisons from the saved Spark joint aggregate.

All rates use summed survey-weight numerators and denominators. This module does
not infer causation, standard errors, or population counts.
"""
from __future__ import annotations
import pandas as pd


def aggregate(cube: pd.DataFrame, dimensions: list[str]) -> pd.DataFrame:
    fields=['n','weight_denominator','weighted_employed']
    out=cube.groupby(dimensions,as_index=False,observed=True)[fields].sum()
    out['rate']=100*out['weighted_employed']/out['weight_denominator']
    return out


def age_standardized_sector(cube: pd.DataFrame) -> tuple[pd.DataFrame, dict[str,float]]:
    """Apply the combined sample's weighted age distribution to each sector."""
    grouped=aggregate(cube,['sector','age_band'])
    mix=grouped.groupby('age_band',observed=True)['weight_denominator'].sum()
    mix=mix/mix.sum()
    rates={}
    for sector in ['Rural','Urban']:
        sub=grouped[grouped['sector']==sector].set_index('age_band')
        if set(sub.index)!=set(mix.index):
            raise ValueError('Age bands differ by sector')
        rates[sector]=float((sub['rate']*mix).sum())
    return grouped,rates


def marital_by_age(cube: pd.DataFrame) -> pd.DataFrame:
    return aggregate(cube,['age_band','marital'])


def education_by_sector(cube: pd.DataFrame) -> pd.DataFrame:
    return aggregate(cube,['education','sector'])


def state_by_sector(cube: pd.DataFrame) -> pd.DataFrame:
    return aggregate(cube,['state','sector'])
