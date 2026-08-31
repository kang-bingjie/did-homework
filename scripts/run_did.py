import pandas as pd
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

# 1. 读取数据
df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
print("数据读取成功！行数：", len(df))
print("变量名：", list(df.columns))

# 2. 设置面板索引
df = df.set_index(['firm_id', 'year'])

# 3. 定义变量（使用数据中实际存在的变量名）
x_vars = ['digital', 'capital_intensity', 'export_share', 'soe']

# 4. 运行 DID 主回归
model = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
results = model.fit(cov_type='clustered', cluster_entity=True)

# 5. 输出结果
print("\n" + "="*50)
print("DID 主回归结果")
print("="*50)
print(results)

# 6. digital 系数摘要
print("\n" + "="*50)
print("digital 系数摘要")
print("="*50)
print(f"系数: {results.params['digital']:.4f}")
print(f"标准误: {results.std_errors['digital']:.4f}")
print(f"p值: {results.pvalues['digital']:.4f}")
# 7. 保存结果到 CSV
results_df = pd.DataFrame({
    'variable': results.params.index,
    'coefficient': results.params.values,
    'std_error': results.std_errors.values,
    'p_value': results.pvalues.values
})
results_df.to_csv('output/main_did_results.csv', index=False)
print("\n结果已保存到 output/main_did_results.csv")