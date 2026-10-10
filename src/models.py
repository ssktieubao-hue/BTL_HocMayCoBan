"""Các mô hình gợi ý. Giao diện chung: fit(train_df) -> self; recommend(query, k) -> list."""
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity


class PopularityBaseline:
    """Gợi ý các sản phẩm bán chạy nhất toàn cục (đếm số hóa đơn trong train)."""

    def fit(self, train: pd.DataFrame):
        counts = train.drop_duplicates(["Invoice", "StockCode"])["StockCode"].value_counts()
        self.counts = counts.to_dict()
        # xếp theo số hóa đơn giảm dần; nếu bằng nhau thì theo mã, để kết quả cố định
        self.ranking = sorted(self.counts, key=lambda s: (-self.counts[s], s))
        return self

    def recommend(self, query, k):
        q = set(query)
        out = []
        for s in self.ranking:
            if s not in q:  # không gợi ý món đã có trong giỏ
                out.append(s)
                if len(out) == k:
                    break
        return out


class CosineItemInvoice:
    """Cosine giữa các vector nhị phân item-invoice (học từ train).

    min_count: chỉ giữ sản phẩm xuất hiện trong ít nhất min_count hóa đơn của train.
    """

    def __init__(self, min_count: int = 1):
        self.min_count = min_count

    def fit(self, train: pd.DataFrame):
        pairs = train.drop_duplicates(["Invoice", "StockCode"])[["Invoice", "StockCode"]]
        freq = pairs["StockCode"].value_counts()
        items = sorted(freq[freq >= self.min_count].index)
        pairs = pairs[pairs["StockCode"].isin(set(items))]

        self.items = items
        self.index = {s: i for i, s in enumerate(items)}
        rows = pairs["StockCode"].map(self.index).to_numpy()
        cols = pd.factorize(pairs["Invoice"])[0]
        X = csr_matrix(
            (np.ones(len(pairs), dtype=np.float32), (rows, cols)),
            shape=(len(items), cols.max() + 1),
        )
        self.sim = cosine_similarity(X, dense_output=True)
        np.fill_diagonal(self.sim, 0.0)
        return self

    def recommend(self, query, k):
        idx = [self.index[s] for s in query if s in self.index]
        if not idx:  # không món nào của giỏ có trong mô hình
            return []
        scores = self.sim[idx].sum(axis=0)
        scores[idx] = 0.0  # không gợi ý món đã có trong giỏ
        order = np.argsort(-scores, kind="stable")[:k]
        return [self.items[i] for i in order if scores[i] > 0]