import streamlit as st
import pandas as pd
import numpy as np
from investment_calculator import InvestmentCalculator
from visualization import InvestmentVisualizer
import plotly.graph_objects as go

# 設定頁面配置
st.set_page_config(
    page_title="投資模擬器",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 主標題
st.title("💰 長期投資成效模擬器")
st.markdown("---")

# 側邊欄 - 投資參數輸入
st.sidebar.header("📊 投資參數設定")

# 基本投資參數
st.sidebar.subheader("💵 投資金額設定")
initial_investment = st.sidebar.number_input(
    "初始投資額 (USD)", 
    min_value=0.0, 
    value=10000.0, 
    step=1000.0,
    help="一次性投入的初始金額"
)

monthly_investment = st.sidebar.number_input(
    "每月投資額 (USD)", 
    min_value=0.0, 
    value=1000.0, 
    step=100.0,
    help="每月定期投入的金額"
)

annual_contribution_growth = st.sidebar.number_input(
    "每年投資額增長率 (%)", 
    min_value=0.0, 
    max_value=20.0, 
    value=3.0, 
    step=0.5,
    help="每年投資額的增長百分比"
)

# 報酬率與通脹設定
st.sidebar.subheader("📈 報酬率與通脹設定")
annual_return = st.sidebar.number_input(
    "預期年報酬率 (%)", 
    min_value=0.0, 
    max_value=30.0, 
    value=7.0, 
    step=0.5,
    help="預期的年化投資報酬率"
)

inflation_rate = st.sidebar.number_input(
    "通脹率 (%)", 
    min_value=0.0, 
    max_value=10.0, 
    value=2.5, 
    step=0.1,
    help="年通脹率，用於計算實質購買力"
)

# 投資期間
st.sidebar.subheader("⏰ 投資期間")
investment_years = st.sidebar.slider(
    "投資年期", 
    min_value=1, 
    max_value=50, 
    value=30,
    help="投資的總年數"
)

# 進階選項
st.sidebar.subheader("⚙️ 進階選項")
enable_4_percent_rule = st.sidebar.checkbox(
    "啟用 4% 退休提領規則", 
    value=True,
    help="根據 4% 規則計算退休後的年度提領金額"
)

compare_no_investment = st.sidebar.checkbox(
    "比較不投資情境", 
    value=True,
    help="顯示僅存款不投資的情境比較"
)

show_real_value = st.sidebar.checkbox(
    "顯示通脹調整後的實質價值", 
    value=True,
    help="在圖表中顯示考慮通脹後的實質購買力"
)

# 計算按鈕
calculate_button = st.sidebar.button("🔄 重新計算", type="primary")

# 計算投資模擬
if calculate_button or 'calculator' not in st.session_state:
    calculator = InvestmentCalculator(
        initial_investment=initial_investment,
        monthly_investment=monthly_investment,
        annual_contribution_growth=annual_contribution_growth,
        annual_return=annual_return,
        inflation_rate=inflation_rate,
        investment_years=investment_years
    )
    
    st.session_state.calculator = calculator
    st.session_state.investment_data = calculator.calculate_investment_growth()
    st.session_state.no_investment_data = calculator.calculate_no_investment_scenario()
    st.session_state.summary_stats = calculator.get_summary_statistics()

# 如果有計算結果，顯示內容
if 'calculator' in st.session_state:
    calculator = st.session_state.calculator
    investment_data = st.session_state.investment_data
    no_investment_data = st.session_state.no_investment_data
    summary_stats = st.session_state.summary_stats
    
    # 主要內容區域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 投資成長軌跡")
        
        # 投資成長比較圖表
        growth_chart = InvestmentVisualizer.create_growth_comparison_chart(
            investment_data, 
            no_investment_data if compare_no_investment else {'year': [], 'total_savings': [], 'real_value': []},
            show_real_value
        )
        st.plotly_chart(growth_chart, use_container_width=True)
        
        # 最終結果比較圖表
        st.header("📈 最終投資結果比較")
        comparison_chart = InvestmentVisualizer.create_final_comparison_bar_chart(
            summary_stats, 
            show_real_value
        )
        st.plotly_chart(comparison_chart, use_container_width=True)
    
    with col2:
        st.header("💡 投資摘要")
        
        # 關鍵數據摘要
        st.metric(
            "累積投入資金", 
            f"${summary_stats['total_contributions']:,.0f}",
            help="總投入本金"
        )
        
        st.metric(
            "最終投資價值（名目）", 
            f"${summary_stats['final_nominal_value']:,.0f}",
            delta=f"${summary_stats['investment_gain']:,.0f}",
            help="未考慮通脹的最終投資價值"
        )
        
        if show_real_value:
            st.metric(
                "最終投資價值（實質）", 
                f"${summary_stats['final_real_value']:,.0f}",
                delta=f"${summary_stats['real_gain']:,.0f}",
                help="考慮通脹後的實質購買力"
            )
        
        # 投資組成分析
        st.subheader("🥧 投資組成分析")
        pie_chart = InvestmentVisualizer.create_investment_breakdown_pie_chart(summary_stats)
        st.plotly_chart(pie_chart, use_container_width=True)
        
        # 不投資情境比較
        if compare_no_investment:
            st.subheader("🔍 不投資情境比較")
            investment_advantage = summary_stats['final_nominal_value'] - summary_stats['no_investment_final']
            st.metric(
                "投資優勢",
                f"${investment_advantage:,.0f}",
                help="投資相對於不投資的額外收益"
            )
            
            if show_real_value:
                real_advantage = summary_stats['final_real_value'] - summary_stats['no_investment_real']
                st.metric(
                    "實質投資優勢",
                    f"${real_advantage:,.0f}",
                    help="考慮通脹後的投資優勢"
                )
    
    # 4% 退休提領分析
    if enable_4_percent_rule:
        st.header("🏖️ 退休提領分析（4% 規則）")
        
        withdrawal_chart = InvestmentVisualizer.create_withdrawal_chart(
            summary_stats['withdrawal_data']
        )
        st.plotly_chart(withdrawal_chart, use_container_width=True)
        
        # 提領金額詳細資訊
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "年度提領（名目）",
                f"${summary_stats['withdrawal_data']['annual_withdrawal']:,.0f}",
                help="按照4%規則的年度提領金額"
            )
        
        with col2:
            st.metric(
                "月度提領（名目）",
                f"${summary_stats['withdrawal_data']['monthly_withdrawal']:,.0f}",
                help="按照4%規則的月度提領金額"
            )
        
        with col3:
            st.metric(
                "年度提領（實質）",
                f"${summary_stats['withdrawal_data']['real_annual_withdrawal']:,.0f}",
                help="以今日購買力計算的年度提領金額"
            )
        
        with col4:
            st.metric(
                "月度提領（實質）",
                f"${summary_stats['withdrawal_data']['real_monthly_withdrawal']:,.0f}",
                help="以今日購買力計算的月度提領金額"
            )
    
    # 月投資額成長軌跡
    if annual_contribution_growth > 0:
        st.header("💹 月投資額成長軌跡")
        contribution_chart = InvestmentVisualizer.create_contribution_growth_chart(investment_data)
        st.plotly_chart(contribution_chart, use_container_width=True)
    
    # 資料匯出功能
    st.header("📁 資料匯出")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 匯出為 CSV"):
            filename = calculator.export_to_csv()
            st.success(f"✅ 資料已匯出至 {filename}")
    
    with col2:
        # 建立 DataFrame 以供下載
        df = pd.DataFrame({
            'Year': investment_data['year'],
            'Total_Contributions': investment_data['total_contributions'],
            'Investment_Nominal_Value': investment_data['nominal_value'],
            'Investment_Real_Value': investment_data['real_value'],
            'Monthly_Contribution': investment_data['monthly_contribution']
        })
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ 下載 CSV 檔案",
            data=csv,
            file_name='investment_simulation.csv',
            mime='text/csv'
        )

# 頁腳資訊
st.markdown("---")
st.markdown("""
### 📝 重要說明：
- 此模擬器僅供教育和規劃參考，不構成投資建議
- 實際投資報酬率可能因市場波動而有所不同
- 通脹率和投資報酬率基於歷史數據的估算
- 4% 規則是基於歷史回測的經驗法則，實際情況可能不同
- 投資前請諮詢專業財務顧問
""")

st.markdown("---")
st.markdown("**💡 Made with Streamlit | 長期投資模擬器 v1.0**")