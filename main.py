import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from matplotlib.colors import LogNorm

# ==========================================
# 1. パラメータ設定 (Kawahata, 2026 - Epistemic Injustice Validation)
# ==========================================
N_list = np.logspace(1, 10, num=10)  # N = 10^1 から 10^10 まで
trials = 500                         # 各Nに対するシミュレーション試行回数
steps = 50                           # 1試行あたりの時間ステップ数

J = 1.0     # 同調圧力 (相互作用の強さ)
H = 0.05    # 外部磁場 (マジョリティへの微小なシステム的バイアス)
T = 1.2     # 社会的温度 (ノイズの大きさ。臨界温度付近に設定)
beta = 1/T

m_init = -0.2  # 初期状態: マイノリティ(-1)が60%、マジョリティ(+1)が40%の状態でスタート

# 結果保存用辞書
results_m_final = {int(N): [] for N in N_list}
trajectories = {int(N): [] for N in N_list}

# ==========================================
# 2. 大規模シミュレーション実行
# ==========================================
np.random.seed(42)

print("シミュレーションを開始します...")
for N in N_list:
    N_int = int(N)
    
    for _ in range(trials):
        m = m_init
        traj = [m]
        
        for _ in range(steps):
            # 多数派(+1)に反転する確率 (Glauberダイナミクス)
            p_plus = 1.0 / (1.0 + np.exp(-2.0 * beta * (J * m + H)))
            
            # Nが巨大な場合はメモリ/計算量回避のため正規分布近似を使用
            if N_int < 1e6:
                n_plus = np.random.binomial(N_int, p_plus)
            else:
                mu = N_int * p_plus
                sigma = np.sqrt(N_int * p_plus * (1.0 - p_plus))
                n_plus = np.random.normal(mu, sigma)
                n_plus = np.clip(n_plus, 0, N_int) # 範囲外エラー防止
                
            # 磁化(平均オピニオン)の更新: m = (N_plus - N_minus) / N
            m = (2.0 * n_plus - N_int) / N_int
            traj.append(m)
            
        results_m_final[N_int].append(m)
        if len(trajectories[N_int]) < 5: # 可視化用に5本だけ軌跡を保存
            trajectories[N_int].append(traj)

print("シミュレーション完了。統計検定を実行します。\n")

# ==========================================
# 3. 統計的有意性の検定 (多角的アプローチ)
# ==========================================
# A. 分散の崩壊検定 (Levene's Test) - N間で分散が有意に異なるか（多様性の喪失）
data_arrays = [results_m_final[int(N)] for N in N_list]
levene_stat, levene_p = stats.levene(*data_arrays)

# B. 代表値のシフト検定 (Kruskal-Wallis H-test) - N間で最終的なオピニオンの偏りが有意に異なるか
kw_stat, kw_p = stats.kruskal(*data_arrays)

# C. Signal Cliff (閾値) の特定
# 分散が初期N(10^1)の1%未満に落ち込む最初のNを閾値として定義
variances = [np.var(results_m_final[int(N)]) for N in N_list]
initial_var = variances[0]
threshold_N = None
for i, var in enumerate(variances):
    if var < initial_var * 0.01:
        threshold_N = N_list[i]
        break

print("-" * 50)
print("【統計検定結果】")
print(f"1. Levene検定 (分散の均一性): 統計量 = {levene_stat:.2f}, p値 = {levene_p:.2e}")
if levene_p < 0.05:
    print("  -> [有意] Nの拡大に伴い、オピニオンの分散（意見の揺らぎ）が統計的に有意に崩壊しています。")

print(f"\n2. Kruskal-Wallis検定 (中央値の差異): 統計量 = {kw_stat:.2f}, p値 = {kw_p:.2e}")
if kw_p < 0.05:
    print("  -> [有意] Nの拡大に伴い、マジョリティ側への偏り（偽の安定）が統計的に有意に発生しています。")

print(f"\n3. Signal Cliff (閾値) の検出:")
if threshold_N:
    print(f"  -> N = {threshold_N:.0e} にて、マイノリティのシグナル分散が初期の1%未満に崩壊（認識論的不正義の発生点）。")
print("-" * 50)

# ==========================================
# 4. 可視化 (Visualization)
# ==========================================
sns.set_theme(style="whitegrid")
fig = plt.figure(figsize=(16, 10))

# [Plot 1] Nごとのオピニオン収束の軌跡 (Phase Space)
ax1 = plt.subplot(2, 2, 1)
colors = plt.cm.viridis(np.linspace(0, 1, len(N_list)))
for i, N in enumerate([10**1, 10**4, 10**7, 10**10]):
    for traj in trajectories[int(N)]:
        ax1.plot(traj, color=colors[i*3], alpha=0.6, 
                 label=f'N=10^{int(np.log10(N))}' if traj == trajectories[int(N)][0] else "")
ax1.axhline(0, color='red', linestyle='--', alpha=0.5, label='Neutral Line')
ax1.set_title("Time Evolution of Opinion (Sample Trajectories)", fontsize=14)
ax1.set_xlabel("Time Steps")
ax1.set_ylabel("Magnetization (m) \n [-1: Minority, +1: Majority]")
ax1.legend(loc='lower right')

# [Plot 2] Nの拡大に伴う分散の崩壊 (Signal Cliff) - Log-Log Scale
ax2 = plt.subplot(2, 2, 2)
ax2.plot(N_list, variances, marker='o', linestyle='-', color='purple', linewidth=2)
if threshold_N:
    ax2.axvline(threshold_N, color='red', linestyle='-.', label=f'Signal Cliff (N={threshold_N:.0e})')
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_title("Variance Collapse: The 'Signal Cliff'", fontsize=14)
ax2.set_xlabel("Population Size (N)")
ax2.set_ylabel("Variance of Final Opinion (Log scale)")
ax2.legend()

# [Plot 3] バイオリンプロットによる確率密度の推移 (False Stabilityの証明)
ax3 = plt.subplot(2, 1, 2)
# データをSeaborn用に整形
plot_data = []
for N in N_list:
    for val in results_m_final[int(N)]:
        plot_data.append({"N": f"10^{int(np.log10(N))}", "Magnetization": val})
import pandas as pd
df = pd.DataFrame(plot_data)

sns.violinplot(x="N", y="Magnetization", data=df, ax=ax3, palette="viridis", inner="quartile")
ax3.axhline(0, color='red', linestyle='--', alpha=0.5)
ax3.set_title("Probability Density of Final States (Proof of Structural Silencing)", fontsize=14)
ax3.set_xlabel("Population Size (N)")
ax3.set_ylabel("Final Magnetization (m)")

plt.tight_layout()
plt.show()
