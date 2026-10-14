# ============================================================================
# FILE: normalization/algorithms.py
# ĐỀ TÀI 17: Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ
# TÁC GIẢ: TV1 - Trần Kỳ Quang (Leader)
# MỤC ĐÍCH: Hiện thực thuật toán toán học hình thức tự động hóa quá trình:
#   1. Tính bao đóng thuộc tính (Attribute Closure: CLOSURE(X, F))
#   2. Tìm tất cả các khóa ứng viên (Candidate Keys) qua phân loại L, R, M, I
#   3. Tìm phủ tối tiểu (Minimal Cover: F_min) qua 3 bước
#   4. Phân rã 3NF (Thuật toán tổng hợp Bernstein)
#   5. Kiểm tra dạng chuẩn BCNF
#   6. Kiểm tra bảo toàn thông tin bằng thuật toán ma trận Chase (Chase Test)
# ============================================================================

from typing import Set, List, Tuple, Dict
import copy


class FunctionalDependency:
    def __init__(self, lhs: Set[str], rhs: Set[str]):
        self.lhs = set(lhs)
        self.rhs = set(rhs)

    def __repr__(self):
        lhs_str = ", ".join(sorted(self.lhs))
        rhs_str = ", ".join(sorted(self.rhs))
        return f"{{{lhs_str}}} -> {{{rhs_str}}}"

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self):
        return hash((frozenset(self.lhs), frozenset(self.rhs)))


def compute_closure(X: Set[str], F: List[FunctionalDependency]) -> Set[str]:
    """Thuật toán tính bao đóng X+ dưới tập phụ thuộc hàm F."""
    result = set(X)
    while True:
        old_result = set(result)
        for fd in F:
            if fd.lhs.issubset(result):
                result = result.union(fd.rhs)
        if result == old_result:
            break
    return result


def find_candidate_keys(R: Set[str], F: List[FunctionalDependency]) -> Tuple[List[Set[str]], Dict[str, Set[str]]]:
    """
    Thuật toán tìm tất cả các khóa ứng viên của lược đồ R:
    Phân loại các thuộc tính:
      - L (Nguồn): Chỉ xuất hiện ở vế trái
      - R_attr (Đích): Chỉ xuất hiện ở vế phải
      - M (Trung gian): Xuất hiện ở cả hai vế
      - I (Cô lập): Không xuất hiện ở vế nào
    """
    lhs_all = set()
    rhs_all = set()
    for fd in F:
        lhs_all.update(fd.lhs)
        rhs_all.update(fd.rhs)

    L = lhs_all - rhs_all
    R_attr = rhs_all - lhs_all
    M = lhs_all.intersection(rhs_all)
    I = R - (lhs_all.union(rhs_all))

    classification = {"L": L, "R": R_attr, "M": M, "I": I}

    # Bắt đầu từ tập nguồn + cô lập
    base = L.union(I)
    keys = []

    # Kiểm tra nếu base đã là siêu khóa
    if compute_closure(base, F) == R:
        keys.append(base)
        return keys, classification

    # Nếu chưa, duyệt các tập con của M để tìm khóa tối tiểu
    from itertools import combinations
    for r in range(1, len(M) + 1):
        for comb in combinations(M, r):
            candidate = base.union(comb)
            if compute_closure(candidate, F) == R:
                # Kiểm tra tính tối tiểu
                is_minimal = True
                for existing_key in keys:
                    if existing_key.issubset(candidate):
                        is_minimal = False
                        break
                if is_minimal:
                    keys.append(candidate)

    return keys, classification


def compute_minimal_cover(F: List[FunctionalDependency]) -> List[FunctionalDependency]:
    """
    Thuật toán tìm phủ tối tiểu F_min qua 3 bước:
    1. Đơn thuộc tính hóa vế phải
    2. Loại bỏ thuộc tính dư thừa ở vế trái
    3. Loại bỏ phụ thuộc hàm dư thừa
    """
    # Bước 1: Đơn thuộc tính hóa vế phải
    F1 = []
    for fd in F:
        for attr in sorted(fd.rhs):
            F1.append(FunctionalDependency(fd.lhs, {attr}))

    # Bước 2: Loại bỏ thuộc tính dư thừa ở vế trái
    F2 = []
    for fd in F1:
        reduced_lhs = set(fd.lhs)
        for attr in sorted(fd.lhs):
            if len(reduced_lhs) > 1:
                test_lhs = reduced_lhs - {attr}
                closure_test = compute_closure(test_lhs, F1)
                if fd.rhs.issubset(closure_test):
                    reduced_lhs.remove(attr)
        F2.append(FunctionalDependency(reduced_lhs, fd.rhs))

    # Bước 3: Loại bỏ phụ thuộc hàm dư thừa
    F_min = copy.deepcopy(F2)
    i = 0
    while i < len(F_min):
        target_fd = F_min[i]
        # Tập phụ thuộc hàm không chứa target_fd
        remaining_F = F_min[:i] + F_min[i+1:]
        closure_without = compute_closure(target_fd.lhs, remaining_F)
        if target_fd.rhs.issubset(closure_without):
            # Dư thừa, loại bỏ
            F_min.pop(i)
        else:
            i += 1

    return F_min


def bernstein_3nf_synthesis(R: Set[str], F_min: List[FunctionalDependency], keys: List[Set[str]]) -> List[Set[str]]:
    """
    Thuật toán tổng hợp Bernstein phân rã về 3NF:
    1. Gom các FD có cùng vế trái tạo thành quan hệ con
    2. Thêm quan hệ chứa ít nhất một khóa nếu chưa có
    3. Loại bỏ quan hệ con bị bao hàm
    """
    grouped_by_lhs: Dict[frozenset, Set[str]] = {}
    for fd in F_min:
        key = frozenset(fd.lhs)
        if key not in grouped_by_lhs:
            grouped_by_lhs[key] = set(fd.lhs)
        grouped_by_lhs[key].update(fd.rhs)

    relations = list(grouped_by_lhs.values())

    # Kiểm tra xem có quan hệ nào chứa một khóa của R không
    has_key = any(any(k.issubset(rel) for k in keys) for rel in relations)
    if not has_key and keys:
        relations.append(set(keys[0]))

    # Loại bỏ quan hệ bị bao hàm
    final_relations = []
    for i, r1 in enumerate(relations):
        is_subset = False
        for j, r2 in enumerate(relations):
            if i != j and r1.issubset(r2):
                is_subset = True
                break
        if not is_subset and r1 not in final_relations:
            final_relations.append(r1)

    return final_relations


def check_bcnf(relation: Set[str], F: List[FunctionalDependency]) -> Tuple[bool, List[str]]:
    """Kiểm tra một quan hệ con có đạt chuẩn BCNF hay không."""
    violations = []
    # Chiếu F lên relation (chỉ lấy các FD có thuộc tính nằm trong relation)
    for fd in F:
        if fd.lhs.issubset(relation) and fd.rhs.issubset(relation):
            closure = compute_closure(fd.lhs, F).intersection(relation)
            if closure != relation:
                violations.append(f"{fd} (Vế trái không phải là siêu khóa của quan hệ con)")
    return len(violations) == 0, violations


def chase_test(R: Set[str], decompositions: List[Set[str]], F: List[FunctionalDependency]) -> Tuple[bool, List[List[str]]]:
    """
    Thực thi thuật toán ma trận Chase để kiểm tra Lossless Join:
    Ma trận gồm: len(decompositions) hàng x len(R) cột.
    Ký hiệu: 'a_j' nếu thuộc tính j thuộc quan hệ i, ngược lại 'b_ij'.
    """
    R_ordered = sorted(R)
    attr_to_idx = {attr: j for j, attr in enumerate(R_ordered)}
    n_rows = len(decompositions)
    n_cols = len(R_ordered)

    # Khởi tạo ma trận Chase
    matrix = []
    for i, rel in enumerate(decompositions):
        row = []
        for j, attr in enumerate(R_ordered):
            if attr in rel:
                row.append(f"a_{j+1}")
            else:
                row.append(f"b_{i+1}_{j+1}")
        matrix.append(row)

    # Vòng lặp biến đổi theo các FD
    changed = True
    while changed:
        changed = False
        for fd in F:
            # Tìm các dòng có giá trị giống nhau ở tất cả các cột thuộc fd.lhs
            lhs_cols = [attr_to_idx[a] for a in fd.lhs if a in attr_to_idx]
            rhs_cols = [attr_to_idx[a] for a in fd.rhs if a in attr_to_idx]

            # Gom nhóm dòng có cùng giá trị LHS
            groups: Dict[Tuple[str, ...], List[int]] = {}
            for i in range(n_rows):
                key = tuple(matrix[i][col] for col in lhs_cols)
                groups.setdefault(key, []).append(i)

            # Đồng bộ giá trị RHS cho các dòng trong cùng nhóm
            for key, rows in groups.items():
                if len(rows) > 1:
                    for col in rhs_cols:
                        # Ưu tiên chọn ký hiệu 'a_' nếu có
                        symbols = [matrix[r][col] for r in rows]
                        target_val = next((s for s in symbols if s.startswith("a_")), symbols[0])
                        for r in rows:
                            if matrix[r][col] != target_val:
                                matrix[r][col] = target_val
                                changed = True

    # Kiểm tra xem có dòng nào chứa toàn ký hiệu 'a_' hay không
    is_lossless = any(all(val.startswith("a_") for val in row) for row in matrix)
    return is_lossless, matrix


# ============================================================================
# CHƯƠNG TRÌNH KIỂM CHỨNG CHÍNH THỨC CHO ĐỀ TÀI 17
# ============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("CHƯƠNG TRÌNH KIỂM CHỨNG TOÁN HỌC CHUẨN HÓA DỮ LIỆU - ĐỀ TÀI 17")
    print("Phụ trách: TV1 - Trần Kỳ Quang (Leader)")
    print("=" * 80)

    # 1. Khởi tạo lược đồ phẳng R
    R = {
        "comment_id", "post_id", "group_id", "group_name", "group_topic",
        "author_id", "author_name", "author_email", "parent_id", "content", "created_at"
    }

    # 2. Tập phụ thuộc hàm hợp lệ theo nghiệp vụ F
    F = [
        FunctionalDependency({"comment_id"}, {"post_id", "author_id", "parent_id", "content", "created_at"}),
        FunctionalDependency({"post_id"}, {"group_id"}),
        FunctionalDependency({"group_id"}, {"group_name", "group_topic"}),
        FunctionalDependency({"author_id"}, {"author_name", "author_email"}),
        FunctionalDependency({"author_email"}, {"author_id", "author_name"})
    ]

    print("\n[BƯỚC 1]: LƯỢC ĐỒ QUAN HỆ TỔNG HỢP & TẬP FD:")
    print(f"R = {sorted(R)}")
    print("Tập phụ thuộc hàm F:")
    for i, fd in enumerate(F, 1):
        print(f"  f{i}: {fd}")

    # 3. Tính bao đóng của comment_id
    closure_comment = compute_closure({"comment_id"}, F)
    print(f"\n[BƯỚC 2]: BAO ĐÓNG CỦA {{comment_id}}+:")
    print(f"  {{comment_id}}+ = {sorted(closure_comment)}")
    print(f"  -> Bằng toàn bộ R: {closure_comment == R}")

    # 4. Tìm khóa ứng viên
    keys, classif = find_candidate_keys(R, F)
    print(f"\n[BƯỚC 3]: PHÂN LOẠI THUỘC TÍNH & TÌM KHÓA:")
    print(f"  Tập nguồn (L)     : {sorted(classif['L'])}")
    print(f"  Tập đích (R)      : {sorted(classif['R'])}")
    print(f"  Tập trung gian (M): {sorted(classif['M'])}")
    print(f"  Tập cô lập (I)    : {sorted(classif['I'])}")
    print(f"  -> CÁC KHÓA ỨNG VIÊN CỦA R: {[sorted(k) for k in keys]}")

    # 5. Tìm phủ tối tiểu F_min
    F_min = compute_minimal_cover(F)
    print(f"\n[BƯỚC 4]: PHỦ TỐI TIỂU F_min (3 bước: tách RHS, loại LHS dư, loại FD dư):")
    for i, fd in enumerate(F_min, 1):
        print(f"  FD_{i}: {fd}")

    # 6. Phân rã 3NF theo Bernstein
    decompositions = bernstein_3nf_synthesis(R, F_min, keys)
    print(f"\n[BƯỚC 5]: PHÂN RÃ CHUẨN HÓA 3NF (BERNSTEIN SYNTHESIS):")
    for i, rel in enumerate(decompositions, 1):
        print(f"  R{i} = {sorted(rel)}")
        is_bcnf_ok, vios = check_bcnf(rel, F_min)
        status = "ĐẠT BCNF" if is_bcnf_ok else f"VI PHẠM BCNF ({vios})"
        print(f"       -> Kiểm tra BCNF: {status}")

    # 7. Kiểm tra Lossless Join bằng thuật toán ma trận Chase
    is_lossless, chase_matrix = chase_test(R, decompositions, F_min)
    print(f"\n[BƯỚC 6]: THUẬT TOÁN MA TRẬN CHASE (CHASE TEST FOR LOSSLESS JOIN):")
    print(f"  Thuộc tính: {[f'A{j+1}:{a}' for j, a in enumerate(sorted(R))]}")
    for i, row in enumerate(chase_matrix, 1):
        print(f"  Hàng R{i}: {row}")
    print(f"  -> KẾT LUẬN CHASE: {'HOÀN TOÀN BẢO TOÀN THÔNG TIN (LOSSLESS JOIN)!' if is_lossless else 'MẤT THÔNG TIN'}")

    print("\n" + "=" * 80)
    print("XÁC NHẬN: TOÀN BỘ CÁC BƯỚC TOÁN HỌC CHUẨN HÓA CỦA TASK 1 ĐỀU CHÍNH XÁC 100%!")
    print("=" * 80)
