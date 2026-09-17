"""Local model-assisted segmentation annotator.

Run with: streamlit run annotation_tool.py
"""

import io
import json
import zipfile
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas


ROOT = Path(__file__).parent
DEFAULT_TASK = ROOT / "data" / "tiers" / "easy_semantic"


def load_labels(task_dir: Path) -> list[str]:
    labels_file = task_dir / "cvat-labels.json"
    return [item["name"] for item in json.loads(labels_file.read_text())]


def image_files(task_dir: Path) -> list[Path]:
    return sorted((task_dir / "images").glob("*"))


def rgba_color(index: int) -> tuple[int, int, int, int]:
    palette = [(220, 20, 60), (0, 0, 142), (0, 60, 100), (0, 0, 230), (119, 11, 32)]
    red, green, blue = palette[index % len(palette)]
    return red, green, blue, 170


def run_model(model_path: str, image: Image.Image) -> list[dict]:
    from ultralytics import YOLO

    model = YOLO(model_path)
    result = model.predict(np.asarray(image), verbose=False)[0]
    if result.masks is None:
        return []
    names = result.names
    detections = []
    for index, mask in enumerate(result.masks.data.cpu().numpy()):
        class_id = int(result.boxes.cls[index].item())
        detections.append(
            {
                "class": names[class_id],
                "mask": Image.fromarray((mask * 255).astype("uint8")).resize(image.size),
                "score": float(result.boxes.conf[index].item()),
            }
        )
    return detections


@st.cache_resource(show_spinner="Đang tải Mask2Former Cityscapes...")
def load_mask2former(model_name: str):
    from transformers import AutoImageProcessor, Mask2FormerForUniversalSegmentation

    return (
        AutoImageProcessor.from_pretrained(model_name),
        Mask2FormerForUniversalSegmentation.from_pretrained(model_name),
    )


def run_mask2former(model_name: str, image: Image.Image) -> list[dict]:
    import torch

    processor, model = load_mask2former(model_name)
    inputs = processor(images=image, return_tensors="pt")
    with torch.inference_mode():
        outputs = model(**inputs)
    result = processor.post_process_panoptic_segmentation(
        outputs, target_sizes=[(image.height, image.width)]
    )[0]
    id_to_label = model.config.id2label
    segmentation = result["segmentation"].cpu().numpy()
    detections = []
    for segment in result["segments_info"]:
        segment_id = int(segment["id"])
        label_id = int(segment["label_id"])
        mask = Image.fromarray((segmentation == segment_id).astype("uint8") * 255)
        detections.append(
            {
                "class": id_to_label.get(label_id, str(label_id)),
                "mask": mask,
                "score": float(segment.get("score", 1.0)),
                "source": "Mask2Former",
            }
        )
    return detections


def mask_png(mask: Image.Image, size: tuple[int, int]) -> bytes:
    return np.asarray(mask.resize(size).convert("L")).astype("uint8").tobytes()


def coco_rle(mask: np.ndarray) -> dict:
    pixels = np.asarray(mask, dtype=np.uint8).flatten(order="F")
    runs = []
    current = 0
    count = 0
    for pixel in pixels:
        if pixel != current:
            runs.append(count)
            count = 0
            current = int(pixel)
        count += 1
    runs.append(count)
    if len(runs) % 2 == 0:
        runs.append(0)
    return {"size": list(mask.shape), "counts": runs}


st.set_page_config(page_title="Segmentation Annotator", layout="wide")
st.title("Model-assisted Segmentation Annotator")
st.caption("YOLO mask gợi ý, sau đó dùng brush/eraser để chỉnh đè trước khi export.")

with st.sidebar:
    task_text = st.text_input("Task folder", str(DEFAULT_TASK))
    task_dir = Path(task_text).expanduser()
    model_path = st.text_input("YOLOv8-seg model", "yolov8n-seg.pt")
    mask2former_name = st.text_input(
        "Mask2Former Cityscapes model",
        "facebook/mask2former-swin-large-cityscapes-panoptic",
    )
    mode = st.selectbox("Export type", ["semantic", "instance"])
    brush_size = st.slider("Brush size", 1, 80, 12)

if not task_dir.exists():
    st.error("Không tìm thấy task folder.")
    st.stop()

labels = load_labels(task_dir)
files = image_files(task_dir)
if not files:
    st.error("Task chưa có ảnh trong thư mục images.")
    st.stop()

if "annotations" not in st.session_state:
    st.session_state.annotations = {}
if "predictions" not in st.session_state:
    st.session_state.predictions = {}

image_path = st.selectbox("Image", files, format_func=lambda path: path.name)
image = Image.open(image_path).convert("RGB")
label = st.selectbox("Class to paint", labels)
tool = st.radio("Edit mode", ["Paint", "Erase"], horizontal=True)

left, right = st.columns([3, 1])
with right:
    if st.button("Run both models", use_container_width=True):
        try:
            yolo_predictions = run_model(model_path, image)
            mask2former_predictions = run_mask2former(mask2former_name, image)
            st.session_state.predictions[image_path.name] = yolo_predictions + mask2former_predictions
            st.success("Đã chạy song song YOLOv8n-seg và Mask2Former Cityscapes.")
        except Exception as error:
            st.error(f"Không chạy được một trong hai model: {error}")
    if st.button("Run YOLO", use_container_width=True):
        try:
            predictions = run_model(model_path, image)
            for prediction in predictions:
                prediction["source"] = "YOLOv8-seg"
            st.session_state.predictions[image_path.name] = predictions
            st.success("Đã tạo mask gợi ý.")
        except Exception as error:
            st.error(f"Không chạy được model: {error}")
    if st.button("Use both model masks", use_container_width=True):
        predictions = st.session_state.predictions.get(image_path.name, [])
        current = st.session_state.annotations.setdefault(image_path.name, {})
        applied = 0
        for prediction in predictions:
            if prediction["class"] in labels:
                current.setdefault(prediction["class"], []).append(prediction["mask"])
                applied += 1
        if applied:
            st.success(f"Đã đưa {applied} mask từ hai model vào bản nhãn.")
        else:
            st.warning("Chưa có class phù hợp. Hãy chạy cả hai model trước.")
    if st.button("Use model masks", use_container_width=True):
        predictions = st.session_state.predictions.get(image_path.name, [])
        current = st.session_state.annotations.setdefault(image_path.name, {})
        applied = 0
        for prediction in predictions:
            if prediction["class"] in labels:
                current.setdefault(prediction["class"], []).append(prediction["mask"])
                applied += 1
        if applied:
            st.success(f"Đã đưa {applied} mask model vào bản nhãn để chỉnh sửa.")
        elif predictions:
            st.warning("Model có phát hiện object, nhưng class của model không có trong task này.")
        else:
            st.warning("Chưa có mask model. Hãy bấm Run YOLO trước.")
    if st.button("Clear selected class", use_container_width=True):
        st.session_state.annotations.setdefault(image_path.name, {}).pop(label, None)
        st.rerun()

    predictions = st.session_state.predictions.get(image_path.name, [])
    if predictions:
        st.write("**Model detections**")
        for prediction in predictions:
            st.write(f"{prediction.get('source', 'model')}: {prediction['class']} ({prediction['score']:.2f})")

with left:
    current = st.session_state.annotations.setdefault(image_path.name, {})
    instance_count = len(current.get(label, []))
    instance_index = st.number_input("Instance", min_value=1, max_value=max(1, instance_count + 1), value=1) - 1
    class_masks = current.setdefault(label, [])
    if instance_index >= len(class_masks):
        class_masks.append(Image.new("L", image.size))
    drawing_mode = "freedraw"
    stroke_color = "rgba(255,255,255,1)" if tool == "Paint" else "rgba(0,0,0,1)"
    canvas = st_canvas(
        fill_color="rgba(255,255,255,0)",
        stroke_width=brush_size,
        stroke_color=stroke_color,
        background_image=image,
        update_streamlit=True,
        return_image_data=True,
        height=image.height,
        width=image.width,
        drawing_mode=drawing_mode,
        key=f"canvas-{image_path.name}-{label}-{instance_index}",
    )
    if canvas.image_data is not None:
        alpha = canvas.image_data[:, :, 3] > 0
        previous = np.array(class_masks[instance_index], dtype=np.uint8, copy=True)
        if tool == "Paint":
            previous[alpha] = 255
        else:
            previous[alpha] = 0
        class_masks[instance_index] = Image.fromarray(previous, mode="L")

    if st.button("Save annotation", type="primary"):
        st.session_state.annotations.setdefault(image_path.name, {})
        st.success("Đã lưu trong phiên làm việc. Hãy export khi hoàn tất các ảnh.")


def export_zip() -> bytes:
    output = io.BytesIO()
    annotations = []
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            masks = st.session_state.annotations.get(path.name, {})
            source = Image.open(path).convert("RGB")
            if mode == "semantic":
                result = np.zeros((source.height, source.width), dtype=np.uint8)
                for class_id, class_name in enumerate(labels, start=1):
                    class_masks = masks.get(class_name, [])
                    if not isinstance(class_masks, list):
                        class_masks = [class_masks]
                    mask = np.zeros((source.height, source.width), dtype=bool)
                    for class_mask in class_masks:
                        mask |= np.asarray(class_mask.resize(source.size)) > 0
                    result[mask] = class_id
                buffer = io.BytesIO()
                Image.fromarray(result).save(buffer, format="PNG")
                archive.writestr(f"SegmentationClass/{path.stem}.png", buffer.getvalue())
            else:
                for class_id, class_name in enumerate(labels, start=1):
                    class_masks = masks.get(class_name, [])
                    if not isinstance(class_masks, list):
                        class_masks = [class_masks]
                    for mask in class_masks:
                        if mask is None:
                            continue
                        array = np.asarray(mask) > 0
                        ys, xs = np.where(array)
                        if len(xs) == 0:
                            continue
                        annotations.append({
                            "id": len(annotations) + 1,
                            "image_id": files.index(path) + 1,
                            "category_id": class_id,
                            "segmentation": coco_rle(array),
                            "area": int(array.sum()),
                            "bbox": [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)],
                            "iscrowd": 0,
                        })
                        buffer = io.BytesIO()
                        mask.save(buffer, format="PNG")
                        archive.writestr(f"masks/{path.stem}_{class_id}_{len(annotations)}_{class_name}.png", buffer.getvalue())
        if mode == "instance":
            payload = {
                "images": [
                    {"id": index, "file_name": item.name,
                     "height": Image.open(item).height, "width": Image.open(item).width}
                    for index, item in enumerate(files, start=1)
                ],
                "categories": [{"id": index, "name": name} for index, name in enumerate(labels, start=1)],
                "annotations": annotations,
            }
            archive.writestr("annotations/instances_default.json", json.dumps(payload))
        if mode == "semantic":
            archive.writestr("labelmap.txt", "\n".join(f"{name}:1,2,3::" for name in labels))
    return output.getvalue()


st.sidebar.download_button(
    "Export masks ZIP",
    data=export_zip(),
    file_name=f"{task_dir.name}_masks.zip",
    mime="application/zip",
)