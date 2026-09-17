# Báo cáo Day 5 — điền trực tiếp trong fork của bạn

**Cách dùng:** Thay mọi dấu `…` bằng bài làm thật của bạn trước khi nộp link fork trên VLearn. Giữ nguyên bốn mục và bảng để coach đọc nhanh. Viết ngắn, cụ thể theo ảnh/vùng; không cần thuật ngữ chuyên sâu. Ví dụ trong [hướng dẫn mẫu](reports/REPORT_TEMPLATE.md) chỉ giúp hiểu cách điền, không phải câu trả lời để chép lại.

- Mã học viên theo lớp: 2A202602260
- Ngày / CVAT local: 17/09/2026 / localhost:8080
- Công cụ đã dùng: Brush, Eraser

Mã học viên là mã lớp cấp; không cần ghi họ tên trong report nếu kênh VLearn đã nhận diện bạn. Chỉ ghi công cụ thật sự đã dùng; không có SAM vẫn làm bài bình thường.

## 1. Bài đã nộp

Ghi tên ZIP đúng như file trong `submissions/` và số ảnh đã vẽ, Save. Chưa làm hoặc export lỗi thì ghi `chưa có`, không tạo ZIP rỗng. Cột điểm là điểm tối đa của task, **không phải điểm tự chấm**.

| Task | File ZIP đúng tên | Hoàn thành mấy ảnh | Điểm tối đa (coach chấm sau) |
| --- | --- | ---: | ---: |
| easy_semantic | easy_semantic.zip | 3 / 3 | 20 |
| medium_instance | medium_instance.zip | 3 / 3 | 32 |
| hard_panoptic | hard_panoptic.zip | 2 / 2 | 30 |
| cp1_holes | cp1_holes.zip | 1 / 1 | 3 |
| cp2_slice | cp2_slice.zip | 1 / 1 | 3 |
| cp5_occlusion | cp5_occlusion.zip | 1 / 1 | 3 |
| cp3_thin | cp3_thin.zip | 1 / 1 | 3 |
| cp4_curb | cp4_curb.zip | 1 / 1 | 3 |
| cp6_coverage | cp6_coverage.zip | 1 / 1 | 3 |
| **Tổng tối đa** | | | **100** |

Nếu export lỗi, ghi task, dữ liệu đã Save đến đâu và lỗi đã báo coach.

## 2. Một quyết định trước khi dùng gợi ý

Chọn object đầu tiên bạn tự vẽ ở `medium_instance`, trước khi xem bất kỳ đề xuất tự động nào cho object đó. Ghi ảnh/vị trí đủ để tìm lại; “quy tắc biên” là lý do bạn chọn hoặc dừng mask ở ranh đó.

- Ảnh, vị trí và object Medium đầu tiên tự vẽ: Ảnh `000000458325.jpg`, chiếc xe ô tô con đỗ sát lề đường bên trái.
- Class và quy tắc tôi dùng để chọn biên: Class `car`. Dùng Brush ôm sát đường viền thân xe thực tế nhìn thấy, dừng mask đúng mép tiếp xúc giữa lốp xe với mặt đường, không tô lấn sang phần đường (`road`).
- Nếu dùng gợi ý sau đó: không dùng
- Nếu không dùng gợi ý: ghi “không dùng”; vẫn giải thích một quyết định gán nhãn của mình: không dùng; tự dùng Brush và chỉnh kích thước cọ nhỏ để vẽ ôm sát các góc gương chiếu hậu và kính xe, sau đó dùng Eraser tỉa viền thừa.

## 3. Một lỗi tôi tìm thấy và sửa

Chọn một lỗi **có thật** trong bài. Nếu công cụ lỗi khiến bạn chưa sửa được, ghi rõ đã thử gì và cần coach hỗ trợ gì; không ghi “đã sửa” khi chưa sửa.

- Task/ảnh/vùng: Task `cp2_slice`, ảnh `000000017627.jpg`, hai xe ô tô cùng đỗ song song rất sát nhau.
- Lỗi thuộc loại: gộp-tách
- Bằng chứng tôi nhìn thấy: Khi dùng Brush tô nhanh, nét cọ bị dính liền ranh giới khiến hai xe bị gộp chung thành một shape duy nhất trong bảng Objects.
- Quy tắc và hành động sửa: Quy tắc instance segmentation yêu cầu mỗi cá thể xe phải là một mask riêng. Tôi đã dùng Eraser khoét tách khe hở giữa hai xe, xóa một xe và tạo Shape mới để vẽ riêng xe thứ hai thành hai dòng độc lập trên Objects.
- Sau sửa đã Save và export lại chưa? Đã Save trên CVAT và export lại file `cp2_slice.zip` định dạng COCO 1.0.

Nếu bạn **đã xem Summary tự đánh giá trên GitHub Actions hoặc tự chạy script**, ghi ngắn một kết quả liên quan lỗi vừa sửa (ví dụ task, metric trước/sau nếu có): chưa có điểm (Actions đã chạy thành công kiểm tra cấu trúc ZIP, đang chờ reference chính thức từ lớp). Scorecard ba tier tối đa **82**, không phải điểm cuối trên 100. Không tự ghi PASS/top 3/bonus; người phụ trách xác nhận theo tiêu chí lớp. Không đưa file ground truth vào fork.

## 4. Ba ca chưa chắc hoặc đã cân nhắc

Mỗi ca là một **vùng cụ thể** khiến bạn phải cân nhắc hai cách hiểu. Ghi dấu hiệu nhìn thấy hoặc quy tắc đã dùng, rồi nêu quyết định hoặc câu hỏi cho coach. Không cần ba lỗi; ca đã quyết định được cũng hợp lệ.

| Ảnh/vị trí | Hai cách hiểu có thể | Quy tắc/chứng cứ | Quyết định hoặc câu hỏi cho coach |
| --- | --- | --- | --- |
| 1. Task `cp4_curb`, ảnh `7d83710e-4697c3b2.jpg`, đoạn vỉa hè bị bóng râm đổ sẫm màu trùng màu lòng đường | Có thể hiểu là `road` do màu sắc tối như nhựa đường, hoặc là `sidewalk` do nằm trên gờ đá | Dựa vào gờ nổi của bó vỉa và chức năng phân làn người đi bộ/xe chạy thay vì nhìn theo màu sắc | Quyết định phân tách ranh giới theo chân bó vỉa; phần gờ bó vỉa gán vào `sidewalk`, phần lòng đường thấp hơn gán vào `road` |
| 2. Task `cp5_occlusion`, ảnh `000000336232.jpg`, thân xe bị cột cản phía trước che ngang chia làm 2 nửa nhìn thấy | Có thể hiểu là 2 instance xe riêng biệt (vì mask bị đứt đoạn), hoặc vẽ nối liền đè xuyên qua thân cột | Quy tắc chỉ vẽ pixel nhìn thấy thực tế và giữ nguyên 1 instance cho một vật thể ngoài đời | Quyết định gán 1 instance xe duy nhất gồm hai phần nhìn thấy rời nhau, dùng Eraser làm sạch phần đè lên cột |
| 3. Task `cp3_thin`, ảnh `839f7736-abe28069.jpg`, thân cột cắm biển báo ở xa rất mảnh (rộng 1-2 pixel) | Bỏ qua vì quá mảnh khó tô, hoặc tô nhanh bằng cọ to làm thân cột phình dày gấp đôi | Quy tắc `cp3_thin` yêu cầu không bỏ sót cột mảnh nhưng không được vẽ phồng ăn lấn nền | Quyết định phóng to 100%, hạ cọ Brush xuống kích thước tối thiểu để viền đúng độ mảnh thực tế của `pole` |
