import gradio as gr
from PIL import Image
import io
import os
from google.colab import drive  # Chỉ dùng khi chạy trên Colab

# Kết nối Google Drive và tạo thư mục dự án (chỉ chạy trên Colab)
def setup_drive(project_folder='/content/drive/MyDrive/ImageConverter'):
    drive.mount('/content/drive', force_remount=True)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    return project_folder

# Hàm chuyển đổi ảnh sang WebP và lưu vào thư mục nếu chỉ định
def convert_to_webp(img, save_path=None):
    img = Image.open(img).convert("RGBA")  # Hỗ trợ transparency
    webp_io = io.BytesIO()
    img.save(webp_io, format="WEBP")
    webp_io.seek(0)
    
    if save_path:
        with open(save_path, 'wb') as f:
            f.write(webp_io.getvalue())
    
    return webp_io

# Giao diện Gradio
def gradio_interface(project_folder):
    def process_img(img):
        if img is None:
            return None, "Vui lòng tải ảnh lên."
        
        # Tạo tên file output với timestamp để tránh trùng
        output_filename = f"converted_{os.path.basename(img.name).split('.')[0]}.webp"
        output_path = os.path.join(project_folder, output_filename)
        
        webp_file = convert_to_webp(img, output_path)
        return webp_file, f"Ảnh đã lưu tại: {output_path}"

    with gr.Blocks() as demo:
        gr.Markdown("### Chatbot Chuyển Đổi Ảnh Sang WebP")
        gr.Markdown("Tải ảnh lên, chuyển đổi và tải về. Ảnh sẽ được lưu vào Google Drive nếu chạy trên Colab.")
        
        with gr.Row():
            inp = gr.Image(type="filepath", label="Tải ảnh lên (hỗ trợ JPG, PNG, v.v.)")
            out = gr.File(label="Tải ảnh WebP về")
        
        status = gr.Textbox(label="Trạng thái")
        btn = gr.Button("Chuyển Đổi")
        
        btn.click(fn=process_img, inputs=inp, outputs=[out, status])

    return demo

if __name__ == "__main__":
    try:
        # Kiểm tra nếu đang trong IPython/Colab
        get_ipython()  # Nếu không phải IPython, sẽ raise lỗi
        project_folder = setup_drive()
        print(f"Thư mục dự án: {project_folder}")
    except NameError:
        # Nếu không phải Colab/IPython, bỏ qua mount và dùng thư mục cục bộ
        project_folder = os.getcwd()
        print("Chạy cục bộ hoặc không phải Colab, không kết nối Drive.")
    except Exception as e:
        # Xử lý lỗi khác, như AttributeError
        print(f"Lỗi khi mount Drive: {e}")
        project_folder = os.getcwd()
        print("Bỏ qua mount Drive, sử dụng thư mục cục bộ.")

    demo = gradio_interface(project_folder)
    demo.launch(debug=True, share=True)

