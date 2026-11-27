"""O "modelo do cientista": soma térmica (graus-dia) e fase da cultura.

Valores ilustrativos para a POC, não são recomendações agronômicas reais.
"""

import polars as pl

BASE_TEMP_C = 10.0

STAGES = [
    (100, "emergence"),
    (700, "vegetative"),
    (1300, "flowering"),
]

def growing_degree_days(weather: pl.DataFrame, base_temp: float = BASE_TEMP_C) -> float:
    """ Soma, dia a dia, quanto a temperatura média passou da temperatura base. """
    result = weather.select(
        (((pl.col("t_min") + pl.col("t_max")) / 2) - base_temp)
        .clip(lower_bound=0)
        .sum()
        .alias("gdd")
    )
    return float(result.item())

def crop_stage(gdd: float) -> str:
    for limit, stage in STAGES:
        if gdd < limit:
            return stage
    return "maturity"