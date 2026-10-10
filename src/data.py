"""Tải và đọc dữ liệu Online Retail II (UCI, CC BY 4.0)."""
import hashlib
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
ZIP_PATH = RAW_DIR / "online_retail_ii.zip"
XLSX_PATH = RAW_DIR / "online_retail_II.xlsx"
CSV_PATH = RAW_DIR / "online_retail_II.csv"
DTYPES = {"Invoice": str, "StockCode": str}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download() -> None:
    """Tải file zip từ UCI và giải nén vào data/raw/."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if not XLSX_PATH.exists():
        print("Đang tải dữ liệu từ UCI...")
        urlretrieve(URL, ZIP_PATH)
        with zipfile.ZipFile(ZIP_PATH) as z:
            z.extractall(RAW_DIR)
    print("SHA256 của file xlsx:", sha256(XLSX_PATH))


def to_csv() -> None:
    """Gộp 2 sheet của file xlsx thành 1 file CSV (đọc nhanh hơn xlsx nhiều)."""
    if CSV_PATH.exists():
        return
    print("Đang đọc xlsx (mất vài phút)...")
    sheets = pd.read_excel(XLSX_PATH, sheet_name=None, dtype=DTYPES)
    for name, sh in sheets.items():
        print(f"  Sheet '{name}': {len(sh)} dòng")
    pd.concat(sheets.values(), ignore_index=True).to_csv(CSV_PATH, index=False)


def load_raw() -> pd.DataFrame:
    """Đọc dữ liệu thô. Dùng hàm này ở các bước sau."""
    return pd.read_csv(CSV_PATH, dtype=DTYPES, parse_dates=["InvoiceDate"])


if __name__ == "__main__":
    download()
    to_csv()
    df = load_raw()
    print("Kích thước:", df.shape)
    print(df.dtypes)
    print(df.head())