import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List

class InvestmentVisualizer:
    """
    投資視覺化類別，用於創建各種投資相關圖表
    """
    
    @staticmethod
    def create_growth_comparison_chart(investment_data: Dict, no_investment_data: Dict, 
                                     show_real_value: bool = True) -> go.Figure:
        """
        創建投資成長比較圖表
        
        Args:
            investment_data: 投資數據
            no_investment_data: 不投資數據
            show_real_value: 是否顯示實質價值
            
        Returns:
            Plotly 圖表對象
        """
        fig = go.Figure()
        
        years = investment_data['year']
        
        # 添加投資名目價值線
        fig.add_trace(go.Scatter(
            x=years,
            y=investment_data['nominal_value'],
            mode='lines+markers',
            name='投資名目價值',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6)
        ))
        
        # 添加投資實質價值線（如果啟用）
        if show_real_value:
            fig.add_trace(go.Scatter(
                x=years,
                y=investment_data['real_value'],
                mode='lines+markers',
                name='投資實質價值（考慮通脹）',
                line=dict(color='#ff7f0e', width=3, dash='dash'),
                marker=dict(size=6)
            ))
        
        # 添加累積投入資金線
        fig.add_trace(go.Scatter(
            x=years,
            y=investment_data['total_contributions'],
            mode='lines+markers',
            name='累積投入資金',
            line=dict(color='#2ca02c', width=2),
            marker=dict(size=5)
        ))
        
        # 添加不投資情境線
        fig.add_trace(go.Scatter(
            x=years,
            y=no_investment_data['total_savings'],
            mode='lines+markers',
            name='不投資（純存款）',
            line=dict(color='#d62728', width=2, dash='dot'),
            marker=dict(size=5)
        ))
        
        # 添加不投資實質價值線（如果啟用）
        if show_real_value:
            fig.add_trace(go.Scatter(
                x=years,
                y=no_investment_data['real_value'],
                mode='lines+markers',
                name='不投資實質價值',
                line=dict(color='#9467bd', width=2, dash='dashdot'),
                marker=dict(size=5)
            ))
        
        # 更新佈局
        fig.update_layout(
            title='長期投資成長比較',
            xaxis_title='投資年數',
            yaxis_title='金額 (USD)',
            hovermode='x unified',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            height=600,
            showlegend=True
        )
        
        # 格式化 Y 軸
        fig.update_yaxes(tickformat='$,.0f')
        
        return fig
    
    @staticmethod
    def create_final_comparison_bar_chart(summary_stats: Dict, show_real_value: bool = True) -> go.Figure:
        """
        創建最終結果比較條形圖
        
        Args:
            summary_stats: 摘要統計數據
            show_real_value: 是否顯示實質價值
            
        Returns:
            Plotly 圖表對象
        """
        categories = ['投入總資金', '投資最終價值', '不投資最終價值']
        nominal_values = [
            summary_stats['total_contributions'],
            summary_stats['final_nominal_value'],
            summary_stats['no_investment_final']
        ]
        
        fig = go.Figure()
        
        # 添加名目價值條形圖
        fig.add_trace(go.Bar(
            x=categories,
            y=nominal_values,
            name='名目價值',
            marker_color=['#2ca02c', '#1f77b4', '#d62728'],
            text=[f'${val:,.0f}' for val in nominal_values],
            textposition='auto',
        ))
        
        # 如果啟用實質價值，添加實質價值條形圖
        if show_real_value:
            real_values = [
                summary_stats['total_contributions'],  # 投入資金不需要通脹調整
                summary_stats['final_real_value'],
                summary_stats['no_investment_real']
            ]
            
            fig.add_trace(go.Bar(
                x=categories,
                y=real_values,
                name='實質價值（考慮通脹）',
                marker_color=['#90EE90', '#FFA500', '#FFB6C1'],
                text=[f'${val:,.0f}' for val in real_values],
                textposition='auto',
                opacity=0.7
            ))
        
        # 更新佈局
        fig.update_layout(
            title='最終投資結果比較',
            xaxis_title='類別',
            yaxis_title='金額 (USD)',
            barmode='group',
            height=500,
            showlegend=True
        )
        
        # 格式化 Y 軸
        fig.update_yaxes(tickformat='$,.0f')
        
        return fig
    
    @staticmethod
    def create_withdrawal_chart(withdrawal_data: Dict) -> go.Figure:
        """
        創建退休提領圖表
        
        Args:
            withdrawal_data: 提領數據
            
        Returns:
            Plotly 圖表對象
        """
        categories = ['年度提領', '月度提領']
        nominal_values = [
            withdrawal_data['annual_withdrawal'],
            withdrawal_data['monthly_withdrawal']
        ]
        real_values = [
            withdrawal_data['real_annual_withdrawal'],
            withdrawal_data['real_monthly_withdrawal']
        ]
        
        fig = go.Figure()
        
        # 添加名目提領金額
        fig.add_trace(go.Bar(
            x=categories,
            y=nominal_values,
            name='名目提領金額',
            marker_color=['#1f77b4', '#ff7f0e'],
            text=[f'${val:,.0f}' for val in nominal_values],
            textposition='auto',
        ))
        
        # 添加實質提領金額
        fig.add_trace(go.Bar(
            x=categories,
            y=real_values,
            name='實質提領金額（今日購買力）',
            marker_color=['#87CEEB', '#FFCCCB'],
            text=[f'${val:,.0f}' for val in real_values],
            textposition='auto',
            opacity=0.7
        ))
        
        # 更新佈局
        fig.update_layout(
            title='退休提領金額（4% 規則）',
            xaxis_title='提領週期',
            yaxis_title='金額 (USD)',
            barmode='group',
            height=400,
            showlegend=True
        )
        
        # 格式化 Y 軸
        fig.update_yaxes(tickformat='$,.0f')
        
        return fig
    
    @staticmethod
    def create_contribution_growth_chart(investment_data: Dict) -> go.Figure:
        """
        創建投資額成長圖表
        
        Args:
            investment_data: 投資數據
            
        Returns:
            Plotly 圖表對象
        """
        fig = go.Figure()
        
        years = investment_data['year']
        monthly_contributions = investment_data['monthly_contribution']
        
        fig.add_trace(go.Scatter(
            x=years,
            y=monthly_contributions,
            mode='lines+markers',
            name='月投資額',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=6),
            fill='tonexty'
        ))
        
        # 更新佈局
        fig.update_layout(
            title='月投資額成長軌跡',
            xaxis_title='投資年數',
            yaxis_title='月投資額 (USD)',
            hovermode='x unified',
            height=400,
            showlegend=False
        )
        
        # 格式化 Y 軸
        fig.update_yaxes(tickformat='$,.0f')
        
        return fig
    
    @staticmethod
    def create_investment_breakdown_pie_chart(summary_stats: Dict) -> go.Figure:
        """
        創建投資組成餅圖
        
        Args:
            summary_stats: 摘要統計數據
            
        Returns:
            Plotly 圖表對象
        """
        labels = ['投入本金', '投資收益']
        values = [
            summary_stats['total_contributions'],
            summary_stats['investment_gain']
        ]
        colors = ['#ff9999', '#66b3ff']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker_colors=colors,
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}',
            hovertemplate='%{label}<br>金額: $%{value:,.0f}<br>佔比: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title='投資組成分析',
            height=400,
            showlegend=True
        )
        
        return fig