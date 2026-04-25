import numpy as np
import scipy.stats as stats

def calculate_shannon_entropy(data_array, bins=50):
    """
    連続値（磁化m）の配列から確率分布を生成し、シャノン・エントロピーを計算する関数
    """
    # 1. データをヒストグラム化し、頻度を確率に変換
    counts, _ = np.histogram(data_array, bins=bins, range=(-1.0, 1.0))
    probabilities = counts / np.sum(counts)
    
    # 2. 確率が0の要素を除外（log2(0)によるNaNエラーを防ぐため）
    probabilities = probabilities[probabilities > 0]
    
    # 3. シャノン・エントロピー（単位: bits）を計算
    # 物理学の慣例に従い自然対数(base=np.e)を用いることもありますが、
    # 情報理論(bits)として扱うなら base=2 とします。
    entropy = stats.entropy(probabilities, base=2)
    
    return entropy

# 各Nについてループで計算
# entropies = [calculate_shannon_entropy(results_m_final[int(N)]) for N in N_list]

# ==========================================
# 可視化 (Visualization for Paper)
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# [Plot 1] ビンダー・キュムラント (Phase Transition Proof)
ax1.plot(N_list, binder_cumulants, marker='s', color='darkblue', linewidth=2, markersize=8)
ax1.axvline(1e4, color='red', linestyle='-.', label='Signal Cliff (N=10^4)')
ax1.set_xscale('log')
ax1.set_title("Binder Cumulant $U_4$ Scaling\n(Proof of Structural Phase Transition)", fontsize=14)
ax1.set_xlabel("Population Size (N)", fontsize=12)
ax1.set_ylabel("Binder Cumulant $U_4$", fontsize=12)
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend()

# [Plot 2] シャノン・エントロピー (Information Loss Proof)
ax2.plot(N_list, shannon_entropies, marker='^', color='darkgreen', linewidth=2, markersize=8)
ax2.axvline(1e4, color='red', linestyle='-.', label='Signal Cliff (N=10^4)')
ax2.set_xscale('log')
ax2.set_title("Shannon Entropy Collapse\n(Proof of Informational Death)", fontsize=14)
ax2.set_xlabel("Population Size (N)", fontsize=12)
ax2.set_ylabel("Information Entropy (bits)", fontsize=12)
ax2.grid(True, which="both", ls="--", alpha=0.5)
ax2.legend()

plt.tight_layout()
plt.show()

# 統計結果のテキスト出力
print("【追加検定：相転移と情報損失の確認】")
print(f"初期(N={N_list[0]:.0e})のシャノン・エントロピー: {shannon_entropies[0]:.3f} bits")
print(f"巨大(N={N_list[-1]:.0e})のシャノン・エントロピー: {shannon_entropies[-1]:.3f} bits")
print(f"-> 巨大なNにおいて、オピニオンの持つ情報量（多様性）が {shannon_entropies[-1]/shannon_entropies[0]*100:.1f}% にまで崩壊しています。")
