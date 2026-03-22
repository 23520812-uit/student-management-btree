# Ứng Dụng Quản Lý Sinh Viên với B-Tree Index

# Quản Lý Sinh Viên B-Tree Indexing

Dự án ứng dụng Web cơ bản sử dụng **Streamlit** mô phỏng hệ thống quản lý sinh viên với cấu trúc dữ liệu B-Tree (bậc 3) làm chỉ mục (index). Dự án giúp trực quan hóa cơ chế lưu trữ và tìm kiếm trên cơ sở dữ liệu dựa vào Index.

## Tính năng nổi bật
- **Thêm/Xóa Sinh viên**: Thao tác cập nhật dữ liệu tự động đồng bộ.
- **Phân loại Tìm kiếm**:
  - Dùng _Index (Mã SV)_: Sử dụng tính chất của B-Tree ($O(\log N)$).
  - Dùng _Quét Bảng (Họ Tên)_: Quét toàn bộ dữ liệu (Full Table Scan - $O(N)$).
- **Trực quan hóa**: Màn hình hiển thị liên tục sự biến đổi của cấu trúc Cây B-Tree và Bảng Data.

## Cấu trúc thư mục

```text
├── btree.py           # Core logic mô phỏng thuật toán B-Tree (Order 3)
├── student.py         # Kiểu dữ liệu tương đương với 1 record
├── database.py        # Controller quản lý thao tác CSDL, Mapping Bảng và Index
├── app.py             # File khởi chạy giao diện Web Streamlit
├── requirements.txt   # Các dependency để deploy hoặc cài bằng Pip
├── environment.yml    # Định nghĩa cấu hình môi trường chuẩn cho Conda
├── README.md         
└── .gitignore
```

## Cài đặt và Chạy ở Local

Dự án có thể chạy bằng Virtual Environment thông thường qua `pip` hoặc dùng `conda`.

### Sử dụng Conda (Khuyên dùng)
```bash
conda env create -f environment.yml
conda activate cs523
streamlit run app.py
```

### Sử dụng Pip
```bash
pip install -r requirements.txt
streamlit run app.py
```

Mặc định, ứng dụng sẽ chạy tại địa chỉ `http://localhost:8501`.
