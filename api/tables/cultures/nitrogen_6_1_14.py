"""
    Tabela 6.1.14 Nitrogênio pg.125
"""
from api.tables.classifiers import CLASSIFIERS


def _organic_matter_classifier(organic_matter):
    if organic_matter <= 2.5:
        return CLASSIFIERS.LOW
    elif 2.5 < organic_matter <= 5:
        return CLASSIFIERS.MEDIUM
    else:
        return CLASSIFIERS.HIGH


def _grass_classifier(organic_matter: float, yield_expectation_kg: int, plant_density_hectare: int):
    values = {
        CLASSIFIERS.LOW: 90,
        CLASSIFIERS.MEDIUM: 70,
        CLASSIFIERS.HIGH: 50,
    }
    organic_matter_class = _organic_matter_classifier(organic_matter)
    kg_N_ha = values[organic_matter_class]

    # PENSAR EM UM METODO DE DEIXAR UMA MANEIRA DE EXPRESSAR
    # A CONDIÇÃO NA TABELA <= 50
    # if organic_matter_class == 3:
    # kg_N_ha *= 1 - organic_matter

    # Pode-se aumentar a quantidade de N em 20 a 40 kg/ha
    if organic_matter > 4:
        kg_N_ha += 30

    # Acrescentar aos valores da tabela 15kg de N/ha, por tonelada adicional a serem produzidos.
    if yield_expectation_kg > 6000:
        kg_N_ha += ((yield_expectation_kg - 6000) / 1000) * 15

        # Aumentar as quantidades de N em 20 a 40%
        if yield_expectation_kg > 10000:
            kg_N_ha *= 1.3

    # Aumentar as doses de N em 10 kh/ha, para cada incremento de 5000 plantas/ha.
    if plant_density_hectare > 60000:
        kg_N_ha += ((plant_density_hectare - 60000) / 5000) * 5

    return kg_N_ha


NITROGEN_6_1_14 = {
    'organic_matter_classifier': _organic_matter_classifier,
    "grass": _grass_classifier,
    "consortium": {},
    "legume": {}
}
