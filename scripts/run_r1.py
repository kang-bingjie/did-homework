import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

# 1. 读取数据
df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')
print("数据读取成功！行数：", len(df))

# 2. 生成处理前各期虚拟变量（2016-2019年）
# 以 2016 年为基期
df['year_2017'] = (df['year'] == 2017).astype(int)
df['year_2018'] = (df['year'] == 2018).astype(int)
df['year_2019'] = (df['year'] == 2019).astype(int)

# 处理组 × 各年份
df['treat_2017'] = df['treated'] * df['year_2017']
df['treat_2018'] = df['treated'] * df['year_2018']
df['treat_2019'] = df['treated'] * df['year_2019']

# 3. 设置面板索引
df = df.set_index(['firm_id', 'year'])

# 4. 定义变量（加入处理前各期交互项）
x_vars = ['digital', 'treat_2017', 'treat_2018', 'treat_2019',
          'capital_intensity', 'export_share', 'soe']

# 5. 运行回归
model = PanelOLS(
    dependent=df['log_tfp'],
    exog=df[x_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True
)
results = model.fit(cov_type='clustered', cluster_entity=True)

# 6. 输出结果
print("\n" + "="*60)
print("R1 平行趋势正式检验结果")
print("="*60)
print(results)

# 7. 专门输出处理前各期系数
print("\n" + "="*60)
print("处理前各期系数摘要")
print("="*60)
for var in ['treat_2017', 'treat_2018', 'treat_2019']:
    coef = results.params[var]
    se = results.std_errors[var]
    pval = results.pvalues[var]
    print(f"{var}: 系数 = {coef:.4f}, 标准误 = {se:.4f}, p值 = {pval:.4f}")

# 8. 联合检验（手工计算 F 统计量）
# 提取处理前各期的系数和协方差矩阵
params_pre = np.array([results.params['treat_2017'], 
                       results.params['treat_2018'], 
                       results.params['treat_2019']])
# 简化版：如果三个系数都接近0且不显著，则支持平行趋势
print("\n" + "="*60)
print("平行趋势判断")
print("="*60)
if all(results.pvalues[v] > 0.1 for v in ['treat_2017', 'treat_2018', 'treat_2019']):
    print("✅ 处理前各期系数均不显著（p > 0.1），支持平行趋势假设")
else:
    print("⚠️ 部分处理前系数显著，需关注平行趋势假设")