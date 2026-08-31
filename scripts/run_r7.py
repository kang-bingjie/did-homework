import pandas as pd
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
print("数据读取成功！行数：", len(df))

x_vars = ['digital', 'capital_intensity', 'export_share', 'soe']

# 基准模型（全样本）
df_full = df.set_index(['firm_id', 'year'])
model_full = PanelOLS(
    dependent=df_full['log_tfp'],
    exog=df_full[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result_full = model_full.fit(cov_type='clustered', cluster_entity=True)

# 剔除电子行业
df_no_electronics = df[df['industry'] != '电子'].set_index(['firm_id', 'year'])
model_no_electronics = PanelOLS(
    dependent=df_no_electronics['log_tfp'],
    exog=df_no_electronics[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result_no_electronics = model_no_electronics.fit(cov_type='clustered', cluster_entity=True)

# 剔除最大/最小 5%
q05 = df['log_tfp'].quantile(0.05)
q95 = df['log_tfp'].quantile(0.95)
df_trim = df[(df['log_tfp'] >= q05) & (df['log_tfp'] <= q95)].set_index(['firm_id', 'year'])
model_trim = PanelOLS(
    dependent=df_trim['log_tfp'],
    exog=df_trim[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result_trim = model_trim.fit(cov_type='clustered', cluster_entity=True)

# 缩短窗口（2018-2022）
df_short = df[(df['year'] >= 2018) & (df['year'] <= 2022)].set_index(['firm_id', 'year'])
model_short = PanelOLS(
    dependent=df_short['log_tfp'],
    exog=df_short[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result_short = model_short.fit(cov_type='clustered', cluster_entity=True)

print("\n" + "="*60)
print("R7 样本调整检验")
print("="*60)
print(f"全样本：digital 系数 = {result_full.params['digital']:.4f}")
print(f"剔除电子行业：digital 系数 = {result_no_electronics.params['digital']:.4f}")
print(f"剔除最大/最小 5%：digital 系数 = {result_trim.params['digital']:.4f}")
print(f"缩短窗口（2018-2022）：digital 系数 = {result_short.params['digital']:.4f}")