import math, json

from rest_framework import status
from rest_framework.exceptions import APIException

from api.models import BiologicalLabReport, PhysicalLabReport
from api.services.soil_quality_enums import SoilQualityClasses, SoilTextures

class SoilQualityService():
    def generate_iqs(self, analysis):

        if (not isinstance(analysis.biological_lab_report, BiologicalLabReport)):
            exception = APIException({
                'details': "É preciso vincular um relatório laboratorial biológico à análise para gerar uma Recomendação!",
            })
            exception.status_code = status.HTTP_400_BAD_REQUEST
            raise exception
        final_iqs_object = prepare_iqs(analysis.biological_lab_report)
        return final_iqs_object.to_dict()

    def classify_soil(self, analysis):

        if (not isinstance(analysis.physical_lab_report, PhysicalLabReport)):
            exception = APIException({
                'details': "É preciso vincular um relatório laboratorial físico à análise para gerar uma Recomendação!",
            })
            exception.status_code = status.HTTP_400_BAD_REQUEST
            raise exception
        final_soil_class_object = prepare_soil_texture(analysis.physical_lab_report)
        return final_soil_class_object.__dict__


class IqsClass:
    value = 0.0
    soil_class = SoilQualityClasses.LOW


class Iqs:
    biomass_carbon = IqsClass()
    beta_glucosidase = IqsClass()
    ariphosphatase = IqsClass()
    acid_phosphatase = IqsClass()
    organic_matter = IqsClass()
    iqs = IqsClass()

    def to_dict(self):
        return_value = self.__dict__
        return_value['biomass_carbon'] = self.biomass_carbon.__dict__
        return_value['beta_glucosidase'] = self.beta_glucosidase.__dict__
        return_value['ariphosphatase'] = self.ariphosphatase.__dict__
        return_value['acid_phosphatase'] = self.acid_phosphatase.__dict__
        return_value['organic_matter'] = self.organic_matter.__dict__
        return_value['iqs'] = self.iqs.__dict__
        return return_value



class SoilClass:
    clay = 0.0
    silt = 0.0
    sand = 0.0
    general_name=""
    texture=""
    texture_class=""
    texture_id=""

    def set_texture_definitions(self, texture_enum):
        self.general_name = texture_enum["general_name"]
        self.texture = texture_enum["texture"]
        self.texture_class = texture_enum["texture_class"]
        self.texture_id = texture_enum["texture_id"]


# FUNÇÕES QUE CALCULAM OS RESULTADOS

def prepare_iqs(biological_lab_report):
    iqs = Iqs()
    iqs.biomass_carbon.value = biological_lab_report.cbm
    iqs.biomass_carbon.soil_class = classify_iqs_part(biological_lab_report.cbm, 153, 324)
    iqs.beta_glucosidase.value = biological_lab_report.beta_glucosidase
    iqs.beta_glucosidase.soil_class = classify_iqs_part(biological_lab_report.beta_glucosidase, 37, 115)
    iqs.ariphosphatase.value = biological_lab_report.ariphosphatase
    iqs.ariphosphatase.soil_class = classify_iqs_part(biological_lab_report.ariphosphatase, 31, 70)
    iqs.acid_phosphatase.value = biological_lab_report.acid_phosphatase
    iqs.acid_phosphatase.soil_class = classify_iqs_part(biological_lab_report.acid_phosphatase, 264, 494)
    iqs.organic_matter.value = biological_lab_report.organic_matter
    iqs.organic_matter.soil_class = classify_iqs_part(biological_lab_report.organic_matter, 2.5, 5)
    iqs = calculate_iqs(iqs)
    return iqs


def prepare_soil_texture(physical_lab_report):
    soil_class = SoilClass()
    soil_class.sand = physical_lab_report.sand
    soil_class.clay = physical_lab_report.clay
    soil_class.silt = physical_lab_report.silt
    soil_class = classify_soil_texture(soil_class)
    return soil_class


def classify_iqs_part(value, min, max):
    return_class = SoilQualityClasses.LOW

    if (float(value) < float(min)):
        return_class = SoilQualityClasses.LOW
    elif ((float(value) >= float(min)) & (float(value) <= float(max))):
        return_class = SoilQualityClasses.MEDIUM
    elif (float(value) > float(max)):
        return_class = SoilQualityClasses.HIGH
    return return_class

def normalize_value(values, max_value):
    return round((values - 0)/(max_value - 0), 2)


def calculate_iqs(iqs_object):
    cbm = iqs_object.biomass_carbon.value
    bg = iqs_object.beta_glucosidase.value
    arp = iqs_object.ariphosphatase.value
    acp = iqs_object.acid_phosphatase.value
    om = iqs_object.organic_matter.value
    value_iqs_brute = (cbm+bg+arp+acp+om)/(50+10+10+10+20)
    value_iqs = normalize_value(value_iqs_brute, 15)
    class_iqs = SoilQualityClasses.VERY_LOW

    if (value_iqs < 0.2):
        class_iqs = SoilQualityClasses.VERY_LOW
    elif ((value_iqs >= 0.2) & (value_iqs < 0.4)):
        class_iqs = SoilQualityClasses.LOW
    elif ((value_iqs >= 0.4) & (value_iqs < 0.6)):
        class_iqs = SoilQualityClasses.MEDIUM
    elif ((value_iqs >= 0.6) & (value_iqs < 0.8)):
        class_iqs = SoilQualityClasses.HIGH
    elif (value_iqs >= 0.8):
        class_iqs = SoilQualityClasses.VERY_HIGH
    iqs_object.iqs.value = value_iqs
    iqs_object.iqs.soil_class = class_iqs
    return iqs_object


def classify_soil_texture(sc_object):

    if (sc_object.sand+sc_object.clay+sc_object.silt != 100):
        exception = APIException({
            'details': "A soma das porcentagens entre Areia, Silte e Argila precisa ser 100%!",
        })
        exception.status_code = status.HTTP_400_BAD_REQUEST
        raise exception

    if (validate_soil_texture_percentages(sc_object, c=(0,10), si=(0,10), sa=(85,100))):
        sc_object.set_texture_definitions(SoilTextures.SAND) # AREIA
    elif (validate_soil_texture_percentages(sc_object, c=(10,15), si=(0,30), sa=(70,85))):
        sc_object.set_texture_definitions(SoilTextures.LOAMY_SAND) # AREIA FRANCA
    elif (validate_soil_texture_percentages(sc_object, c=(15,20), si=(0,50), sa=(50,70))):
        sc_object.set_texture_definitions(SoilTextures.SANDY_LOAM) # FRANCO ARENOSO
    elif (validate_soil_texture_percentages(sc_object, c=(20,35), si=(0,27), sa=(45,80))):
        sc_object.set_texture_definitions(SoilTextures.SANDY_CLAY_LOAM) # FRANCO ARGILOSO ARENOSO
    elif (validate_soil_texture_percentages(sc_object, c=(35,55), si=(0,20), sa=(45,65))):
        sc_object.set_texture_definitions(SoilTextures.SANDY_CLAY) # ARGILO ARENOSO
    elif (validate_soil_texture_percentages(sc_object, c=(5,27), si=(27,50), sa=(22,53))):
        sc_object.set_texture_definitions(SoilTextures.LOAM) # FRANCO
    elif (validate_soil_texture_percentages(sc_object, c=(27,40), si=(15,52), sa=(20,45))):
        sc_object.set_texture_definitions(SoilTextures.CLAY_LOAM) # FRANCO ARGILOSO
    elif (validate_soil_texture_percentages(sc_object, c=(40,60), si=(0,40), sa=(0,45))):
        sc_object.set_texture_definitions(SoilTextures.CLAY) # ARGILA
    elif (validate_soil_texture_percentages(sc_object, c=(60,100), si=(0,40), sa=(0,40))):
        sc_object.set_texture_definitions(SoilTextures.STRONG_CLAY) # MUITO ARGILOSO
    elif (validate_soil_texture_percentages(sc_object, c=(40,60), si=(40,60), sa=(0,20))):
        sc_object.set_texture_definitions(SoilTextures.SILTY_CLAY) # ARGILO SILTOSO
    elif (validate_soil_texture_percentages(sc_object, c=(27,40), si=(60,72), sa=(0,20))):
        sc_object.set_texture_definitions(SoilTextures.SILTY_CLAY_LOAM) # FRANCO ARGILO SILTOSO
    elif (validate_soil_texture_percentages(sc_object, c=(0,27), si=(73,100), sa=(0,50))):
        sc_object.set_texture_definitions(SoilTextures.SILTY_LOAM) # FRANCO SILTOSO
    elif (validate_soil_texture_percentages(sc_object, c=(0,10), si=(80,100), sa=(0,20))):
        sc_object.set_texture_definitions(SoilTextures.SILT) # SILTE
    return sc_object


def validate_soil_texture_percentages(stc, c, si, sa):
    clay_validate = ((stc.clay >= c[0]) & (stc.clay <= c[1]))
    silt_validate = ((stc.silt >= si[0]) & (stc.silt <= si[1]))
    sand_validate = ((stc.sand >= sa[0]) & (stc.sand <= sa[1]))

    if (clay_validate & silt_validate & sand_validate):
        return True
    return False

