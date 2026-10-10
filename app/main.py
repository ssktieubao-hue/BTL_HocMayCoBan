"""API gợi ý mua kèm. Chỉ nạp model đã lưu, không huấn luyện lại ở mỗi request.

  python -m uvicorn app.main:create_app --factory --reload
"""
import json
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

ARTIFACT = Path(__file__).resolve().parents[1] / "models" / "item_invoice_cosine.json"


class ApiError(Exception):
    def __init__(self, status, code, message, **extra):
        self.status, self.code, self.message, self.extra = status, code, message, extra


class Product(BaseModel):
    stock_code: str
    description: str
    invoice_count: int


class Recommendation(Product):
    rank: int
    cosine: float


class SimilarItemsResponse(BaseModel):
    stock_code: str
    description: str
    k: int
    returned: int
    recommendations: list[Recommendation]
    note: str | None = None


def create_app(path: Path = ARTIFACT) -> FastAPI:
    if not Path(path).exists():
        raise FileNotFoundError("Chưa có model. Chạy: python -m src.build_artifact")
    art = json.loads(Path(path).read_text(encoding="utf-8"))
    meta, items = art["meta"], art["items"]
    index = {s: i for i, s in enumerate(items)}
    k_max = meta["k_max"]

    def product(i):
        return Product(stock_code=items[i], description=art["descriptions"][i],
                       invoice_count=art["invoice_count"][i])

    app = FastAPI(title="Gợi ý mua kèm", version="1.0")

    @app.exception_handler(ApiError)
    async def api_error(_: Request, e: ApiError):
        body = {"code": e.code, "message": e.message, **e.extra}
        return JSONResponse(status_code=e.status, content={"error": body})

    @app.exception_handler(RequestValidationError)
    async def validation_error(_: Request, e: RequestValidationError):
        msgs = [f"{x['loc'][-1]}: {x['msg']}" for x in e.errors()]
        return JSONResponse(status_code=422, content={"error": {
            "code": "invalid_input", "message": "Tham số không hợp lệ: " + "; ".join(msgs)}})

    @app.get("/api/health")
    def health():
        return {"status": "ok", "n_items": len(items), "built_on": meta["built_on"]}

    @app.get("/api/search", response_model=list[Product])
    def search(q: str = Query(...), limit: int = 10):
        q = q.strip()
        if not 2 <= len(q) <= 60:
            raise ApiError(422, "invalid_query", "q phải dài từ 2 đến 60 ký tự.")
        if not 1 <= limit <= 50:
            raise ApiError(422, "limit_out_of_range", "limit phải từ 1 đến 50.")
        ql = q.lower()
        hits = [i for i, s in enumerate(items)
                if s.lower().startswith(ql) or ql in art["descriptions"][i].lower()]
        hits.sort(key=lambda i: (not items[i].lower().startswith(ql), -art["invoice_count"][i]))
        return [product(i) for i in hits[:limit]]

    @app.get("/api/similar-items", response_model=SimilarItemsResponse)
    def similar_items(stock_code: str = Query(...), k: int = 10):
        if not stock_code or len(stock_code) > 20 or stock_code != stock_code.strip():
            raise ApiError(422, "invalid_stock_code",
                           "stock_code không được để trống, không có khoảng trắng đầu/cuối "
                           "và dài tối đa 20 ký tự.")
        if not 1 <= k <= k_max:
            raise ApiError(422, "k_out_of_range",
                           f"k phải là số nguyên từ 1 đến {k_max} (nhận được {k}).")
        i = index.get(stock_code)
        if i is None:
            sug = [s for s in items if s.lower().startswith(stock_code.lower())][:5]
            raise ApiError(404, "unknown_stock_code",
                           f"Không có mã '{stock_code}' trong mô hình (mã phân biệt hoa thường).",
                           suggestions=sug)
        recs = [Recommendation(**product(j).model_dump(), rank=r, cosine=art["scores"][i][r - 1])
                for r, j in enumerate(art["neighbors"][i][:k], 1)]
        note = None if len(recs) == k else (
            f"Chỉ có {len(recs)} sản phẩm từng xuất hiện cùng sản phẩm này "
            "trong các hóa đơn huấn luyện.")
        p = product(i)
        return SimilarItemsResponse(stock_code=stock_code, description=p.description, k=k,
                                    returned=len(recs), recommendations=recs, note=note)

    return app