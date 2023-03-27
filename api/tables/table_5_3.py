"""
    Tabela 5.3 pg.75
    Critérios para a indicação da necessidade e da quantidade de corretivos da acidez para culturas de grãos.
"""

TABLE_5_3 = {
    "in_all_cases": {
        "decision_making": {
            "ph": 5.5,
            "al": None
        },
        "ph_reference": 6,
        "aplication_mode": "incorporated"
    },
    "system_implementation": {
        "decision_making": {
            "ph": 5.5,
            "al": None
        },
        "ph_reference": 6,
        "aplication_mode": "incorporated"

    },
    "Consolidated_system_no_restriction": {
        "decision_making": {
            "ph": 5.5,
            "al": None
        },
        "ph_reference": 6,
        "aplication_mode": "shallow"

    },
    "Consolidated_system_with_restriction": {
        "decision_making": {
            "ph": 5.5,
            "al": 30
        },
        "ph_reference": 6,
        "aplication_mode": "incorporated"

    },
}
