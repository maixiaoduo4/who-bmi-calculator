"""WHO BMI Calculator

基于WHO儿童生长标准的BMI计算器，支持0-19岁儿童青少年的BMI百分位计算。
"""

from .age_calculator import AgeCalculator
from .percentile_descriptions import (
    get_percentile_description,
    HEIGHT_PERCENTILE_DESCRIPTIONS,
    WEIGHT_PERCENTILE_DESCRIPTIONS,
    BMI_PERCENTILE_DESCRIPTIONS_UNDER_2,
    BMI_PERCENTILE_DESCRIPTIONS_OVER_2,
    BMI_PERCENTILE_DESCRIPTIONS_GENERAL
)
from .bmi_data_final import BMI_STANDARD_DATA
from .who_standard_service import WHOStandardService, who_standard_service

__version__ = "1.0.0"
__author__ = "WHO BMI Calculator Team"

__all__ = [
    "AgeCalculator",
    "get_percentile_description",
    "HEIGHT_PERCENTILE_DESCRIPTIONS",
    "WEIGHT_PERCENTILE_DESCRIPTIONS",
    "BMI_PERCENTILE_DESCRIPTIONS_UNDER_2",
    "BMI_PERCENTILE_DESCRIPTIONS_OVER_2",
    "BMI_PERCENTILE_DESCRIPTIONS_GENERAL",
    "BMI_STANDARD_DATA",
    "WHOStandardService",
    "who_standard_service",
]
