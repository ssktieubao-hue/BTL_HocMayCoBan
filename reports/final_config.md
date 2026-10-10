# Cấu hình đóng băng trước khi đánh giá test
Ngày chốt: <điền ngày>

- Mô hình chính: cosine item–invoice, min_count = 1, không lọc nhóm G.
  Baseline: top sản phẩm bán chạy toàn cục.
- K báo cáo chính = 10; vẫn báo K = 5 và K = 20.
- Dữ liệu học cuối: train + validation. Không chọn lại tham số nào. Từ vựng sản phẩm và
  top 100 phổ biến tính từ train + validation.
- Ca đánh giá: hóa đơn test có ít nhất 2 sản phẩm khác nhau và ít nhất 1 sản phẩm đã thấy;
  món bị giấu chọn ngẫu nhiên trong các sản phẩm đã thấy, random_state = 42.
- Kết quả chính theo seed 42. Thêm trung bình, độ lệch chuẩn, nhỏ nhất, lớn nhất qua 20 seed
  (0 đến 19) của việc chọn món bị giấu.
- Tiêu chí kết luận (chốt trước): cosine "vượt" baseline nếu Hit-rate@10 của cosine trừ ci95
  vẫn lớn hơn Hit-rate@10 của baseline cộng ci95.
- Test chỉ chạy một lần bằng `python -m src.final_test`. Chạy lại bằng --force chỉ khi có lỗi
  kỹ thuật, và phải ghi lý do vào báo cáo.
- Phân tích lỗi chỉ để mô tả giới hạn. Không dùng nó để đổi mô hình hay cấu hình.