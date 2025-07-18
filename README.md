# 💰 長期投資成效模擬器

一個使用 Streamlit 建立的互動式長期投資模擬器，幫助您視覺化投資成長、比較不同情境，並計算退休提領金額。

## 🌟 功能特色

### 📊 核心功能
- **複利計算模擬** - 根據複利公式計算長期投資成長
- **通脹調整** - 考慮通脹因素的實質購買力分析
- **4% 退休提領規則** - 模擬退休後的可提領金額
- **投資情境比較** - 比較投資 vs 不投資的成果差異
- **互動式圖表** - 使用 Plotly 提供豐富的視覺化效果

### 🔧 輸入參數
- 初始投資額
- 每月投資額
- 每年投資額增長率
- 預期年報酬率
- 通脹率
- 投資年期
- 退休提領規則開關
- 不投資情境比較開關

### 📈 視覺化圖表
1. **投資成長軌跡圖** - 顯示投資價值隨時間的變化
2. **最終結果比較圖** - 條形圖比較各種情境的最終結果
3. **退休提領分析圖** - 顯示 4% 規則下的提領金額
4. **投資組成餅圖** - 分析投入本金與投資收益的比例
5. **月投資額成長圖** - 顯示投資額隨時間的增長軌跡

## 🌐 在線使用

您可以直接在瀏覽器中使用此應用程式，無需安裝任何軟體：

**[🚀 立即使用 - 長期投資成效模擬器](https://personal-investment-stremlit-app-mkvhdjnajcd28vvkvlbabs.streamlit.app/)**

## 🚀 快速開始

### 系統需求
- Python 3.8+
- pip 套件管理器

### 安裝步驟

1. **克隆或下載專案**
   ```bash
   git clone <repository-url>
   cd investment-simulator
   ```

2. **安裝依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

3. **啟動應用程式**
   ```bash
   streamlit run app.py
   ```

4. **開啟瀏覽器**
   應用程式將在 `http://localhost:8501` 啟動

## 📋 使用指南

### 基本操作
1. **設定投資參數** - 在左側邊欄調整各項投資參數
2. **選擇顯示選項** - 選擇是否顯示通脹調整、4% 規則等
3. **查看結果** - 主畫面會即時顯示計算結果和圖表
4. **匯出資料** - 可將結果匯出為 CSV 檔案

### 參數說明
- **初始投資額**: 一次性投入的起始金額
- **每月投資額**: 定期定額投資的月度金額
- **年投資額增長率**: 每年投資額的增長百分比（通常反映薪資成長）
- **預期年報酬率**: 投資組合的預期年化報酬率
- **通脹率**: 年通脹率，用於計算實質購買力
- **投資年期**: 投資的總年數

### 進階功能
- **4% 規則**: 根據退休規劃經驗法則計算可提領金額
- **實質價值**: 考慮通脹後的真實購買力
- **情境比較**: 比較投資與不投資的長期差異

## 🧮 計算公式

### 複利計算
投資價值計算採用複利公式：
```
月報酬率 = (1 + 年報酬率)^(1/12) - 1
每月價值 = 前月價值 × (1 + 月報酬率) + 當月投資額
```

### 通脹調整
實質價值計算：
```
實質價值 = 名目價值 ÷ (1 + 通脹率)^年數
```

### 4% 退休提領規則
年度提領金額：
```
年度提領 = 最終投資價值 × 4%
```

## 📁 專案結構

```
investment-simulator/
├── app.py                    # 主要 Streamlit 應用程式
├── investment_calculator.py  # 投資計算核心邏輯
├── visualization.py          # 圖表視覺化模組
├── requirements.txt          # Python 依賴套件
└── README.md                # 專案說明文件
```

## 🔍 技術細節

### 主要套件
- **Streamlit**: 網頁應用程式框架
- **Plotly**: 互動式圖表庫
- **Pandas**: 資料處理與分析
- **NumPy**: 數值計算

### 核心類別
- **InvestmentCalculator**: 處理所有投資計算邏輯
- **InvestmentVisualizer**: 負責圖表生成與視覺化

## 📊 範例情境

### 預設範例
- 初始投資：$10,000
- 每月投資：$1,000
- 年投資額增長：3%
- 年報酬率：7%
- 通脹率：2.5%
- 投資期間：30年

### 預期結果
30年後的投資價值約為 $1,200,000（名目價值），考慮通脹後約為 $570,000（實質價值）。

## ⚠️ 重要聲明

- 此模擬器僅供教育和規劃參考，不構成投資建議
- 實際投資報酬率可能因市場波動而有所不同
- 通脹率和投資報酬率基於歷史數據的估算
- 4% 規則是基於歷史回測的經驗法則，實際情況可能不同
- 投資前請諮詢專業財務顧問

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request 來改進此專案。

## 📄 授權

本專案採用 MIT 授權條款。

## 🔗 相關資源

- [Streamlit 官方文檔](https://docs.streamlit.io/)
- [Plotly 圖表庫](https://plotly.com/python/)
- [4% 規則詳細說明](https://www.investopedia.com/terms/f/four-percent-rule.asp)
- [複利計算原理](https://www.investopedia.com/terms/c/compoundinterest.asp)

---

**💡 Made with Streamlit | 長期投資模擬器 v1.0**