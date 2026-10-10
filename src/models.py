"""Các mô hình gợi ý. Giao diện chung: fit(train_df) -> self; recommend(query, k) -> list."""
import pandas as pd


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