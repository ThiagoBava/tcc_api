""" Potassium """
from api.tables.classifiers import CLASSIFIERS


def potassium_1_classifier(k_class, yield_expectation_kg):
    values = {
        CLASSIFIERS.VERY_LOW: 140,
        CLASSIFIERS.LOW: 100,
        CLASSIFIERS.MEDIUM: 90,
        CLASSIFIERS.HIGH: 60,
        CLASSIFIERS.VERY_HIGH: 0,
    }
    kg_K2_O_ha = values[k_class]

    # Acrescentar 10 kg de K2O/ha por tonelada adicional de grãos a serem produzidos.
    if yield_expectation_kg > 6000:
        kg_K2_O_ha += ((yield_expectation_kg - 6000) / 1000) * 10

    return kg_K2_O_ha


def potassium_2_classifier(k_class, yield_expectation_kg):
    values = {
        CLASSIFIERS.VERY_LOW: 100,
        CLASSIFIERS.LOW: 80,
        CLASSIFIERS.MEDIUM: 60,
        CLASSIFIERS.HIGH: 60,
        CLASSIFIERS.VERY_HIGH: 30 # ==> ver com professor: <= 60
    }
    kg_K2_O_ha = values[k_class]

    # Acrescentar 10 kg de K2O/ha por tonelada adicional de grãos a serem produzidos.
    if yield_expectation_kg > 6000:
        kg_K2_O_ha += ((yield_expectation_kg - 6000) / 1000) * 10

    return kg_K2_O_ha


POTASSIUM_6_1_14 = {
    1: potassium_1_classifier,
    2: potassium_2_classifier,
}
