import pandas as pd
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
print("数据读取成功！行数：", len(df))

df = df.set_index(['firm_id', 'year'])

x_vars = ['digital', 'capital_intensity', 'export_share', 'soe']

# 基准模型（log_tfp）
model1 = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result1 = model1.fit(cov_type='clustered', cluster_entity=True)

# 替代模型（labor_productivity）
model2 = PanelOLS(
    dependent=df['labor_productivity'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result2 = model2.fit(cov_type='clustered', cluster_entity=True)

print("\n" + "="*60)
print("R3 替换结果变量检验")
print("="*60)
print(f"基准（log_tfp）digital 系数：{result1.params['digital']:.4f}, p值：{result1.pvalues['digital']:.4f}")
print(f"替代（labor_productivity）digital 系数：{result2.params['digital']:.4f}, p值：{result2.pvalues['digital']:.4f}")

if result1.params['digital'] * result2.params['digital'] > 0:
    print("\n✅ 方向一致")
else:
    print("\n⚠️ 方向不一致")