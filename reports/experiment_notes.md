# Kết quả thí nghiệm 1 và 4 (validation, 5.424 ca, ci95 khoảng ±1,2 điểm phần trăm)

## Thí nghiệm 1: vector hóa đơn và vector khách hàng (K = 10)
| Mô hình | Hit-rate@10 | Coverage@10 | Tỷ lệ gợi ý hàng phổ biến |
|---|---|---|---|
| top bán chạy (baseline) | 4,8% | 0,6% | 100% |
| item–invoice | 25,5% | 43,5% | 44,2% |
| item–customer | 25,5% | 42,2% | 63,0% |
- Hai mô hình ngang nhau ở K = 10. Ở K = 20 item–customer cao hơn 1,5 điểm, ở mức ranh giới
  ci95, không kết luận.
- Item–customer thiên về hàng phổ biến hơn rõ (60% đến 64% so với 43% đến 45%).
- Chỉ 11/5.424 ca có món bị giấu ngoài danh mục của item–customer; việc thiếu 203 sản
  phẩm không giải thích chênh lệch.
- Quyết định: giữ item–invoice làm mô hình chính (theo luật đã chốt, và dùng được cho mọi
  hóa đơn kể cả hóa đơn thiếu Customer ID).

## Thí nghiệm 4: nhóm túi/phụ kiện quà phổ biến (G, 27 sản phẩm)
- G chiếm 0,6% danh mục, 6,5% sản phẩm trong giỏ thật, 22,1% gợi ý top 10.
- Khi món bị giấu thuộc G (403 ca): Hit-rate@10 = 66,8% (±4,6).
- Bỏ G khỏi gợi ý: Hit-rate@10 trên ca ngoài G tăng từ 22,2% lên 24,4% (vượt ci95), nhưng
  trên toàn bộ ca giảm từ 25,5% xuống khoảng 22,5%. Hệ quả cơ học: suất G luôn trượt khi
  món bị giấu ngoài G, nên phải so trên toàn bộ ca.
- Bỏ thêm G khỏi đầu vào: tăng thêm 0,2 đến 0,8 điểm, nhỏ hơn ci95, chưa thấy ảnh hưởng.
- Quyết định: không lọc G. Ghi nhận thiên lệch về nhóm túi như giới hạn của mô hình.
- Giới hạn: 25/27 sản phẩm trong G là túi (sản phẩm bán, không hẳn bao bì quà).