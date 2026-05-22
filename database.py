import sqlite3

DB_NAME = "database.db"

def khoi_tao_db():
    """Khởi tạo cấu trúc bảng câu hỏi chuẩn 15 cột (tách riêng cột ảnh)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ngan_hang_de (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mon_hoc TEXT NOT NULL,
            chu_de TEXT,
            dang_bai TEXT,
            muc_do TEXT,
            noi_dung TEXT NOT NULL,
            dap_an TEXT,
            loi_giai TEXT,
            muc_tieu TEXT,
            ban_chat TEXT,
            kien_thuc_nen TEXT,
            bay_thuong_gap TEXT,
            khau_quyet TEXT,
            anh_de_bai TEXT,
            anh_loi_giai TEXT
        )
    """)
    conn.commit()
    conn.close()

def lay_toan_bo_cau_hoi():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ngan_hang_de ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def them_cau_hoi_db(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Thực thi nạp chuỗi dữ liệu gồm 14 tham số (không tính ID)
    cursor.execute("""
        INSERT INTO ngan_hang_de (
            mon_hoc, chu_de, dang_bai, muc_do, noi_dung, 
            dap_an, loi_giai, muc_tieu, ban_chat, kien_thuc_nen, 
            bay_thuong_gap, khau_quyet, anh_de_bai, anh_loi_giai
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def sua_cau_hoi_db(q_id, data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ngan_hang_de 
        SET mon_hoc=?, chu_de=?, dang_bai=?, muc_do=?, noi_dung=?, 
            dap_an=?, loi_giai=?, muc_tieu=?, ban_chat=?, kien_thuc_nen=?, 
            bay_thuong_gap=?, khau_quyet=?, anh_de_bai=?, anh_loi_giai=?
        WHERE id=?
    """, (*data, q_id))
    conn.commit()
    conn.close()

def xoa_cau_hoi_db(q_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ngan_hang_de WHERE id=?", (q_id,))
    conn.commit()
    conn.close()

# Tự động kích hoạt tạo bảng khi tầng Data được nạp
khoi_tao_db()