# Dữ liệu: Online Retail II

## Nguồn
- Tên: Online Retail II
- Trang dữ liệu: https://archive.ics.uci.edu/dataset/502/online%2Bretail
- DOI: https://doi.org/10.24432/C5CG6D
- Giấy phép: CC BY 4.0 (được dùng, bắt buộc ghi nguồn)
- Ngày tải: 2026-10-10
- Tệp sử dụng: online_retail_II.xlsx (2 sheet: 2009-2010 và 2010-2011)
- SHA256: <BCBE73B35F5B7BABF197FB0CB983A11F5D9FF929078D4AA53D171B1F2DF2E980>

## Trích dẫn
Chen, D. (2019). Online Retail II [Dataset]. UCI Machine Learning Repository.
https://doi.org/10.24432/C5CG6D
(Bạn đối chiếu lại mục "Cite" trên trang UCI để chép đúng tác giả và năm.)

## Cách tái tạo
    python src/data.py
Script tải file zip, giải nén vào data/raw/ và gộp 2 sheet thành online_retail_II.csv.
Thư mục data/raw/ không được đưa vào Git.

## Data dictionary
| Biến | Kiểu | Ý nghĩa | Vai trò | Có sẵn khi nào |
|---|---|---|---|---|
| Invoice | chuỗi | Mã hóa đơn; bắt đầu bằng "C" là đơn hủy | ID giỏ hàng | Khi đặt hàng |
| StockCode | chuỗi | Mã sản phẩm | ID item | Khi đặt hàng |
| Description | chuỗi | Tên sản phẩm | Chỉ hiển thị | Khi đặt hàng |
| Quantity | số nguyên | Số lượng mua (âm = hủy/trả) | Dùng để lọc | Khi đặt hàng |
| InvoiceDate | datetime | Thời điểm lập hóa đơn | Dùng để chia theo thời gian | Khi đặt hàng |
| Price | số thực | Đơn giá (GBP) | Dùng để lọc | Khi đặt hàng |
| Customer ID | số | Mã khách hàng (có thiếu) | ID khách (vector item–customer); phải ẩn trên giao diện | Khi đặt hàng |
| Country | chuỗi | Quốc gia của khách | Phụ (phần mở rộng) | Khi đặt hàng |

Dự án này không có biến target theo nghĩa thường. Với mỗi giỏ hàng, ta giữ lại một
mặt hàng làm nhãn để đo Hit-rate@K.

## Báo cáo chất lượng
Sẽ bổ sung ở Bước 3 (missing, trùng lặp, ngoại lệ, các dòng bị loại kèm lý do).