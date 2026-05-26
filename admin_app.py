import streamlit as st
import os
import re
from bus import ThitotNghiepBUS

# =====================================================================
# 1. CẤU HÌNH HỆ THỐNG & GIAO DIỆN CHUYÊN NGHIỆP
# =====================================================================
st.set_page_config(page_title="Hệ Thống Ôn Thi Đa Môn Vào 10 TP.HCM 😎", layout="wide")

# CSS Custom nâng cấp trải nghiệm thị giác, xử lý triệt để bài toán dính chữ câu a, b, c
st.markdown("""
<style>
    /* Bo góc và làm mịn các khối nút bấm */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    /* Khung hiển thị đề bài dạng Card cao cấp */
    .question-card {
        background-color: #f8f9fa;
        border-left: 5px solid #4A90E2;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .question-text {
        font-size: 1.15rem !important;
        line-height: 1.6 !important;
        color: #1E293B !important;
        font-weight: 500;
    }
    /* Định dạng nhãn thông tin nhỏ gọn (Badges) */
    .badge-subject {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-right: 8px;
    }
    .badge-level {
        background-color: #FEF3C7;
        color: #D97706;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
    }
    /* Khung lời giải chi tiết cao cấp */
    .solution-card {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Hàm bổ trợ: Tự động phát hiện câu a,b,c,d hoặc A,B,C,D dính liền để tự ngắt dòng
def format_text_breaks(text):
    if not text:
        return ""
    # Thay thế và chèn dấu xuống dòng trước các mục phụ: a), b), c), d), A., B., C., D. hoặc dấu gạch đầu dòng
    # Nếu trước đó đã có dấu xuống dòng rồi thì không chèn thêm tránh bị hở quá xa
    text = str(text)
    # Bẻ dòng trước a), b), c), d)
    text = re.sub(r'(?<!\n)(?=\b[a-d]\))', r'\n', text)
    # Bẻ dòng trước A., B., C., D. câu trắc nghiệm
    text = re.sub(r'(?<!\n)(?=\b[A-D]\.)', r'\n', text)
    # Bẻ dòng trước dấu gạch đầu dòng hoặc dấu cộng đầu dòng phân đoạn
    text = re.sub(r'(?<!\n)(?= - )', r'\n', text)
    return text

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

DANH_SACH_MON = ["Toán HCM", "Toán Học", "Tiếng Anh", "Ngữ Văn"]


# =====================================================================
# PHÂN HỆ 1: INTERFACE DÀNH CHO HỌC SINH LUYỆN ĐỀ (TỐI ƯU TOÀN DIỆN)
# =====================================================================
if chuc_nang == "👨‍🎓 HỌC SINH LUYỆN THI":
    st.title("🎯 PHÒNG TỰ LUYỆN THI VÀO 10 ĐA MÔN CHẤT LƯỢNG CAO")
    
    # Khu vực bộ lọc thiết kế tinh gọn thanh thoát
    c_m1, c_m2, c_m3, c_m4, c_m5 = st.columns([1.5, 1.5, 1.2, 1.2, 1.5])
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
        st.write("") 
        st.write("")
        mode_var = st.checkbox("🔄 Ngẫu nhiên (Random)", value=False)
        
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
        if st.button("🔥 ĐỔI CÂU HỎI MỚI", use_container_width=True, type="primary"):
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
        
        if topic_var and q[2] != topic_var:
            st.session_state.current_q = filtered_questions[0] if filtered_questions else None
            q = st.session_state.current_q

        if q:
            # Header nhãn thông tin câu hỏi
            st.markdown(
                f'<span class="badge-subject">📚 {q[1]}</span>'
                f'<span class="badge-level">📊 Mức độ: {q[4]}</span>'
                f' <small style="color:#64748B;">| Chủ đề: {q[2]} - Dạng bài: {q[3]}</small>', 
                unsafe_allow_html=True
            )
            st.write("")

            # Cơ chế Split-Screen UI: Tự động chia đôi khi xem đáp án để đối chiếu trực quan
            if st.session_state.show_ans:
                col_left, col_right = st.columns([5, 5], gap="large")
            else:
                col_left, col_right = st.columns([10, 1])

            # -----------------------------------------------------------------
            # CỘT TRÁI: KHU VỰC ĐỀ BÀI (Xử lý bẻ dòng tự động cho câu a, b, c)
            # -----------------------------------------------------------------
            with col_left:
                st.markdown("### 📝 ĐỀ BÀI CHÍNH:")
                
                # Thực hiện format chèn xuống dòng tự động cho text đề bài
                formatted_question_text = format_text_breaks(q[5])
                
                st.markdown(
                    f'<div class="question-card">'
                    f'<p class="question-text" style="white-space: pre-line; margin-bottom: 0;">{formatted_question_text}</p>'
                    f'</div>', 
                    unsafe_allow_html=True
                )
                
                # SỬA LỖI WARNING: Đổi use_container_width=True thành width='stretch'
                path_de = str(q[13]).strip() if q[13] else ""
                if path_de and path_de != "" and os.path.exists(path_de):
                    st.image(path_de, caption="Hình vẽ / Đồ thị minh họa kèm theo đề", width='stretch')
                
                st.write("")
                # Điều hướng tương tác dưới đề bài
                c_b1, c_b2 = st.columns(2)
                with c_b1:
                    if st.button("👁️ XEM ĐÁP ÁN & LỜI GIẢI CHI TIẾT", use_container_width=True, type="secondary" if st.session_state.show_ans else "primary"):
                        st.session_state.show_ans = not st.session_state.show_ans
                        st.rerun()
                with c_b2:
                    if st.button("🧠 PHÂN TÍCH TƯ DUY CHUYÊN SÂU", use_container_width=True):
                        st.session_state.show_info = not st.session_state.show_info
                        st.rerun()

            # -----------------------------------------------------------------
            # CỘT PHẢI: KHU VỰC LỜI GIẢI CHI TIẾT (Tự động tách dòng bước giải)
            # -----------------------------------------------------------------
            if st.session_state.show_ans:
                with col_right:
                    st.markdown("### 🔑 ĐÁP ÁN & LỜI GIẢI:")
                    
                    # Kết quả nhanh dạng Badge nổi bật nhẹ
                    st.markdown(
                        f'<div style="background-color: #DCFCE7; color: #166534; padding: 10px 15px; border-radius: 6px; font-weight: bold; margin-bottom: 15px;">'
                        f'🎯 Kết quả nhanh: {q[6]}'
                        f'</div>', 
                        unsafe_allow_html=True
                    )
                    
                    # Thực hiện format chèn xuống dòng tự động cho phần lời giải dài ngoằn
                    formatted_solution_text = format_text_breaks(q[7])
                    
                    st.markdown(
                        f'<div class="solution-card" style="white-space: pre-line; line-height: 1.7; color: #0F172A; font-size: 1.05rem;">'
                        f'{formatted_solution_text}'
                        f'</div>', 
                        unsafe_allow_html=True
                    )
                    
                    # SỬA LỖI WARNING: Đổi use_container_width=True thành width='stretch'
                    path_giai = str(q[14]).strip() if q[14] else ""
                    if path_giai and path_giai != "" and os.path.exists(path_giai):
                        st.write("")
                        st.image(path_giai, caption="Sơ đồ / Hình vẽ minh họa bài giải", width='stretch')

            # 3. Khu vực phân tích tư duy học thuật từ chuyên gia (Nằm tràn dòng phía dưới cùng)
            if st.session_state.show_info:
                st.write("---")
                st.subheader("📊 PHÂN TÍCH KHOA HỌC TỪ THẦY CÔ CHUYÊN GIA")
                col_i1, col_i2 = st.columns(2, gap="medium")
                with col_i1:
                    st.info(f"**🎯 Mục tiêu kiểm tra:** {q[8]}\n\n**💎 Bản chất tư duy:** {q[9]}\n\n**📚 Kiến thức nền tảng:** {q[10]}")
                with col_i2:
                    st.warning(f"**⚠️ Lỗi sai / Bẫy dễ sập:** {q[11]}")
                    st.error(f"**💡 Khẩu quyết vàng hạ gục bài toán:** {q[12]}")
    else:
        st.write("💡 *Mời thầy chọn môn học, chủ đề và nhấn **'🔥 ĐỔI CÂU HỎI MỚI'** để bắt đầu thi thử.*")


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
        
        def_val = {i: "" for i in range(15)} 
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
        
        st.write("🖼️ **HÌNH ẢNH MINH HỌA (Lưu vào cột chuyên biệt trong DB):**")
        col_img1, col_img2 = st.columns(2)
        
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