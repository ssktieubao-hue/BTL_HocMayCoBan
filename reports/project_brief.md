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