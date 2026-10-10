"""Huấn luyện offline và lưu model cho serving. Cấu hình theo reports/final_config.md.

  python -m src.build_artifact
"""
import json
from datetime import date

import numpy as np
import pandas as pd

from src.data import ROOT
from src.evaluate import POP_N, RANDOM_STATE
from src.models import CosineItemInvoice, PopularityBaseline
from src.preprocess import load_split

ARTIFACT = ROOT / "models" / "item_invoice_cosine.json"
MIN_COUNT = 1
K_MAX = 50


def build():
    fit = pd.concat([load_split("train"), load_split("val")], ignore_index=True)
    base = PopularityBaseline().fit(fit)
    model = CosineItemInvoice(min_count=MIN_COUNT).fit(fit)
    desc = fit.groupby("StockCode")["Description"].agg(lambda s: s.mode().iloc[0])
    items, sim = model.items, model.sim  # đường chéo của sim đã bằng 0

    order = np.argsort(-sim, axis=1, kind="stable")[:, :K_MAX]
    neighbors, scores = [], []
    for i in range(len(items)):
        idx = [int(j) for j in order[i] if sim[i, j] > 0]
        neighbors.append(idx)
        scores.append([round(float(sim[i, j]), 4) for j in idx])

    # Kiểm tra: kết quả lưu phải trùng với model.recommend của mô hình đã đánh giá
    rng = np.random.default_rng(RANDOM_STATE)
    for i in rng.choice(len(items), 20, replace=False):
        assert model.recommend([items[i]], K_MAX) == [items[j] for j in neighbors[i]]

    artifact = {
        "meta": {
            "model": "cosine item-invoice (vector nhị phân)",
            "min_count": MIN_COUNT, "k_max": K_MAX, "random_state": RANDOM_STATE,
            "trained_on": "train+val", "pop_n": POP_N,
            "data_from": fit["InvoiceDate"].min().strftime("%Y-%m-%d"),
            "data_to": fit["InvoiceDate"].max().strftime("%Y-%m-%d"),
            "n_invoices": int(fit["Invoice"].nunique()), "n_items": len(items),
            "built_on": date.today().isoformat(),
        },
        "items": items,
        "descriptions": [str(desc.get(s, "")).strip() for s in items],
        "invoice_count": [int(base.counts[s]) for s in items],
        "neighbors": neighbors,
        "scores": scores,
        "popular": base.ranking[:POP_N],
    }
    ARTIFACT.parent.mkdir(exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, ensure_ascii=False, separators=(",", ":")),
                        encoding="utf-8")
    print(f"Đã lưu {ARTIFACT} ({ARTIFACT.stat().st_size / 1e6:.1f} MB), {len(items)} sản phẩm")


if __name__ == "__main__":
    build()