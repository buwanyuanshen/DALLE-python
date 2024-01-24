import string
import tkinter as tk
from tkinter import ttk
import openai
import random
import json
from PIL import Image, ImageTk
from io import BytesIO
import requests
import threading

class ImageGenerationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dalle Paint")

        # 注册窗口关闭事件
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 设置默认参数
        self.model_var = tk.StringVar(value="dall-e-2")
        self.prompt_var = tk.StringVar()
        self.size_var = tk.StringVar(value="512x512")
        self.n_var = tk.StringVar(value="1")
        self.quality_var = tk.StringVar(value="standard")
        self.style_var = tk.StringVar(value="vivid")
        self.api_key_var = tk.StringVar()
        self.proxy_var = tk.StringVar(value="https://api.openai-proxy.com/v1")  # 默认代理网址

        # 图片列表和当前显示的图片索引
        self.image_paths = []
        self.current_image_index = 0

        # 加载配置
        self.load_config()

        # 创建左右两个框架
        self.left_frame = tk.Frame(root)
        self.right_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        # 设置列比例
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=8)
        # 创建界面元素
        self.create_widgets()

    def create_widgets(self):
        # 左侧框架部件
        model_label = ttk.Label(self.left_frame, text="Model:")
        model_combobox = ttk.Combobox(self.left_frame, textvariable=self.model_var, values=["dall-e-2", "dall-e-3"], state="readonly")

        prompt_label = ttk.Label(self.left_frame, text="Prompt:")
        prompt_entry = ttk.Entry(self.left_frame, textvariable=self.prompt_var, width=24)

        size_label = ttk.Label(self.left_frame, text="Size:")
        size_combobox = ttk.Combobox(self.left_frame, textvariable=self.size_var, values=["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], state="readonly")

        n_label = ttk.Label(self.left_frame, text="Number(1-10):")
        n_entry = ttk.Entry(self.left_frame, textvariable=self.n_var)

        quality_label = ttk.Label(self.left_frame, text="Quality:")
        quality_combobox = ttk.Combobox(self.left_frame, textvariable=self.quality_var, values=["standard", "hd"], state="readonly")

        style_label = ttk.Label(self.left_frame, text="Style:")
        style_combobox = ttk.Combobox(self.left_frame, textvariable=self.style_var, values=["vivid", "natural"], state="readonly")

        api_key_label = ttk.Label(self.left_frame, text="API Key(s):")
        api_key_entry = ttk.Entry(self.left_frame, textvariable=self.api_key_var)

        proxy_label = ttk.Label(self.left_frame, text="Proxy:")
        proxy_entry = ttk.Entry(self.left_frame, textvariable=self.proxy_var)

        generate_button = ttk.Button(self.left_frame, text="生成图片", command=self.generate_image)

        # 在左侧框架布局部件
        model_label.grid(row=0, column=0, sticky="e", pady=20)
        model_combobox.grid(row=0, column=1, padx=5, pady=20, sticky="w")
        prompt_label.grid(row=1, column=0, sticky="e", pady=20)
        prompt_entry.grid(row=1, column=1, padx=5, pady=20, sticky="w")
        size_label.grid(row=2, column=0, sticky="e", pady=20)
        size_combobox.grid(row=2, column=1, padx=5, pady=20, sticky="w")
        n_label.grid(row=3, column=0, sticky="e", pady=20)
        n_entry.grid(row=3, column=1, padx=5, pady=20, sticky="w")
        quality_label.grid(row=4, column=0, sticky="e", pady=20)
        quality_combobox.grid(row=4, column=1, padx=5, pady=20, sticky="w")
        style_label.grid(row=5, column=0, sticky="e", pady=20)
        style_combobox.grid(row=5, column=1, padx=5, pady=20, sticky="w")
        api_key_label.grid(row=6, column=0, sticky="e", pady=5)
        api_key_entry.grid(row=6, column=1, padx=5, pady=20, sticky="w")
        proxy_label.grid(row=7, column=0, sticky="e", pady=5)
        proxy_entry.grid(row=7, column=1, padx=5, pady=20, sticky="w")
        generate_button.grid(row=8, column=0, columnspan=2, pady=30)

        # 右侧框架部件
        prev_button = ttk.Button(self.right_frame, text="< Prev", command=self.show_previous_image)
        next_button = ttk.Button(self.right_frame, text="Next >", command=self.show_next_image)
        self.image_label = tk.Label(self.right_frame)

        # 在右侧框架布局部件
        prev_button.grid(row=0, column=0, padx=5, pady=5)
        next_button.grid(row=0, column=1, padx=5, pady=5)
        self.image_label.grid(row=1, column=1, rowspan=9, padx=10, pady=10)

        # 设置风格
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", background="sky blue")
        style.configure("TCombobox", background="light blue")  # 修改此行为浅蓝色
        style.configure("TEntry", background="light blue")  # 修改此行为浅蓝色
        style.configure("TButton", background="sky blue")

    def generate_image(self):
        model = self.model_var.get()
        prompt = self.prompt_var.get()
        size = self.size_var.get()
        n = int(self.n_var.get())
        quality = self.quality_var.get()
        style = self.style_var.get()
        api_keys = self.api_key_var.get().split(",")
        proxy = self.proxy_var.get()

        openai.api_key = random.choice(api_keys)
        openai.api_base = proxy  # 设置代理

        params = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size,
            "quality": quality,
            "style": style
        }

        threading.Thread(target=self.process_image_generation, args=(params,)).start()

    def process_image_generation(self, params):
        try:
            response = openai.Image.create(**params)
            self.image_paths = [image['url'] for image in response['data']]
            for i, image_path in enumerate(self.image_paths):
                prompt = self.prompt_var.get()
                self.save_image(image_path, f"{prompt}_{i}.jpg")
            self.show_image(0)
            self.save_config()
        except Exception as e:
            print(f"Error during image generation: {e}")

    def show_image(self, index):
        if 0 <= index < len(self.image_paths):
            img = Image.open(self.load_image(self.image_paths[index]))
            # 图像大小调整
            img = img.resize((512, 512))
            tk_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=tk_img)
            self.image_label.photo = tk_img
            self.current_image_index = index

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.show_image(self.current_image_index - 1)

    def show_next_image(self):
        if self.current_image_index < len(self.image_paths) - 1:
            self.show_image(self.current_image_index + 1)

    def save_image(self, image_url, file_name):
        response = requests.get(image_url)
        image_content = response.content
        with open(file_name, "wb") as image_file:
            image_file.write(image_content)

    def load_image(self, image_url):
        response = requests.get(image_url)
        image_content = response.content
        image = Image.open(BytesIO(image_content))
        prompt = self.prompt_var.get()
        temp_path = f"{prompt}_{self.current_image_index}.jpg"  # 修改图片命名为prompt+i
        image.save(temp_path, "JPEG")
        return temp_path

    def save_config(self):
        config = {
            "model": self.model_var.get(),
            "prompt": self.prompt_var.get(),
            "size": self.size_var.get(),
            "n": self.n_var.get(),
            "quality": self.quality_var.get(),
            "style": self.style_var.get(),
            "api_keys": self.api_key_var.get(),
            "proxy": self.proxy_var.get()
        }
        with open("dalle-config.json", "w") as config_file:
            json.dump(config, config_file)

    def load_config(self):
        try:
            with open("dalle-config.json", "r") as config_file:
                config = json.load(config_file)
                self.model_var.set(config.get("model", ""))
                self.prompt_var.set(config.get("prompt", ""))
                self.size_var.set(config.get("size", ""))
                self.n_var.set(config.get("n", ""))
                self.quality_var.set(config.get("quality", ""))
                self.style_var.set(config.get("style", ""))
                self.api_key_var.set(config.get("api_keys", ""))
                self.proxy_var.set(config.get("proxy", ""))
        except FileNotFoundError:
            self.save_config()

    def on_closing(self):
        # 窗口关闭时保存配置
        self.save_config()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGenerationApp(root)
    root.geometry("888x600")
    root.resizable(False, False)
    root.mainloop()