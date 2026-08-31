import pandas as pd
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
df = df.set_index(['firm_id', 'year'])

x_vars = ['digital', 'capital_intensity', 'export_share', 'soe']

# 聚类到企业层面
model1 = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result1 = model1.fit(cov_type='clustered', cluster_entity=True)

# 聚类到行业层面
result2 = model1.fit(cov_type='clustered', clusters=df['industry'])

# 聚类到地区层面
result3 = model1.fit(cov_type='clustered', clusters=df['province'])

print("\n" + "="*60)
print("R5 改变聚类层级检验")
print("="*60)
print(f"企业层面聚类：digital 系数 = {result1.params['digital']:.4f}, 标准误 = {result1.std_errors['digital']:.4f}")
print(f"行业层面聚类：digital 系数 = {result2.params['digital']:.4f}, 标准误 = {result2.std_errors['digital']:.4f}")
print(f"地区层面聚类：digital 系数 = {result3.params['digital']:.4f}, 标准误 = {result3.std_errors['digital']:.4f}")