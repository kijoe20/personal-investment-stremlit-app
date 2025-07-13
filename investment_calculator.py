import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class InvestmentCalculator:
    """
    投資計算器類別，用於計算長期投資的複利成長與通脹調整
    """
    
    def __init__(self, initial_investment: float, monthly_investment: float, 
                 annual_contribution_growth: float, annual_return: float,
                 inflation_rate: float, investment_years: int):
        """
        初始化投資計算器
        
        Args:
            initial_investment: 初始投資額
            monthly_investment: 每月投資額
            annual_contribution_growth: 每年投資額增長率 (%)
            annual_return: 預期年報酬率 (%)
            inflation_rate: 通脹率 (%)
            investment_years: 投資年期
        """
        self.initial_investment = initial_investment
        self.monthly_investment = monthly_investment
        self.annual_contribution_growth = annual_contribution_growth / 100
        self.annual_return = annual_return / 100
        self.inflation_rate = inflation_rate / 100
        self.investment_years = investment_years
        
        # 計算月報酬率
        self.monthly_return = (1 + self.annual_return) ** (1/12) - 1
        self.monthly_inflation = (1 + self.inflation_rate) ** (1/12) - 1
    
    def calculate_investment_growth(self) -> Dict:
        """
        計算投資成長軌跡
        
        Returns:
            包含年度數據的字典
        """
        results = {
            'year': [],
            'total_contributions': [],
            'nominal_value': [],
            'real_value': [],
            'monthly_contribution': []
        }
        
        total_contributions = self.initial_investment
        nominal_value = self.initial_investment
        current_monthly = self.monthly_investment
        
        for year in range(1, self.investment_years + 1):
            # 計算該年度的投資成長
            for month in range(12):
                # 應用月報酬率
                nominal_value = nominal_value * (1 + self.monthly_return) + current_monthly
                total_contributions += current_monthly
            
            # 年度調整月投資額
            current_monthly = current_monthly * (1 + self.annual_contribution_growth)
            
            # 計算實質價值（考慮通脹）
            real_value = nominal_value / ((1 + self.inflation_rate) ** year)
            
            # 記錄結果
            results['year'].append(year)
            results['total_contributions'].append(total_contributions)
            results['nominal_value'].append(nominal_value)
            results['real_value'].append(real_value)
            results['monthly_contribution'].append(current_monthly)
        
        return results
    
    def calculate_no_investment_scenario(self) -> Dict:
        """
        計算不投資情境（僅存款）
        
        Returns:
            包含年度數據的字典
        """
        results = {
            'year': [],
            'total_savings': [],
            'real_value': []
        }
        
        total_savings = self.initial_investment
        current_monthly = self.monthly_investment
        
        for year in range(1, self.investment_years + 1):
            # 該年度總存款
            total_savings += current_monthly * 12
            
            # 年度調整月存款額
            current_monthly = current_monthly * (1 + self.annual_contribution_growth)
            
            # 計算實質價值（考慮通脹）
            real_value = total_savings / ((1 + self.inflation_rate) ** year)
            
            results['year'].append(year)
            results['total_savings'].append(total_savings)
            results['real_value'].append(real_value)
        
        return results
    
    def calculate_retirement_withdrawal(self, final_value: float) -> Dict:
        """
        計算 4% 規則下的退休提領
        
        Args:
            final_value: 最終投資價值
            
        Returns:
            退休提領相關數據
        """
        annual_withdrawal = final_value * 0.04
        monthly_withdrawal = annual_withdrawal / 12
        
        # 計算實質提領金額
        real_annual_withdrawal = annual_withdrawal / ((1 + self.inflation_rate) ** self.investment_years)
        real_monthly_withdrawal = real_annual_withdrawal / 12
        
        return {
            'annual_withdrawal': annual_withdrawal,
            'monthly_withdrawal': monthly_withdrawal,
            'real_annual_withdrawal': real_annual_withdrawal,
            'real_monthly_withdrawal': real_monthly_withdrawal
        }
    
    def get_summary_statistics(self) -> Dict:
        """
        取得投資摘要統計
        
        Returns:
            摘要統計字典
        """
        investment_data = self.calculate_investment_growth()
        no_investment_data = self.calculate_no_investment_scenario()
        
        final_nominal = investment_data['nominal_value'][-1]
        final_real = investment_data['real_value'][-1]
        total_contributions = investment_data['total_contributions'][-1]
        
        withdrawal_data = self.calculate_retirement_withdrawal(final_nominal)
        
        return {
            'total_contributions': total_contributions,
            'final_nominal_value': final_nominal,
            'final_real_value': final_real,
            'investment_gain': final_nominal - total_contributions,
            'real_gain': final_real - (total_contributions / ((1 + self.inflation_rate) ** self.investment_years)),
            'withdrawal_data': withdrawal_data,
            'no_investment_final': no_investment_data['total_savings'][-1],
            'no_investment_real': no_investment_data['real_value'][-1]
        }
    
    def export_to_csv(self, filename: str = "investment_simulation.csv"):
        """
        匯出計算結果到 CSV 檔案
        
        Args:
            filename: 檔案名稱
        """
        investment_data = self.calculate_investment_growth()
        no_investment_data = self.calculate_no_investment_scenario()
        
        df = pd.DataFrame({
            'Year': investment_data['year'],
            'Total_Contributions': investment_data['total_contributions'],
            'Investment_Nominal_Value': investment_data['nominal_value'],
            'Investment_Real_Value': investment_data['real_value'],
            'No_Investment_Total': no_investment_data['total_savings'],
            'No_Investment_Real': no_investment_data['real_value'],
            'Monthly_Contribution': investment_data['monthly_contribution']
        })
        
        df.to_csv(filename, index=False)
        return filename