# Hệ thống Gợi ý Mua kèm Bán lẻ (Retail Recommender System)

Dự án Bài tập lớn môn Học Máy: Xây dựng hệ thống gợi ý sản phẩm mua kèm (Cross-sell / Next-Basket Recommendation) dựa trên tập dữ liệu thực tế **UCI Online Retail II**.

---

## 📌 1. Tổng quan bài toán & Phương pháp luận

- **Bài toán**: Khi khách hàng đang xem một món đồ hoặc đã chọn một số món vào giỏ, hệ thống sẽ đề xuất danh sách Top-$K$ sản phẩm thường xuyên được mua kèm nhất.
- **Mô hình chính**: **Cosine Item–Invoice trên vector nhị phân**. Mỗi sản phẩm được biểu diễn bằng vector các hóa đơn đã chứa nó; độ tương đồng Cosine giữa 2 vector thể hiện tần suất đồng xuất hiện đã được chuẩn hóa theo độ phổ biến của từng món.
- **Mô hình cơ sở (Baseline)**: Gợi ý các sản phẩm có tần suất bán chạy nhất toàn cục (Top Popularity).
- **Chống rò rỉ dữ liệu (No Data Leakage)**:
  - Chia tập theo hóa đơn (Invoice) và theo trục thời gian (Time-based split) theo tỷ lệ 70% Train, 15% Validation, 15% Test.
  - Mọi luật làm sạch là luật cố định, không học trước từ dữ liệu. Ngưỡng tần suất chỉ đếm trên Train.
  - Cấu hình mô hình được đóng băng tại Git tag `frozen-before-test` trước khi đánh giá trên tập Test độc lập đúng 1 lần.
- **Kiến trúc phục vụ (Serving Architecture)**:
  - Huấn luyện offline lưu trước Top-50 láng giềng vào file JSON gọn nhẹ (`models/item_invoice_cosine.json`, ~2.9 MB).
  - Backend FastAPI tải artifact vào bộ nhớ RAM khi khởi động, phản hồi API với độ trễ dưới 2ms, không tính toán lại mô hình trực tuyến.

---

## 📊 2. Kết quả đánh giá trên tập Test độc lập (5.461 ca, seed 42)

| Chỉ số | Top bán chạy (Baseline) | Cosine Item–Invoice | Mức cải thiện |
|---|---|---|---|
| **Hit-rate@5** | $2,38\% \pm 0,40$ | **$15,89\% \pm 0,97$** | Gấp **6,7 lần** |
| **Hit-rate@10** | $3,85\% \pm 0,51$ | **$21,59\% \pm 1,09$** | Gấp **5,6 lần** |
| **Hit-rate@20** | $5,68\% \pm 0,61$ | **$27,49\% \pm 1,18$** | Gấp **4,8 lần** |
| **Độ phủ (Coverage@10)** | $0,85\%$ | **$40,86\%$** | Phủ rộng gấp **48 lần** |
| **Tỷ lệ hàng phổ biến** | $100\%$ | **$28,96\%$** | Giảm thiên lệch rõ rệt |

*(Dấu $\pm$ là khoảng tin cậy 95% $ci_{95}$; kiểm định độ nhạy qua 20 random seeds cho thấy Cosine duy trì ưu thế ổn định gấp 5,6 đến 6,8 lần baseline).*

---

## 🚀 3. Hướng dẫn cài đặt & Khởi chạy từ máy mới (Quickstart)

### 3.1. Thiết lập môi trường
Yêu cầu Python 3.11+.

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo:
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### 3.2. Chạy kiểm thử tự động
Toàn bộ 31 test cases kiểm tra tiền xử lý, mô hình, độ đo và API:
```bash
pytest
```

### 3.3. Khởi chạy Ứng dụng Web & API
```bash
python -m uvicorn app.main:create_app --factory --reload
```
Truy cập:
- **Giao diện Web tương tác**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Tài liệu API Swagger / OpenAPI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3.4. (Tùy chọn) Chạy bằng Docker
```bash
docker build -t retail-recommender .
docker run -p 8000:8000 retail-recommender
```

---

## 🔄 4. Tái lập toàn bộ quy trình (Pipeline Reproduction)

Nếu muốn chạy lại toàn bộ quy trình từ dữ liệu thô:
```bash
# 1. Tải dữ liệu từ UCI và gộp sheet
python -m src.data

# 2. Làm sạch theo luật cố định và chia train/val/test theo thời gian
python -m src.preprocess

# 3. Chạy thí nghiệm 2 & 3 trên validation (khảo sát ngưỡng tần suất)
python -m src.train

# 4. Chạy thí nghiệm 1 & 4 trên validation (vector khách hàng & phân tích nhóm túi)
python -m src.experiments

# 5. Huấn luyện offline trên train+val và xuất artifact phục vụ serving
python -m src.build_artifact

# 6. Đánh giá test cuối cùng (chỉ chạy 1 lần, ghi kết quả ra reports/)
python -m src.final_test

# 7. Phân tích lỗi theo kích thước giỏ, độ phổ biến và thời gian
python -m src.error_analysis
```

---

## 🌐 5. Đặc tả API Endpoint

| Phương thức | Endpoint | Chức năng |
|---|---|---|
| `GET` | `/api/health` | Kiểm tra tình trạng dịch vụ, số lượng sản phẩm, ngày build |
| `GET` | `/api/search?q=&limit=` | Tìm kiếm sản phẩm theo mã hoặc tên mô tả |
| `GET` | `/api/similar-items?stock_code=&k=` | Gợi ý Top-$k$ sản phẩm mua kèm theo 1 sản phẩm chỉ định |
| `POST` | `/api/recommend-basket` | Gợi ý Top-$k$ sản phẩm mua kèm cho **cả giỏ hàng nhiều món** (Body: `{"stock_codes": [...], "k": 10}`) |
| `GET` | `/api/recommend-basket?stock_codes=&k=` | Phiên bản GET tiện lợi cho gợi ý theo giỏ hàng |
| `GET` | `/api/dashboard` | Cung cấp dữ liệu bảng biểu kết quả test và phân tích lỗi cho giao diện |

---

## 📁 6. Cấu trúc thư mục

```
retail-recommender/
├── app/
│   ├── main.py                  # FastAPI server, định nghĩa route & validation
│   └── static/index.html        # Giao diện SPA (Trang chủ, Chi tiết SP, Giỏ hàng, Model Card)
├── data/
│   ├── README.md                # Nguồn dữ liệu, checksum, từ điển dữ liệu
│   ├── raw/                     # Dữ liệu thô (được bỏ qua bởi Git)
│   └── processed/               # Dữ liệu đã làm sạch & phân chia (bỏ qua bởi Git)
├── models/
│   └── item_invoice_cosine.json # Artifact Top-50 láng giềng đã tính toán trước
├── reports/
│   ├── figures/                 # Biểu đồ EDA và biểu đồ phân tích lỗi
│   ├── final_config.md          # Đặc tả cấu hình đóng băng trước test
│   ├── final_test.csv           # Bảng kết quả test độc lập
│   └── error_analysis.csv       # Dữ liệu phân tích lỗi đa chiều
├── src/
│   ├── data.py                  # Tải dữ liệu UCI & xuất CSV
│   ├── preprocess.py            # Làm sạch luật cố định & chia tập theo thời gian
│   ├── models.py                # Thuật toán Baseline & Cosine Binary
│   ├── evaluate.py              # Đánh giá Hit-rate@K, Coverage, Popularity Share
│   ├── train.py                 # Thí nghiệm 2 & 3 (ngưỡng tần suất)
│   ├── experiments.py           # Thí nghiệm 1 & 4 (Item-Customer & nhóm túi)
│   ├── build_artifact.py        # Xuất artifact phục vụ API
│   ├── final_test.py            # Chạy test độc lập với chốt chặn
│   └── error_analysis.py        # Phân tích lỗi theo nhóm
├── tests/                       # Bộ kiểm thử tự động pytest
├── Dockerfile                   # Cấu hình container hóa ứng dụng
├── pytest.ini                   # Cấu hình kiểm thử
├── requirements.txt             # Danh sách thư viện phụ thuộc (UTF-8)
└── README.md                    # Tài liệu hướng dẫn chính của dự án
```