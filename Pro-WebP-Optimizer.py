import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import threading
import io

# إعداد المظهر العام
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

TEXTS = {
    "ar": {
        "app_title": "مُحسن وصانع صور WebP الاحترافي Pro",
        "header": "تحسين وتحويل الصور إلى WebP",
        "subheader": "أداء عالي ومعاينة حية بدون تعليق (Debounced Live Preview)",
        "tab_basic": "الإعدادات الأساسية",
        "tab_adv": "الإعدادات المتقدمة",
        "select_btn": "📁 اختيار الصور (PNG, JPG...)",
        "no_files": "لم يتم اختيار أي صور",
        "quality": "جودة الصورة (الافتراضي 85%):",
        "scale": "أبعاد الصورة (% من الأصل):",
        "lossless": "تفعيل الضغط الذكي بدون فقدان الجودة (Lossless)",
        "keep_exif": "الاحتفاظ بالبيانات الوصفية للصور (EXIF)",
        "suffix": "لاحقة الملف الجديد:",
        "convert_btn": "🚀 بدء تحويل الكل",
        "converting": "⏳ جاري المعالجة الرقمية...",
        "success": "تم التحويل بنجاح!",
        "alert": "تنبيه من النظام",
        "select_first": "الرجاء اختيار صور أولاً لبدء العمل!",
        "stats": "تم توفير {:.2f} MB (تقلص الحجم بنسبة {:.1f}%)",
        "preview_panel": "🖥️ شاشة المعاينة الحية (المقارنة الرقمية)",
        "before": "قبل (الأصل)",
        "after": "بعد (المعاينة الحية)",
        "size_lbl": "الحجم: ",
        "resolution_lbl": "الأبعاد: ",
        "no_preview": "قم باختيار صورة لعرض المعاينة الحية قبل وبعد هنا",
        "zoom_in": "🔍+ تقريب",
        "zoom_out": "🔍- إبعاد",
        "zoom_reset": "🔄 إعادة الضبط"
    },
    "en": {
        "app_title": "Pro WebP Optimizer Suite",
        "header": "WebP Image Optimization Suite",
        "subheader": "High performance Debounced Live Preview",
        "tab_basic": "Basic Settings",
        "tab_adv": "Advanced Engine",
        "select_btn": "📁 Select Images (PNG, JPG...)",
        "no_files": "No images loaded",
        "quality": "Image Quality (Default 85%):",
        "scale": "Image Scale (% of original):",
        "lossless": "Enable Lossless Compression (No Quality Loss)",
        "keep_exif": "Keep Image Metadata (EXIF Data)",
        "suffix": "New File Suffix:",
        "convert_btn": "🚀 Start Batch Conversion",
        "converting": "⏳ Processing Images...",
        "success": "Conversion Successful!",
        "alert": "System Alert",
        "select_first": "Please select images first to begin!",
        "stats": "Saved {:.2f} MB (Size reduced by {:.1f}%)",
        "preview_panel": "🖥️ Live Workspace Preview (Comparison)",
        "before": "Before (Original)",
        "after": "After (Live Preview)",
        "size_lbl": "Size: ",
        "resolution_lbl": "Dim: ",
        "no_preview": "Select an image to display the live before/after comparison here",
        "zoom_in": "🔍+ Zoom In",
        "zoom_out": "🔍- Zoom Out",
        "zoom_reset": "🔄 Reset"
    }
}

class WebPConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_lang = "ar"  
        self.title(TEXTS[self.current_lang]["app_title"])
        self.geometry("1150x750")
        self.resizable(True, True)

        self.file_paths = []
        self.is_converting = False
        self.preview_raw_img = None 
        self.preview_opt_img = None 
        
        # متغيرات المعاينة المتقدمة
        self.preview_timer = None # لمنع التعليق (Debounce)
        self.zoom_factor = 1.0    # مستوى الزوم

        self.create_layout()
        self.update_ui_language()
        
        # الإعدادات الافتراضية
        self.quality_slider.set(85)
        self.lossless_var.set(False) # إيقاف Lossless لتفعيل التحكم بالجودة
        self.toggle_lossless()

    def create_layout(self):
        self.top_bar = ctk.CTkFrame(self, height=40, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=20, pady=(10, 0))
        
        self.lang_switch = ctk.CTkSwitch(self.top_bar, text="English UI", command=self.toggle_language)
        self.lang_switch.pack(side="right" if self.current_lang == "ar" else "left")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.control_panel = ctk.CTkFrame(self.main_container, width=420)
        self.control_panel.pack(side="right", fill="both", expand=False, padx=(10, 0))

        self.workspace_panel = ctk.CTkFrame(self.main_container)
        self.workspace_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.build_control_panel()
        self.build_workspace_panel()

    def build_control_panel(self):
        self.title_label = ctk.CTkLabel(self.control_panel, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 5), padx=15, anchor="e")

        self.subtitle_label = ctk.CTkLabel(self.control_panel, text="", text_color="gray", font=ctk.CTkFont(size=12))
        self.subtitle_label.pack(pady=(0, 15), padx=15, anchor="e")

        self.select_btn = ctk.CTkButton(self.control_panel, text="", command=self.select_files, height=42, font=ctk.CTkFont(weight="bold"))
        self.select_btn.pack(pady=10, padx=20, fill="x")

        self.files_label = ctk.CTkLabel(self.control_panel, text="", text_color="gray")
        self.files_label.pack(pady=(0, 10))

        self.tabs = ctk.CTkTabview(self.control_panel, height=240)
        self.tabs.pack(padx=15, pady=10, fill="both", expand=True)
        
        self.tab_basic = self.tabs.add("basic")
        self.tab_adv = self.tabs.add("adv")

        self.quality_label = ctk.CTkLabel(self.tab_basic, text="", font=ctk.CTkFont(weight="bold"))
        self.quality_label.pack(pady=(10, 0), padx=15, anchor="e")

        self.quality_slider = ctk.CTkSlider(self.tab_basic, from_=10, to=100, command=self.on_slider_change)
        self.quality_slider.pack(pady=5, padx=15, fill="x")

        self.quality_val_label = ctk.CTkLabel(self.tab_basic, text="85%")
        self.quality_val_label.pack()

        self.scale_label = ctk.CTkLabel(self.tab_basic, text="", font=ctk.CTkFont(weight="bold"))
        self.scale_label.pack(pady=(10, 0), padx=15, anchor="e")

        self.scale_slider = ctk.CTkSlider(self.tab_basic, from_=10, to=100, command=self.on_slider_change)
        self.scale_slider.set(100)
        self.scale_slider.pack(pady=5, padx=15, fill="x")

        self.scale_val_label = ctk.CTkLabel(self.tab_basic, text="100%")
        self.scale_val_label.pack()

        self.lossless_var = ctk.BooleanVar(value=False)
        self.lossless_checkbox = ctk.CTkCheckBox(self.tab_adv, text="", variable=self.lossless_var, command=self.toggle_lossless)
        self.lossless_checkbox.pack(pady=(20, 10), padx=15, anchor="e")

        self.exif_var = ctk.BooleanVar(value=False)
        self.exif_checkbox = ctk.CTkCheckBox(self.tab_adv, text="", variable=self.exif_var, command=self.trigger_preview_update)
        self.exif_checkbox.pack(pady=10, padx=15, anchor="e")

        self.suffix_frame = ctk.CTkFrame(self.tab_adv, fg_color="transparent")
        self.suffix_frame.pack(pady=10, padx=15, fill="x")
        
        self.suffix_label = ctk.CTkLabel(self.suffix_frame, text="")
        self.suffix_label.pack(side="right", padx=(0, 5))
        
        self.suffix_entry = ctk.CTkEntry(self.suffix_frame, width=140)
        self.suffix_entry.insert(0, "_optimized")
        self.suffix_entry.pack(side="right")

        self.progress_bar = ctk.CTkProgressBar(self.control_panel)
        self.progress_bar.pack(pady=(15, 2), padx=20, fill="x")
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self.control_panel, text="", text_color="#28a745", font=ctk.CTkFont(weight="bold"))
        self.status_label.pack(pady=(0, 5))

        self.convert_btn = ctk.CTkButton(self.control_panel, text="", command=self.start_conversion, height=48, fg_color="#28a745", hover_color="#218838", font=ctk.CTkFont(size=15, weight="bold"))
        self.convert_btn.pack(pady=(5, 20), padx=20, fill="x")

    def build_workspace_panel(self):
        # شريط علوي لمساحة العمل يحتوي على العنوان وأزرار الزوم
        self.workspace_header_frame = ctk.CTkFrame(self.workspace_panel, fg_color="transparent")
        self.workspace_header_frame.pack(fill="x", pady=10, padx=15)

        self.preview_panel_header = ctk.CTkLabel(self.workspace_header_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.preview_panel_header.pack(side="right" if self.current_lang == "ar" else "left")

        # أزرار الزوم (Zoom Controls)
        self.zoom_controls = ctk.CTkFrame(self.workspace_header_frame, fg_color="transparent")
        self.zoom_controls.pack(side="left" if self.current_lang == "ar" else "right")

        self.btn_zoom_out = ctk.CTkButton(self.zoom_controls, text="", width=60, command=lambda: self.change_zoom(-0.2))
        self.btn_zoom_out.pack(side="left", padx=2)
        
        self.btn_zoom_reset = ctk.CTkButton(self.zoom_controls, text="", width=60, fg_color="#555", hover_color="#444", command=lambda: self.change_zoom(0, reset=True))
        self.btn_zoom_reset.pack(side="left", padx=2)
        
        self.btn_zoom_in = ctk.CTkButton(self.zoom_controls, text="", width=60, command=lambda: self.change_zoom(0.2))
        self.btn_zoom_in.pack(side="left", padx=2)

        self.preview_split_frame = ctk.CTkFrame(self.workspace_panel, fg_color="#1e1e1e", border_width=1, border_color="#333333")
        self.preview_split_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.no_preview_label = ctk.CTkLabel(self.preview_split_frame, text="", text_color="gray", font=ctk.CTkFont(size=14))
        self.no_preview_label.place(relx=0.5, rely=0.5, anchor="center")

        # استخدام إطارات قابلة للتمرير لدعم الزوم (Scrollable Frames)
        self.before_frame = ctk.CTkScrollableFrame(self.preview_split_frame, fg_color="transparent")
        self.after_frame = ctk.CTkScrollableFrame(self.preview_split_frame, fg_color="transparent")

        self.before_title = ctk.CTkLabel(self.before_frame, text="", font=ctk.CTkFont(weight="bold"), text_color="#ffc107")
        self.before_title.pack(pady=5)
        self.before_img_label = ctk.CTkLabel(self.before_frame, text="")
        self.before_img_label.pack(expand=True, anchor="center", padx=5, pady=5)
        self.before_stats_label = ctk.CTkLabel(self.before_frame, text="", text_color="gray")
        self.before_stats_label.pack(pady=5)

        self.after_title = ctk.CTkLabel(self.after_frame, text="", font=ctk.CTkFont(weight="bold"), text_color="#00ced1")
        self.after_title.pack(pady=5)
        self.after_img_label = ctk.CTkLabel(self.after_frame, text="")
        self.after_img_label.pack(expand=True, anchor="center", padx=5, pady=5)
        self.after_stats_label = ctk.CTkLabel(self.after_frame, text="", text_color="gray")
        self.after_stats_label.pack(pady=5)

    def update_ui_language(self):
        lang = TEXTS[self.current_lang]
        
        self.title(lang["app_title"])
        self.title_label.configure(text=lang["header"])
        self.subtitle_label.configure(text=lang["subheader"])
        self.tabs._segmented_button._buttons_dict["basic"].configure(text=lang["tab_basic"])
        self.tabs._segmented_button._buttons_dict["adv"].configure(text=lang["tab_adv"])
        self.select_btn.configure(text=lang["select_btn"])
        if not self.file_paths:
            self.files_label.configure(text=lang["no_files"])
            self.no_preview_label.configure(text=lang["no_preview"])
            
        self.quality_label.configure(text=lang["quality"])
        self.scale_label.configure(text=lang["scale"])
        self.lossless_checkbox.configure(text=lang["lossless"])
        self.exif_checkbox.configure(text=lang["keep_exif"])
        self.suffix_label.configure(text=lang["suffix"])
        self.preview_panel_header.configure(text=lang["preview_panel"])
        
        self.before_title.configure(text=lang["before"])
        self.after_title.configure(text=lang["after"])
        
        # أزرار الزوم
        self.btn_zoom_in.configure(text=lang["zoom_in"])
        self.btn_zoom_out.configure(text=lang["zoom_out"])
        self.btn_zoom_reset.configure(text=lang["zoom_reset"])

        if not self.is_converting:
            self.convert_btn.configure(text=lang["convert_btn"])

        align = "w" if self.current_lang == "en" else "e"
        self.title_label.configure(anchor=align)
        self.subtitle_label.configure(anchor=align)
        self.quality_label.configure(anchor=align)
        self.scale_label.configure(anchor=align)
        
        side = "left" if self.current_lang == "en" else "right"
        self.preview_panel_header.pack_configure(side=side)
        self.zoom_controls.pack_configure(side="right" if self.current_lang == "ar" else "left")
        
        self.suffix_label.pack_configure(side=side)
        self.suffix_entry.pack_configure(side=side)
        
        self.trigger_preview_update()

    def toggle_language(self):
        self.current_lang = "en" if self.lang_switch.get() == 1 else "ar"
        self.update_ui_language()

    def toggle_lossless(self):
        state = "disabled" if self.lossless_var.get() else "normal"
        self.quality_slider.configure(state=state)
        self.trigger_preview_update()

    def on_slider_change(self, value):
        self.quality_val_label.configure(text=f"{int(self.quality_slider.get())}%")
        self.scale_val_label.configure(text=f"{int(self.scale_slider.get())}%")
        self.trigger_preview_update()

    def trigger_preview_update(self):
        """Debouncing: إلغاء الأمر القديم وتشغيل مؤقت جديد لمنع تعليق الواجهة"""
        if self.preview_timer:
            self.after_cancel(self.preview_timer)
        # انتظر 300 ملي ثانية (حتى يتوقف المستخدم عن تحريك المؤشر) ثم نفذ
        self.preview_timer = self.after(300, self.start_preview_thread)

    def start_preview_thread(self):
        if not self.preview_raw_img: return
        # تشغيل المعالجة في مسار منفصل تماماً عن الواجهة
        threading.Thread(target=self.process_preview_background, daemon=True).start()

    def change_zoom(self, amount, reset=False):
        if reset:
            self.zoom_factor = 1.0
        else:
            self.zoom_factor += amount
            # منع تصغير الصورة بشكل يختفي
            if self.zoom_factor < 0.2: self.zoom_factor = 0.2
            if self.zoom_factor > 5.0: self.zoom_factor = 5.0
            
        self.render_preview_images()

    def select_files(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp")]
        paths = filedialog.askopenfilenames(title="Select Images", filetypes=filetypes)
        
        if paths:
            self.file_paths = list(paths)
            file_word = "files" if self.current_lang == "en" else "صور تم تحميلها"
            self.files_label.configure(text=f"{len(self.file_paths)} {file_word}", text_color="#00BFFF")
            self.status_label.configure(text="")
            
            self.no_preview_label.place_forget()
            self.before_frame.pack(side="left", fill="both", expand=True)
            self.after_frame.pack(side="right", fill="both", expand=True)
            
            self.preview_raw_img = Image.open(self.file_paths[0])
            self.zoom_factor = 1.0 # تصفير الزوم عند اختيار صور جديدة
            self.trigger_preview_update()

    def process_preview_background(self):
        """هذه الوظيفة تعمل في الخلفية ولا تسبب أي تعليق"""
        lang = TEXTS[self.current_lang]
        path = self.file_paths[0]
        
        orig_width, orig_height = self.preview_raw_img.width, self.preview_raw_img.height
        orig_size_kb = os.path.getsize(path) / 1024
        before_text = f"{lang['resolution_lbl']}{orig_width}x{orig_height}px  |  {lang['size_lbl']}{orig_size_kb:.1f} KB"

        try:
            scale_val = int(self.scale_slider.get()) / 100.0
            quality_val = int(self.quality_slider.get())
            is_lossless = self.lossless_var.get()
            keep_exif = self.exif_var.get()

            preview_work_img = self.preview_raw_img.copy()

            if scale_val < 1.0:
                new_w = int(orig_width * scale_val)
                new_h = int(orig_height * scale_val)
                preview_work_img = preview_work_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            save_kwargs = {"format": "webp", "method": 4, "lossless": is_lossless} 
            if not is_lossless:
                save_kwargs["quality"] = quality_val
            if keep_exif and 'exif' in preview_work_img.info:
                save_kwargs["exif"] = preview_work_img.info['exif']
                
            preview_work_img.save(buffer, **save_kwargs)
            opt_size_kb = len(buffer.getvalue()) / 1024
            
            comp_ratio = ((orig_size_kb - opt_size_kb) / orig_size_kb) * 100 if orig_size_kb > 0 else 0
            after_text = f"{lang['resolution_lbl']}{preview_work_img.width}x{preview_work_img.height}px  |  {lang['size_lbl']}{opt_size_kb:.1f} KB (-{comp_ratio:.1f}%)"

            buffer.seek(0)
            self.preview_opt_img = Image.open(buffer).copy() # حفظ الصورة المعالجة في الذاكرة للزوم
            
            # العودة للمسار الرئيسي لتحديث الواجهة بأمان
            self.after(0, self.update_preview_ui, before_text, after_text)

        except Exception as e:
            print(f"Error in background preview: {e}")

    def update_preview_ui(self, before_text, after_text):
        """تحديث النصوص والواجهة من الـ Main Thread"""
        self.before_stats_label.configure(text=before_text)
        self.after_stats_label.configure(text=after_text)
        self.render_preview_images()

    def render_preview_images(self):
        """رسم الصور وعمل الزوم"""
        if not self.preview_raw_img or not self.preview_opt_img:
            return
            
        # الحجم الأساسي للمعاينة (الـ Fit Screen)
        base_w, base_h = 350, 350
        
        # حساب أبعاد الصورة قبل المعالجة
        w_orig, h_orig = self.preview_raw_img.size
        scale_orig = min(base_w / w_orig, base_h / h_orig)
        disp_w_orig = int(w_orig * scale_orig * self.zoom_factor)
        disp_h_orig = int(h_orig * scale_orig * self.zoom_factor)
        
        # حساب أبعاد الصورة بعد المعالجة (قد تكون أصغر بسبب شريط الأبعاد)
        w_opt, h_opt = self.preview_opt_img.size
        scale_opt = min(base_w / w_opt, base_h / h_opt)
        disp_w_opt = int(w_opt * scale_opt * self.zoom_factor)
        disp_h_opt = int(h_opt * scale_opt * self.zoom_factor)

        # تحديث الصور في الواجهة
        ctk_img_before = ctk.CTkImage(light_image=self.preview_raw_img, dark_image=self.preview_raw_img, size=(disp_w_orig, disp_h_orig))
        self.before_img_label.configure(image=ctk_img_before)
        
        ctk_img_after = ctk.CTkImage(light_image=self.preview_opt_img, dark_image=self.preview_opt_img, size=(disp_w_opt, disp_h_opt))
        self.after_img_label.configure(image=ctk_img_after)

    def start_conversion(self):
        if not self.file_paths:
            messagebox.showwarning(TEXTS[self.current_lang]["alert"], TEXTS[self.current_lang]["select_first"])
            return

        save_dir = filedialog.askdirectory(title="Save Directory")
        if not save_dir:
            return

        self.is_converting = True
        self.convert_btn.configure(state="disabled", text=TEXTS[self.current_lang]["converting"])
        self.select_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="")

        threading.Thread(target=self.process_images_batch, args=(save_dir,), daemon=True).start()

    def process_images_batch(self, save_dir):
        quality_val = int(self.quality_slider.get())
        scale_val = int(self.scale_slider.get()) / 100.0
        is_lossless = self.lossless_var.get()
        keep_exif = self.exif_var.get()
        suffix = self.suffix_entry.get()

        total_files = len(self.file_paths)
        original_size_bytes = 0
        new_size_bytes = 0

        for index, path in enumerate(self.file_paths):
            try:
                original_size_bytes += os.path.getsize(path)
                img = Image.open(path)
                
                if scale_val < 1.0:
                    new_width = int(img.width * scale_val)
                    new_height = int(img.height * scale_val)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                exif = img.info.get('exif') if keep_exif else None
                filename = os.path.basename(path)
                name, _ = os.path.splitext(filename)
                new_filepath = os.path.join(save_dir, f"{name}{suffix}.webp")

                save_kwargs = {
                    "format": "webp",
                    "method": 6, 
                    "lossless": is_lossless
                }
                if not is_lossless:
                    save_kwargs["quality"] = quality_val
                if exif:
                    save_kwargs["exif"] = exif

                img.save(new_filepath, **save_kwargs)
                new_size_bytes += os.path.getsize(new_filepath)
                
                progress = (index + 1) / total_files
                self.progress_bar.set(progress)
                
            except Exception as e:
                print(f"Error processing file {path}: {e}")

        saved_bytes = original_size_bytes - new_size_bytes
        saved_mb = saved_bytes / (1024 * 1024)
        reduction_percent = (saved_bytes / original_size_bytes * 100) if original_size_bytes > 0 else 0

        self.is_converting = False
        lang = TEXTS[self.current_lang]
        self.after(0, self.finish_conversion, lang, saved_mb, reduction_percent)

    def finish_conversion(self, lang, saved_mb, reduction_percent):
        self.convert_btn.configure(state="normal", text=lang["convert_btn"])
        self.select_btn.configure(state="normal")
        self.file_paths = []
        self.preview_raw_img = None
        self.preview_opt_img = None
        self.files_label.configure(text=lang["no_files"], text_color="gray")
        
        self.before_frame.pack_forget()
        self.after_frame.pack_forget()
        self.no_preview_label.configure(text=lang["no_preview"])
        self.no_preview_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.status_label.configure(text=lang["success"])
        
        stats_msg = lang["stats"].format(max(0, saved_mb), max(0, reduction_percent))
        messagebox.showinfo(lang["alert"], f"{lang['success']}\n\n{stats_msg}")

if __name__ == "__main__":
    app = WebPConverterApp()
    app.mainloop()