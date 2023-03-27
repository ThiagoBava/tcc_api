MANAGEMENT_SYSTEM = (
    ('conventional', 'Convencional'),
    ('no-till', 'Plantio direto'),
    ('irrigated rice', 'Arroz irrigado'),
)

AREA_CONDITION = (
        ('in_all_cases', 'Em todos os casos'),
        ('system_implementation', 'Implantação do sistema'),
        ('Consolidated_system_no_restriction', 'Consolidado sem restrições'),
        ('Consolidated_system_with_restriction', 'Consolidado com restrições'),
        ('Sowing_in_dry_soil', 'Semeadura em solo seco'),
        ('Pre_germinated_or_seedling_transplant', 'Pré-germinado ou transplante de muda'),
    )

SOIL_SAMPLING = (
    ('0_10', '0_10'),
    ('0_20', '0_20'),
    ('10_20', '10_20'),
)

REFERENCE_PH = (
    ('6', 6),
    ('5,5', 5.5),
)

CULTURE_TO_BE_IMPLEMENTED = (
    ('corn', 'Milho'),
    ('soy', 'Soja')
)

PREDECESSOR_CULTURE = (
    ('grass', 'Gramínea'),
    ('legume', 'Leguminosa')
)

FIRST_OR_SECOND_PLANTING = (
    (1, 'Primeiro'),
    (2, 'Segundo')
)

PLANTING_TYPE = (
    ('harvest_20_21', 'Safra 20/21'),
    ('off-season_20_21', 'Safrinha 20/21'),
    ('harvest_21_22', 'Safra 21/22'),
    ('off-season_21_22', 'Safrinha 21/22'),
    ('harvest_22_23', 'Safra 22/23'),
    ('off-season_22_23', 'Safrinha 22/23'),
    ('harvest_24_25', 'Safra 24/25'),
    ('off-season_24_25', 'Safrinha 24/25'),
)
