# NBA Hall of Fame Predictor — Results Summary (Longevity + Accolades First)

**Last updated:** Aug 13, 2025

This project estimates **Hall of Fame probabilities** with a deliberate emphasis on **body of work**—career length, durability, cumulative totals, and accolades—while de-emphasizing efficiency-heavy stats that can overweight short peaks.

---

## What we built

- **Data:** Career-level table (`master.csv`) from scraped web tables + merged awards.
- **Feature philosophy:**
  - **No per-game stats.** Keep per-season rates only to reflect body-of-work pace.
  - **No efficiency composites** (e.g., no PER/BPM/TS% blends).
  - Longevity & durability (e.g., `career_years`, `games_per_season`, iron-man flag),  
    accolades (`major_awards_score`, `all_nba_score`, `total_accolades`),  
    and simple volume (`volume_score` from log-scaled totals).
  - Greatness proxies without efficiency (`mvp_calibre`, `superstar_flag`, `greatness_score`).
- **Models compared:** Logistic Regression (baseline), Random Forest, **Gradient Boosting**, **XGBoost**, **LightGBM**.
- **Split:** Stratified holdout on non-active players; active players scored post-fit.
- **Metrics:** ROC-AUC (ranking), Brier (calibration), class precision/recall/F1, accuracy.

---

## Key results (test set)

| Model        | ROC-AUC ↑ | Brier ↓ | HoF Recall ↑ | HoF F1 ↑ | Accuracy |
|--------------|:---------:|:-------:|:------------:|:--------:|:--------:|
| GradientBoost| **0.987** | 0.020   | 0.848        | 0.889    | 0.979    |
| XGBoost      | 0.981     | **0.015** | 0.848      | 0.903    | 0.982    |
| LightGBM     | 0.978     | **0.015** | **0.879**  | **0.921**| **0.985**|

**Takeaways**
- **Best ranking (AUC):** GradientBoost.
- **Best calibration (Brier):** XGBoost & LightGBM (tie).
- **Best positive-class performance (recall & F1) + accuracy:** **LightGBM**.

**Pragmatic choice:** If missing a deserving inductee is costly, deploy **LightGBM** (highest recall/F1, well-calibrated). For pure ranking lists, GradientBoost edges out on AUC.

> FYI: LightGBM logs like “No further splits with positive gain” are benign pruning messages.

---

## What the models valued (global signals)

Consistently high-impact features:
- **Longevity & durability:** `longevity_score`, `career_years`, `games`, `games_per_season`, iron-man flag, All-Star consistency.
- **Accolades:** `major_awards_score`, `all_nba_score`, `total_accolades`, `accolades_per_season`, `has_mvp/has_finals_mvp/has_dpoy`.
- **Totals & proxies:** `pts`, `ast`, `trb`, `volume_score`, `mvp_calibre`, `superstar_flag`.

Efficiency metrics did **not** dominate—matching our design goal.

---

## Active players

We scored all `is_active = True` players with every model and saved per-model HoF probabilities (see `reports/active_hof_predictions.csv`). A consensus rank (average of per-model ranks) highlights durable multi-All-NBA resumes.

---

## Limitations & next steps

- **Era effects:** thresholds like 70 games/season or 1000+ games may favor certain eras. Next: era-normalized durability & totals.
- **Subjectivity in awards:** the model learns from real voting patterns; that’s a feature, not a bug—but worth noting.
- **Temporal validation:** add time-aware splits by `end_year` to better mimic future predictions.
- **Interpretability:** add SHAP for LightGBM (global + local explanations).
- **Calibration:** keep probabilities calibrated (isotonic/Platt) if surfaced publicly.

---

> If you want the how-to and code details, see the repo files.  
> This page is intentionally a **results summary**. For a standalone report, copy this into `MODEL_REPORT.md` and link to it from the README.

