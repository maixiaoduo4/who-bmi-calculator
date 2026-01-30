"""百分位描述常量定义"""

# 身高百分位描述
HEIGHT_PERCENTILE_DESCRIPTIONS = {
    "p01": "偏低身高 (<1%)",
    "p1": "偏低身高 (<1%)",
    "p3": "偏低身高 (1-3%)",
    "p5": "偏低身高 (3-5%)",
    "p10": "偏低身高 (5-10%)",
    "p15": "偏低身高 (10-15%)",
    "p25": "正常身高 (15-25%)",
    "p50": "中等身高 (25-50%)",
    "p75": "正常偏高 (50-75%)",
    "p85": "偏高身高 (75-85%)",
    "p90": "偏高身高 (85-90%)",
    "p95": "高身高 (90-95%)",
    "p97": "高身高 (95-97%)",
    "p99": "极高身高 (≥97%)",
    "p999": "极高身高 (>99%)",
    "unknown": "未知"
}

# 体重百分位描述
WEIGHT_PERCENTILE_DESCRIPTIONS = {
    "p01": "极低体重 (<1%)",
    "p1": "极低体重 (<1%)",
    "p3": "低体重 (1-3%)",
    "p5": "低体重 (3-5%)",
    "p10": "偏低体重 (5-10%)",
    "p15": "偏低体重 (10-15%)",
    "p25": "正常偏低 (15-25%)",
    "p50": "中等体重 (25-50%)",
    "p75": "正常偏高 (50-75%)",
    "p85": "偏高体重 (75-85%)",
    "p90": "偏高体重 (85-90%)",
    "p95": "高体重 (90-95%)",
    "p97": "高体重 (95-97%)",
    "p99": "极高体重 (≥97%)",
    "p999": "极高体重 (>99%)",
    "unknown": "未知"
}

# BMI百分位描述 - 2岁以下（<24个月）
BMI_PERCENTILE_DESCRIPTIONS_UNDER_2 = {
    "p01": "偏瘦 (<15%)",
    "p1": "偏瘦 (<15%)",
    "p3": "偏瘦 (<15%)",
    "p5": "偏瘦 (<15%)",
    "p10": "偏瘦 (<15%)",
    "p15": "偏瘦 (<15%)",
    "p25": "正常 (15-97.7%)",
    "p50": "正常 (15-97.7%)",
    "p75": "正常 (15-97.7%)",
    "p85": "正常 (15-97.7%)",
    "p90": "正常 (15-97.7%)",
    "p95": "正常 (15-97.7%)",
    "p97": "正常 (15-97.7%)",
    "p977": "肥胖 (>97.7%)",
    "p99": "肥胖 (>97.7)",
    "p999": "肥胖 (>97.7%)",
    "unknown": "未知"
}

# BMI百分位描述 - 2岁以上（≥24个月）
BMI_PERCENTILE_DESCRIPTIONS_OVER_2 = {
    "p01": "偏瘦 (<15%)",
    "p1": "偏瘦 (<15%)",
    "p3": "偏瘦 (<15%)",
    "p5": "偏瘦 (<15%)",
    "p10": "偏瘦 (<15%)",
    "p15": "偏瘦 (<15%)",
    "p25": "正常 (15-85%)",
    "p50": "正常 (15-85%)",
    "p75": "正常 (15-85%)",
    "p85": "正常 (15-85%)",
    "p90": "超重 (85-98%)",
    "p95": "超重 (85-95%)",
    "p97": "肥胖 (95-99%)",
    "p99": "重度肥胖 (>99%)",
    "p999": "重度肥胖 (>99%)",
    "unknown": "未知"
}

# BMI百分位描述 - 通用（兼容旧逻辑）
BMI_PERCENTILE_DESCRIPTIONS_GENERAL = {
    "p01": "极低BMI (<1%)",
    "p1": "极低BMI (<1%)",
    "p3": "低BMI (1-3%)",
    "p5": "低BMI (3-5%)",
    "p10": "偏低BMI (5-10%)",
    "p15": "偏低BMI (10-15%)",
    "p25": "正常偏低 (15-25%)",
    "p50": "中等BMI (25-50%)",
    "p75": "正常偏高 (50-75%)",
    "p85": "偏高BMI (75-85%)",
    "p90": "偏高BMI (85-90%)",
    "p95": "高BMI (90-95%)",
    "p97": "高BMI (95-97%)",
    "p977": "极高BMI (97.7-99%)",
    "p99": "极高BMI (97-99%)",
    "p999": "极高BMI (>99%)",
    "unknown": "未知"
}


def get_percentile_description(percentile: str, metric_type: str, age_months: int = None) -> str:
    """获取百分位描述
    
    Args:
        percentile: 百分位值，如 "p50", "P50", "p999" 等（大小写不敏感）
        metric_type: 指标类型，"height", "weight", "bmi"
        age_months: 年龄（月），用于区分2岁以下和2岁以上的BMI标准
        
    Returns:
        str: 百分位描述
    """
    # 参数验证
    if not isinstance(percentile, str):
        return f"无效的百分位类型: {type(percentile)}"
    
    # 统一转为小写，以兼容大小写输入
    percentile_lower = percentile.lower()
    
    if metric_type == "height":
        return HEIGHT_PERCENTILE_DESCRIPTIONS.get(percentile_lower, "未知百分位")
    elif metric_type == "weight":
        return WEIGHT_PERCENTILE_DESCRIPTIONS.get(percentile_lower, "未知百分位")
    elif metric_type == "bmi" and age_months is not None:
        # 2岁以下（<24个月）的BMI标准
        if age_months < 24:
            return BMI_PERCENTILE_DESCRIPTIONS_UNDER_2.get(percentile_lower, "未知百分位")
        # 2岁以上（≥24个月）的BMI标准
        else:
            return BMI_PERCENTILE_DESCRIPTIONS_OVER_2.get(percentile_lower, "未知百分位")
    elif metric_type == "bmi":
        # 兼容旧调用方式
        return BMI_PERCENTILE_DESCRIPTIONS_GENERAL.get(percentile_lower, "未知百分位")
    else:
        return "未知指标类型"
