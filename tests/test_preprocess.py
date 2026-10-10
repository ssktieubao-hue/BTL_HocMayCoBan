import pandas as pd

from src.preprocess import clean_data, split_by_time


def row(inv, code="85048", desc="X", qty=1, price=1.0, date="2010-01-01", cust=1.0):
    return {"Invoice": inv, "StockCode": code, "Description": desc, "Quantity": qty,
            "InvoiceDate": pd.Timestamp(date), "Price": price,
            "Customer ID": cust, "Country": "UK"}


def test_clean_removes_bad_rows():
    df = pd.DataFrame([
        row("1"),                 # hợp lệ
        row("C2"),                # hóa đơn hủy
        row("3", qty=-1),         # số lượng âm
        row("4", price=0),        # giá 0
        row("5", code="POST"),    # không phải sản phẩm
        row("6", desc=None),      # thiếu mô tả
    ])
    clean, _ = clean_data(df)
    assert list(clean["Invoice"]) == ["1"]


def test_split_by_time_has_no_leak():
    start = pd.Timestamp("2010-01-01")
    df = pd.DataFrame([row(str(i), date=start + pd.Timedelta(days=i)) for i in range(100)])
    train, val, test = split_by_time(df, 0.2, 0.1)
    assert (len(train), len(val), len(test)) == (70, 20, 10)
    assert not set(train["Invoice"]) & set(val["Invoice"])
    assert not set(train["Invoice"]) & set(test["Invoice"])
    assert not set(val["Invoice"]) & set(test["Invoice"])
    assert train["InvoiceDate"].max() < val["InvoiceDate"].min()
    assert val["InvoiceDate"].max() < test["InvoiceDate"].min()