# BAO ĐÓNG, KHÓA, PHỦ TỐI TIỂU & PHÂN RÃ CHUẨN HÓA

> **Mục đích file:** Trình bày chi tiết các bước tính toán hình thức: thuật toán bao đóng thuộc tính, tìm tất cả các khóa, tìm phủ tối tiểu $F_{min}$, phân rã về 3NF/BCNF, kiểm tra tính bảo toàn thông tin (Lossless Join) và bảo toàn phụ thuộc hàm (Dependency Preservation).  
> **Người phụ trách:** TV1 (Review: TV3).

---

## 1. Thuật Toán Tìm Bao Đóng ($X^+$)

### [VÍ DỤ MẪU]
Xét tập thuộc tính $X = \{UserID\}$ với tập FD $F$:
1. Khởi tạo: $X^{(0)} = \{UserID\}$
2. Áp dụng $FD_1: UserID \rightarrow FullName, Email$:  
   $X^{(1)} = \{UserID, FullName, Email\}$
3. Không còn FD nào áp dụng thêm được.  
$\Rightarrow \{UserID\}^+ = \{UserID, FullName, Email\}$.

---

## 2. Tìm Khóa Ứng Viên (Candidate Keys)

- **Thuộc tính nguồn (chỉ xuất hiện ở vế trái):** $UserID$...
- **Thuộc tính trung gian (xuất hiện cả 2 vế):** $Email$...
- **Kết luận:** Khóa ứng viên cho quan hệ người dùng là $\{UserID\}$ và $\{Email\}$.

---

## 3. Thuật Toán Phủ Tối Tiểu (Minimal Cover - $F_{min}$)

Các bước thực hiện:
1. **Bước 1 (Đơn thuộc tính vế phải):** Tách các vế phải thành thuộc tính đơn (Ví dụ: $X \rightarrow YZ \Rightarrow X \rightarrow Y, X \rightarrow Z$).
2. **Bước 2 (Loại thuộc tính dư thừa ở vế trái):** Với mỗi $A \in X$ trong $X \rightarrow Y$, nếu $Y \in (X \setminus \{A\})^+$ thì thay $X \rightarrow Y$ bằng $(X \setminus \{A\}) \rightarrow Y$.
3. **Bước 3 (Loại phụ thuộc hàm dư thừa):** Với mỗi $f: X \rightarrow Y \in F$, nếu $Y \in X^+_{(F \setminus \{f\})}$ thì loại bỏ $f$.

*(TODO: TV1 viết chi tiết từng bước tính toán trên tập FD hoàn chỉnh của đề tài).*

---

## 4. Phân Rã Về 3NF (Thuật toán Tổng hợp Bernstein)

1. Tìm phủ tối tiểu $F_{min}$.
2. Với mỗi $X \rightarrow Y \in F_{min}$, tạo quan hệ $R_i = X \cup Y$.
3. Nếu chưa có quan hệ nào chứa một khóa của $R$, thêm quan hệ $R_k$ gồm các thuộc tính của một khóa.
4. Loại bỏ các quan hệ bị bao hàm trong quan hệ khác.

---

## 5. Kiểm Tra Dạng Chuẩn BCNF và Phân Rã BCNF

- **Định nghĩa BCNF:** Mọi phụ thuộc hàm không tầm thường $X \rightarrow Y$ đều có $X$ là siêu khóa (superkey).
- **Kiểm tra tính bảo toàn:**
  - Kiểm tra nối không mất thông tin (Lossless Join) bằng bảng ma trận/thuật toán kiểm tra.
  - Kiểm tra tính bảo toàn phụ thuộc hàm.
