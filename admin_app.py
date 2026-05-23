import streamlit as st
import os
from bus import ThitotNghiepBUS

# Cấu hình UI
st.set_page_config(page_title="Hệ Thống Ôn Thi Đa Môn Vào 10 TP.HCM 😎", layout="wide")

# Thiết lập thư mục lưu tệp ảnh vật lý trong project
IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Khởi tạo Session State quản lý câu hỏi
if "current_q" not in st.session_state: st.session_state.current_q = None
if "show_ans" not in st.session_state: st.session_state.show_ans = False
if "show_info" not in st.session_state: st.session_state.show_info = False
if "seq_index" not in st.session_state: st.session_state.seq_index = 0

# --- SIDEBAR ĐIỀU HƯỚNG MÔ-ĐUN ---
st.sidebar.title("HỆ THỐNG VÀO 10 🚀")
chuc_nang = st.sidebar.radio("CHỌN PHÂN HỆ VẬN HÀNH:", ["👨‍🎓 HỌC SINH LUYỆN THI", "😎 QUẢN LÝ NGÂN HÀNG ĐỀ"])

DANH_SACH_MON = ["Toán HCM","Toán", "Tiếng Anh", "Ngữ Văn"]

# =====================================================================
# PHÂN HỆ 1: INTERFACE DÀNH CHO HỌC SINH LUYỆN ĐỀ
# =====================================================================
if chuc_nang == "👨‍🎓 HỌC SINH LUYỆN THI":
    st.title("🎯 PHÒNG TỰ LUYỆN THI VÀO 10 ĐA MÔN CHẤT LƯỢNG CAO")
    
    c_m1, c_m2, c_m3, c_m4, c_m5 = st.columns([1.5, 1.5, 1.2, 1.2, 1.2])
    with c_m1:
        mon_var = st.selectbox("📚 Chọn Môn Học:", DANH_SACH_MON)
    
    cac_chu_de_sẵn_co = ThitotNghiepBUS.lay_danh_sach_chu_de(mon_var)
    
    with c_m2:
        if cac_chu_de_sẵn_co:
            topic_var = st.selectbox("📌 Chọn Chủ Đề:", cac_chu_de_sẵn_co)
        else:
            st.info("Chưa có chủ đề!")
            topic_var = None
            
    with c_m3:
        mode_var = st.checkbox("Chế độ ngẫu nhiên (Random)", value=False)
        
    with c_m4:
        if not mode_var and topic_var:
            cac_muc_do_sẵn_co = ThitotNghiepBUS.lay_danh_sach_muc_do(mon_var, topic_var)
            level_var = st.selectbox("📊 Chọn Mức Độ:", cac_muc_do_sẵn_co if cac_muc_do_sẵn_co else ["Mặc định"])
            filtered_questions = ThitotNghiepBUS.loc_cau_hoi_hoc_sinh(mon_var, topic_var, level_var)
        else:
            level_var = None
            filtered_questions = ThitotNghiepBUS.loc_cau_hoi_hoc_sinh(mon_var, topic_var) if topic_var else []

    with c_m5:
        st.write("") 
        st.write("")
        if st.button("🔄 ĐỔI CÂU HỎI MỚI", use_container_width=True):
            if not filtered_questions:
                st.warning("Không tìm thấy câu nào khớp bộ lọc!")
                st.session_state.current_q = None
            else:
                next_q, next_index = ThitotNghiepBUS.boc_cau_hoi_moi(
                    filtered_questions, st.session_state.current_q, mode_var, st.session_state.seq_index
                )
                st.session_state.current_q = next_q
                st.session_state.seq_index = next_index
                st.session_state.show_ans = False
                st.session_state.show_info = False
                st.rerun()

    st.write("---")
    
    if st.session_state.current_q:
        q = st.session_state.current_q
        
        # Chống lệch bộ lọc khi đổi cấu hình Selectbox đột ngột
        if topic_var and q[2] != topic_var:
            st.session_state.current_q = filtered_questions[0] if filtered_questions else None
            q = st.session_state.current_q

        if q:
            st.subheader(f"📝 Đề bài môn {q[1]} ({q[3]} - Mức độ: {q[4]}):")
            st.info(q[5]) # Đề bài chữ
            
            # 🖼️ LOAD ẢNH ĐỀ BÀI (Đọc động trực tiếp từ cột số 13 - anh_de_bai)
            if q[13] and os.path.exists(str(q[13])):
                st.image(q[13], caption="Hình ảnh đồ thị / Sơ đồ kèm theo đề bài", width=500)
                
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("👁️ XEM ĐÁP ÁN & LỜI GIẢI CHI TIẾT", use_container_width=True):
                    st.session_state.show_ans = not st.session_state.show_ans
            with col_btn2:
                if st.button("🧠 XEM PHÂN TÍCH ĐÁNH GIÁ CHUYÊN SÂU", use_container_width=True):
                    st.session_state.show_info = not st.session_state.show_info
                    
            if st.session_state.show_ans:
                st.write("### 🔑 ĐÁP ÁN GỌN:")
                st.success(q[6])
                st.write("### 📝 LỜI GIẢI CHI TIẾT VÀ BÀI MẪU:")
                st.markdown(q[7])
                
                # 🖼️ LOAD ẢNH LỜI GIẢI (Đọc động trực tiếp từ cột số 14 - anh_loi_giai)
                if q[14] and os.path.exists(str(q[14])):
                    st.image(q[14], caption="Sơ đồ phân tích / Hình vẽ minh họa bài giải", width=550)
                
            if st.session_state.show_info:
                st.write("---")
                st.subheader("📊 PHÂN TÍCH KHOA HỌC TỪ THẦY CÔ CHUYÊN GIA:")
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    # Các trường text trả về đúng nhiệm vụ lưu text gốc của nó
                    st.markdown(f"**🎯 Mục tiêu kiểm tra:** {q[8]}")
                    st.markdown(f"**💎 Bản chất tư duy:** {q[9]}")
                    st.markdown(f"**📚 Kiến thức nền tảng:** {q[10]}")
                with col_i2:
                    st.markdown(f"**⚠️ Lỗi sai / Bẫy học sinh cần né:** {q[11]}")
                    st.error(f"**💡 Khẩu quyết vàng ra điểm:** {q[12]}")
    else:
        st.write("💡 *Mời thầy chọn môn học, chủ đề và nhấn **'🔄 ĐỔI CÂU HỎI MỚI'** để bắt đầu thi thử.*")

# =====================================================================
# PHÂN HỆ 2: FORM ADMIN BIÊN SOẠN & CẬP NHẬT DATABASE
# =====================================================================
else:
    st.title("🎛️ TRUNG TÂM ĐIỀU HÀNH NGÂN HÀNG ĐỀ THI")
    all_data = ThitotNghiepBUS.lay_danh_sach_gốc()
    
    col_grid, col_form = st.columns([2, 3])
    
    with col_grid:
        st.header("📋 Hệ Thống Quét Dữ Liệu")
        search_keyword = st.text_input("🔍 Lọc nhanh theo từ khóa:", placeholder="Nhập tên môn, tên chủ đề...")
        
        if search_keyword:
            display_data = [q for q in all_data if search_keyword.lower() in str(q).lower()]
        else:
            display_data = all_data
            
        if display_data:
            list_options = {f"[{q[1]}] ID {q[0]} | Chủ đề: {q[2]} | Dạng: {q[3]}": q for q in display_data}
            selected_option = st.radio("Chọn bản ghi để cập nhật hệ thống:", list(list_options.keys()))
            active_q = list_options[selected_option]
        else:
            st.warning("Không tìm thấy bản ghi nào!")
            active_q = None

    with col_form:
        st.header("📝 Trình Biên Soạn Đa Năng (Chuẩn 15 Cột)")
        che_do = st.radio("Trạng thái Form thao tác:", ["Thêm Câu Hỏi Mới", "Chỉnh Sửa Câu Đang Chọn"], horizontal=True)
        
        def_val = {i: "" for i in range(15)} # Khởi tạo mảng đệm 15 trường dữ liệu rỗng
        if che_do == "Chỉnh Sửa Câu Đang Chọn" and active_q:
            def_val = {i: active_q[i] for i in range(15)}
            
        c_f1, c_f2, c_f3, c_f4 = st.columns(4)
        with c_f1:
            try: idx_mon = DANH_SACH_MON.index(def_val[1])
            except: idx_mon = 0
            chu_de_mon_hoc = st.selectbox("MÔN HỌC", DANH_SACH_MON, index=idx_mon)
        with c_f2:
            chu_de = st.text_input("CHỦ ĐỀ", value=def_val[2])
        with c_f3:
            dang_bai = st.text_input("DẠNG BÀI", value=def_val[3])
        with c_f4:
            muc_do = st.text_input("MỨC ĐỘ", value=def_val[4])
            
        noi_dung = st.text_area("NỘI DUNG ĐỀ BÀI CHÍNH (CHỮ)", value=def_val[5], height=120)
        dap_an = st.text_input("ĐÁP ÁN GỌN", value=def_val[6])
        loi_giai = st.text_area("LỜI GIẢI CHI TIẾT HOẶC BÀI VĂN MẪU", value=def_val[7], height=120)
        
        # --- KHU VỰC BỐ TRÍ FORM UPLOAD ẢNH ĐỘC LẬP ---
        st.write("🖼️ **HÌNH ẢNH MINH HỌA (Lưu vào cột chuyên biệt trong DB):**")
        col_img1, col_img2 = st.columns(2)
        
        # Mặc định lấy giá trị cũ từ DB (cột 13 và 14) nếu không upload file mới
        path_anh_de_bai = def_val[13]
        path_anh_loi_giai = def_val[14]
        
        with col_img1:
            if def_val[13]: st.caption(f"Đường dẫn ảnh đề hiện tại: `{def_val[13]}`")
            uploaded_file_de = st.file_uploader("Chọn ảnh cho ĐỀ BÀI (.png, .jpg)", type=["png", "jpg", "jpeg"], key="up_de")
            if uploaded_file_de is not None:
                path_anh_de_bai = os.path.join(IMAGE_DIR, f"de_{chu_de_mon_hoc}_{uploaded_file_de.name}")
                with open(path_anh_de_bai, "wb") as f:
                    f.write(uploaded_file_de.getbuffer())
                st.success("✓ Đã nhận ảnh đề bài!")
                
        with col_img2:
            if def_val[14]: st.caption(f"Đường dẫn ảnh giải hiện tại: `{def_val[14]}`")
            uploaded_file_giai = st.file_uploader("Chọn ảnh cho LỜI GIẢI (.png, .jpg)", type=["png", "jpg", "jpeg"], key="up_giai")
            if uploaded_file_giai is not None:
                path_anh_loi_giai = os.path.join(IMAGE_DIR, f"giai_{chu_de_mon_hoc}_{uploaded_file_giai.name}")
                with open(path_anh_loi_giai, "wb") as f:
                    f.write(uploaded_file_giai.getbuffer())
                st.success("✓ Đã nhận ảnh lời giải!")

        st.write("---")
        muc_tieu = st.text_input("MỤC TIÊU KIỂM TRA (CHỮ)", value=def_val[8])
        ban_chat = st.text_input("BẢN CHẤT TƯ DUY (CHỮ)", value=def_val[9])
        kien_thuc_nen = st.text_input("KIẾN THỨC NỀN CẦN LƯU Ý", value=def_val[10])
        bay_thuong_gap = st.text_input("BẪY THƯỜNG GẶP", value=def_val[11])
        khau_quyet = st.text_input("KHẨU QUYẾT BẢN CHẤT 😎", value=def_val[12])
        
        # Đóng gói cấu trúc mảng tham số chuẩn 14 phần tử để đẩy vào hàm SQL
        form_data = (
            chu_de_mon_hoc, chu_de, dang_bai, muc_do, noi_dung, 
            dap_an, loi_giai, muc_tieu, ban_chat, kien_thuc_nen, 
            bay_thuong_gap, khau_quyet, path_anh_de_bai, path_anh_loi_giai
        )
        
        st.write("")
        if che_do == "Thêm Câu Hỏi Mới":
            if st.button("➕ XÁC NHẬN THÊM VÀO NGÂN HÀNG ĐỀ", type="primary", use_container_width=True):
                if noi_dung.strip() == "":
                    st.error("Yêu cầu nhập nội dung đề bài!")
                else:
                    ThitotNghiepBUS.them_cau_hoi(form_data)
                    st.success("Đã nạp câu hỏi đa môn mới thành công vào Database! 😎")
                    st.rerun()
                    
        elif che_do == "Chỉnh Sửa Câu Đang Chọn" and active_q:
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("💾 CẬP NHẬT BIẾN ĐỘNG", type="primary", use_container_width=True):
                    ThitotNghiepBUS.sua_cau_hoi(active_q[0], form_data)
                    st.success(f"Cập nhật thành công câu hỏi ID {active_q[0]}!")
                    st.rerun()
            with c_btn2:
                if st.button("🗑️ XÓA VĨNH VIỄN KHỎI HỆ THỐNG", type="secondary", use_container_width=True):
                    ThitotNghiepBUS.xoa_cau_hoi(active_q[0])
                    st.warning(f"Đã xóa vĩnh viễn câu hỏi ID {active_q[0]}!")
                    st.rerun()
