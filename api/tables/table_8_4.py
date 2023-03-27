"""
    Tabela 8.4 Fertilizantes  pg.304
"""

TABLE_8_4 = {
    'nitrogen': {
        'urea': {
            'minimum_guarantee': 45,
        },
        'ammonium_sulfate': {
            'minimum_guarantee': 20,
            'comments': {
                's': 23
            }
        },
        'ammonium_nitrate': {
            'minimum_guarantee': 32
        },
        'calcium_nitrate': {
            'minimum_guarantee': 14,
            'comments': {
                'ca': 17.5
            }
        },
    },
    'phosphate': {
        'single_superphosphate': {
            'minimum_guarantee': 18,
            'comments': {
                'ca': 18,
                's': 10
            }
        },
        'triple_superphosphate': {
            'minimum_guarantee': 41,
            'comments': {
                'ca': 10
            }
        },
        'monoammonium_phosphate_map': {
            'minimum_guarantee': 48,
            'comments': {
                'n': 9
            }
        },
        'diammonium_phosphate_dap': {
            'minimum_guarantee': 45,
            'comments': {
                'n': 17
            }
        },
        'partially_acidulated_rock_phosphate': {
            'minimum_guarantee': 9,
            'comments': {
                'ca': 21.5,
                's': 3,
                'mg': 1
            }
        },
        'magnesium_thermophosphate': {
            'minimum_guarantee': 17,
            'comments': {
                'ca': 18,
                'mg': 7
            }
        },
        'rock_phosphate': {
            'minimum_guarantee': 4,
            'comments': {
                'ca': 23.5,
            }
        },
        'reactive_rock_phosphate': {
            'minimum_guarantee': 9,
            'comments': {
                'ca': 31,
            }
        },
        'calcined_bone_meal': {
            'minimum_guarantee': 16,
            'comments': {
                'n': 1,
            }
        },
    },
    'potash': {
        'potassium_chloride': {
            'minimum_guarantee': 58,
        },
        'potassium_sulfate': {
            'minimum_guarantee': 48,
            'comments': {
                'cl': 46.5,
                's': 16
            }
        },
    }
}

