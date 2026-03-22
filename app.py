import streamlit as st
import pandas as pd
from database import Database

st.set_page_config(page_title="App Quản Lý Sinh Viên", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="InputInstructions"] {
        display: none !important;
    }
    
    div[data-testid="stTextInput"] input:disabled {
        -webkit-text-fill-color: white !important;
        color: white !important;
    }
    
    div[data-testid="stTextInput"]:has(input:disabled) {
        opacity: 1 !important; 
    }
    
    div[data-testid="stTextInput"]:has(input:disabled) label p,
    div[data-testid="stTextInput"]:has(input:disabled) div[data-testid="stWidgetLabel"] p {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "db" not in st.session_state:
    st.session_state.db = Database()

db = st.session_state.db

st.title("Hệ thống quản lý Sinh viên (B-Tree Index)")
st.markdown("App sử dụng B-Tree bậc 3 như chỉ mục cho Database")

col_left, col_right = st.columns([3, 2])
contain_left = col_left.container()

with col_right:
    st.subheader("Thêm sinh viên mới")
    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            mssv_col1, mssv_col2 = st.columns([1, 8])
            with mssv_col1:
                st.text_input("Mã SV", value="SV", disabled=True)
            with mssv_col2:
                mssv = st.text_input("Nhập phần sau", placeholder="Ví dụ: 001", label_visibility="hidden")
            ho_ten = st.text_input("Họ và Tên")
        with c2:
            gioi_tinh = st.selectbox("Giới tính", ["Nam", "Nữ", "Khác"])
            nganh = st.text_input("Ngành học")
            
        submitted = st.form_submit_button("Thêm Sinh Viên")
        if submitted:
            if mssv and ho_ten:
                mssv_normalized = "SV" + mssv.strip().upper()
                ho_ten_normalized = ho_ten.strip().title()
                
                success, msg = db.add_student(mssv_normalized, ho_ten_normalized, gioi_tinh, nganh.strip())
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Vui lòng nhập đầy đủ Mã SV và Họ Tên!")
                
    st.divider()
    
    st.subheader("Xóa sinh viên")
    with st.form("delete_form", clear_on_submit=True):
        del_col1, del_col2 = st.columns([1, 16])
        with del_col1:
            st.text_input("Mã SV", value="SV", disabled=True)
        with del_col2:
            del_mssv = st.text_input("Nhập Mã SV cần xóa", placeholder="Nhập phần số...", label_visibility="hidden")
            
        del_submitted = st.form_submit_button("Xóa Sinh Viên")
        if del_submitted:
            if del_mssv:
                del_mssv_normalized = "SV" + del_mssv.strip().upper()
                success, msg = db.remove_student(del_mssv_normalized)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Vui lòng nhập Mã SV!")

    st.divider()

    st.subheader("Tìm kiếm")
    search_type = st.radio("Tìm kiếm theo", ["Mã SV (Dùng Index)", "Họ Tên (Quét bảng gốc)"], horizontal=True)
    
    if "Mã SV" in search_type:
        search_col1, search_col2 = st.columns([1, 16])
        with search_col1:
            st.text_input("Mã SV", value="SV", disabled=True, label_visibility="collapsed")
        with search_col2:
            search_query = st.text_input("Nhập thông tin tìm kiếm", placeholder="Nhập phần số mã SV...", label_visibility="collapsed")
    else:
        search_query = st.text_input("Nhập thông tin tìm kiếm", placeholder="Nhập tên cần tìm...", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Tìm kiếm"):
        if search_query:
            search_query_normalized = search_query.strip()
            
            if "Mã SV" in search_type:
                search_query_normalized = "SV" + search_query_normalized.upper()
                res = db.search_student(search_query_normalized)
                if res:
                    st.write("**Đã tìm thấy 1 sinh viên:**")
                    st.json(res.to_dict())
                else:
                    st.write("**Không tìm thấy sinh viên nào.**")
            else:
                res = db.search_by_name(search_query_normalized)
                st.write(f"**Đã tìm thấy {len(res)} sinh viên:**")
                if res:
                    st.table(pd.DataFrame([s.to_dict() for s in res]))
        else:
            st.write("Vui lòng nhập thông tin tìm kiếm!")

with contain_left:
    st.subheader("Bảng dữ liệu gốc")
    students = db.get_all_students()
    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, width='stretch')
    else:
        st.write("Chưa có dữ liệu sinh viên.")
        
    st.subheader("Cây chỉ mục B-Tree")
    tree_vis = db.get_tree_visualization()
    st.code(tree_vis, language="text")
