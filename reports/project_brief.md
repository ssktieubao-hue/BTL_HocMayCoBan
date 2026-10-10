# Project brief
- Câu hỏi: vector hóa đơn/khách hàng + cosine có gợi ý mua kèm hợp lý không?
- Đơn vị quan sát: một sản phẩm (StockCode). Vector chính: các hóa đơn đã chứa sản phẩm đó (nhị phân).
  So sánh với vector khách hàng.
- Làm sạch: bỏ hóa đơn hủy, Quantity<=0, Price<=0, StockCode không phải sản phẩm, thiếu Description.
- Chia dữ liệu: theo hóa đơn, theo thời gian, 70/15/15. Chốt từ ngày <hôm nay>, không đổi sau khi xem test.
- Đánh giá: với mỗi hóa đơn test có >= 2 sản phẩm, giấu ngẫu nhiên 1 sản phẩm (random_state=42),
  dùng phần còn lại để gợi ý Top-K; trúng nếu sản phẩm bị giấu nằm trong Top-K (Hit-rate@K).
  Ngoài ra báo coverage và tỷ lệ gợi ý hàng phổ biến.
- Baseline: top sản phẩm bán chạy toàn cục, đếm trên train.
- Chọn K, ngưỡng tần suất, mô hình: chỉ dựa trên validation. Test dùng một lần để báo cáo cuối.
- Hàng phổ biến = 100 sản phẩm bán chạy nhất trong train; K thử ở 5, 10, 20; baseline là top bán chạy toàn cục. 
- Hàng phổ biến = 100 sản phẩm bán chạy nhất trong train. K thử ở 5, 10, 20.
- Điểm gợi ý cho một giỏ = tổng cosine giữa sản phẩm ứng viên và từng món trong giỏ.
- Quy tắc chọn ngưỡng tần suất (chốt trước khi xem kết quả): chọn ngưỡng có Hit-rate@10 cao
  nhất trên validation; nếu hai ngưỡng chênh nhau trong khoảng ci95 thì chọn ngưỡng nhỏ hơn
  (coverage cao hơn, mô hình đơn giản hơn).

  ## Quyết định sau thí nghiệm vòng 1 (validation, 5.424 ca)
- Cosine item–invoice vượt baseline ở mọi K (Hit-rate@10: 25,5% so với 4,8%).
- Hit-rate@10 giữa các ngưỡng chênh tối đa 0,9 điểm phần trăm, nằm trong ci95 (±1,2),
  nên theo quy tắc đã chốt chọn min_count = 1 (không lọc).
- K báo cáo chính = 10; vẫn báo cáo K = 5 và 20. API mặc định k = 10.
- Giới hạn: pop_share của cosine còn khoảng 44%, nên ở phân tích lỗi cần tách kết quả theo
  độ phổ biến của món bị giấu.

  ## Thí nghiệm 1 và 4 (chốt trước khi xem kết quả)
- Thí nghiệm 1: item–customer học từ các dòng có Customer ID, min_count = 1. So sánh với
  item–invoice trên cùng bộ ca đánh giá; báo thêm kết quả trên tập con ca có món bị giấu
  nằm trong danh mục của mô hình khách. Giữ item–invoice làm mô hình chính nếu
  Hit-rate@10 của item–customer không cao hơn quá ci95; ngược lại phải giải thích hoặc đổi
  mô hình chính.
- Thí nghiệm 4: nhóm G = sản phẩm trong top 100 bán chạy của train có mô tả chứa BAG,
  SHOPPER, WRAP, GIFT, RIBBON hoặc TISSUE (27 sản phẩm, danh sách ở
  reports/gift_items.csv; sửa số này nếu bạn đổi từ khóa). Đo: tỷ lệ G trong danh mục, giỏ
  thật và gợi ý; Hit-rate theo món bị giấu thuộc/không thuộc G; bỏ G khỏi gợi ý và bỏ G khỏi
  cả đầu vào, so trên cùng tập ca có món bị giấu ngoài G. Chênh lệch nhỏ hơn ci95 thì kết
  luận "chưa thấy ảnh hưởng".