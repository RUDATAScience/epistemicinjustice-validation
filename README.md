# Signal Cliff Simulator: 巨大データにおける「情報の崖」検証モデル

## 概要 (Overview)
本リポジトリは、社会物理学におけるオピニオンダイナミクス（GalamのIsingベースモデル, 1982）を拡張し、現代のビッグデータ社会における「情報の機能不全」を数理的に検証するためのシミュレーションコードを提供します。

サンプルサイズ $N$ を $10^1$ から $10^{10}$（100億人規模）までスケーリングさせ、同調圧力（Conformity Pressure）と微小なシステムバイアスが存在する空間において、マイノリティの意見（警告シグナル）が数学的・構造的に完全に消失する閾値**「シグナルの崖（Signal Cliff）」**を可視化します。

この検証は、大規模データセットにおける「精度（Precision）」の向上が、必ずしも「正確さ（Accuracy）」や「多様性（Diversity）」を保証しないという「認識論的不正義（Epistemic Injustice）」を証明するものです。

## 理論的背景 (Theoretical Background)
本コードは、川畑（2026）が提唱する「情報的健康診断（Informational Health Diagnostics）」の数理的基盤となります。
従来の多数決モデルやエージェントベースモデルでは、$N=10^{10}$ といった地球規模の計算は計算コストの観点から不可能でした。本プログラムでは以下の近似手法を導入することで、巨大スケールでの相転移のシミュレーションを可能にしています。

* **ミクロスケール ($N < 10^6$)**: Glauberダイナミクスに基づく正確な二項分布サンプリング。
* **マクロスケール ($N \ge 10^6$)**: 中心極限定理を用いた正規分布近似による計算量 $O(1)$ への圧縮。

## 出力される検証結果 (Outputs & Validation)
スクリプトを実行すると、以下の統計検定および可視化グラフが出力されます。

1. **分散の崩壊（Levene検定）**: $N$の拡大に伴い、意見の揺らぎ（多様性）が有意に崩壊するプロセスを検証します。
2. **偽の安定への収束（Kruskal-Wallis検定）**: マイノリティが優勢な初期状態からでも、巨大な$N$の下ではシステムバイアスによってマジョリティ側へと結果が強引に引き寄せられる現象を検証します。
3. **Signal Cliff の特定**: 分散が初期の1%未満に落ち込む境界となる $N$ の閾値を自動検出します。


git clone [https://github.com/YourUsername/signal-cliff-simulator.git](https://github.com/YourUsername/signal-cliff-simulator.git)
cd signal-cliff-simulator
python signal_cliff_simulator.py


## 必要要件 (Requirements)
* Python 3.8+
* `numpy`
* `scipy`
* `matplotlib`
* `seaborn`
* `pandas`

パラメータ設定 (Parameters)コード内の以下の変数を変更することで、様々な社会状況をシミュレーション可能です。N_list: 検証するサンプルサイズの配列（デフォルト: $10^1 \sim 10^{10}$）J: 同調圧力・相互作用の強さ（デフォルト: 1.0）H: 外部磁場・システム的バイアス（デフォルト: 0.05）T: 社会的温度・ノイズ（デフォルト: 1.2）m_init: 初期オピニオンの平均値（デフォルト: -0.2 / マイノリティ優勢）


```bash
pip install numpy scipy matplotlib seaborn pandas

参考文献 (References)
Galam, S., Gefen, Y., & Shapir, Y. (1982). Sociophysics: A new approach of sociological collective behaviour. I. Mean-behaviour description of a strike. Journal of Mathematical Sociology, 9(1), 1-13.

Kawahata, Y. (2026). Epistemic Injustice Validation: Simulations of Signal Disappearance under Minority Suppression.
