# WHO BMI Calculator

基于 WHO（世界卫生组织）儿童生长标准的 BMI 计算器，支持 0-19 岁儿童青少年的 BMI 百分位计算。

## 功能特性

- **BMI 计算**：根据身高和体重计算 BMI 值
- **百分位评估**：基于 WHO 标准数据，计算儿童 BMI 所处的百分位
- **年龄计算**：支持多种日期格式的年龄计算
- **分类描述**：提供中文的 BMI 分类描述（偏瘦、正常、超重、肥胖等）
- **成人 BMI 分类**：支持成人 BMI 分类（区分男女标准）

## 数据来源

本项目使用的 BMI 标准数据来源于 WHO 儿童生长标准：
- 覆盖年龄范围：0-228 个月（0-19 岁）
- 支持性别：男孩（boy）和女孩（girl）
- 百分位范围：P0.1, P1, P3, P5, P10, P15, P25, P50, P75, P85, P90, P95, P97, P99, P99.9

## 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/who-bmi-calculator.git
cd who-bmi-calculator

# 安装（可选，本项目仅使用 Python 标准库）
pip install -e .
```

## 快速开始

### 计算 BMI 值

```python
from who_standard_service import WHOStandardService

# 计算 BMI
bmi = WHOStandardService.calculate_bmi(height_cm=120, weight_kg=25)
print(f"BMI: {bmi}")  # 输出: BMI: 17.36
```

### 计算 BMI 百分位

```python
from who_standard_service import WHOStandardService

# 计算 5 岁男孩的 BMI 百分位
result = WHOStandardService.calculate_bmi_percentile(
    gender="boy",
    age_in_months=60,  # 5 岁 = 60 个月
    bmi=17.36
)
print(result)
# 输出: {'percentile': 'p75', 'description': '正常 (15-85%)'}
```

### 一步计算 BMI 及百分位

```python
from who_standard_service import WHOStandardService

# 计算 8 岁女孩的 BMI 及百分位
result = WHOStandardService.calculate_bmi_with_percentile(
    gender="girl",
    age_in_months=96,  # 8 岁 = 96 个月
    height_cm=130,
    weight_kg=28
)
print(result)
# 输出: {'bmi': 16.57, 'percentile': 'p50', 'description': '正常 (15-85%)'}
```

### 年龄计算

```python
from age_calculator import AgeCalculator
from datetime import date

# 计算年龄（年和月）
years, months = AgeCalculator.calculate_age_in_months(
    birth_date=date(2020, 6, 15),
    current_date=date(2025, 1, 30)
)
print(f"年龄: {years}岁{months}个月")  # 输出: 年龄: 4岁7个月

# 计算年龄（周数）
weeks = AgeCalculator.calculate_age_in_weeks(
    birth_date=date(2024, 10, 1),
    current_date=date(2025, 1, 30)
)
print(f"年龄: {weeks}周")  # 输出: 年龄: 17周
```

### 成人 BMI 分类

```python
from who_standard_service import WHOStandardService

# 成人 BMI 分类（男性）
result = WHOStandardService.calculate_adult_bmi_category(bmi=23.5, gender="boy")
print(result)  # 输出: {'category': 'normal', 'description': '正常 (20≤BMI<25)'}

# 成人 BMI 分类（女性）
result = WHOStandardService.calculate_adult_bmi_category(bmi=23.5, gender="girl")
print(result)  # 输出: {'category': 'normal', 'description': '正常 (19≤BMI<24)'}
```

## 项目结构

```
who-bmi-calculator/
├── __init__.py              # 包初始化文件
├── age_calculator.py        # 年龄计算工具类
├── bmi_data_final.py        # WHO BMI 标准数据
├── percentile_descriptions.py  # 百分位描述常量
├── who_standard_service.py  # WHO 标准计算服务
├── requirements.txt         # 依赖文件
├── setup.py                 # 安装脚本
├── LICENSE                  # MIT 许可证
└── README.md                # 项目说明文档
```

## API 参考

### WHOStandardService

| 方法 | 描述 |
|------|------|
| `calculate_bmi(height_cm, weight_kg)` | 计算 BMI 值 |
| `calculate_bmi_percentile(gender, age_in_months, bmi)` | 计算 BMI 百分位 |
| `calculate_bmi_with_percentile(gender, age_in_months, height_cm, weight_kg)` | 计算 BMI 及百分位 |
| `calculate_adult_bmi_category(bmi, gender)` | 成人 BMI 分类 |
| `get_bmi_data_by_gender(gender)` | 获取指定性别的 BMI 标准数据 |

### AgeCalculator

| 方法 | 描述 |
|------|------|
| `calculate_age_in_months(birth_date, current_date)` | 计算年龄（年和月） |
| `calculate_age_in_days(birth_date, current_date)` | 计算年龄（月和天） |
| `calculate_age_in_weeks(birth_date, current_date)` | 计算年龄（周数） |
| `calculate_and_format_age(age_date, current_date)` | 计算并格式化年龄 |

## BMI 分类标准

### 儿童青少年（0-19 岁）

根据 WHO 标准，使用百分位进行评估：

**2 岁以下（<24 个月）：**
| 百分位 | 分类 |
|--------|------|
| <15% | 偏瘦 |
| 15-97.7% | 正常 |
| >97.7% | 肥胖 |

**2 岁以上（≥24 个月）：**
| 百分位 | 分类 |
|--------|------|
| <15% | 偏瘦 |
| 15-85% | 正常 |
| 85-95% | 超重 |
| 95-99% | 肥胖 |
| >99% | 重度肥胖 |

### 成人

**男性：**
| BMI 范围 | 分类 |
|----------|------|
| <20 | 偏瘦 |
| 20-25 | 正常 |
| 25-30 | 超重 |
| ≥30 | 肥胖 |

**女性：**
| BMI 范围 | 分类 |
|----------|------|
| <19 | 偏瘦 |
| 19-24 | 正常 |
| 24-29 | 超重 |
| ≥29 | 肥胖 |

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 参考资料

- [WHO Child Growth Standards](https://www.who.int/tools/child-growth-standards)
- [WHO Growth Reference 5-19 years](https://www.who.int/tools/growth-reference-data-for-5to19-years)
