# Kết quả đánh giá test (cấu hình đóng băng tại tag frozen-before-test)

Mô hình học trên train + validation (860.227 dòng, 33.589 hóa đơn). Test: 5.927 hóa đơn;
loại 414 hóa đơn chỉ có 1 sản phẩm và 52 hóa đơn không có món nào đã thấy; còn 5.461 ca.
4,8% cặp (hóa đơn, sản phẩm) ở test chứa sản phẩm chưa thấy khi học.

## Kết quả chính (seed 42; ± là ci95)
| K | Top bán chạy | Cosine item–invoice | Coverage (cosine) | Gợi ý hàng phổ biến (cosine) |
|---|---|---|---|---|
| 5 | 2,38% ±0,40 | 15,89% ±0,97 | 33,1% | 29,0% |
| 10 | 3,85% ±0,51 | 21,59% ±1,09 | 40,9% | 29,0% |
| 20 | 5,68% ±0,61 | 27,49% ±1,18 | 49,4% | 29,9% |

Theo tiêu chí đã chốt trước, cosine vượt baseline (20,50% > 4,36% ở K = 10).

## Biến thiên theo 20 seed chọn món bị giấu (Hit-rate)
| Mô hình | K | Trung bình | Độ lệch chuẩn | Nhỏ nhất | Lớn nhất |
|---|---|---|---|---|---|
| Cosine | 5 | 16,25% | 0,55 | 14,78% | 16,92% |
| Cosine | 10 | 21,43% | 0,57 | 19,79% | 22,38% |
| Cosine | 20 | 27,23% | 0,66 | 25,33% | 28,29% |
| Top bán chạy | 5 | 1,90% | 0,14 | 1,61% | 2,20% |
| Top bán chạy | 10 | 3,13% | 0,22 | 2,73% | 3,50% |
| Top bán chạy | 20 | 5,04% | 0,29 | 4,49% | 5,44% |
Seed 42 cho baseline cao hơn cả 20 seed này; theo trung bình, lợi thế của cosine lớn hơn
con số chính (khoảng 6,8 lần thay vì 5,6 lần ở K = 10).

## So với validation (K = 10)
Cosine 25,52% → 21,59%; baseline 4,78% → 3,85%; tỷ lệ cosine/baseline 5,3 → 5,6 lần.
Hai bộ ca khác thời kỳ, từ vựng và dữ liệu học nên không quy mức giảm cho riêng mô hình.
Chỉ số gợi ý hàng phổ biến giảm từ 44% xuống 29% nhưng top 100 được tính lại trên dữ liệu
lớn hơn, nên không so sánh trực tiếp.

## Phân tích lỗi (Hit-rate@10)
- Theo độ phổ biến của món bị giấu: nhóm từ 500 hóa đơn đạt 32,0% (n = 2.251), các nhóm còn
  lại 11,6% đến 15,9%; khoảng 61% lượt trúng đến từ nhóm từ 500 hóa đơn (nhóm này chiếm 41%
  số ca). Baseline chỉ trúng ở nhóm này (9,3%).
- Theo kích thước giỏ: 33,1% (2–5 món), 30,2% (6–15), 16,3% (16–40), 9,2% (trên 40).
  Baseline 3,4% đến 4,5% ở mọi nhóm. Giỏ từ 16 món trở lên chiếm 55% số ca.
- Theo tháng: 21,1% đến 21,4% từ tháng 10 đến 12; tháng 9 (330 ca) là 26,7% ±4,8.
- Trúng/trượt: cosine thắng 1.062 ca, baseline thắng 93 ca, cả hai trúng 117, cả hai trượt
  4.189. Có 45 ca cosine không gợi ý được, tính là trượt.
- Ví dụ định tính: các ca trúng thường là biến thể cùng dòng sản phẩm; các ca trượt ở giỏ
  rất lớn thường nhận gợi ý chung chung theo mùa. Đây là giả thuyết, chưa kiểm chứng.

## Giới hạn
Hit-rate chỉ đo một món bị giấu, các gợi ý hợp lý khác bị tính là trượt. Dữ liệu chủ yếu của
khách UK (92,6%), test chỉ gồm khoảng 10 tuần cuối năm 2011 nên không khái quát cho năm
khác. Chưa đo đa dạng của danh sách gợi ý. Hơn một nửa số ca là giỏ từ 16 món trở lên, nơi
mô hình yếu nhất. Mô hình không giải quyết sản phẩm mới (cold-start).
