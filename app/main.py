"""API gợi ý mua kèm. Chỉ nạp model đã lưu, không huấn luyện lại ở mỗi request.

  python -m uvicorn app.main:create_app --factory --reload
"""
import csv
import json
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ARTIFACT = Path(__file__).resolve().parents[1] / "models" / "item_invoice_cosine.json"
REPORTS = Path(__file__).resolve().parents[1] / "reports"
STATIC = Path(__file__).resolve().parent / "static"


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


class BasketRecommendationRequest(BaseModel):
    stock_codes: list[str]
    k: int = 10


class BasketRecommendationResponse(BaseModel):
    basket: list[Product]
    k: int
    returned: int
    recommendations: list[Recommendation]
    note: str | None = None


class ErrorBody(BaseModel):
    code: str
    message: str
    suggestions: list[str] | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody


def create_app(path: Path = ARTIFACT, reports: Path = REPORTS) -> FastAPI:
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

    @app.get("/api/search", response_model=list[Product],
             responses={422: {"model": ErrorResponse}})
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

    @app.get("/api/similar-items", response_model=SimilarItemsResponse,
             responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
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

    @app.post("/api/recommend-basket", response_model=BasketRecommendationResponse,
              responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
    def recommend_basket(body: BasketRecommendationRequest):
        raw_codes = [s.strip() for s in body.stock_codes if s and s.strip()]
        if not raw_codes:
            raise ApiError(422, "empty_basket", "Giỏ hàng phải có ít nhất một mã sản phẩm.")
        if len(raw_codes) > 50:
            raise ApiError(422, "basket_too_large", "Giỏ hàng chỉ hỗ trợ tối đa 50 sản phẩm mỗi lần gọi.")
        if not 1 <= body.k <= k_max:
            raise ApiError(422, "k_out_of_range",
                           f"k phải là số nguyên từ 1 đến {k_max} (nhận được {body.k}).")

        basket_items, unknown_codes, query_indices, query_set = [], [], [], set()
        for s in raw_codes:
            idx_s = index.get(s)
            if idx_s is None:
                unknown_codes.append(s)
            elif s not in query_set:
                query_set.add(s)
                query_indices.append(idx_s)
                basket_items.append(product(idx_s))

        if unknown_codes:
            sug = [c for c in items if any(c.lower().startswith(u.lower()) for u in unknown_codes)][:5]
            raise ApiError(404, "unknown_stock_code",
                           "Các mã sau không có trong mô hình: "
                           + ", ".join(f"'{u}'" for u in unknown_codes) + " (mã phân biệt hoa thường).",
                           suggestions=sug)

        scores = {}
        for qi in query_indices:
            for nb, sc in zip(art["neighbors"][qi], art["scores"][qi]):
                if items[nb] not in query_set:
                    scores[nb] = scores.get(nb, 0.0) + sc

        ranked = sorted(scores.items(), key=lambda x: (-x[1], -art["invoice_count"][x[0]]))[:body.k]
        recs = [Recommendation(**product(j).model_dump(), rank=r, cosine=round(score, 4))
                for r, (j, score) in enumerate(ranked, 1)]
        note = None if len(recs) == body.k else (
            f"Chỉ có {len(recs)} sản phẩm từng xuất hiện cùng các sản phẩm trong giỏ này.")

        return BasketRecommendationResponse(basket=basket_items, k=body.k, returned=len(recs),
                                            recommendations=recs, note=note)

    @app.get("/api/recommend-basket", response_model=BasketRecommendationResponse,
             responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
    def recommend_basket_get(stock_codes: str = Query(..., description="Mã sản phẩm, cách nhau bằng dấu phẩy"),
                             k: int = 10):
        codes = [s.strip() for s in stock_codes.split(",") if s.strip()]
        return recommend_basket(BasketRecommendationRequest(stock_codes=codes, k=k))

    @app.get("/api/dashboard")
    def dashboard():
        def rows(name):
            f = Path(reports) / name
            if not f.exists():
                return []
            with f.open(encoding="utf-8-sig") as fh:
                return list(csv.DictReader(fh))

        popular = [{**product(index[s]).model_dump(),
                    "share": round(art["invoice_count"][index[s]] / meta["n_invoices"], 4)}
                   for s in art["popular"][:10]]
        return {"meta": meta, "test_results": rows("final_test.csv"),
                "error_analysis": rows("error_analysis.csv"), "popular": popular}

    # Phải đặt sau mọi route /api/..., nếu không trang tĩnh sẽ che mất API
    app.mount("/", StaticFiles(directory=STATIC, html=True), name="static")
    return app