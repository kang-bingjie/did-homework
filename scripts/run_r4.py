import pandas as pd
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
df = df.set_index(['firm_id', 'year'])

# 模型1：无控制变量
model1 = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[['digital']],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result1 = model1.fit(cov_type='clustered', cluster_entity=True)

# 模型2：全部控制变量
x_vars = ['digital', 'capital_intensity', 'export_share', 'soe']
model2 = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result2 = model2.fit(cov_type='clustered', cluster_entity=True)

# 模型3：加入 firm_size
x_vars2 = ['digital', 'capital_intensity', 'export_share', 'soe', 'firm_size']
model3 = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars2],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result3 = model3.fit(cov_type='clustered', cluster_entity=True)

print("\n" + "="*60)
print("R4 改变控制变量集合检验")
print("="*60)
print(f"模型1（无控制变量）：digital 系数 = {result1.params['digital']:.4f}, p值 = {result1.pvalues['digital']:.4f}")
print(f"模型2（全部控制变量）：digital 系数 = {result2.params['digital']:.4f}, p值 = {result2.pvalues['digital']:.4f}")
print(f"模型3（加 firm_size）：digital 系数 = {result3.params['digital']:.4f}, p值 = {result3.pvalues['digital']:.4f}")