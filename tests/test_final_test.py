import pandas as pd

from src.evaluate import build_eval_cases
from src.final_test import case_invoices, rank_of


def test_case_invoices_match_build_eval_cases():
    rows = [("10", "A"), ("10", "B"), ("10", "C"), ("11", "A"),
            ("12", "Z"), ("12", "Y"), ("13", "B"), ("13", "Z")]
    df = pd.DataFrame(rows, columns=["Invoice", "StockCode"])
    vocab = {"A", "B", "C"}
    cases, _ = build_eval_cases(df, vocab)
    assert len(cases) == 2
    assert case_invoices(df, vocab) == ["10", "13"]


class Fixed:
    def recommend(self, query, k):
        return ["X", "Y", "Z"][:k]


def test_rank_of():
    ranks, tops = rank_of(Fixed(), [(["A"], "Y"), (["A"], "Q")], k=3)
    assert ranks[0] == 2 and pd.isna(ranks[1])
    assert tops[0] == "X|Y|Z"