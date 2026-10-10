"""Khung đánh giá: Hit-rate@K, coverage, tỷ lệ gợi ý hàng phổ biến."""
import numpy as np
import pandas as pd

from src.data import ROOT
from src.preprocess import load_split

RANDOM_STATE = 42
KS = (5, 10, 20)
POP_N = 100  # "hàng phổ biến" = 100 sản phẩm bán chạy nhất trong train
REPORT_DIR = ROOT / "reports"


def build_eval_cases(df, vocab, seed=RANDOM_STATE):
    """Mỗi hóa đơn có >= 2 sản phẩm -> (món đầu vào, món bị giấu).
    Món bị giấu chỉ chọn trong số sản phẩm đã có ở train (vocab)."""
    rng = np.random.default_rng(seed)
    cases, n_single, n_unknown = [], 0, 0
    baskets = df.groupby("Invoice")["StockCode"].unique()  # duyệt theo thứ tự cố định
    for items in baskets:
        items = sorted(set(items))
        if len(items) < 2:
            n_single += 1
            continue
        known = [i for i in items if i in vocab]
        if not known:
            n_unknown += 1
            continue
        hidden = known[rng.integers(len(known))]
        cases.append(([i for i in items if i != hidden], hidden))
    info = {
        "hoa_don": len(baskets),
        "bi_loai_chi_co_1_san_pham": n_single,
        "bi_loai_khong_co_mon_da_thay": n_unknown,
        "so_ca_danh_gia": len(cases),
    }
    return cases, info


def evaluate(model, cases, vocab, popular, ks=KS):
    recs = [model.recommend(query, max(ks)) for query, _ in cases]
    rows = []
    for k in ks:
        hits = sum(hidden in r[:k] for r, (_, hidden) in zip(recs, cases))
        shown = [x for r in recs for x in r[:k]]
        rows.append({
            "K": k,
            "hit_rate": hits / len(cases),
            "coverage": len(set(shown)) / len(vocab),
            "pop_share": sum(x in popular for x in shown) / len(shown),
            "n_cases": len(cases),
        })
    return pd.DataFrame(rows)


def main():
    from src.models import PopularityBaseline

    train, val = load_split("train"), load_split("val")  # KHÔNG đọc test ở bước này
    model = PopularityBaseline().fit(train)
    vocab = set(model.ranking)
    popular = set(model.ranking[:POP_N])

    cases, info = build_eval_cases(val, vocab)
    print("Bộ ca đánh giá (val):", info)
    res = evaluate(model, cases, vocab, popular)
    print(res.round(4).to_string(index=False))

    REPORT_DIR.mkdir(exist_ok=True)
    res.assign(model="top_popular", split="val").to_csv(
        REPORT_DIR / "baseline_val.csv", index=False)


if __name__ == "__main__":
    main()