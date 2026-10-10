"""Thí nghiệm 2 và 3 trên validation: baseline vs cosine item-invoice theo ngưỡng tần suất."""
import numpy as np
import pandas as pd

from src.evaluate import POP_N, REPORT_DIR, build_eval_cases, evaluate
from src.models import CosineItemInvoice, PopularityBaseline
from src.preprocess import load_split

MIN_COUNTS = (1, 5, 10, 20, 50)


def run():
    train, val = load_split("train"), load_split("val")  # KHÔNG đọc test

    base = PopularityBaseline().fit(train)
    vocab = set(base.ranking)  # danh mục đầy đủ của train, dùng làm mẫu số coverage
    popular = set(base.ranking[:POP_N])
    cases, info = build_eval_cases(val, vocab)
    print("Bộ ca đánh giá (val):", info)

    results = [evaluate(base, cases, vocab, popular).assign(model="top_popular", min_count=1)]
    for m in MIN_COUNTS:
        model = CosineItemInvoice(min_count=m).fit(train)
        print(f"cosine min_count={m}: {len(model.items)} sản phẩm trong mô hình")
        res = evaluate(model, cases, vocab, popular)
        results.append(res.assign(model="cosine_item_invoice", min_count=m))

    out = pd.concat(results, ignore_index=True)
    out["ci95"] = 1.96 * np.sqrt(out["hit_rate"] * (1 - out["hit_rate"]) / out["n_cases"])
    out["split"] = "val"
    out = out[["model", "min_count", "K", "hit_rate", "ci95", "coverage",
               "pop_share", "n_cases", "split"]]

    REPORT_DIR.mkdir(exist_ok=True)
    out.to_csv(REPORT_DIR / "experiments_val.csv", index=False)
    print(out.round(4).to_string(index=False))


if __name__ == "__main__":
    run()