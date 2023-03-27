"""
    Tabela 6.4 Argila pg.95
"""
from api.tables.classifiers import CLASSIFIERS


def class_1_classifier(phosphor):
    if phosphor <= 3:
        return CLASSIFIERS.VERY_LOW
    elif 3 < phosphor <= 6:
        return CLASSIFIERS.LOW
    elif 6 < phosphor <= 9:
        return CLASSIFIERS.MEDIUM
    elif 9 < phosphor <= 12:
        return CLASSIFIERS.HIGH
    else:
        return CLASSIFIERS.VERY_HIGH


def class_2_classifier(phosphor):
    if phosphor <= 4:
        return CLASSIFIERS.VERY_LOW
    elif 4 < phosphor <= 8:
        return CLASSIFIERS.LOW
    elif 8 < phosphor <= 12:
        return CLASSIFIERS.MEDIUM
    elif 12 < phosphor <= 24:
        return CLASSIFIERS.HIGH
    else:
        return CLASSIFIERS.VERY_HIGH


def class_3_classifier(phosphor):
    if phosphor <= 6:
        return CLASSIFIERS.VERY_LOW
    elif 6 < phosphor <= 12:
        return CLASSIFIERS.LOW
    elif 12 < phosphor <= 18:
        return CLASSIFIERS.MEDIUM
    elif 18 < phosphor <= 36:
        return CLASSIFIERS.HIGH
    else:
        return CLASSIFIERS.VERY_HIGH


def class_4_classifier(phosphor):
    if phosphor <= 10:
        return CLASSIFIERS.VERY_LOW
    elif 10 < phosphor <= 20:
        return CLASSIFIERS.LOW
    elif 20 < phosphor <= 30:
        return CLASSIFIERS.MEDIUM
    elif 30 < phosphor <= 60:
        return CLASSIFIERS.HIGH
    else:
        return CLASSIFIERS.VERY_HIGH


TABLE_6_4 = {
    1: class_1_classifier,
    2: class_2_classifier,
    3: class_3_classifier,
    4: class_4_classifier
}
