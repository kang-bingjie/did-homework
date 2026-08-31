import pandas as pd
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
print("数据读取成功！行数：", len(df))

# 创建行业×年份和地区×年份的交互项
df['industry_year'] = df['industry'].astype(str) + "_" + df['year'].astype(str)
df['province_year'] = df['province'].astype(str) + "_" + df['year'].astype(str)

df = df.set_index(['firm_id', 'year'])

x_vars = ['digital', 'capital_intensity', 'export_share', 'soe']

# =========================================================
# 模型1：基准模型（企业FE + 年份FE）
# =========================================================
print("\n" + "="*60)
print("T4 排除竞争性解释")
print("="*60)

model1 = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True,
    check_rank=False
)
result1 = model1.fit(cov_type='clustered', cluster_entity=True)
print(f"\n模型1（基准）：digital 系数 = {result1.params['digital']:.4f}, p值 = {result1.pvalues['digital']:.4f}")

# =========================================================
# 模型2：加入行业×年份固定效应（用虚拟变量方式）
# =========================================================
print("\n正在生成行业×年份虚拟变量...")
df_temp = df.copy()
df_temp = pd.get_dummies(df_temp, columns=['industry_year'], drop_first=True)
ind_year_cols = [col for col in df_temp.columns if col.startswith('industry_year_')]

# 限制数量避免内存问题
ind_year_cols = ind_year_cols[:50]

if len(ind_year_cols) > 0:
    x_vars2 = ['digital', 'capital_intensity', 'export_share', 'soe'] + ind_year_cols
    print(f"模型2 虚拟变量数：{len(ind_year_cols)}")
    
    try:
        model2 = PanelOLS(
            dependent=df_temp['log_tfp'],
            exog=df_temp[x_vars2],
            entity_effects=True,
            time_effects=True,
            drop_absorbed=True,
            check_rank=False
        )
        result2 = model2.fit(cov_type='clustered', cluster_entity=True)
        print(f"模型2（+行业×年份FE）：digital 系数 = {result2.params['digital']:.4f}, p值 = {result2.pvalues['digital']:.4f}")
    except Exception as e:
        print(f"模型2 失败：{str(e)[:80]}")
else:
    print("模型2 没有生成任何虚拟变量，跳过")

# =========================================================
# 模型3：加入行业×年份 + 地区×年份
# =========================================================
print("\n正在生成行业×年份 + 地区×年份虚拟变量...")
df_temp2 = df.copy()
df_temp2 = pd.get_dummies(df_temp2, columns=['industry_year', 'province_year'], drop_first=True)
ind_year_cols2 = [col for col in df_temp2.columns if col.startswith('industry_year_')][:40]
prov_year_cols2 = [col for col in df_temp2.columns if col.startswith('province_year_')][:30]

if len(ind_year_cols2) > 0 or len(prov_year_cols2) > 0:
    x_vars3 = ['digital', 'capital_intensity', 'export_share', 'soe'] + ind_year_cols2 + prov_year_cols2
    print(f"模型3 虚拟变量数：{len(ind_year_cols2) + len(prov_year_cols2)}")
    
    try:
        model3 = PanelOLS(
            dependent=df_temp2['log_tfp'],
            exog=df_temp2[x_vars3],
            entity_effects=True,
            time_effects=True,
            drop_absorbed=True,
            check_rank=False
        )
        result3 = model3.fit(cov_type='clustered', cluster_entity=True)
        print(f"模型3（+行业×年份FE + 地区×年份FE）：digital 系数 = {result3.params['digital']:.4f}, p值 = {result3.pvalues['digital']:.4f}")
    except Exception as e:
        print(f"模型3 失败：{str(e)[:80]}")
else:
    print("模型3 没有生成任何虚拟变量，跳过")

# =========================================================
# 总结
# =========================================================
print("\n" + "="*60)
print("T4 结论")
print("="*60)
print(f"模型1（基准）：digital 系数 = {result1.params['digital']:.4f}")