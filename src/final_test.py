"""Đánh giá cuối cùng trên TEST, đúng một lần.

Cấu hình đã đóng băng trong reports/final_config.md. Học lại trên train + val
(không chọn lại tham số nào), rồi đánh giá trên test.

  python -m src.final_test            # chạy một lần
  python -m src.final_test --force    # chỉ khi có lỗi kỹ thuật; ghi lý do vào báo cáo
"""
import sys

import numpy as np
import pandas as pd

from src.evaluate import KS, POP_N, RANDOM_STATE, REPORT_DIR, build_eval_cases, evaluate
from src.models import CosineItemInvoice, PopularityBaseline
from src.preprocess import PROCESSED_DIR, load_split

MIN_COUNT = 1
SEEDS = range(20)
FINAL_CSV = REPORT_DIR / "final_test.csv"


def case_invoices(df, vocab):
    """Mã hóa đơn của từng ca, cùng thứ tự và cùng luật loại với build_eval_cases."""
    ids = []
    for inv, items in df.groupby("Invoice")["StockCode"].unique().items():
        items = set(items)
        if len(items) >= 2 and any(i in vocab for i in items):
            ids.append(inv)
    return ids


def rank_of(model, cases, k=max(KS)):
    """Hạng (1..k) của món bị giấu trong danh sách gợi ý; NaN nếu không nằm trong top k."""
    ranks, tops = [], []
    for query, hidden in cases:
        recs = model.recommend(query, k)
        ranks.append(recs.index(hidden) + 1 if hidden in recs else np.nan)
        tops.append("|".join(recs[:10]))
    return np.array(ranks), tops


def main():
    if FINAL_CSV.exists() and "--force" not in sys.argv:
        sys.exit("Đã có kết quả test. Test chỉ chạy một lần; dùng --force nếu thật sự cần "
                 "và ghi lý do vào báo cáo.")

    train, val, test = (load_split(n) for n in ("train", "val", "test"))
    fit = pd.concat([train, val], ignore_index=True)
    print(f"Học trên train + val: {len(fit):,} dòng, {fit['Invoice'].nunique():,} hóa đơn")

    base = PopularityBaseline().fit(fit)
    cosine = CosineItemInvoice(min_count=MIN_COUNT).fit(fit)
    vocab = set(base.ranking)
    popular = set(base.ranking[:POP_N])
    models = {"top_popular": base, "item_invoice": cosine}

    # 1) Kết quả đóng băng (seed 42)
    cases, info = build_eval_cases(test, vocab, RANDOM_STATE)
    print("Bộ ca đánh giá (test):", info)
    pairs = test.drop_duplicates(["Invoice", "StockCode"])
    print(f"Tỷ lệ cặp (hóa đơn, sản phẩm) ở test có sản phẩm chưa thấy khi học: "
          f"{(~pairs['StockCode'].isin(vocab)).mean():.3f}")

    out = pd.concat([evaluate(m, cases, vocab, popular).assign(model=n)
                     for n, m in models.items()], ignore_index=True)
    out["ci95"] = 1.96 * np.sqrt(out["hit_rate"] * (1 - out["hit_rate"]) / out["n_cases"])
    out["split"] = "test"
    out = out[["model", "K", "hit_rate", "ci95", "coverage", "pop_share", "n_cases", "split"]]
    print("\n=== KẾT QUẢ TEST (seed 42) ===")
    print(out.round(4).to_string(index=False))

    # 2) Chi tiết từng ca, dùng cho phân tích lỗi (nằm trong data/processed, không lên Git)
    ids = case_invoices(test, vocab)
    assert len(ids) == len(cases), "Lệch số ca so với build_eval_cases"
    date = test.groupby("Invoice")["InvoiceDate"].min()
    rank_pop, _ = rank_of(base, cases)
    rank_cos, top_cos = rank_of(cosine, cases)
    for name, r in (("top_popular", rank_pop), ("item_invoice", rank_cos)):
        row = out[(out["model"] == name) & (out["K"] == 10)].iloc[0]
        assert abs(np.mean(r <= 10) - row["hit_rate"]) < 1e-9, "Hạng và hit-rate không khớp"
    detail = pd.DataFrame({
        "Invoice": ids,
        "InvoiceDate": date.loc[ids].to_numpy(),
        "basket_size": [len(q) + 1 for q, _ in cases],
        "hidden": [h for _, h in cases],
        "hidden_freq": [base.counts[h] for _, h in cases],
        "query": ["|".join(q) for q, _ in cases],
        "top10_cosine": top_cos,
        "rank_pop": rank_pop,
        "rank_cos": rank_cos,
    })

    # 3) Biến thiên theo seed chọn món bị giấu
    rows = []
    for seed in SEEDS:
        cs, _ = build_eval_cases(test, vocab, seed)
        for n, m in models.items():
            rows.append(evaluate(m, cs, vocab, popular).assign(model=n, seed=seed))
    spread = (pd.concat(rows, ignore_index=True)
              .groupby(["model", "K"])["hit_rate"]
              .agg(trung_binh="mean", do_lech_chuan="std", nho_nhat="min", lon_nhat="max")
              .reset_index())
    print(f"\n=== Hit-rate qua {len(SEEDS)} seed chọn món bị giấu ===")
    print(spread.round(4).to_string(index=False))

    REPORT_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    detail.to_csv(PROCESSED_DIR / "test_cases.csv", index=False)
    spread.to_csv(REPORT_DIR / "final_test_seeds.csv", index=False)
    out.to_csv(FINAL_CSV, index=False)  # ghi cuối cùng: có file này nghĩa là đã chạy xong


if __name__ == "__main__":
    main()