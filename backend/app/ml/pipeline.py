from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest, RandomForestClassifier


class MLOrchestrator:
    def build_features(self, candles: list[dict], news_items: list[dict]) -> pd.DataFrame:
        frame = pd.DataFrame(candles).sort_values("timestamp")
        frame["return_1"] = frame["close"].pct_change().fillna(0)
        frame["volatility_5"] = frame["return_1"].rolling(5).std().fillna(0)
        frame["momentum_5"] = frame["close"].pct_change(5).fillna(0)
        sentiment = np.mean([item.get("sentiment", 0.0) for item in news_items]) if news_items else 0.0
        frame["sentiment_mean"] = sentiment
        frame["target"] = (frame["return_1"].shift(-1) > 0).astype(int).fillna(0)
        return frame

    def score_market(self, features: pd.DataFrame) -> dict:
        usable = features[["return_1", "volatility_5", "momentum_5", "sentiment_mean"]].fillna(0)
        if len(usable) < 10:
            latest = usable.iloc[-1].to_dict()
            probability_up = float(max(0.1, min(0.9, 0.5 + latest["momentum_5"] + latest["sentiment_mean"] * 0.1)))
            return {
                "probability_up": round(probability_up, 4),
                "confidence": round(abs(probability_up - 0.5) * 2, 4),
                "regime_cluster": 0,
                "anomaly_score": 0.0,
                "top_features": latest,
            }

        model = RandomForestClassifier(n_estimators=32, random_state=42)
        model.fit(usable.iloc[:-1], features["target"].iloc[:-1])
        probability_up = float(model.predict_proba(usable.iloc[[-1]])[0][1])

        clusters = KMeans(n_clusters=3, n_init=10, random_state=42).fit_predict(usable)
        anomaly = IsolationForest(random_state=42, contamination=0.1).fit(usable).decision_function(usable.iloc[[-1]])[0]

        importances = dict(zip(usable.columns.tolist(), model.feature_importances_.tolist()))
        return {
            "probability_up": round(probability_up, 4),
            "confidence": round(abs(probability_up - 0.5) * 2, 4),
            "regime_cluster": int(clusters[-1]),
            "anomaly_score": round(float(anomaly), 4),
            "top_features": {k: round(v, 4) for k, v in importances.items()},
        }
