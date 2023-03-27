"""
    Tabela 6.9 Potássio / CTC pg.96
"""
from api.tables.classifiers import CLASSIFIERS


def class_0_to_7_5_classifier(potassium):
    if potassium <= 20:
        return CLASSIFIERS.VERY_LOW
    elif 20 < potassium <= 40:
        return CLASSIFIERS.LOW
    elif 40 < potassium <= 60:
        return CLASSIFIERS.MEDIUM
    elif 60 < potassium <= 120:
        return CLASSIFIERS.HIGH
    else:
        return CLASSIFIERS.VERY_HIGH


def class_7_6_to_15_classifier(potassium):
    if potassium <= 30:
        return CLASSIFIERS.VERY_LOW
    elif 30 < potassium <= 60:
        return CLASSIFIERS.LOW
    elif 60 < potassium <= 90:
        return CLASSIFIERS.MEDIUM
    elif 90 < potassium <= 180:
        return CLASSIFIERS.HIGH
    else:
        return CLASSIFIERS.VERY_HIGH


def class_15_1_to_30_classifier(potassium):
    if potassium <= 40:
        return CLASSIFIERS.VERY_LOW
    elif 40 < potassium <= 80:
        return CLASSIFIERS.LOW
    elif 80 < potassium <= 120:
        return CLASSIFIERS.MEDIUM
    elif 120 < potassium <= 240:
        return CLASSIFIERS.HIGH
    else:
        return CLASSIFIERS.VERY_HIGH


def class_30_1_upper_classifier(potassium):
    if potassium <= 45:
        return CLASSIFIERS.VERY_LOW
    elif 45 < potassium <= 90:
        return CLASSIFIERS.LOW
    elif 90 < potassium <= 135:
        return CLASSIFIERS.MEDIUM
    elif 135 < potassium <= 270:
        return CLASSIFIERS.HIGH
    else:
        return CLASSIFIERS.VERY_HIGH


def ctc_classifier(ctc_dm_3, potassium):
    if ctc_dm_3 <= 7.5:
        return class_0_to_7_5_classifier(potassium)
    elif 7.5 < potassium <= 15:
        return class_7_6_to_15_classifier(potassium)
    elif 15 < potassium <= 30:
        return class_15_1_to_30_classifier(potassium)
    else:
        return class_30_1_upper_classifier(potassium)


TABLE_6_9 = ctc_classifier
