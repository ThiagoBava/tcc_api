"""
    Tabela 6.1.14 Fósforo pg.127
"""

from api.tables.classifiers import CLASSIFIERS


def phosphor_1_classifier(phosphor_class: str, yield_expectation_kg: int) -> int:
    values = {
        CLASSIFIERS.VERY_LOW: 200,
        CLASSIFIERS.LOW: 140,
        CLASSIFIERS.MEDIUM: 130,
        CLASSIFIERS.HIGH: 90,
        CLASSIFIERS.VERY_HIGH: 0,
    }
    kg_P2_O5_ha = values[phosphor_class]

    # Acrescentar 15 kg de P2O5/ha por tonelada adicional de grãos a serem produzidos.
    if yield_expectation_kg > 6000:
        kg_P2_O5_ha += ((yield_expectation_kg - 6000) / 1000) * 15

    return kg_P2_O5_ha


def phosphor_2_classifier(phosphor_class, yield_expectation_kg):
    values = {
        CLASSIFIERS.VERY_LOW: 140,
        CLASSIFIERS.LOW: 120,
        CLASSIFIERS.MEDIUM: 90,
        CLASSIFIERS.HIGH: 90,
        CLASSIFIERS.VERY_HIGH: 45 # ==> ver com professor: <= 90
    }
    kg_P2_O5_ha = values[phosphor_class]

    # Acrescentar 15 kg de P2O5/ha por tonelada adicional de grãos a serem produzidos.
    if yield_expectation_kg > 6000:
        kg_P2_O5_ha += ((yield_expectation_kg - 6000) / 1000) * 15

    return kg_P2_O5_ha


PHOSPHOR_6_1_14 = {
    1: phosphor_1_classifier,
    2: phosphor_2_classifier,
}
