class BTreeNode:
    """Lớp biểu diễn một nút (Node) trong cây B-Tree."""
    def __init__(self, leaf=True):
        """Khởi tạo một nút."""
        self.leaf = leaf
        self.keys = []      # List chứa danh sách các tuple (khóa, đối_tượng_đích)
        self.children = []  # List trỏ tới các nút con (BTreeNode)

class BTree:
    """
    Cấu trúc dữ liệu B-Tree làm Chỉ mục (Index). 
    Mô phỏng cho Cây bậc 3 (2-3 Tree), số lượng Key tối đa tại một Nút là 2.
    """
    def __init__(self, t=2):
        self.root = BTreeNode(True)
        self.t = t  
        self.order = 3
        self.max_keys = self.order - 1

    def get_tree_string(self, node=None, level=0):
        """Hàm đệ quy trực quan hóa cây B-Tree sang định dạng chuỗi (String)."""
        if node is None:
            node = self.root
        
        keys = [k[0] for k in node.keys]
        result = "    " * level + str(keys) + "\n"
        
        for child in node.children:
            result += self.get_tree_string(child, level + 1)
            
        return result

    def search(self, key, node=None):
        """
        Tìm kiếm một key trong cây B-Tree.
        Trả về: Tuple (key, value) nếu tìm thấy, ngược lại trả về None.
        """
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1
        if i < len(node.keys) and key == node.keys[i][0]:
            return node.keys[i]
        elif node.leaf:
            return None
        else:
            return self.search(key, node.children[i])

    def insert(self, key, value):
        """
        Chèn một (key, value) mới vào cây B-Tree.
        Xử lý trường hợp nút gốc bị đầy (full).
        """
        root = self.root
        if len(root.keys) == self.max_keys:
            new_root = BTreeNode(False)
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(self.root, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _insert_non_full(self, node, key, value):
        """Hàm hỗ trợ: Chèn giá trị vào nút chưa bị điền đầy."""
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append((None, None))
            while i >= 0 and key < node.keys[i][0]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = (key, value)
        else:
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.max_keys:
                self.split_child(node, i)
                if key > node.keys[i][0]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def split_child(self, parent, index):
        """
        Hàm hỗ trợ: Tách một nút con đang bị đầy, đẩy phần tử ở giữa lên nút cha.
        Thích hợp cho thuật toán B-Tree nói chung và điều chỉnh đúng max_keys theo bậc của cây.
        """
        t_child = parent.children[index]
        new_node = BTreeNode(t_child.leaf)
        
        mid_idx = self.max_keys // 2
        up_key = t_child.keys[mid_idx]

        parent.keys.insert(index, up_key)
        
        new_node.keys = t_child.keys[mid_idx + 1:]
        if not t_child.leaf:
            new_node.children = t_child.children[mid_idx + 1:]
            
        t_child.keys = t_child.keys[:mid_idx]
        if not t_child.leaf:
            t_child.children = t_child.children[:mid_idx + 1]
            
        parent.children.insert(index + 1, new_node)
