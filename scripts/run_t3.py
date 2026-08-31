import pandas as pd
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
print("数据读取成功！行数：", len(df))

# 交互项
df['digital_x_mc'] = df['digital'] * df['managerial_capability']

df = df.set_index(['firm_id', 'year'])

x_vars = ['digital', 'managerial_capability', 'digital_x_mc', 'capital_intensity', 'export_share', 'soe']

model = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
results = model.fit(cov_type='clustered', cluster_entity=True)

print("\n" + "="*60)
print("T3 机制检验：能力互补性")
print("="*60)
print(results)

coef_inter = results.params['digital_x_mc']
p_inter = results.pvalues['digital_x_mc']

print(f"\n交互项系数：{coef_inter:.4f}, p值：{p_inter:.4f}")

if coef_inter > 0 and p_inter < 0.05:
    print("\n✅ 支持互补性机制：管理能力越高的企业，数字化效应越强")
else:
    print("\n⚠️ 未发现互补性证据")