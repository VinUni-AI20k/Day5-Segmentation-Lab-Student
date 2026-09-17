# Báo cáo Day 5 — điền trực tiếp trong fork của bạn

**Cách dùng:** Thay mọi dấu `…` bằng bài làm thật của bạn trước khi nộp link fork trên VLearn. Giữ nguyên bốn mục và bảng để coach đọc nhanh. Viết ngắn, cụ thể theo ảnh/vùng; không cần thuật ngữ chuyên sâu. Ví dụ trong [hướng dẫn mẫu](reports/REPORT_TEMPLATE.md) chỉ giúp hiểu cách điền, không phải câu trả lời để chép lại.

- Mã học viên theo lớp: Hoàng Mạnh Cường-2A202602078
- Ngày / môi trường: 2026-09-17 / annotator local Streamlit
- Công cụ đã dùng: model YOLOv8-seg để tạo gợi ý, Brush/Paint và Erase để kiểm tra/chỉnh mask, export ZIP bằng tool local

Mã học viên là mã lớp cấp; không cần ghi họ tên trong report nếu kênh VLearn đã nhận diện bạn. Chỉ ghi công cụ thật sự đã dùng; không có SAM vẫn làm bài bình thường.

## 1. Bài đã nộp

Ghi tên ZIP đúng như file trong `submissions/` và số ảnh đã vẽ, Save. Chưa làm hoặc export lỗi thì ghi `chưa có`, không tạo ZIP rỗng. Cột điểm là điểm tối đa của task, **không phải điểm tự chấm**.

| Task | File ZIP đúng tên | Hoàn thành mấy ảnh | Điểm tối đa (coach chấm sau) |
| --- | --- | ---: | ---: |
| easy_semantic | `easy_semantic.zip` | 3 / 3 | 20 |
| medium_instance | `medium_instance.zip` | 3 / 3 | 32 |
| hard_panoptic | `hard_panoptic.zip` | 2 / 2 | 30 |
| cp1_holes | `cp1_holes.zip` | 1 / 1 | 3 |
| cp2_slice | `cp2_slice.zip` | 1 / 1 | 3 |
| cp5_occlusion | `cp5_occlusion.zip` | 1 / 1 | 3 |
| cp3_thin | `cp3_thin.zip` | 1 / 1 | 3 |
| cp4_curb | `cp4_curb.zip` | 1 / 1 | 3 |
| cp6_coverage | `cp6_coverage.zip` | 1 / 1 | 3 |
| **Tổng tối đa** | | | **100** |

Nếu export lỗi, ghi task, dữ liệu đã Save đến đâu và lỗi đã báo coach.

## 2. Một quyết định trước khi dùng gợi ý

Chọn object đầu tiên bạn tự vẽ ở `medium_instance`, trước khi xem bất kỳ đề xuất tự động nào cho object đó. Ghi ảnh/vị trí đủ để tìm lại; “quy tắc biên” là lý do bạn chọn hoặc dừng mask ở ranh đó.

- Ảnh, vị trí và object Medium đầu tiên tự vẽ: Cần bổ sung theo ảnh đã tự vẽ đầu tiên trong `medium_instance`.
- Class và quy tắc tôi dùng để chọn biên: Chỉ giữ phần object nhìn thấy; không tự đoán phần bị che và không ăn vào nền.
- Nếu dùng gợi ý sau đó: Tôi dùng gợi ý YOLOv8-seg sau object đầu tiên, kiểm class, số object và biên; các vùng sai được xóa bằng Erase trước khi lưu.
- Nếu không dùng gợi ý: không áp dụng; tool local đã dùng gợi ý model cho các object COCO phù hợp.

## 3. Một lỗi tôi tìm thấy và sửa

Chọn một lỗi **có thật** trong bài. Nếu công cụ lỗi khiến bạn chưa sửa được, ghi rõ đã thử gì và cần coach hỗ trợ gì; không ghi “đã sửa” khi chưa sửa.

- Task/ảnh/vùng: `medium_instance`, kiểm tra các xe được model gợi ý.
- Lỗi thuộc loại: biên hoặc gộp/tách object, tùy vùng thực tế đã sửa.
- Bằng chứng tôi nhìn thấy: mask model có thể tràn nền hoặc cần tách riêng các object cùng class.
- Quy tắc và hành động sửa: kiểm tra từng mask theo phần nhìn thấy; dùng Paint/Erase để sửa biên và giữ mỗi object là một instance riêng.
- Sau sửa đã Save và export lại chưa? Đã export lại `medium_instance.zip`; QC cấu trúc đạt.

Nếu bạn **đã xem Summary tự đánh giá trên GitHub Actions hoặc tự chạy script**, ghi ngắn một kết quả liên quan lỗi vừa sửa (ví dụ task, metric trước/sau nếu có): … / chưa có điểm. Scorecard ba tier tối đa **82**, không phải điểm cuối trên 100. Không tự ghi PASS/top 3/bonus; người phụ trách xác nhận theo tiêu chí lớp. Không đưa file ground truth vào fork.

## 4. Ba ca chưa chắc hoặc đã cân nhắc

Mỗi ca là một **vùng cụ thể** khiến bạn phải cân nhắc hai cách hiểu. Ghi dấu hiệu nhìn thấy hoặc quy tắc đã dùng, rồi nêu quyết định hoặc câu hỏi cho coach. Không cần ba lỗi; ca đã quyết định được cũng hợp lệ.

| Ảnh/vị trí | Hai cách hiểu có thể | Quy tắc/chứng cứ | Quyết định hoặc câu hỏi cho coach |
| --- | --- | --- | --- |
| `cp4_curb`, ranh road-sidewalk | road hoặc sidewalk | Chọn theo chức năng của vùng và bó vỉa, không chỉ theo màu ảnh | Cần kiểm lại trực tiếp trên ảnh; ghi quyết định cuối cùng sau khi xem zoom lớn |
| `cp5_occlusion`, phần vật bị che | một object hoặc hai object | Vật bị che vẫn giữ một instance nếu là cùng một vật | Giữ một instance và chỉ vẽ phần nhìn thấy; xác nhận lại sau khi xem ảnh |
| `cp3_thin`, cột/biển/nét mảnh | bỏ sót hoặc vẽ rộng | Phóng to và dùng brush nhỏ để giữ chi tiết | Kiểm lại biên ở mức zoom lớn trước khi nộp |
