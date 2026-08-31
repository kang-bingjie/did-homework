import pandas as pd
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/raw/digital_transformation_firm_panel.csv')

# 添加常量（截距项）
df['const'] = 1

print("\n" + "="*60)
print("T2 异质性检验（分组OLS回归）")
print("="*60)

# 变量列表
x_vars = ['digital', 'capital_intensity', 'export_share', 'soe', 'const']

# =========================================================
# 1. 行业分组回归
# =========================================================
print("\n【1. 行业分组】")
for ind in df['industry'].unique():
    sub = df[df['industry'] == ind]
    print(f"\n行业 {ind}（样本量：{len(sub)}）")
    
    try:
        model = sm.OLS(sub['log_tfp'], sub[x_vars])
        result = model.fit(cov_type='HC1')  # 异方差稳健标准误
        coef = result.params['digital']
        pval = result.pvalues['digital']
        print(f"  digital 系数 = {coef:.4f}, p值 = {pval:.4f}")
    except Exception as e:
        print(f"  模型失败：{str(e)[:50]}")

# =========================================================
# 2. 所有制分组回归
# =========================================================
print("\n" + "-"*60)
print("\n【2. 所有制分组】")
for soe_val in df['soe'].unique():
    label = "SOE" if soe_val == 1 else "非SOE"
    sub = df[df['soe'] == soe_val]
    print(f"\n{label}（样本量：{len(sub)}）")
    
    try:
        model = sm.OLS(sub['log_tfp'], sub[x_vars])
        result = model.fit(cov_type='HC1')
        coef = result.params['digital']
        pval = result.pvalues['digital']
        print(f"  digital 系数 = {coef:.4f}, p值 = {pval:.4f}")
    except Exception as e:
        print(f"  模型失败：{str(e)[:50]}")

# =========================================================
# 3. 规模分组回归
# =========================================================
print("\n" + "-"*60)
print("\n【3. 规模分组】")
median_size = df['firm_size'].median()
for label, condition in [("大型", df['firm_size'] >= median_size), ("中小", df['firm_size'] < median_size)]:
    sub = df[condition]
    print(f"\n{label}企业（样本量：{len(sub)}）")
    
    try:
        model = sm.OLS(sub['log_tfp'], sub[x_vars])
        result = model.fit(cov_type='HC1')
        coef = result.params['digital']
        pval = result.pvalues['digital']
        print(f"  digital 系数 = {coef:.4f}, p值 = {pval:.4f}")
    except Exception as e:
        print(f"  模型失败：{str(e)[:50]}")