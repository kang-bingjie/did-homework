import pandas as pd
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
print("数据读取成功！行数：", len(df))

# 构造数字化强度变量：managerial_capability * digital（标准化的管理能力）
df['digital_intensity'] = df['digital'] * (df['managerial_capability'] - df['managerial_capability'].mean()) / df['managerial_capability'].std()

df = df.set_index(['firm_id', 'year'])

# 基准模型（0/1 digital）
x_vars = ['digital', 'capital_intensity', 'export_share', 'soe']
model1 = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result1 = model1.fit(cov_type='clustered', cluster_entity=True)

# 替代模型（数字化强度）
x_vars2 = ['digital_intensity', 'capital_intensity', 'export_share', 'soe']
model2 = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars2],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result2 = model2.fit(cov_type='clustered', cluster_entity=True)

print("\n" + "="*60)
print("T1 处理变量测度检验")
print("="*60)
print(f"基准（0/1 digital）：系数 = {result1.params['digital']:.4f}, p值 = {result1.pvalues['digital']:.4f}")
print(f"替代（数字化强度）：系数 = {result2.params['digital_intensity']:.4f}, p值 = {result2.pvalues['digital_intensity']:.4f}")

if result1.params['digital'] * result2.params['digital_intensity'] > 0:
    print("\n✅ 方向一致")
else:
    print("\n⚠️ 方向不一致")