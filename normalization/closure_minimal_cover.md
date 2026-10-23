# BAO ĐÓNG, KHÓA, PHỦ TỐI TIỂU & PHÂN RÃ CHUẨN HÓA

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Người phụ trách:** TV1 - Trần Quang (Leader)  
> **Review:** TV3 (Hữu - Đối chiếu schema.sql)  
> **Nội dung:** Trình bày chi tiết các bước tính toán toán học: Thuật toán bao đóng thuộc tính, Tìm tất cả khóa ứng viên, Phủ tối tiểu F_min, Phân rã 3NF theo Bernstein, Kiểm tra BCNF, Chứng minh Lossless Join (Bảng Chase) & Bảo toàn phụ thuộc hàm, và Phân tích Phi chuẩn hóa có kiểm soát.

---

## 1. THUẬT TOÁN TÌM BAO ĐÓNG THUỘC TÍNH (X+)

### 1.1 Định nghĩa và Giả mã thuật toán
Cho lược đồ quan hệ `R`, tập phụ thuộc hàm `F`, và tập thuộc tính `X ⊆ R`. Bao đóng của `X` dưới tập `F`, ký hiệu là `X+` (hoặc `X⁺`), là tập hợp tất cả các thuộc tính `A ∈ R` sao cho phụ thuộc hàm `X → A` được suy dẫn logic từ `F` thông qua hệ luật dẫn Armstrong (Phản xạ, Tăng trưởng, Bắc cầu).

**Mã giả thuật toán CLOSURE(X, F):**
```text
Thuật toán: CLOSURE(X, F)
Đầu vào: Tập thuộc tính X, tập phụ thuộc hàm F
Đầu ra: Bao đóng X+

Bước 1: result := X;
Bước 2: repeat
            old_result := result;
            for each (Y → Z) in F do
                if Y ⊆ result then
                    result := result ∪ Z;
        until (result = old_result);
Bước 3: return result;
```

---

### 1.2 Thực thi tính toán bao đóng trên hệ thống Đề tài 17
Xét lược đồ tổng hợp phẳng:
```text
R = { comment_id, post_id, group_id, group_name, group_topic, author_id, author_name, author_email, parent_id, content, created_at }
```

Tập phụ thuộc hàm nghiệp vụ `F`:
- `f1: comment_id → post_id, author_id, parent_id, content, created_at`
- `f2: post_id → group_id`
- `f3: group_id → group_name, group_topic`
- `f4: author_id → author_name, author_email`
- `f5: author_email → author_id, author_name`

#### Ví dụ 1: Tính bao đóng của {comment_id}+
1. Khởi tạo: `result(0) = { comment_id }`
2. Vòng lặp 1:
   - Xét `f1`: `{ comment_id } ⊆ result(0)` ⇒ `result(1) = { comment_id, post_id, author_id, parent_id, content, created_at }`
   - Xét `f2`: `{ post_id } ⊆ result(1)` ⇒ `result(2) = result(1) ∪ { group_id }`
   - Xét `f3`: `{ group_id } ⊆ result(2)` ⇒ `result(3) = result(2) ∪ { group_name, group_topic }`
   - Xét `f4`: `{ author_id } ⊆ result(3)` ⇒ `result(4) = result(3) ∪ { author_name, author_email }`
3. Vòng lặp 2: Không thể bổ sung thêm thuộc tính nào mới ⇒ Thuật toán dừng.
4. **Kết quả:**  
   `{ comment_id }+ = R`  
   Vì bao đóng của `{ comment_id }` chứa toàn bộ thuộc tính của lược đồ `R`, nên `{ comment_id }` là một **siêu khóa (Superkey)** của `R`.

#### Ví dụ 2: Tính bao đóng của {post_id}+
- `result(0) = { post_id }`
- Áp dụng `f2` ⇒ `result(1) = { post_id, group_id }`
- Áp dụng `f3` ⇒ `result(2) = { post_id, group_id, group_name, group_topic }`
- Không áp dụng thêm được FD nào khác.
- **Kết quả:**  
  `{ post_id }+ = { post_id, group_id, group_name, group_topic } ≠ R`

#### Ví dụ 3: Tính bao đóng của {author_id}+ và {author_email}+
- `{ author_id }+ = { author_id, author_name, author_email }`
- `{ author_email }+ = { author_email, author_id, author_name }`

#### Ứng dụng: Kiểm tra phụ thuộc hàm được suy dẫn logic
- Hỏi: `comment_id → group_name` có thuộc `F+` hay không?  
  *Trả lời:* Ta thấy `group_name ∈ { comment_id }+`. Do đó, `comment_id → group_name ∈ F+` (suy dẫn qua tính chất bắc cầu: `comment_id → post_id → group_id → group_name`).
- Hỏi: `group_name → comment_id` có thuộc `F+` không?  
  *Trả lời:* `{ group_name }+ = { group_name }`. Vì `comment_id ∉ { group_name }+` nên `group_name → comment_id ∉ F+`.

---

## 2. THUẬT TOÁN TÌM TẤT CẢ CÁC KHÓA ỨNG VIÊN (CANDIDATE KEYS)

Để tìm tất cả các khóa ứng viên của lược đồ `R` một cách chặt chẽ theo giáo trình chuẩn (Elmasri & Navathe), ta tiến hành phân loại tập thuộc tính của `R` dựa trên sự xuất hiện ở vế trái và vế phải của các FD trong `F`:

1. **Tập nguồn (L - Thuộc tính chỉ xuất hiện ở vế trái):**  
   `L = { comment_id }`  
   *(Thuộc tính này không xuất hiện ở bất kỳ vế phải của FD nào, do đó bắt buộc phải có mặt trong mọi khóa ứng viên của R).*

2. **Tập đích (R_attr - Thuộc tính chỉ xuất hiện ở vế phải):**  
   `R_attr = { parent_id, content, created_at, group_topic }`  
   *(Các thuộc tính này không thể suy ra thuộc tính khác và luôn được xác định bởi thuộc tính khác, nên không bao giờ thuộc về một khóa tối tiểu nào).*

3. **Tập trung gian (M - Thuộc tính xuất hiện ở cả hai vế trái và phải):**  
   `M = { post_id, group_id, group_name, author_id, author_name, author_email }`

4. **Tập cô lập (I - Thuộc tính không xuất hiện ở cả hai vế):**  
   `I = ∅ (tập rỗng)`

### Xác định khóa:
- Ta lấy tập nguồn `L = { comment_id }` và tính bao đóng:
  `L+ = { comment_id }+ = R`
- Vì bao đóng của tập nguồn đã phủ kín toàn bộ thuộc tính của lược đồ `R`, và `L` chỉ có duy nhất 1 thuộc tính (không thể loại bỏ thuộc tính con nào), nên:
  - Tập nguồn `L` chính là một **khóa ứng viên (Candidate Key)**.
  - Hơn nữa, vì mọi khóa đều phải chứa `L`, mà `L` đã là khóa tối tiểu, nên trên lược đồ phẳng `R` **không tồn tại bất kỳ khóa ứng viên nào khác**.
- **Kết luận:** Lược đồ `R` có duy nhất một khóa ứng viên là:
  `Key = { comment_id }`

---

## 3. THUẬT TOÁN TÌM PHỦ TỐI TIỂU (MINIMAL COVER - F_min)

Phủ tối tiểu của tập phụ thuộc hàm `F` là một tập phụ thuộc hàm tương đương `F_min ≡ F` thỏa mãn 3 điều kiện:
1. Vế phải của mọi FD chỉ chứa đúng một thuộc tính đơn.
2. Vế trái của mọi FD không chứa thuộc tính dư thừa.
3. Không có phụ thuộc hàm nào trong `F_min` là dư thừa.

### Bước 1: Đơn thuộc tính hóa vế phải (Right-hand side decomposition)
Áp dụng quy tắc phân rã (`X → YZ` ⇒ `X → Y, X → Z`), ta tách các FD thành tập `F1` gồm 10 FD đơn:
- `f1a: comment_id → post_id`
- `f1b: comment_id → author_id`
- `f1c: comment_id → parent_id`
- `f1d: comment_id → content`
- `f1e: comment_id → created_at`
- `f2:  post_id → group_id`
- `f3a: group_id → group_name`
- `f3b: group_id → group_topic`
- `f4a: author_id → author_name`
- `f4b: author_id → author_email`

### Bước 2: Loại bỏ thuộc tính dư thừa ở vế trái (Extraneous attributes)
Xét từng FD dạng `X → A ∈ F1`: Một thuộc tính `B ∈ X` là dư thừa nếu `A ∈ (X \ {B})+`.
- Quan sát: Mọi FD trong `F1` đều có vế trái chỉ gồm duy nhất một thuộc tính đơn (`|X| = 1` với `X ∈ { comment_id, post_id, group_id, author_id }`).
- Do không có vế trái nào có từ 2 thuộc tính trở lên, nên không có thuộc tính dư thừa ở vế trái.
- Ta thu được `F2 = F1`.

### Bước 3: Loại bỏ phụ thuộc hàm dư thừa (Redundant functional dependencies)
Một phụ thuộc hàm `f: X → A ∈ F2` là dư thừa nếu `A ∈ X+` khi tính trên tập `F2 \ {f}`. Ta kiểm tra lần lượt cả 10 FD:
1. Xét `f1a: comment_id → post_id`:  
   Tính `{ comment_id }+` khi bỏ `f1a` = `{ comment_id, author_id, parent_id, content, created_at, author_name, author_email }`.  
   Không chứa `post_id` ⇒ `f1a` không dư thừa.
2. Xét `f1b: comment_id → author_id`:  
   Tính `{ comment_id }+` khi bỏ `f1b` không chứa `author_id` ⇒ `f1b` không dư thừa.
3. Tương tự với `f1c, f1d, f1e`: `parent_id, content, created_at` chỉ xuất hiện ở vế phải của các FD này ⇒ Không dư thừa.
4. Xét `f2: post_id → group_id`:  
   Tính `{ post_id }+` khi bỏ `f2` = `{ post_id }`. Không chứa `group_id` ⇒ `f2` không dư thừa.
5. Xét `f3a, f3b`: `{ group_id }+` khi bỏ `f3a` = `{ group_id, group_topic }` (không chứa `group_name`) ⇒ Không dư thừa.
6. Xét `f4a, f4b`: `{ author_id }+` khi bỏ `f4a` = `{ author_id, author_email }` (không chứa `author_name`) ⇒ Không dư thừa.

### Kết luận Phủ tối tiểu:
Phủ tối tiểu `F_min` gồm đúng 10 FD độc lập trên. Khi gộp lại các FD có cùng vế trái, ta được:
```text
F_min = {
    f1: comment_id → post_id, author_id, parent_id, content, created_at,
    f2: post_id → group_id,
    f3: group_id → group_name, group_topic,
    f4: author_id → author_name, author_email
}
```

---

## 4. PHÂN RÃ CHUẨN HÓA ĐẠT 3NF (THUẬT TOÁN TỔNG HỢP BERNSTEIN)

### 4.1 Đánh giá vi phạm chuẩn trên lược đồ phẳng R
- **Dạng chuẩn 1 (1NF):** Đạt, vì các thuộc tính đều là giá trị nguyên tố (Atomic values).
- **Dạng chuẩn 2 (2NF):** Đạt, vì khóa của `R` chỉ có 1 thuộc tính duy nhất là `comment_id`, do đó không thể tồn tại bất kỳ phụ thuộc bộ phận nào (không thể có thuộc tính không khóa nào phụ thuộc vào một phần của khóa).
- **Dạng chuẩn 3 (3NF):** **BỊ VI PHẠM NGHIÊM TRỌNG**.  
  *Lý do:* Tồn tại các phụ thuộc bắc cầu giữa các thuộc tính không khóa:
  - `comment_id → post_id → group_id → group_name`
  - `comment_id → author_id → author_name`  
  Trong các FD `f2, f3, f4`, vế trái (`post_id, group_id, author_id`) đều **không phải là siêu khóa** của `R`, và vế phải đều là các thuộc tính không khóa.

### 4.2 Thuật toán phân rã tổng hợp Bernstein
1. **Bước 1:** Từ phủ tối tiểu `F_min`, với mỗi nhóm FD có cùng vế trái `X`, tạo một lược đồ quan hệ con `Ri = X ∪ { tất cả các vế phải tương ứng }`:
   - Từ `f1` ⇒ `R1(comment_id, post_id, author_id, parent_id, content, created_at)` với khóa chính là `comment_id`.
   - Từ `f2` ⇒ `R2(post_id, group_id)` với khóa chính là `post_id`.
   - Từ `f3` ⇒ `R3(group_id, group_name, group_topic)` với khóa chính là `group_id`.
   - Từ `f4` ⇒ `R4(author_id, author_name, author_email)` với khóa chính là `author_id`.
2. **Bước 2 (Kiểm tra khóa của R):**  
   Kiểm tra xem có quan hệ con nào chứa một khóa của `R` hay không.  
   Ta thấy `R1` chứa `{ comment_id }` là khóa của `R`, do đó không cần tạo thêm quan hệ con mới.
3. **Bước 3 (Loại bỏ quan hệ con bị bao hàm):**  
   Không có quan hệ nào là tập con của quan hệ khác.

---

## 5. KIỂM TRA DẠNG CHUẨN BOYCE-CODD (BCNF)

### 5.1 Kiểm tra từng quan hệ con
Một quan hệ đạt chuẩn BCNF nếu với mọi phụ thuộc hàm không tầm thường `X → Y`, `X` bắt buộc phải là một **siêu khóa (Superkey)**.
- **Xét R1:** FD duy nhất là `comment_id → ...`, mà `comment_id` là khóa của `R1` ⇒ `R1` đạt BCNF.
- **Xét R2:** FD duy nhất là `post_id → group_id`, mà `post_id` là khóa của `R2` ⇒ `R2` đạt BCNF.
- **Xét R3:** FD duy nhất là `group_id → ...`, mà `group_id` là khóa của `R3` ⇒ `R3` đạt BCNF.
- **Xét R4:** Các FD là `author_id → author_name, author_email` và `author_email → author_id`. Cả `author_id` và `author_email` đều là siêu khóa của `R4` ⇒ `R4` đạt BCNF.

⇒ **Kết luận:** Trên bài toán này, kết quả phân rã đạt đồng thời cả **3NF và BCNF**. Không có sự đánh đổi giữa việc bảo toàn phụ thuộc hàm và đạt chuẩn BCNF.

### 5.2 Trường hợp kinh điển 3NF khác BCNF (Lý giải chiều sâu)
Để làm rõ tại sao có trường hợp 3NF không đạt BCNF, xét ví dụ kinh điển:
- Quan hệ `R(A, B, C)` với tập FD: `F = { AB → C, C → B }`.
- Các khóa ứng viên là: `K1 = { A, B }` và `K2 = { A, C }`.
- **Đạt 3NF:** Vì trong `C → B`, mặc dù `C` không phải là siêu khóa, nhưng thuộc tính `B` là một thuộc tính nguyên tố (thuộc khóa `AB`).
- **Vi phạm BCNF:** Do `C` không phải là siêu khóa.
- Nếu cố phân rã về BCNF thành `R1(C, B)` và `R2(A, C)` thì sẽ **làm mất phụ thuộc hàm** `AB → C`. Trong đề tài của nhóm, do không có thuộc tính nguyên tố phụ thuộc vào định thức không phải khóa, nên 3NF và BCNF hoàn toàn trùng khớp!

---

## 6. CHỨNG MINH TÍNH BẢO TOÀN THÔNG TIN (LOSSLESS JOIN)

Một phép phân rã `D = { R1, R2, R3, R4 }` của `R` được gọi là bảo toàn thông tin (Lossless Decomposition) nếu thực hiện phép nối tự nhiên các quan hệ con sẽ khôi phục lại chính xác quan hệ `R` ban đầu mà không sinh thêm bất kỳ bộ giả nào:
```text
R1 ⋈ R2 ⋈ R3 ⋈ R4 = R
```

### 6.1 Chứng minh bằng phương pháp nhị phân từng bước (Binary Join Condition)
Định lý: Phép tách `R` thành `RA` và `RB` là không mất thông tin nếu và chỉ nếu:
`(RA ∩ RB) → RA ∈ F+` hoặc `(RA ∩ RB) → RB ∈ F+`  
*(Giao của hai quan hệ phải là siêu khóa của ít nhất một trong hai quan hệ).*

1. **Bước 1: Nối R1 và R2**
   - `R1 ∩ R2 = { post_id }`
   - Trong `R2`, ta có `post_id → group_id`, do đó `{ post_id }` là khóa của `R2`.
   - ⇒ `R12 = R1 ⋈ R2` là phép nối **không mất thông tin**.
2. **Bước 2: Nối R12 với R3**
   - `R12 ∩ R3 = { group_id }`
   - Trong `R3`, ta có `group_id → group_name, group_topic`, do đó `{ group_id }` là khóa của `R3`.
   - ⇒ `R123 = R12 ⋈ R3` là phép nối **không mất thông tin**.
3. **Bước 3: Nối R123 với R4**
   - `R123 ∩ R4 = { author_id }`
   - Trong `R4`, ta có `author_id → author_name, author_email`, do đó `{ author_id }` là khóa của `R4`.
   - ⇒ `R1234 = R123 ⋈ R4 = R` là phép nối **không mất thông tin**.

---

### 6.2 Chứng minh bằng Bảng ma trận Chase (Chase Test Matrix)
Lập bảng ma trận Chase gồm 4 hàng (tương ứng 4 quan hệ `R1, R2, R3, R4`) và 11 cột (tương ứng 11 thuộc tính của `R`).  
Quy ước: Thuộc tính `Aj ∈ Ri` được đánh dấu bằng `aj`; ngược lại đánh dấu bằng `bij`.

| Quan hệ | comment_id (A1) | post_id (A2) | group_id (A3) | group_name (A4) | group_topic (A5) | author_id (A6) | author_name (A7) | author_email (A8) | parent_id (A9) | content (A10) | created_at (A11) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **R1** | a1 | a2 | b13 | b14 | b15 | a6 | b17 | b18 | a9 | a10 | a11 |
| **R2** | b21 | a2 | a3 | b24 | b25 | b26 | b27 | b28 | b29 | b210 | b211 |
| **R3** | b31 | b32 | a3 | a4 | a5 | b36 | b37 | b38 | b39 | b310 | b311 |
| **R4** | b41 | b42 | b43 | b44 | b45 | a6 | a7 | a8 | b49 | b410 | b411 |

**Thực thi các bước biến đổi Chase dựa trên F:**
1. Áp dụng `f2: post_id → group_id`:  
   Hàng `R1` và `R2` cùng có giá trị `a2` tại cột `post_id`. Do `R2` có `a3` tại cột `group_id`, nên ta thay `b13` ở hàng `R1` bằng `a3`.
2. Áp dụng `f3: group_id → group_name, group_topic`:  
   Hàng `R1` (vừa có `a3`) và hàng `R3` (có `a3`) trùng nhau ở cột `group_id`. Vì hàng `R3` có `a4, a5`, nên ta thay `b14, b15` ở hàng `R1` lần lượt bằng `a4, a5`.
3. Áp dụng `f4: author_id → author_name, author_email`:  
   Hàng `R1` và hàng `R4` cùng có giá trị `a6` tại cột `author_id`. Vì hàng `R4` có `a7, a8`, nên ta thay `b17, b18` ở hàng `R1` lần lượt bằng `a7, a8`.

**Kết quả ma trận Chase sau biến đổi:**
Hàng `R1` trở thành:
```text
[ a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11 ]
```
Do hàng `R1` chứa toàn bộ ký hiệu `a` trên tất cả 11 cột, **thuật toán Chase kết luận: Phép phân rã hoàn toàn bảo toàn thông tin (Lossless Join)**.

---

## 7. CHỨNG MINH TÍNH BẢO TOÀN PHỤ THUỘC HÀM (DEPENDENCY PRESERVATION)

Một phép phân rã bảo toàn phụ thuộc hàm nếu tập hợp các phép chiếu của `F` lên các quan hệ con tương đương logic với `F`:
```text
(π(R1) ∪ π(R2) ∪ π(R3) ∪ π(R4))+ = F+
```

- Xét `f1`: Toàn bộ các thuộc tính `{ comment_id, post_id, author_id, parent_id, content, created_at } ⊆ R1` ⇒ `f1 ∈ π(R1)`.
- Xét `f2`: `{ post_id, group_id } ⊆ R2` ⇒ `f2 ∈ π(R2)`.
- Xét `f3`: `{ group_id, group_name, group_topic } ⊆ R3` ⇒ `f3 ∈ π(R3)`.
- Xét `f4, f5`: `{ author_id, author_name, author_email } ⊆ R4` ⇒ `f4, f5 ∈ π(R4)`.

Vì mọi phụ thuộc hàm của phủ tối tiểu `F_min` đều nằm trọn vẹn trong ít nhất một quan hệ con tương ứng, phép phân rã **bảo toàn 100% các phụ thuộc hàm**.

---

## 8. PHÂN TÍCH PHI CHUẨN HÓA CÓ KIỂM SOÁT (CONTROLLED DENORMALIZATION)

Mặc dù chuẩn hóa 3NF/BCNF triệt tiêu hoàn toàn dư thừa dữ liệu và dị thường cập nhật, nhưng trong các hệ thống thực tế có tần suất đọc lớn (như Mạng xã hội học tập), việc chuẩn hóa tuyệt đối sẽ dẫn tới chi phí ghép nối (`JOIN`) quá cao. Đồ án 17 áp dụng kỹ thuật **Phi chuẩn hóa có kiểm soát** ở 4 vị trí then chốt:

| Mô hình / Cột phi chuẩn hóa | Dữ liệu dẫn xuất / Dư thừa | Lý do kỹ thuật & Đánh đổi | Cơ chế kiểm soát rủi ro |
| :--- | :--- | :--- | :--- |
| **`comment_path.path`** *(Path Enumeration / ltree)* | Lưu toàn bộ chuỗi tiền tố tổ tiên (ví dụ: `'1.2.5'`). | Cho phép lấy toàn bộ cây con hoặc đường dẫn tổ tiên bằng toán tử ltree `<@` và `@>` mà không cần chạy đệ quy `WITH RECURSIVE`. | Thao tác di chuyển nhánh (`move_comment`) phải cập nhật lại `path` của toàn bộ nút con; bắt buộc gom trong một **Transaction nguyên tử**. |
| **`comment_ns (lft, rgt)`** *(Nested Set)* | Lưu khoảng tọa độ bao con số. | Biến phép duyệt cây thành điều kiện khoảng số học liên tục `BETWEEN lft AND rgt`, tốc độ đọc cây con nhanh nhất. | Chi phí ghi cực lớn khi chèn/xóa phải dịch chuyển hàng loạt `lft/rgt`. Kiểm soát bằng khóa bảng hoặc khóa cố vấn `pg_advisory_xact_lock(post_id)`. |
| **`comment_closure`** *(Closure Table)* | Lưu trữ trước tất cả các cặp `(ancestor, descendant, depth)`. | Đọc quan hệ phả hệ đa chiều bằng 1 phép nối đơn giản; hỗ trợ truy vấn theo độ sâu `depth`. | Tốn dung lượng lưu trữ O(N × depth); kiểm soát bằng Foreign Key `ON DELETE CASCADE`. |
| **`users.friend_count`** | Lưu tổng số bạn bè hiện tại. | Tránh việc mỗi lần hiển thị trang cá nhân lại phải thực thi câu lệnh đếm `COUNT(*)` quét trên toàn bộ bảng bạn bè. | Đồng bộ qua Stored Procedure `proc_add_friend` có Transaction; kiểm chứng định kỳ bằng truy vấn Audit. |
