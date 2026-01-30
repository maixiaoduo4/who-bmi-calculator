from datetime import datetime, date
from typing import Tuple, Optional
import re
import calendar


class AgeCalculator:
    """年龄计算工具类"""
    
    @staticmethod
    def parse_age_date(age_date: str) -> Tuple[Optional[date], str]:
        """解析age_date字段
        
        Args:
            age_date: 年龄日期字符串，格式：2025-09-00（月份）或 2025-09-23（周数）
            
        Returns:
            Tuple[Optional[date], str]: (解析后的日期, 类型：'month'或'week')
            
        Raises:
            ValueError: 格式不正确时抛出异常
        """
        if not age_date:
            raise ValueError("age_date不能为空")
        
        # 匹配基本格式：YYYY-MM-DD
        basic_pattern = r'^(\d{4})-(\d{2})-(\d{2})$'
        basic_match = re.match(basic_pattern, age_date)
        if not basic_match:
            raise ValueError(f"age_date格式不正确：{age_date}，应为'YYYY-MM-DD'格式")
        
        year = int(basic_match.group(1))
        month = int(basic_match.group(2))
        day = int(basic_match.group(3))
        
        # 如果日期为00，按月份处理
        if day == 0:
            # 月份格式使用该月的第一天
            try:
                parsed_date = date(year, month, 1)
                return parsed_date, 'month'
            except ValueError:
                raise ValueError(f"无效的年月：{year}-{month}")
        else:
            # 非00日期，按周数处理
            try:
                parsed_date = date(year, month, day)
                return parsed_date, 'week'
            except ValueError:
                raise ValueError(f"无效的日期：{year}-{month}-{day}")
        
        raise ValueError(f"age_date格式不正确：{age_date}，应为'YYYY-MM-DD'格式")
    
    @staticmethod
    def calculate_age_in_months(birth_date: date, current_date: Optional[date] = None) -> Tuple[int, int]:
        """计算年龄（年和月）
        
        Args:
            birth_date: 出生日期
            current_date: 当前日期，默认为今天
            
        Returns:
            Tuple[int, int]: (年龄的年数, 年龄的月数)
        """
        if current_date is None:
            current_date = date.today()
        
        if birth_date > current_date:
            return 0, 0
        
        years = current_date.year - birth_date.year
        months = current_date.month - birth_date.month
        
        # 如果当前日期的天数小于出生日期的天数，说明还没到满月
        if current_date.day < birth_date.day:
            months -= 1
        
        # 如果月数为负，需要从年数中借位
        if months < 0:
            years -= 1
            months += 12
        
        return years, months
    
    @staticmethod
    def calculate_age_in_days(birth_date: date, current_date: Optional[date] = None) -> Tuple[int, int]:
        """计算年龄（月和天），用于一岁以内的婴儿
        
        Args:
            birth_date: 出生日期
            current_date: 当前日期，默认为今天
            
        Returns:
            Tuple[int, int]: (月数, 天数)
        """
        if current_date is None:
            current_date = date.today()
        
        if birth_date > current_date:
            return 0, 0
        
        # 计算总月数
        total_months = (current_date.year - birth_date.year) * 12 + (current_date.month - birth_date.month)
        
        # 如果当前日期的天数小于出生日期的天数，月数减1
        if current_date.day < birth_date.day:
            total_months -= 1
        
        # 计算剩余天数
        # 找到上一个月份的同一天（或该月最后一天）
        if current_date.day >= birth_date.day:
            days = current_date.day - birth_date.day
        else:
            # 需要计算上个月有多少天
            prev_month = current_date.month - 1 if current_date.month > 1 else 12
            prev_year = current_date.year if current_date.month > 1 else current_date.year - 1
            days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
            days = days_in_prev_month - birth_date.day + current_date.day
        
        return total_months, days
    
    @staticmethod
    def calculate_age_in_weeks(birth_date: date, current_date: Optional[date] = None) -> int:
        """计算年龄（周数）
        
        Args:
            birth_date: 出生日期
            current_date: 当前日期，默认为今天
            
        Returns:
            int: 年龄的周数
        """
        if current_date is None:
            current_date = date.today()
        
        if birth_date > current_date:
            return 0
        
        delta = current_date - birth_date
        weeks = delta.days // 7
        return weeks
    
    @staticmethod
    def format_age_for_display(age_type: str, years: int = 0, months: int = 0, weeks: int = 0, days: int = 0) -> str:
        """格式化年龄用于显示
        
        Args:
            age_type: 年龄类型，'month'、'week'或'day'
            years: 年数
            months: 月数
            weeks: 周数
            days: 天数
            
        Returns:
            str: 格式化后的年龄字符串
        """
        if age_type == 'week':
            return f"{weeks}周"
        elif age_type == 'day':
            # 一岁以内：XX月XX天（始终显示完整格式）
            return f"{months}月{days}天"
        else:  # month
            if years == 0:
                return f"{months}个月"
            elif months == 0:
                return f"{years}岁"
            else:
                return f"{years}岁{months}个月"
    
    @staticmethod
    def format_age_for_storage(years: int, months: int) -> str:
        """格式化年龄用于数据库存储（总是存储为X岁X个月格式）
        
        Args:
            years: 年数
            months: 月数
            
        Returns:
            str: 格式化后的年龄字符串，始终为"X岁Y个月"格式
        """
        return f"{years}岁{months}个月"
    
    @staticmethod
    def calculate_and_format_age(age_date: str, current_date: Optional[date] = None) -> Tuple[str, str]:
        """计算并格式化年龄
        
        规则：
        - 一岁以内：显示XX月XX天
        - 一岁以上：显示XX岁XX月
        
        Args:
            age_date: 年龄日期字符串，格式：YYYY-MM-DD（精确到天）
            current_date: 当前日期，默认为今天
            
        Returns:
            Tuple[str, str]: (用于显示的年龄字符串, 用于存储的年龄字符串)
        """
        parsed_date, age_type = AgeCalculator.parse_age_date(age_date)
        
        # 计算年龄（年和月）
        years, months = AgeCalculator.calculate_age_in_months(parsed_date, current_date)
        
        # 根据年龄决定显示格式
        if years < 1:
            # 一岁以内：显示XX月XX天
            total_months, days = AgeCalculator.calculate_age_in_days(parsed_date, current_date)
            display_age = AgeCalculator.format_age_for_display('day', months=total_months, days=days)
        else:
            # 一岁以上：显示XX岁XX月
            display_age = AgeCalculator.format_age_for_display('month', years=years, months=months)
        
        # 存储格式统一为 X岁X个月
        storage_age = AgeCalculator.format_age_for_storage(years, months)
        
        return display_age, storage_age