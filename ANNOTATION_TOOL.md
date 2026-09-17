# Local annotation tool

Tool này tạo mask gợi ý bằng YOLOv8-seg và Mask2Former Cityscapes, sau đó cho phép chỉnh đè thủ công bằng chuột.

## Chạy

```bash
python3 -m pip install -r requirements.txt
streamlit run annotation_tool.py
```

Mở URL Streamlit hiển thị trong terminal. Trong sidebar, chọn task folder, model và loại export.

1. Chọn ảnh và class.
2. Bấm `Run both models` để chạy YOLOv8n-seg và Mask2Former Cityscapes.
3. Bấm `Use both model masks` để đưa các mask phù hợp vào vùng chỉnh sửa.
4. Chọn `Paint` để tô đè hoặc `Erase` để xóa bằng chuột.
5. Bấm `Save annotation`, rồi tải `Export masks ZIP`.

Model mặc định là `yolov8n-seg.pt` cho object COCO và `facebook/mask2former-swin-large-cityscapes-panoptic` cho semantic/panoptic Cityscapes. Mask2Former được tải khi bấm `Run both models`; lần đầu cần Internet và có thể cần nhiều GB RAM. Hai model đều chỉ tạo gợi ý, vẫn phải kiểm tra class, biên, vùng chồng lấn và instance bằng tay.

Export semantic hiện tạo PNG class-id cho việc kiểm tra nội bộ; export instance hiện giữ từng mask theo class. Khi nộp chính thức, vẫn cần đưa dữ liệu qua format CVAT `Segmentation mask 1.1` hoặc `COCO 1.0` theo yêu cầu của task.