import pandas as pd

from src.models import CosineItemInvoice


def make_train():
    # A và B luôn đi cùng nhau; C và D luôn đi cùng nhau; hai cặp không liên quan
    rows = [("1", "A"), ("1", "B"), ("2", "A"), ("2", "B"), ("3", "A"), ("3", "B"),
            ("4", "C"), ("4", "D"), ("5", "C"), ("5", "D")]
    return pd.DataFrame(rows, columns=["Invoice", "StockCode"])


def test_recommends_co_purchased_item():
    model = CosineItemInvoice().fit(make_train())
    assert model.recommend(["A"], 1) == ["B"]
    assert model.recommend(["C"], 1) == ["D"]


def test_no_query_items_and_no_zero_scores():
    model = CosineItemInvoice().fit(make_train())
    rec = model.recommend(["A"], 10)
    assert "A" not in rec
    assert rec == ["B"]  # C, D không đồng xuất hiện với A nên điểm 0, không được gợi ý


def test_unknown_query_returns_empty():
    model = CosineItemInvoice().fit(make_train())
    assert model.recommend(["ZZZ"], 5) == []


def test_min_count_filters_rare_items():
    rare = pd.DataFrame([("6", "E")], columns=["Invoice", "StockCode"])
    model = CosineItemInvoice(min_count=2).fit(pd.concat([make_train(), rare]))
    assert "E" not in model.index