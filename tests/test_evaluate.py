import pandas as pd

from src.evaluate import build_eval_cases, evaluate
from src.models import PopularityBaseline


def test_baseline_ranking_and_exclusion():
    rows = [("1", "A"), ("1", "B"), ("2", "A"), ("2", "B"), ("3", "A"), ("3", "C")]
    train = pd.DataFrame(rows, columns=["Invoice", "StockCode"])
    model = PopularityBaseline().fit(train)
    assert model.ranking == ["A", "B", "C"]
    assert model.recommend(["A"], 2) == ["B", "C"]  # không gợi ý món đã có trong giỏ


def test_eval_cases_are_valid_and_reproducible():
    rows = [("10", "A"), ("10", "B"), ("10", "C"),   # hợp lệ
            ("11", "A"),                              # chỉ 1 sản phẩm
            ("12", "Z"), ("12", "Y")]                 # toàn sản phẩm chưa thấy
    val = pd.DataFrame(rows, columns=["Invoice", "StockCode"])
    vocab = {"A", "B", "C"}
    cases, info = build_eval_cases(val, vocab)
    assert len(cases) == 1
    query, hidden = cases[0]
    assert hidden in vocab and hidden not in query
    assert sorted(query + [hidden]) == ["A", "B", "C"]
    assert info["bi_loai_chi_co_1_san_pham"] == 1
    assert info["bi_loai_khong_co_mon_da_thay"] == 1
    assert build_eval_cases(val, vocab)[0] == cases  # cùng seed, cùng kết quả


class AlwaysA:
    def recommend(self, query, k):
        return ["A"][:k]


def test_evaluate_metrics():
    res = evaluate(AlwaysA(), [(["B"], "A")], {"A", "B", "C"}, {"A"}, ks=(1,))
    row = res.iloc[0]
    assert row["hit_rate"] == 1.0
    assert abs(row["coverage"] - 1 / 3) < 1e-9
    assert row["pop_share"] == 1.0