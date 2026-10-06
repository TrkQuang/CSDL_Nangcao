# DANH SÁCH PHỤ THUỘC HÀM (FUNCTIONAL DEPENDENCIES - FD)

> **Mục đích file:** Liệt kê và phân tích tập các phụ thuộc hàm $F$ xuất phát từ quy tắc nghiệp vụ BR1–BR10 của hệ thống Mạng xã hội học tập.  
> **Người phụ trách:** TV1 (Hỗ trợ: TV5 | Review: TV3).  
> **Đầu ra:** Cơ sở toán học để tìm bao đóng, tìm khóa chính và thực hiện chuẩn hóa dữ liệu.

---

## 1. Lược Đồ Quan Hệ Tổng Hợp Ban Đầu (Universal Relation Schema)
Giả định ban đầu gộp tất cả thông tin vào một quan hệ lớn:  
$R(UserID, FullName, Email, FriendCount, PostID, GroupID, GroupName, PostTitle, PostType, Content, CommentID, CommentContent, ParentCommentID, ReactionUserID)$

*Các dị thường phát sinh trên $R$:*
- **Dị thường thêm (Insertion Anomaly):** Không thể thêm một người dùng mới nếu họ chưa tham gia nhóm hoặc chưa đăng bài/bình luận nào.
- **Dị thường xóa (Deletion Anomaly):** Xóa một bài viết có thể vô tình xóa mất thông tin của nhóm học tập nếu nhóm đó chỉ có duy nhất 1 bài.
- **Dị thường sửa (Update Anomaly):** Nếu người dùng đổi tên, phải cập nhật trên tất cả các dòng chứa bài viết và bình luận của họ.

---

## 2. Tập Phụ Thuộc Hàm Hợp Lệ Nghiệp Vụ ($F$)

### [VÍ DỤ MẪU]
- $FD_1: UserID \rightarrow FullName, Email$  
  *(Giải thích nghiệp vụ: Mỗi mã người dùng xác định duy nhất tên đầy đủ và email đăng nhập).*
- $FD_2: Email \rightarrow UserID, FullName$  
  *(Giải thích nghiệp vụ: Email là duy nhất, xác định ngược lại thông tin người dùng).*
- $FD_3: GroupID \rightarrow GroupName, Topic, OwnerID$  
  *(Giải thích nghiệp vụ: Mã nhóm xác định tên nhóm, chủ đề và người tạo nhóm).*
- $FD_4: PostID \rightarrow GroupID, AuthorID, PostType, Title, Content, CreatedAt$  
  *(Giải thích nghiệp vụ: Mỗi bài viết thuộc về một nhóm và do một tác giả đăng).*
- $FD_5: CommentID \rightarrow PostID, AuthorID, ParentCommentID, Content, CreatedAt$  
  *(Giải thích nghiệp vụ: Mỗi bình luận thuộc một bài viết cụ thể và có một tác giả).*

---

## 3. Phân Biệt FD Nghiệp Vụ vs FD Tình Cờ Đúng Trên Dữ Liệu

> **LƯU Ý QUAN TRỌNG:**  
> Một phụ thuộc hàm $X \rightarrow Y$ chỉ được coi là hợp lệ khi nó đúng trong **mọi trường hợp nghiệp vụ trong tương lai**, chứ không phải chỉ đúng ngẫu nhiên trên một tập dữ liệu mẫu cụ thể.

- **Ví dụ FD tình cờ (Sai về mặt nghiệp vụ):**  
  Trên tập dữ liệu kiểm chứng nhỏ: `FullName -> Email` có thể đúng vì mỗi bạn tên khác nhau (An, Binh, Chi...).  
  Nhưng trên thực tế: Hai người dùng hoàn toàn có thể trùng họ tên -> Không thể coi `FullName -> Email` là một FD nghiệp vụ.
- **Cách kiểm chứng:** Sử dụng truy vấn SQL trong file [fd_check.sql](file:///c:/Users/shuut/Documents/CSDL_NC/normalization/fd_check.sql) để kiểm tra các vi phạm.
