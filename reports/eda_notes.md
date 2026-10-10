# Ghi chú EDA và quyết định tiền xử lý

Nguồn: notebooks/01_eda.ipynb. EDA chỉ dùng tập train (709.013 dòng, 27.662 hóa đơn,
4.426 sản phẩm, 2009-12-01 đến 2011-05-26). Riêng mục 7 dùng thêm val để đo sản phẩm
chưa thấy. Không dùng test.

## 1. Kích thước giỏ hàng
- Quan sát: trung vị 15 sản phẩm/hóa đơn, trung bình 24,3, 75% hóa đơn có tối đa 28
  sản phẩm, lớn nhất 673. Phân phối lệch phải mạnh. 8,5% hóa đơn chỉ có 1 sản phẩm
  (reports/figures/eda_basket_size.png).
- Quyết định: chỉ đánh giá trên hóa đơn có ít nhất 2 sản phẩm khác nhau (cần 1 món làm
  đầu vào và 1 món bị giấu). Hóa đơn 1 sản phẩm vẫn giữ trong train.
- Rủi ro ghi nhận: giỏ rất lớn (có thể là đơn bán sỉ) tạo nhiều cặp đồng xuất hiện.
  Chưa cắt bỏ; kiểm tra lại ở phân tích lỗi theo kích thước giỏ.

## 2. Tần suất sản phẩm (đuôi dài)
- Quan sát: mỗi sản phẩm xuất hiện trung vị 63 hóa đơn (trung bình 151,7; lớn nhất
  4.261). 25% sản phẩm xuất hiện không quá 17 hóa đơn
  (reports/figures/eda_item_frequency.png).

| Ngưỡng tần suất tối thiểu | Số sản phẩm giữ (trên 4.426) | Tỷ lệ cặp (hóa đơn, sản phẩm) giữ |
|---|---|---|
| 2 | 4.280 | 100,0% |
| 5 | 4.018 | 99,9% |
| 10 | 3.704 | 99,5% |
| 20 | 3.235 | 98,5% |
| 50 | 2.451 | 94,7% |

- Nhận xét: ngưỡng 50 bỏ khoảng 45% số sản phẩm nhưng chỉ mất 5,3% số cặp.
- Quyết định (thí nghiệm 3): khảo sát ngưỡng {không lọc, 5, 10, 20, 50}. Tần suất chỉ
  đếm trên train, chọn ngưỡng bằng validation. Sản phẩm bị lọc sẽ không được gợi ý nên
  coverage giảm; báo cáo cả hai mặt này.

## 3. Sản phẩm phổ biến và tên hiển thị
- Quan sát: sản phẩm số 1 (85123A, WHITE HANGING HEART T-LIGHT HOLDER) có trong 15,4%
  hóa đơn; mọi sản phẩm trong top 20 có mặt ở ít nhất 5,3% hóa đơn. Trong top 20 có 7
  loại túi (JUMBO BAG, LUNCH BAG, JUMBO SHOPPER, JUMBO STORAGE BAG) và 3 loại CAKE CASES.
- Quyết định:
  - Baseline top bán chạy sẽ khá mạnh, nên so sánh với cosine phải cùng split và cùng
    đơn vị đánh giá (thí nghiệm 2).
  - Thí nghiệm 4: nhóm sản phẩm đóng gói/quà phổ biến = sản phẩm trong top 100 bán chạy của
    train có mô tả chứa BAG, SHOPPER, WRAP, GIFT, RIBBON hoặc TISSUE (danh sách ở
    reports/gift_items.csv). CAKE CASES và PAPER NAPKINS là vật tư làm bánh/tiệc nên không
    tính vào nhóm này; BOX bị bỏ vì khớp cả sản phẩm thông thường.
  - Giả thuyết cần kiểm tra ở phân tích lỗi: nhiều sản phẩm là biến thể cùng dòng (ví dụ
    JUMBO BAG đỏ và hồng), nên cosine có thể gợi ý các biến thể na ná nhau.
- 516 trên 4.426 mã (11,7%) có hơn một mô tả. Hiển thị bằng mô tả xuất hiện nhiều nhất
  trong train; mô hình dùng StockCode làm khóa nên không bị ảnh hưởng.

## 4. Customer ID
- Quan sát: 22,6% dòng thiếu Customer ID nhưng chỉ 8,1% hóa đơn không có (91,9% hóa đơn
  có), nghĩa là hóa đơn thiếu mã khách thường có nhiều dòng hơn mức trung bình. Có 4.900
  khách. Nếu chỉ dùng dòng có khách còn 4.223 trên 4.426 sản phẩm.
- Quyết định (thí nghiệm 1):
  - Vector item–invoice dùng mọi hóa đơn; vector item–customer chỉ dùng dòng có
    Customer ID.
  - Hai mô hình đánh giá trên cùng tập (giỏ, món bị giấu). Giỏ đầu vào không cần
    Customer ID.
  - Báo cáo coverage riêng cho item–customer vì 203 sản phẩm không có vector.
  - Customer ID là mã định danh khách, không hiển thị trên web/API.

## 5. Quốc gia
- Quan sát: United Kingdom 92,6%, EIRE 1,7%, Germany 1,5%, France 1,2%, Netherlands 0,5%.
- Quyết định: dùng mô hình và baseline toàn cục, không tách theo quốc gia vì các thị
  trường khác quá ít dữ liệu. Kết luận chủ yếu đúng cho khách tại UK; ghi ở phần giới hạn.

## 6. Mùa vụ theo thời gian
- Quan sát: số hóa đơn/tháng thường nằm quanh 1.400 đến 1.600, thấp nhất tháng 1–2
  (khoảng 1.050 đến 1.100) và đạt đỉnh khoảng 2.700 vào tháng 11/2010
  (reports/figures/eda_monthly_invoices.png). Tháng 5/2011 chưa đủ vì train dừng ở 26/5.
- Hệ quả:
  - Test (26/9 đến 9/12/2011) rơi vào mùa cao điểm cuối năm, trong khi train chỉ có một
    mùa như vậy (quý 4 năm 2010).
  - Val (26/5 đến 26/9/2011) là giai đoạn thấp điểm, không đại diện cho test về mùa vụ
    nên tham số chọn trên val có thể lệch.
- Quyết định: giữ nguyên split đã đóng băng. Ghi vào giới hạn của kết luận và phân tích
  lỗi trên test theo từng tháng.

## 7. Sản phẩm chưa thấy ở train (dùng val)
- Quan sát: 10,3% cặp (hóa đơn, sản phẩm) ở val chứa sản phẩm chưa từng xuất hiện ở train.
- Quyết định: bài toán không giải cold-start. Món bị giấu chỉ chọn trong số sản phẩm đã
  có ở train, chọn cố định một lần (random_state=42) và dùng chung cho mọi mô hình và mọi
  ngưỡng. Nếu để món bị giấu phụ thuộc vào ngưỡng tần suất thì mẫu số mỗi mô hình sẽ khác
  nhau và so sánh không công bằng. Báo cáo kèm tỷ lệ giỏ bị loại vì lý do này.

## Giới hạn đã biết
Dữ liệu chủ yếu của khách UK (92,6%); lệch mùa giữa val và test; không xử lý sản phẩm
mới (cold-start); 22,6% dòng thiếu Customer ID; một số giỏ rất lớn.

  - Thí nghiệm 4: nhóm sản phẩm đóng gói/quà phổ biến = sản phẩm trong top 100 bán chạy của
    train có mô tả chứa BAG, SHOPPER, WRAP, GIFT, RIBBON hoặc TISSUE (danh sách ở
    reports/gift_items.csv). CAKE CASES và PAPER NAPKINS là vật tư làm bánh/tiệc nên không
    tính vào nhóm này; BOX bị bỏ vì khớp cả sản phẩm thông thường.