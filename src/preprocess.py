"""Làm sạch (luật cố định) và chia train/val/test theo thời gian."""
import pandas as pd

from src.data import ROOT, load_raw

PROCESSED_DIR = ROOT / "data" / "processed"
REPORT_DIR = ROOT / "reports"
PRODUCT_CODE = r"^\d{5}[A-Za-z]*$"  # mã sản phẩm thật: 5 chữ số + chữ cái tùy chọn
VAL_FRAC, TEST_FRAC = 0.15, 0.15
READ_DTYPES = {"Invoice": str, "StockCode": str, "Customer ID": str}


def clean_data(df: pd.DataFrame):
    """Chỉ dùng luật cố định, KHÔNG học gì từ dữ liệu. Trả về (df_sạch, nhật_ký)."""
    log = [{"quy_tac": "Dữ liệu thô", "dong_bi_loai": 0, "con_lai": len(df)}]
    d = df

    def keep(mask, rule):
        nonlocal d
        out = d[mask]
        log.append({"quy_tac": rule, "dong_bi_loai": len(d) - len(out), "con_lai": len(out)})
        d = out

    keep(~d["Invoice"].str.startswith("C"), "Hóa đơn hủy (Invoice bắt đầu bằng C)")
    keep(d["Quantity"] > 0, "Quantity <= 0")
    keep(d["Price"] > 0, "Price <= 0")
    keep(d["StockCode"].str.match(PRODUCT_CODE, na=False),
         "StockCode không phải sản phẩm (POST, M, D, BANK CHARGES...)")
    keep(d["Description"].notna() & (d["Description"].str.strip() != ""), "Thiếu Description")

    d = d.copy()
    d["Customer ID"] = d["Customer ID"].astype("Int64").astype("string")  # 13085.0 -> "13085"
    return d.reset_index(drop=True), pd.DataFrame(log)


def split_by_time(df: pd.DataFrame, val_frac=VAL_FRAC, test_frac=TEST_FRAC):
    """Chia theo HÓA ĐƠN, xếp theo thời gian: train (cũ nhất) -> val -> test (mới nhất)."""
    inv_time = df.groupby("Invoice")["InvoiceDate"].min().sort_values(kind="stable")
    n = len(inv_time)
    n_test, n_val = int(n * test_frac), int(n * val_frac)
    n_train = n - n_val - n_test
    train_inv = set(inv_time.index[:n_train])
    val_inv = set(inv_time.index[n_train:n_train + n_val])
    test_inv = set(inv_time.index[n_train + n_val:])
    return tuple(df[df["Invoice"].isin(s)].reset_index(drop=True)
                 for s in (train_inv, val_inv, test_inv))


def check_no_leak(train, val, test):
    a, b, c = (set(x["Invoice"]) for x in (train, val, test))
    assert not (a & b) and not (a & c) and not (b & c), "Hóa đơn bị lẫn giữa các tập!"


def load_split(name: str) -> pd.DataFrame:
    """Đọc 'train' | 'val' | 'test'. Các bước sau dùng hàm này."""
    return pd.read_csv(PROCESSED_DIR / f"{name}.csv", dtype=READ_DTYPES,
                       parse_dates=["InvoiceDate"])


def build_processed():
    clean, log = clean_data(load_raw())
    parts = dict(zip(("train", "val", "test"), split_by_time(clean)))
    check_no_leak(*parts.values())

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)
    for name, part in parts.items():
        part.to_csv(PROCESSED_DIR / f"{name}.csv", index=False)
    log.to_csv(REPORT_DIR / "cleaning_log.csv", index=False, encoding="utf-8-sig")

    print(log.to_string(index=False))
    print()
    for name, p in parts.items():
        print(f"{name:5s} | dòng {len(p):>9,} | hóa đơn {p['Invoice'].nunique():>7,} | "
              f"sản phẩm {p['StockCode'].nunique():>5,} | "
              f"{p['InvoiceDate'].min():%Y-%m-%d} -> {p['InvoiceDate'].max():%Y-%m-%d}")


if __name__ == "__main__":
    build_processed()