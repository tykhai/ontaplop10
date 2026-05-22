import random
import database as db

class ThitotNghiepBUS:
    @staticmethod
    def lay_danh_sach_gốc():
        return db.lay_toan_bo_cau_hoi()

    @staticmethod
    def lay_danh_sach_chu_de(mon_hoc):
        all_data = db.lay_toan_bo_cau_hoi()
        chu_de_set = set([q[2] for q in all_data if q[1] == mon_hoc and q[2]])
        return sorted(list(chu_de_set))

    @staticmethod
    def lay_danh_sach_muc_do(mon_hoc, chu_de):
        all_data = db.lay_toan_bo_cau_hoi()
        muc_do_set = set([q[4] for q in all_data if q[1] == mon_hoc and q[2] == chu_de and q[4]])
        return sorted(list(muc_do_set))

    @staticmethod
    def loc_cau_hoi_hoc_sinh(mon_hoc, chu_de, muc_do=None):
        all_data = db.lay_toan_bo_cau_hoi()
        filtered = [q for q in all_data if q[1] == mon_hoc and q[2] == chu_de]
        if muc_do:
            filtered = [q for q in filtered if q[4] == muc_do]
        return filtered

    @staticmethod
    def boc_cau_hoi_moi(filtered_questions, current_q, is_random, seq_index):
        if not filtered_questions:
            return None, 0
            
        if is_random:
            if len(filtered_questions) > 1 and current_q in filtered_questions:
                pool = [q for q in filtered_questions if q[0] != current_q[0]]
            else:
                pool = filtered_questions
            return random.choice(pool), seq_index
        else:
            new_index = seq_index + 1
            if new_index >= len(filtered_questions):
                new_index = 0
            return filtered_questions[new_index], new_index

    @staticmethod
    def them_cau_hoi(data):
        db.them_cau_hoi_db(data)

    @staticmethod
    def sua_cau_hoi(q_id, data):
        db.sua_cau_hoi_db(q_id, data)

    @staticmethod
    def xoa_cau_hoi(q_id):
        db.xoa_cau_hoi_db(q_id)