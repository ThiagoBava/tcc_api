"""
    Tabela 9.5 pg.323
    Valores médios de eficiência agronômica dos nutrientes de diferentes adubos
    orgânicos aplicados no solo em dois cultivos sucessivos.
"""

TABLE_9_5 = {
    'chicken_bed': {
        'n': {1: 0.5, 2: 0.2},
        'p': {1: 0.8, 2: 0.2},
        'k': {1: 1, 2: None},
    },
    'solid_swine_manure': {
        'n': {1: 0.6, 2: 0.2},
        'p': {1: 0.8, 2: 0.2},
        'k': {1: 1, 2: None},
    },
    'solid_cattle_manure': {
        'n': {1: 0.3, 2: 0.2},
        'p': {1: 0.8, 2: 0.2},
        'k': {1: 1, 2: None},
    },
    'pig_liquid_waste': {
        'n': {1: 0.8, 2: None},
        'p': {1: 0.9, 2: 0.1},
        'k': {1: 1, 2: None},
    },
    'bovine_liquid_waste': {
        'n': {1: 0.5, 2: 0.2},
        'p': {1: 0.8, 2: 0.2},
        'k': {1: 1, 2: None},
    },
    'bunk_bed_and_pig_wishing_compound': {
        'n': {1: 0.2, 2: None},
        'p': {1: 0.7, 2: 0.3},
        'k': {1: 1, 2: None},
    },
    'other_organic_waste': {
        'n': {1: 0.5, 2: 0.2},
        'p': {1: 0.7, 2: 0.2},
        'k': {1: 1, 2: None},
    },
    'sewage_sludge_and_garbage_compost': {
        'n': {1: 0.2, 2: None},
        'p': None,
        'k': None,
    },
}
