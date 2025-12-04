import pandas as pd
import numpy as np
from scipy import stats

# Load data
df = pd.read_csv('carsFixed.csv')

print("=" * 60)
print("SHOP-BY-SHOP ANALYSIS")
print("=" * 60)

results = []

for shop in sorted(df['shopID'].unique()):
    shop_data = df[df['shopID'] == shop]
    absent = shop_data[shop_data['boss'] == 0]['carsFixed']
    present = shop_data[shop_data['boss'] == 1]['carsFixed']
    
    diff = present.mean() - absent.mean()
    
    # Statistical test
    t_stat, p_value = stats.ttest_ind(present, absent)
    
    results.append({
        'shop': shop,
        'absent_mean': absent.mean(),
        'absent_n': len(absent),
        'present_mean': present.mean(),
        'present_n': len(present),
        'difference': diff,
        'p_value': p_value,
        'significant': p_value < 0.05
    })
    
    print(f"\nShop {shop}:")
    print(f"  Absent:  mean={absent.mean():.2f}, std={absent.std():.2f}, n={len(absent)}")
    print(f"  Present: mean={present.mean():.2f}, std={present.std():.2f}, n={len(present)}")
    print(f"  Difference: {diff:+.2f} cars")
    print(f"  P-value: {p_value:.4f} {'***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else ''}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

