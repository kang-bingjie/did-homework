import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

# 读取数据
df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
print("数据读取成功！行数：", len(df))

# 真实 DID 系数
df_temp = df.set_index(['firm_id', 'year'])
model_real = PanelOLS(
    dependent=df_temp['log_tfp'],
    exog=df_temp[['digital', 'capital_intensity', 'export_share', 'soe']],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
result_real = model_real.fit(cov_type='clustered', cluster_entity=True)
real_coef = result_real.params['digital']
print(f"真实 DID 系数：{real_coef:.4f}")

# 安慰剂检验：随机打乱处理时间（保持处理组不变）
n_permutations = 100
coefs = []

# 获取每个企业最初的处理年份
df_orig = df.copy()
treated_firms = df_orig[df_orig['treated'] == 1]['firm_id'].unique()

for i in range(n_permutations):
    df_perm = df.copy()
    # 为每个处理组企业随机分配一个处理年份（2016-2024之间）
    for firm in treated_firms:
        random_year = np.random.randint(2016, 2025)
        df_perm.loc[(df_perm['firm_id'] == firm) & (df_perm['year'] >= random_year), 'fake_digital'] = 1
        df_perm.loc[(df_perm['firm_id'] == firm) & (df_perm['year'] < random_year), 'fake_digital'] = 0
    
    df_perm['fake_digital'] = df_perm['fake_digital'].fillna(0)
    df_perm = df_perm.set_index(['firm_id', 'year'])
    
    # 检查是否有变化
    if df_perm['fake_digital'].sum() == 0:
        continue
    
    try:
        model = PanelOLS(
            dependent=df_perm['log_tfp'],
            exog=df_perm[['fake_digital', 'capital_intensity', 'export_share', 'soe']],
            entity_effects=True,
            time_effects=True,
            drop_absorbed=True
        )
        result = model.fit(cov_type='clustered', cluster_entity=True)
        coefs.append(result.params['fake_digital'])
    except:
        continue

print(f"成功运行次数：{len(coefs)}")

# 结果
if len(coefs) > 0:
    coefs = np.array(coefs)
    p_value = (np.abs(coefs) > np.abs(real_coef)).mean()
    
    print("\n" + "="*60)
    print("R2 安慰剂检验结果")
    print("="*60)
    print(f"随机系数的均值：{np.mean(coefs):.4f}")
    print(f"随机系数的标准差：{np.std(coefs):.4f}")
    print(f"真实系数：{real_coef:.4f}")
    print(f"p值：{p_value:.4f}")

    if p_value < 0.05:
        print("\n✅ 安慰剂检验通过")
    else:
        print("\n⚠️ 安慰剂检验未通过")
else:
    print("\n❌ 所有安慰剂检验都失败了")