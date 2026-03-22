class Student:
    """Lớp đại diện cho một Sinh viên trong hệ thống."""
    
    def __init__(self, mssv, ho_ten, gioi_tinh, nganh):
        """Khởi tạo đối tượng sinh viên với các thuộc tính cơ bản."""
        self.mssv = mssv
        self.ho_ten = ho_ten
        self.gioi_tinh = gioi_tinh
        self.nganh = nganh

    def to_dict(self):
        """Chuyển đổi đối tượng sinh viên thành dictionary lưu trữ dữ liệu."""
        return {
            "MSSV": self.mssv,
            "Họ Tên": self.ho_ten,
            "Giới tính": self.gioi_tinh,
            "Ngành": self.nganh
        }

    def __repr__(self):
        """Hiển thị chuỗi đại diện cho đối tượng sinh viên."""
        return f"[{self.mssv}] {self.ho_ten} - {self.gioi_tinh} - {self.nganh}"
