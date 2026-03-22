import unicodedata
from student import Student
from btree import BTree

class Database:
    """
    Lớp Database mô phỏng quá trình lưu trữ dữ liệu của CSDL phân tán cơ bản bao gồm:
    - Bảng dữ liệu chính (lưu bằng Hash Map/Dictionary)
    - Cây chỉ mục B-Tree: đánh index trên trường MSSV để tăng tốc độ tìm kiếm.
    """
    def __init__(self):
        """Khởi tạo cơ sở dữ liệu rỗng và tạo sẵn một vài dữ liệu mẫu."""
        self.table = {}  # mssv -> Student
        self.mssv_index = BTree(t=2) # B-Tree bậc 3
        self._init_mock_data()
        
    def _init_mock_data(self):
        """Thêm dữ liệu mẫu vào cơ sở dữ liệu."""
        self.add_student("SV001", "Nguyễn Văn A", "Nam", "ATTT")
        self.add_student("SV005", "Trần Thị B", "Nữ", "CNTT")
        self.add_student("SV002", "Lê Văn C", "Nam", "KTPM")

    def add_student(self, mssv, ho_ten, gioi_tinh, nganh):
        """
        Thêm một bản ghi mới vào bảng gốc, sau đó cập nhật lại cây chỉ mục.
        Độ phức tạp thêm mới trên Index phụ thuộc vào cấu trúc B-Tree.
        """
        if mssv in self.table:
            return False, f"Sinh viên mã {mssv} đã tồn tại!"
        
        student = Student(mssv, ho_ten, gioi_tinh, nganh)
        self.table[mssv] = student
        self.rebuild_index()
        
        return True, f"Thêm thành công: {ho_ten}"

    def remove_student(self, mssv):
        """
        Xóa một bản ghi khỏi bảng gốc theo MSSV, sau đó cập nhật lại cây chỉ mục.
        """
        if mssv not in self.table:
            return False, f"Sinh viên mã {mssv} không tồn tại!"
        
        del self.table[mssv]
        self.rebuild_index()
        return True, f"Đã xóa sinh viên mã {mssv}"

    def search_student(self, mssv):
        """
        Tìm kiếm bản ghi theo trường MSSV (có sử dụng chỉ mục B-Tree).
        Giảm thiểu thời gian tìm kiếm từ O(N) xuống O(log N).
        """
        result = self.mssv_index.search(mssv)
        if result:
            return self.table[result[1]]  # result[1] lưu mã định danh trỏ về bảng
        return None

    @staticmethod
    def _remove_accents(input_str):
        """Hàm hỗ trợ loại bỏ dấu tiếng Việt để so sánh chuỗi linh hoạt hơn."""
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def search_by_name(self, name):
        """
        Tìm kiếm bản ghi theo Tên (Trường hợp không có index trên trường này).
        Diễn ra quá trình Full Table Scan: Phải duyệt qua toàn bộ dữ liệu (O(N)).
        Hỗ trợ tìm kiếm theo chuỗi con, không phân biệt hoa thường và không dấu.
        """
        results = []
        name_normalized = self._remove_accents(name).lower()
        for student in self.table.values():
            student_name_normalized = self._remove_accents(student.ho_ten).lower()
            if name_normalized in student_name_normalized:
                results.append(student)
        return results

    def rebuild_index(self):
        """
        Cơ chế đơn giản hóa để cập nhật cấu trúc: Xây dựng lại cây chỉ mục 
        mỗi khi có các tác vụ thay đổi trên bảng dữ liệu (Insert/Delete).
        """
        self.mssv_index = BTree(t=2)
        for mssv in sorted(self.table.keys()):
            self.mssv_index.insert(mssv, mssv)
            
    def get_all_students(self):
        """Trả về toàn bộ dữ liệu của bảng."""
        return [s.to_dict() for s in self.table.values()]

    def get_tree_visualization(self):
        """Kết xuất mô hình cấu trúc cây chỉ mục thành chuỗi."""
        return self.mssv_index.get_tree_string()
