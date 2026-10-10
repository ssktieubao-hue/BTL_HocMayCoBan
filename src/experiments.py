"""Thí nghiệm 1 và 4 trên validation (không đọc test).

  python -m src.experiments gift-list   # xem danh sách sản phẩm quà/đóng gói để chốt trước
  python -m src.experiments             # chạy thí nghiệm 1 và 4
"""
import sys

import numpy as np
import pandas as pd

from src.evaluate import POP_N, REPORT_DIR, build_eval_cases, evaluate
from src.models import CosineItemCustomer, CosineItemInvoice, PopularityBaseline, WithoutItems
from src.preprocess import load_split

K_MAIN = 10
GIFT_KEYWORDS = ("BAG", "SHOPPER", "WRAP", "GIFT", "RIBBON", "TISSUE")
COLS = ["model", "tap", "K", "hit_rate", "ci95", "coverage", "pop_share", "n_cases"]


def add_ci(df):
    df["ci95"] = 1.96 * np.sqrt(df["hit_rate"] * (1 - df["hit_rate"]) / df["n_cases"])
    return df[COLS]


def setup():
    train, val = load_split("train"), load_split("val")  # KHÔNG đọc test
    base = PopularityBaseline().fit(train)
    vocab = set(base.ranking)
    popular = set(base.ranking[:POP_N])
    cases, info = build_eval_cases(val, vocab)
    print("Bộ ca đánh giá (val):", info)
    return train, base, vocab, popular, cases


def gift_items(train, popular):
    """G = sản phẩm trong top POP_N của train có mô tả chứa từ khóa quà/đóng gói."""
    desc = train.groupby("StockCode")["Description"].agg(lambda s: s.mode().iloc[0])
    hit = desc.str.upper().str.contains("|".join(GIFT_KEYWORDS), regex=True)
    codes = [s for s in desc.index[hit.to_numpy()] if s in popular]
    return set(codes), desc


def show_gift_list():
    train = load_split("train")
    base = PopularityBaseline().fit(train)
    popular = set(base.ranking[:POP_N])
    G, desc = gift_items(train, popular)
    tab = pd.DataFrame({"StockCode": sorted(G, key=lambda s: -base.counts[s])})
    tab["so_hoa_don"] = tab["StockCode"].map(base.counts)
    tab["Description"] = tab["StockCode"].map(desc)
    REPORT_DIR.mkdir(exist_ok=True)
    tab.to_csv(REPORT_DIR / "gift_items.csv", index=False, encoding="utf-8-sig")
    print(f"{len(G)} sản phẩm khớp {GIFT_KEYWORDS} trong top {POP_N} bán chạy:")
    print(tab.to_string(index=False))
    print(f"\nTop {POP_N} KHÔNG khớp (kiểm tra xem có sót món quà/đóng gói nào không):")
    print("\n".join(f"{s}: {desc[s]}" for s in base.ranking[:POP_N] if s not in G))


def exp1(train, base, vocab, popular, cases):
    inv = CosineItemInvoice(min_count=1).fit(train)
    cus = CosineItemCustomer(min_count=1).fit(train)
    print(f"Số sản phẩm trong mô hình: item_invoice={len(inv.items)}, "
          f"item_customer={len(cus.items)}")

    in_cus = set(cus.items)
    sub = [c for c in cases if c[1] in in_cus]
    print(f"Ca có món bị giấu thuộc danh mục của item_customer: {len(sub)}/{len(cases)}")

    parts = []
    for tap, cs in (("tat_ca_ca", cases), ("mon_giau_trong_danh_muc_khach", sub)):
        for name, m in (("top_popular", base), ("item_invoice", inv), ("item_customer", cus)):
            parts.append(evaluate(m, cs, vocab, popular).assign(model=name, tap=tap))
    out = add_ci(pd.concat(parts, ignore_index=True))
    out.to_csv(REPORT_DIR / "exp1_val.csv", index=False)
    print("\n=== THÍ NGHIỆM 1 ===")
    print(out.round(4).to_string(index=False))


def exp4(train, vocab, popular, cases, G):
    if not G:
        print("Nhóm G rỗng, kiểm tra lại GIFT_KEYWORDS.")
        return
    model = CosineItemInvoice(min_count=1).fit(train)
    non_g = [c for c in cases if c[1] not in G]
    only_g = [c for c in cases if c[1] in G]
    print(f"\n|G| = {len(G)}; ca có món bị giấu ngoài G: {len(non_g)}, thuộc G: {len(only_g)}")

    variants = (
        ("day_du", model),
        ("bo_G_khoi_goi_y", WithoutItems(model, G)),
        ("bo_G_khoi_goi_y_va_dau_vao", WithoutItems(model, G, drop_query=True)),
    )
    parts = [evaluate(m, non_g, vocab, popular).assign(model=n, tap="mon_giau_ngoai_G")
             for n, m in variants]
    if only_g:
        parts.append(evaluate(model, only_g, vocab, popular)
                     .assign(model="day_du", tap="mon_giau_thuoc_G"))
    parts.append(evaluate(model, cases, vocab, popular).assign(model="day_du", tap="tat_ca_ca"))
    out = add_ci(pd.concat(parts, ignore_index=True))
    out.to_csv(REPORT_DIR / "exp4_val.csv", index=False)
    print("\n=== THÍ NGHIỆM 4 ===")
    print(out.round(4).to_string(index=False))

    recs = [x for q, _ in cases for x in model.recommend(q, K_MAIN)]
    basket = [x for q, h in cases for x in (*q, h)]
    share = pd.DataFrame([{
        "G_trong_danh_muc": len(G) / len(vocab),
        "G_trong_gio_that": np.mean([x in G for x in basket]),
        f"G_trong_goi_y_top{K_MAIN}": np.mean([x in G for x in recs]),
    }])
    share.to_csv(REPORT_DIR / "exp4_g_share.csv", index=False)
    print("\nTỷ lệ sản phẩm thuộc G:")
    print(share.round(4).to_string(index=False))


def run():
    train, base, vocab, popular, cases = setup()
    exp1(train, base, vocab, popular, cases)
    G, _ = gift_items(train, popular)
    exp4(train, vocab, popular, cases, G)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "gift-list":
        show_gift_list()
    else:
        run()