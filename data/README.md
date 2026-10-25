# Dữ liệu: Online Retail II

## 1. Nguồn dữ liệu
- **Tên tập dữ liệu**: Online Retail II
- **Trang dữ liệu**: [UCI Machine Learning Repository: Online Retail II](https://archive.ics.uci.edu/dataset/502/online%2Bretail)
- **DOI**: [10.24432/C5CG6D](https://doi.org/10.24432/C5CG6D)
- **Giấy phép**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Tệp gốc sử dụng**: `online_retail_II.xlsx` (2 sheet: 2009-2010 và 2010-2011)
- **SHA256**: `BCBE73B35F5B7BABF197FB0CB983A11F5D9FF929078D4AA53D171B1F2DF2E980`

## 2. Trích dẫn
```bibtex
@misc{chen2019onlineretail2,
  author       = {Chen, Daqing},
  title        = {{Online Retail II}},
  year         = {2019},
  howpublished = {UCI Machine Learning Repository},
  doi          = {10.24432/C5CG6D}
}
```

## 3. Cách tái tạo dữ liệu
Chạy script tự động tải dữ liệu từ UCI và gộp sheet:
```bash
python -m src.data
```
Script sẽ tải file nén zip, giải nén vào `data/raw/` và xuất thành `data/raw/online_retail_II.csv`.
Thư mục `data/raw/` và `data/processed/` được bỏ qua bởi Git theo chuẩn quản lý dữ liệu lớn.

## 4. Từ điển dữ liệu (Data Dictionary)
| Cột | Kiểu | Ý nghĩa | Vai trò trong mô hình | Thời điểm có sẵn |
|---|---|---|---|---|
| `Invoice` | Chuỗi | Mã số hóa đơn (bắt đầu bằng `C` là đơn hủy) | ID giỏ hàng, đơn vị phân chia tập | Khi đặt hàng |
| `StockCode` | Chuỗi | Mã sản phẩm | ID sản phẩm (khóa quan sát chính) | Khi đặt hàng |
| `Description` | Chuỗi | Tên mô tả sản phẩm | Hiển thị trên giao diện | Khi đặt hàng |
| `Quantity` | Số nguyên | Số lượng mua (âm là đơn hủy/trả) | Lọc bản ghi hợp lệ (`Quantity > 0`) | Khi đặt hàng |
| `InvoiceDate` | Ngày giờ | Thời điểm phát sinh hóa đơn | Phân chia thời gian (Time-based split) | Khi đặt hàng |
| `Price` | Số thực | Đơn giá sản phẩm (GBP) | Lọc bản ghi hợp lệ (`Price > 0`) | Khi đặt hàng |
| `Customer ID` | Chuỗi | Mã định danh khách hàng (có giá trị thiếu) | Thí nghiệm so sánh; ẩn hoàn toàn trên UI | Khi đặt hàng |
| `Country` | Chuỗi | Quốc gia đăng ký của khách hàng | Phân tích phân bổ khu vực | Khi đặt hàng |
