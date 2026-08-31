import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
df['log_tfp_wins'] = df['log_tfp'].clip(lower=df['log_tfp'].quantile(0.01), upper=df['log_tfp'].quantile(0.99))
print("数据读取成功！行数：", len(df))

df = df.set_index(['firm_id', 'year'])
x_vars = ['digital', 'capital_intensity', 'export_share', 'soe']

# 基准模型（原始数据）
model1 = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result1 = model1.fit(cov_type='clustered', cluster_entity=True)

# 极端值处理模型（winsorize）
model2 = PanelOLS(
    dependent=df['log_tfp_wins'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result2 = model2.fit(cov_type='clustered', cluster_entity=True)

print("\n" + "="*60)
print("R6 极端值处理检验")
print("="*60)
print(f"基准（原始数据）：digital 系数 = {result1.params['digital']:.4f}, p值 = {result1.pvalues['digital']:.4f}")
print(f"极端值处理后（winsorize）：digital 系数 = {result2.params['digital']:.4f}, p值 = {result2.pvalues['digital']:.4f}")