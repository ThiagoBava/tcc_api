import math, json

from rest_framework import status
from rest_framework.response import Response
from django.core import serializers

from api.models import SoilAnalysis, Recommendation, Plot
from api.serializer import RecommendationSerializer, ChemicalLabReportSerializer, FarmSerializer, GridSerializer, \
    PlotSerializer
from api.tables.cultures.nitrogen_6_1_14 import NITROGEN_6_1_14
from api.tables.cultures.phosphor_6_1_14 import PHOSPHOR_6_1_14
from api.tables.cultures.potassium_6_1_14 import POTASSIUM_6_1_14
from api.tables.npk_formulas import NPK_FORMULAS
from api.tables.table_5_2 import TABLE_5_2
from api.tables.table_5_3 import TABLE_5_3
from api.tables.table_6_1 import TABLE_6_1
from api.tables.table_6_4 import TABLE_6_4
from api.tables.table_6_9 import TABLE_6_9
from api.tables.table_8_4 import TABLE_8_4
from api.tables.table_9_1 import TABLE_9_1
from api.tables.table_9_5 import TABLE_9_5


class FertilizingService():

    def generate_npk(self, analysis):
        chemical_lab_report = ChemicalLabReportSerializer(analysis.chemical_lab_report).data
        plot = PlotSerializer(analysis.grid.plot).data

        limestone_type, total_lime_to_apply_tn_hac = liming(plot, chemical_lab_report)
        npk_reference, n_to_apply = npk(plot, chemical_lab_report)

        clay_class = TABLE_6_1['clay'](analysis.chemical_lab_report.clay)

        ret = {
            'chemical_lab_report': chemical_lab_report,
            'potassium_class': TABLE_6_9(analysis.chemical_lab_report.ctc_dm_3, analysis.chemical_lab_report.k_mg_l),
            'phosphor_class': TABLE_6_4[clay_class](analysis.chemical_lab_report.p_mg_l),
            'clay_class': clay_class,
            'ctc': TABLE_6_1['ctc'](analysis.chemical_lab_report.ctc_dm_3),
            'organic_matter_class': NITROGEN_6_1_14['organic_matter_classifier'](
                analysis.chemical_lab_report.organic_matter),
            'liming': {
                'limestone_type': limestone_type,
                'total_lime_to_apply_tn_hac': total_lime_to_apply_tn_hac
            },
            'npk': {
                'formule': npk_reference,
                'total_tn_hac': n_to_apply
            }
        }

        return ret

    def generate_mineral_fertilizer(self, request):
        recommendation = Recommendation.objects.get(pk=request.data['recommendationId'])

        data = serializers.serialize('json', [recommendation, ])
        struct = json.loads(data)[0]['fields']
        struct['mineral_fertilizer'] = mineral_fertilizer(recommendation.npk, request.data)
        return struct

    def generate_organic_fertilizer(self, request):
        recommendation = Recommendation.objects.get(pk=request.data['recommendationId'])
        data = serializers.serialize('json', [recommendation, ])
        struct = json.loads(data)[0]['fields']
        struct['organic_fertilizer'] = organic_fertilizer(recommendation, request.data)
        return struct


# REFERENCIA PARA O FUTURO
class Npk:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def liming(plot, analysis):
    # Sistema de manejo?
    # Existe a possibilidade de alterações de valores
    # Disponibiliza o pH necessário para tomada de decisão 6 ou 5,5
    ph_reference = TABLE_5_3[plot['area_condition']]['ph_reference']
    decision_making_ph = TABLE_5_3[plot['area_condition']]['decision_making']['ph']
    decision_making_al = TABLE_5_3[plot['area_condition']]['decision_making']['al']

    if analysis['ph_water'] > decision_making_ph:
        return 'não aplica', 0

    if analysis['ph_water'] > decision_making_ph and \
            analysis['al_mg_l'] >= decision_making_al:
        return 'não aplica', 0

    # Quantidade de calcario (PRNT 100%)
    # pH desejado?
    qty_liming_prnt_100 = TABLE_5_2[analysis['smp']][ph_reference]

    total_lime_to_apply_tn_hac = (qty_liming_prnt_100 * 100) / plot['prnt_applied']

    limestone_type = 'calcítico' if analysis['relation_ca_mg'] < 3 else 'dolomítico'

    # quantidade de calcário de acordo com a referencia da tabela
    return limestone_type, round(total_lime_to_apply_tn_hac, 2)


def nitrogen(plot, analysis):
    # Somente em milho
    if plot['current_culture'] != 'corn':
        return

    organic_matter = analysis['organic_matter']
    yield_expectation_kg = plot['yield_expectation_kg']
    plant_density_hectare = plot['plant_density_hectare']

    qty_kg_N_ha = NITROGEN_6_1_14[plot['predecessor_culture']] \
        (organic_matter, yield_expectation_kg, plant_density_hectare)

    total_base = 0
    total_coverage = 0

    if plot['management_system'] == 'conventional':
        # Sugere-se aplica entre 10 e 30 kg de N/ha
        total_base = 30
        total_coverage = qty_kg_N_ha - total_base

    elif plot['management_system'] == 'no-till':
        # Sugere-se aplica entre 20 a 40 kg de N/ha
        total_base = 40
        total_coverage = qty_kg_N_ha - total_base

    return total_base, total_coverage


def phosphor(plot, analysis):
    clay_class = TABLE_6_1['clay'](analysis['clay'])
    phosphor_class = TABLE_6_4[clay_class](analysis['p_mg_l'])
    yield_expectation_kg = plot['yield_expectation_kg']
    qty_P2_O5_ha = PHOSPHOR_6_1_14[plot['first_or_second_planting']](phosphor_class, yield_expectation_kg)
    return qty_P2_O5_ha


def potassium(plot, analysis):
    potassium_class = TABLE_6_9(analysis['ctc_dm_3'], analysis['k_mg_l'])
    yield_expectation_kg = plot['yield_expectation_kg']
    qty_K2_O_ha = POTASSIUM_6_1_14[plot['first_or_second_planting']](potassium_class, yield_expectation_kg)
    return qty_K2_O_ha


def npk(plot, analysis):
    total_base, total_coverage = nitrogen(plot, analysis)
    qty_P2_O5_ha = phosphor(plot, analysis)
    qty_K2_O_ha = potassium(plot, analysis)

    # Dividir por um número que proporcione uma relação (total_base)
    # Calcular relação entre nutrientes
    n = total_base / total_base
    p = qty_P2_O5_ha / total_base
    k = qty_K2_O_ha / total_base

    formules = {
        'exact': [],
        'alternative': [],
        'alternative_isolete': {
            'p': [],
            'k': [],
        }
    }

    # Avaliar fórmulas cadastradas
    for formule in NPK_FORMULAS:
        n_form_proportion = 1
        p_form_proportion = formule[1] / (formule[0] or 1)
        k_form_proportion = formule[2] / (formule[0] or 1)

        # Verifica se a fórmula atende a necessidade
        if math.trunc(p) == math.trunc(p_form_proportion):
            formules['alternative'].append(formule)
            formules['alternative_isolete']['p'].append(formule)

        if math.trunc(k) == math.trunc(k_form_proportion):
            formules['alternative'].append(formule)
            formules['alternative_isolete']['k'].append(formule)

        if math.trunc(k) == math.trunc(k_form_proportion) and \
                math.trunc(p) == math.trunc(p_form_proportion):
            formules['exact'].append(formule)

    npk_reference = [0]
    if formules['exact']:
        npk_reference = formules['exact'][0]

    elif formules['alternative']:
        npk_reference = formules['alternative'][0]

    n_relation = n * npk_reference[0]
    p_relation = p * npk_reference[0]
    k_relation = k * npk_reference[0]

    # Calcular a quantidade que deve ser aplicada
    # 100 da fórmula
    n_to_apply = math.trunc(total_base * 100 / n_relation)
    p_to_apply = math.trunc(qty_P2_O5_ha * 100 / p_relation)
    k_to_apply = math.trunc(qty_K2_O_ha * 100 / k_relation)

    if n_to_apply == p_to_apply == k_to_apply:
        recommended_dose = n_to_apply

    if total_coverage > 100:
        'Divide em 2 aplicações, nesse caso, preciso mecher em alguma formula anterior?'
        'Preciso gerar outra formula para aplicar em cobertura?'

    return npk_reference, n_to_apply


def mineral_fertilizer(npk, filters):
    # 'https://drive.google.com/drive/u/0/folders/1fICMBOsv3dj-4xiSSxd9lTd4dkCiiE2O - 2021-6-14 50min'
    # 'Utilizar fertilizantes matérias primas, T. 8.4 pg 304 / 317 T. 9.1 - 9.2 - 9.5'

    # 'isso deve ser entrada do usuário'
    # 'sulfato de amônio      20%'
    # 'cloreto de potássio    60%'
    # 'POSSO UTILIZAR MAIS DE 1?'

    nitrogen_minimum_guarantee = TABLE_8_4['nitrogen'][filters['nitrogen']]['minimum_guarantee']
    phosphate_minimum_guarantee = TABLE_8_4['phosphate'][filters['phosphate']]['minimum_guarantee']
    potash_minimum_guarantee = TABLE_8_4['potash'][filters['potash']]['minimum_guarantee']

    # '4-14-8'
    # npk_reference
    #
    # '4%N da fórmula'
    # 'divide por SA 20% N'
    # 'quanto de sulfato estará aplicando?'
    # '4 / 20 * 1000 = 200kg SA'
    # sulphate_source = TABLE_8_4
    # npk_reference[0] / sulphate_source * 1000

    n_to_apply = npk['npk']['formule'][0] / nitrogen_minimum_guarantee * 1000

    # 'quanto de potassio?'
    # '8 / 60 * 1000 = 134kg KCl'
    k_to_apply = npk['npk']['formule'][2] / potash_minimum_guarantee * 1000

    # 'total: 334kg de AS e KCl'
    #
    # 'trabalhar com Tonelada'
    # '1000 - 334 = 666kg'
    #
    # 'escolher fonte de Fósforo, no exemplo super simples 18%'
    # '666 * 18 = 11988 de SS'
    #
    # '14 do fósforo: 14000 - 11988 = 2012'
    # 'qual outra materia prima que tem fósforo? Super fosfato triplo 41%'
    # '2012 / (41-18(qntd. de SS)) => 2012 / 23 = 9,21 kg de SFT'
    # p_to_apply = ((npk['npk']['formule'][1] * 1000) - ((1000 - (n_to_apply+k_to_apply)) * phosphate_minimum_guarantee)) / phosphate_minimum_guarantee

    diference_to_apply = (1000 - (n_to_apply + k_to_apply))
    total_to_apply = (npk['npk']['formule'][1] * 1000) - diference_to_apply * phosphate_minimum_guarantee
    if total_to_apply > 0:
        p_to_apply = total_to_apply / phosphate_minimum_guarantee

    p_to_apply = diference_to_apply

    # p_to_apply = ((npk['npk']['formule'][1] * 1000) - (k_to_apply * phosphate_minimum_guarantee)) / phosphate_minimum_guarantee
    # '666 kg que faltam complementar a fórmula - 9,21 kg de SFT'
    # '666 - 9,21 = 656 kg de SS'

    return {
        'n': {filters['nitrogen']: round(n_to_apply, 2)},
        'p': {filters['phosphate']: round(p_to_apply, 2)},
        'k': {filters['potash']: round(k_to_apply, 2)}
    }

    # ## == qual quantidade aplicar sem analise? == ##
    #
    # 'ver se tem diferença entre as fórmulas'
    # 'sempre iniciar pelo fosforo a recomendação pq é o mais retido'
    #
    # 'revisar https://drive.google.com/drive/u/0/folders/1fICMBOsv3dj-4xiSSxd9lTd4dkCiiE2O - 2021-6-14 114min'

    # TABLE_9_1
    #
    #
    # print('success')


def organic_fertilizer(recommendation, request):
    # vzt-mwpd-faa (2021-09-15 at 17:04 GMT-7)

    def convert_index_table91_to_table95(organic_fertilizer_type):
        if organic_fertilizer_type in TABLE_9_5.keys():
            return organic_fertilizer_type
        elif organic_fertilizer_type == 'chicken_bed_3_4_lots' or \
                organic_fertilizer_type == 'chicken_bed_5_6_lots' or \
                organic_fertilizer_type == 'chicken_bed_7_8_lots' or \
                organic_fertilizer_type == 'turkey_bed_2_lots' or \
                organic_fertilizer_type == 'laying_bed':
            return 'chicken_bed'

        elif organic_fertilizer_type == 'bunk_pig_bed' or \
                organic_fertilizer_type == 'swine_manure_compound':
            return 'bunk_bed_and_pig_wishing_compound'

        elif organic_fertilizer_type == 'compost_of_urban_waste' or \
                organic_fertilizer_type == 'sewage_sludge':
            return 'sewage_sludge_and_garbage_compost'

        else:
            return 'other_organic_waste'

    organic_fertilizer_type = request['organic_fertilizer_type']

    npk_reference = recommendation.npk['npk']['formule']
    recommended_dose = recommendation.npk['npk']['total_tn_hac']

    n_dry_matter = TABLE_9_1[organic_fertilizer_type]['n_total']
    p2o5_dry_matter = TABLE_9_1[organic_fertilizer_type]['p2o5']
    k2o_dry_matter = TABLE_9_1[organic_fertilizer_type]['k2o']
    dry_matter = TABLE_9_1[organic_fertilizer_type]['dry_matter']

    n_in_npk_reference = npk_reference[0] * recommended_dose / 100
    p_in_npk_reference = npk_reference[1] * recommended_dose / 100
    k_in_npk_reference = npk_reference[2] * recommended_dose / 100

    efficiency_index_n = TABLE_9_5[convert_index_table91_to_table95(organic_fertilizer_type)]['n'][
        recommendation.soil_analysis.grid.plot.first_or_second_planting] or 1
    efficiency_index_p = TABLE_9_5[convert_index_table91_to_table95(organic_fertilizer_type)]['p'][
        recommendation.soil_analysis.grid.plot.first_or_second_planting] or 1
    efficiency_index_k = TABLE_9_5[convert_index_table91_to_table95(organic_fertilizer_type)]['k'][
                             recommendation.soil_analysis.grid.plot.first_or_second_planting] or 1

    # Adubo sólido
    # K é disponibilizado 100% sempre no primeiro cultivo
    b = dry_matter / 100
    c_k2o = k2o_dry_matter / 100
    c_p2o5 = p2o5_dry_matter / 100
    c_n = n_dry_matter / 100


    if 'liquid' in organic_fertilizer_type:
        # A=QD/(C*D)
        qd_k = k_in_npk_reference / (c_k2o * efficiency_index_k)
        qd_n = n_in_npk_reference / (c_n * efficiency_index_n)
        qd_p = p_in_npk_reference / (c_p2o5 * efficiency_index_p)
    else:
        # A=QD/((B/100)*(C/100)*D)
        # A = quantidade do material aplicado em kg/ha, ISOLA
        # B = porcentagem de matéria seca do material
        # C = porcentagem do nutriente na materia seca
        # D = indice de eficiencia de cada nutriente

        qd_k = k_in_npk_reference / (b * c_k2o) * efficiency_index_k
        qd_n = qd_k * b * c_n * efficiency_index_n # qd_k / (b * c_n) * efficiency_index_n
        qd_p = qd_k * b * c_p2o5 * efficiency_index_p # k_in_npk_reference / (b * c_p2o5) * efficiency_index_p

        n_to_increment = n_in_npk_reference//qd_n
        p_to_increment = p_in_npk_reference//qd_p
        k_to_increment = k_in_npk_reference//qd_k

        total_to_apply = qd_k

        if bool(n_to_increment):
            total_to_apply *= n_to_increment

        if bool(p_to_increment):
            total_to_apply *= p_to_increment

        if bool(k_to_increment):
            total_to_apply *= k_to_increment

    return {
        "qd_k": round(qd_k, 2),
        "qd_n": round(qd_n, 2),
        "qd_p": round(qd_p, 2),
        "total_to_apply": round(total_to_apply, 2),
    }
