"""
    Tabela 6.1 pg.91
    Interpretação dos teores de argila, matéria orgânica e capacidade de troca de cátions (CTC ph7) do solo.
"""

from api.tables.classifiers import CLASSIFIERS


def clay_classifier(clay):
    if clay <= 20:
        return 4
    elif 20 < clay <= 40:
        return 3
    elif 40 < clay <= 60:
        return 2
    else:
        return 1


def organic_matter_classifier(organic_matter):
    if organic_matter <= 2.5:
        return CLASSIFIERS.LOW
    elif 2.5 < organic_matter <= 5:
        return CLASSIFIERS.MEDIUM
    else:
        return CLASSIFIERS.HIGH


def ctc_classifier(clay):
    if clay <= 7.5:
        return CLASSIFIERS.LOW
    elif 7.5 < clay <= 15:
        return CLASSIFIERS.MEDIUM
    elif 15 < clay <= 30:
        return CLASSIFIERS.HIGH
    else:
        return CLASSIFIERS.VERY_HIGH


TABLE_6_1 = {
    "clay": clay_classifier,
    "organic_matter": organic_matter_classifier,
    "ctc": ctc_classifier,
}
