"""WHO标准计算服务

提供BMI的百分位计算功能，基于WHO儿童生长标准
"""
from typing import Dict, Any, Optional

from .bmi_data_final import BMI_STANDARD_DATA
from .percentile_descriptions import get_percentile_description


class WHOStandardService:
    """WHO标准计算服务类"""
    
    @staticmethod
    def find_percentile_for_weight(gender_data: dict, age: int, weight: float) -> str:
        """根据体重查找对应的百分位值（使用区间判断）
        
        Args:
            gender_data: 对应性别的体重标准数据
            age: 年龄（周或月）
            weight: 体重（kg）
        
        Returns:
            str: 对应的百分位值（如"p50"）
        """
        # 同时检查整数和字符串形式的年龄键
        age_key = age
        age_str_key = str(age)
        
        if age_key not in gender_data and age_str_key not in gender_data:
            return "unknown"
        
        # 使用存在的键获取数据
        age_data = gender_data.get(age_key, gender_data.get(age_str_key))
        
        # 按百分位值排序
        sorted_percentiles = sorted(age_data.items(), key=lambda x: x[1])
        
        # 使用区间判断（左开右闭）
        # 如果体重小于最小百分位值，则返回最小百分位
        if weight <= sorted_percentiles[0][1]:
            return sorted_percentiles[0][0]
        
        # 遍历相邻的百分位对，确定区间
        for i in range(len(sorted_percentiles) - 1):
            current_percentile, current_weight = sorted_percentiles[i]
            next_percentile, next_weight = sorted_percentiles[i + 1]
            
            # 判断是否在区间(current_weight, next_weight]内
            if current_weight < weight <= next_weight:
                return next_percentile
        
        # 如果体重超过所有百分位值，则返回最大百分位
        # 特殊处理：如果最大百分位是p999，返回p99
        max_percentile = sorted_percentiles[-1][0]
        return "p99" if max_percentile == "p999" else max_percentile
    
    @staticmethod
    def find_percentile_for_height(gender_data: dict, age: int, height: float) -> str:
        """根据身高查找对应的百分位值（使用区间判断）
        
        Args:
            gender_data: 对应性别的身高标准数据
            age: 年龄（周或月）
            height: 身高（cm）
        
        Returns:
            str: 对应的百分位值（如"p50"）
        """
        # 先尝试整数类型查找
        if age in gender_data:
            age_data = gender_data[age]
        else:
            # 如果整数查找失败，尝试转为字符串类型查找
            age_str = str(age)
            if age_str in gender_data:
                age_data = gender_data[age_str]
            else:
                return "unknown"
        
        # 按百分位值排序
        sorted_percentiles = sorted(age_data.items(), key=lambda x: x[1])
        
        # 使用区间判断（左开右闭）
        # 如果身高小于最小百分位值，则返回最小百分位
        if height <= sorted_percentiles[0][1]:
            return sorted_percentiles[0][0]
        
        # 遍历相邻的百分位对，确定区间
        for i in range(len(sorted_percentiles) - 1):
            current_percentile, current_height = sorted_percentiles[i]
            next_percentile, next_height = sorted_percentiles[i + 1]
            
            # 判断是否在区间(current_height, next_height]内
            if current_height < height <= next_height:
                return next_percentile
        
        # 如果身高超过所有百分位值，则返回最大百分位
        # 特殊处理：如果最大百分位是p999，返回p99
        max_percentile = sorted_percentiles[-1][0]
        return "p99" if max_percentile == "p999" else max_percentile
    
    @staticmethod
    def find_percentile_for_bmi(gender_data: dict, age: int, bmi: float) -> str:
        """根据BMI查找对应的百分位值（使用区间判断）
        
        Args:
            gender_data: 对应性别的BMI标准数据
            age: 年龄（周或月）
            bmi: BMI数值
        
        Returns:
            str: 对应的百分位值（如"p50"）
        """
        # 先尝试整数类型查找
        if age in gender_data:
            age_data = gender_data[age]
        else:
            # 如果整数查找失败，尝试转为字符串类型查找
            age_str = str(age)
            if age_str in gender_data:
                age_data = gender_data[age_str]
            else:
                return "unknown"
        
        # 按百分位值排序
        sorted_percentiles = sorted(age_data.items(), key=lambda x: x[1])
        
        # 使用区间判断（左闭右开）
        # 逻辑：达到某个百分位的值后，就归属到该百分位，直到达到下一个百分位的值
        # 例如：P97=24.0, P99=25.5，则 24.0 <= BMI < 25.5 返回P97，BMI >= 25.5 返回P99
        
        # 如果BMI小于最小百分位值，则返回最小百分位
        if bmi < sorted_percentiles[0][1]:
            return sorted_percentiles[0][0]
        
        # 遍历相邻的百分位对，确定区间
        for i in range(len(sorted_percentiles) - 1):
            current_percentile, current_bmi = sorted_percentiles[i]
            next_percentile, next_bmi = sorted_percentiles[i + 1]
            
            # 判断是否在区间[current_bmi, next_bmi)内
            # 达到current_bmi就归属到current_percentile，直到达到next_bmi
            if current_bmi <= bmi < next_bmi:
                return current_percentile
        
        # 如果BMI大于等于最大百分位值，则返回最大百分位
        return sorted_percentiles[-1][0]
    
    @staticmethod
    def get_bmi_data_by_gender(gender: str) -> Optional[Dict]:
        """根据性别获取BMI标准数据
        
        Args:
            gender: 性别 ("boy" 或 "girl")
            
        Returns:
            BMI标准数据字典，如果不支持则返回None
        """
        if gender in BMI_STANDARD_DATA:
            return BMI_STANDARD_DATA[gender]
        return None
    
    @staticmethod
    def calculate_bmi_percentile(gender: str, age_in_months: int, bmi: float) -> Dict[str, str]:
        """计算BMI百分位
        
        Args:
            gender: 性别 ("boy" 或 "girl")
            age_in_months: 年龄（月）
            bmi: BMI值
            
        Returns:
            包含百分位和描述的字典
        """
        # 验证年龄范围
        if age_in_months < 0 or age_in_months > 228:
            return {"percentile": "unknown", "description": "年龄超出数据范围(0-228个月)"}
        
        data = WHOStandardService.get_bmi_data_by_gender(gender)
        if not data:
            return {"percentile": "unknown", "description": "不支持的性别"}
        
        percentile = WHOStandardService.find_percentile_for_bmi(data, age_in_months, bmi)
        description = get_percentile_description(percentile, "bmi", age_in_months)
        
        return {"percentile": percentile, "description": description}
    
    @staticmethod
    def calculate_adult_bmi_category(bmi: float, gender: str) -> Dict[str, str]:
        """计算成人BMI分类（中国成人标准，区分男女）
        
        Args:
            bmi: BMI值
            gender: 性别 ("boy" 或 "girl")
            
        Returns:
            包含分类和描述的字典
            
        Note:
            男性标准：偏瘦<20, 正常20-25, 超重25-30, 肥胖≥30
            女性标准：偏瘦<19, 正常19-24, 超重24-29, 肥胖≥29
        """
        if gender == "boy":
            # 男性标准
            if bmi < 20.0:
                return {"category": "underweight", "description": "偏瘦 (BMI<20)"}
            elif bmi < 25.0:
                return {"category": "normal", "description": "正常 (20≤BMI<25)"}
            elif bmi < 30.0:
                return {"category": "overweight", "description": "超重 (25≤BMI<30)"}
            else:
                return {"category": "obese", "description": "肥胖 (BMI≥30)"}
        else:
            # 女性标准
            if bmi < 19.0:
                return {"category": "underweight", "description": "偏瘦 (BMI<19)"}
            elif bmi < 24.0:
                return {"category": "normal", "description": "正常 (19≤BMI<24)"}
            elif bmi < 29.0:
                return {"category": "overweight", "description": "超重 (24≤BMI<29)"}
            else:
                return {"category": "obese", "description": "肥胖 (BMI≥29)"}
    
    @staticmethod
    def calculate_bmi(height_cm: float, weight_kg: float) -> float:
        """计算BMI值
        
        Args:
            height_cm: 身高（厘米）
            weight_kg: 体重（千克）
            
        Returns:
            BMI值，保留两位小数
        """
        if height_cm <= 0 or weight_kg <= 0:
            raise ValueError("身高和体重必须大于0")
        
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)
    
    @staticmethod
    def calculate_bmi_with_percentile(
        gender: str,
        age_in_months: int,
        height_cm: float,
        weight_kg: float
    ) -> Dict[str, Any]:
        """计算BMI及其百分位
        
        Args:
            gender: 性别 ("boy" 或 "girl")
            age_in_months: 年龄（月）
            height_cm: 身高（厘米）
            weight_kg: 体重（千克）
            
        Returns:
            包含BMI值、百分位和描述的字典
        """
        bmi = WHOStandardService.calculate_bmi(height_cm, weight_kg)
        percentile_result = WHOStandardService.calculate_bmi_percentile(gender, age_in_months, bmi)
        
        return {
            "bmi": bmi,
            "percentile": percentile_result["percentile"],
            "description": percentile_result["description"]
        }


# 创建全局实例
who_standard_service = WHOStandardService()


# 向后兼容的函数接口
def find_percentile_for_weight(gender_data: dict, age: int, weight: float) -> str:
    """根据体重查找对应的百分位值（向后兼容接口）"""
    return who_standard_service.find_percentile_for_weight(gender_data, age, weight)


def find_percentile_for_height(gender_data: dict, age: int, height: float) -> str:
    """根据身高查找对应的百分位值（向后兼容接口）"""
    return who_standard_service.find_percentile_for_height(gender_data, age, height)


def find_percentile_for_bmi(gender_data: dict, age: int, bmi: float) -> str:
    """根据BMI查找对应的百分位值（向后兼容接口）"""
    return who_standard_service.find_percentile_for_bmi(gender_data, age, bmi)
