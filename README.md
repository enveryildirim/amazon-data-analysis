# E-Commerce Sales Analysis & Profitability Prediction

A comprehensive big data analytics project for e-commerce sales analysis and profitability prediction using PySpark, pandas, and machine learning.

## Project Overview

This project analyzes e-commerce sales data from multiple platforms (Amazon, Flipkart, Myntra, etc.) to provide insights into sales trends, category performance, platform profitability, and inventory management.

**Full Project Reports:**

- [🇬🇧 Project Report (English)](project_report.md) - Detailed analysis, methodology, and technical findings.
- [🇹🇷 Proje Raporu (Türkçe)](project_report_tr.md) - Kapsamlı analiz ve sonuç raporu.

### Key Features

- **Data Processing**: Load and transform 7 CSV datasets (178K+ rows) into optimized Parquet format
- **Sales Analysis**: Monthly trends, category performance, geographic distribution, B2B vs B2C comparison
- **Platform Profitability**: Compare margins across platforms, analyze warehouse costs
- **Inventory Analysis**: Stock levels by category, size, color; identify low/high stock SKUs
- **Feature Engineering**: Extract time, product, customer, and pricing features
- **Machine Learning**: Sales prediction and profitability modeling with Spark MLlib

## Dataset Description

The `datasets/` directory contains 7 CSV files:

| File                                 | Rows    | Description                                       |
| ------------------------------------ | ------- | ------------------------------------------------- |
| Amazon Sale Report.csv               | 128,976 | Amazon sales transactions with order details      |
| International sale Report.csv        | 37,433  | International sales data                          |
| Sale Report.csv                      | 9,272   | Inventory data with SKU, design, stock levels     |
| May-2022.csv                         | 1,330   | Platform pricing data (MRP across platforms)      |
| P L March 2021.csv                   | 1,330   | Historical pricing and profit/loss data           |
| Expense IIGF.csv                     | 17      | Operational expenses                              |
| Cloud Warehouse Compersion Chart.csv | 50      | Warehouse cost comparison (Shiprocket vs INCREFF) |

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Java 11+** (required for Spark MLlib)

**To install Java on macOS:**

```bash
brew install openjdk@11
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

**To install Java on Linux:**

```bash
sudo apt-get install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```


### Setup Virtual Environment

```bash
uv venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Install Dependencies

```bash
uv pip install -r requirements.txt
```

Or add packages individually:

```bash
uv add pyspark pandas matplotlib seaborn jupyter pyarrow
```

### Dependencies

- `pyspark>=3.4.0` - Big data processing and MLlib
- `pandas>=2.0.0` - Data manipulation
- `matplotlib>=3.7.0` - Plotting
- `seaborn>=0.12.0` - Statistical visualization
- `jupyter>=1.0.0` - Interactive notebooks
- `pyarrow>=14.0.0` - Parquet format support

## Usage

### Data Loading (Optional)

Data has already been pre-processed and saved to Parquet format in `processed/`. To reload:

```bash
source .venv/bin/activate
python data_loader_pandas.py
```

### Running Analysis Notebooks

Launch Jupyter:

```bash
source .venv/bin/activate
jupyter lab
```

Run notebooks in order:

1. **01_data_exploration.ipynb** - Schema inspection, basic statistics, data quality report
2. **02_sales_analysis.ipynb** - Sales trends, category performance, geographic analysis, B2B vs B2C
3. **05_feature_engineering.ipynb** - Extract features for ML (requires Java)
4. **06_sales_prediction_model.ipynb** - Train sales prediction models (requires Java)

## Project Structure

```
big-data/
├── datasets/                   # Raw CSV files (existing)
├── processed/                  # Processed Parquet files
│   ├── amazon_sales.parquet
│   ├── international_sales.parquet
│   ├── inventory.parquet
│   ├── pricing_may2022.parquet
│   ├── pricing_march2021.parquet
│   ├── expenses.parquet
│   └── warehouse_costs.parquet
├── notebooks/                  # Jupyter analysis notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_sales_analysis.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_sales_prediction_model.ipynb
│   └── output/                # Generated visualizations
├── scripts/                   # Batch processing scripts
│   ├── data_loader.py          # Spark-based loader (requires Java)
│   ├── data_loader_pandas.py  # Pandas-based loader (no Java needed)
│   └── train_model.py         # ML model training script (requires Java)
├── models/                    # Saved ML models (empty - to be created)
├── venv/                      # Virtual environment
├── requirements.txt            # Python dependencies
├── AGENTS.md                 # Project guidelines for agentic coding
└── README.md                 # This file
```

## Key Findings

### Sales Analysis

- **Key Trend**: Significant sales surge identified in **Q2 2022 (April, May, June)**.
- **Top Categories**: 'Set', 'Kurta', and 'Western Dress' drive the majority of revenue.
- **Correlation**: Strong correlation between Sales Volume (`Qty`) and Revenue (`Amount`), indicating stable pricing strategies.
- **Comparison**: Platform is 99%+ B2C, with a high volume of cancelled orders requiring operational focus.

### Platform Comparison

- Pricing data available for: Amazon, Ajio, Flipkart, Limeroad, Myntra, Paytm, Snapdeal
- Warehouse costs comparison: Shiprocket vs INCREFF
- Margin analysis possible across platforms

### Inventory

- 9,272 SKUs tracked
- Stock data by category, size, and color
- Design codes and style information available

## ML Pipeline

Feature engineering and model training notebooks:

1. **Feature Engineering** - Extract time, product, customer, and pricing features
2. **Sales Prediction Model** - Train and compare Linear Regression, Decision Tree, Random Forest, and GBT models
3. **Profitability Model** - Predict profit margins per transaction with multiple ML algorithms

### ML Models Implemented

- **Linear Regression** - Baseline model for sales and margin prediction
- **Decision Tree Regressor** - Non-linear relationships
- **Random Forest Regressor** - Ensemble method for better accuracy
- **Gradient Boosted Trees** - Advanced ensemble for best performance

### Model Evaluation Metrics

- **Linear Regression Performance**:
  - **RMSE**: ~253.05 (sınır within acceptable range for item prices of 500-2000)
  - **R²**: ~0.11 (Indicates significant influence of external unmeasured factors like marketing spend)

Models are saved to `models/` directory for reuse.

## Code Style Guidelines

This project follows the guidelines in `AGENTS.md`:

- PEP 8 Python conventions
- Descriptive variable names (e.g., `sales_df`, `customer_features`)
- Google-style docstrings
- Error handling with try-except blocks
- Proper resource cleanup (e.g., `spark.stop()`)

## Troubleshooting

### Java Not Found Error

```
Unable to locate a Java Runtime. Please visit http://www.java.com
```

**Solution:** Install Java 11+:

- macOS: `brew install openjdk@11`
- Linux: `sudo apt-get install openjdk-11-jdk`

### PyArrow Import Error

```
Missing optional dependency 'pyarrow'. pyarrow is required for parquet support.
```

**Solution:**

```bash
source .venv/bin/activate
pip install pyarrow
```

### Spark Session Error

If Spark fails to start without Java, use pandas-based analysis notebooks instead. They don't require Java.

## Contributing

When contributing to this project:

1. Test any changes in notebooks before committing
2. Use descriptive variable and function names
3. Add docstrings to all functions
4. Update this README with significant changes

## License

This project is for educational purposes. Dataset source: [Kaggle](https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data)

## References

- [IJMRE - Big Data + SQL + ML Methodology](https://ijmre.com/index.php/IJMRE/article/download/176/213/685)
- [Kaggle Dataset](https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data)

---

**Last Updated:** 2025-12-30
