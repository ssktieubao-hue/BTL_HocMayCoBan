"""Phân tích lỗi trên kết quả test đã có. Không học lại mô hình, không đọc test.csv.

  python -m src.error_analysis
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.evaluate import REPORT_DIR
from src.preprocess import PROCESSED_DIR, load_split

FIG = REPORT_DIR / "figures"
K = 10


def items_of(text):
    return text.split("|") if isinstance(text, str) and text else []


def hit_by(df, key):
    g = df.groupby(key, observed=True)
    t = pd.DataFrame({
        "n_ca": g.size(),
        "hit_popular": g["rank_pop"].apply(lambda r: (r <= K).mean()),
        "hit_cosine": g["rank_cos"].apply(lambda r: (r <= K).mean()),
    })
    t["ci95_cosine"] = 1.96 * np.sqrt(t["hit_cosine"] * (1 - t["hit_cosine"]) / t["n_ca"])
    return t


def plot_groups(tables, titles, path):
    fig, axes = plt.subplots(1, len(tables), figsize=(5.5 * len(tables), 4), sharey=True)
    for ax, t, title in zip(axes, tables, titles):
        x = np.arange(len(t))
        ax.bar(x - 0.2, t["hit_popular"], 0.4, label="Top bán chạy")
        ax.bar(x + 0.2, t["hit_cosine"], 0.4, yerr=t["ci95_cosine"], label="Cosine item–invoice")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{i}\n(n={n})" for i, n in zip(t.index, t["n_ca"])])
        ax.set_title(title)
    axes[0].set_ylabel(f"Hit-rate@{K} (test)")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")


def main():
    df = pd.read_csv(PROCESSED_DIR / "test_cases.csv", dtype={"Invoice": str, "hidden": str},
                     parse_dates=["InvoiceDate"])
    FIG.mkdir(parents=True, exist_ok=True)

    tables = {
        "do_pho_bien_mon_bi_giau": hit_by(df, pd.cut(
            df["hidden_freq"], [0, 19, 99, 499, np.inf],
            labels=["<20", "20-99", "100-499", ">=500"])),
        "kich_thuoc_gio": hit_by(df, pd.cut(
            df["basket_size"], [1, 5, 15, 40, np.inf],
            labels=["2-5", "6-15", "16-40", ">40"])),
        "thang": hit_by(df, df["InvoiceDate"].dt.to_period("M").astype(str)),
    }
    for name, t in tables.items():
        print(f"\n=== Hit-rate@{K} theo {name} ===")
        print(t.round(4).to_string())
    pd.concat(tables, names=["chieu", "nhom"]).to_csv(
        REPORT_DIR / "error_analysis.csv", encoding="utf-8-sig")
    plot_groups(list(tables.values()),
                ["Độ phổ biến của món bị giấu\n(số hóa đơn trong train+val)",
                 "Kích thước giỏ (số sản phẩm)", "Tháng của hóa đơn test"],
                FIG / "error_analysis.png")

    hc, hp = df["rank_cos"] <= K, df["rank_pop"] <= K
    cross = pd.crosstab(hc.rename("cosine_trung"), hp.rename("top_ban_chay_trung"))
    print(f"\n=== Trúng/trượt @{K}: cosine so với top bán chạy ===")
    print(cross.to_string())
    cross.to_csv(REPORT_DIR / "error_cross.csv")
    print("Ca cosine không gợi ý được (mọi món đầu vào chưa thấy):",
          int(df["top10_cosine"].isna().sum()))

    fit = pd.concat([load_split("train"), load_split("val")])
    desc = fit.groupby("StockCode")["Description"].agg(lambda s: s.mode().iloc[0])

    def name(s):
        return desc.get(s, f"{s} (chưa thấy)")

    for label, sub in (("TRÚNG", df[hc]), ("TRƯỢT", df[~hc])):
        print(f"\n--- 5 ví dụ {label} @{K} (chọn ngẫu nhiên, seed 42) ---")
        for _, r in sub.sample(5, random_state=42).iterrows():
            q, top = items_of(r["query"]), items_of(r["top10_cosine"])
            print(f"Hóa đơn {r['Invoice']} | giỏ {r['basket_size']} món | "
                  f"món bị giấu: {name(r['hidden'])}")
            print("   đầu vào:", "; ".join(name(s) for s in q[:4]), "..." if len(q) > 4 else "")
            print("   top 5 gợi ý:", "; ".join(name(s) for s in top[:5]))


if __name__ == "__main__":
    main()