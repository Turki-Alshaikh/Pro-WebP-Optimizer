# 🖼️ Pro WebP Optimizer Suite | المُحسّن الاحترافي لصور WebP

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-brightgreen)
![Pillow](https://img.shields.io/badge/Image_Processing-Pillow-yellow)
![License](https://img.shields.io/badge/License-MIT-orange)

تطبيق سطح مكتب احترافي ومفتوح المصدر، مبني بلغة بايثون (Python) لتحسين، ضغط، وتحويل الصور إلى صيغة الجيل الجديد **WebP**. صُمم هذا البرنامج خصيصاً لمطوري الويب، خبراء تحسين محركات البحث (SEO)، وأصحاب المتاجر الإلكترونية لتقليل أحجام الصور لأقصى حد مع الحفاظ على أعلى جودة ممكنة.

---

## ✨ المميزات الرئيسية (Key Features)

* **⚡ معاينة حية بدون تعليق (Debounced Live Preview):** تقنية محاكاة في الذاكرة العشوائية (RAM) تتيح لك رؤية حجم الصورة المتوقع ونسبة الضغط فورياً أثناء تعديل الإعدادات، دون تجميد واجهة المستخدم.
* **🔍 نظام تقريب متقدم (Zoom Controls):** فحص دقيق للبكسلات قبل وبعد الضغط (Zoom In/Out) لضمان جودة تفاصيل المنتجات أو الرسوميات.
* **🌍 دعم ثنائي اللغة (Bilingual UI):** تبديل فوري وسلس بين الواجهة العربية والإنجليزية بضغطة زر.
* **🚀 معالجة دفعات متعددة (Batch Processing):** تحويل عشرات أو مئات الصور دفعة واحدة بسلاسة تامة، بفضل الاعتماد على المعالجة الخلفية (Multi-Threading).
* **🎛️ تحكم دقيق بالجودة:**
  * دعم الضغط الذكي بدون فقدان الجودة (Lossless).
  * خيار إزالة أو الاحتفاظ بالبيانات الوصفية (EXIF Data) لحماية الخصوصية وتقليل الحجم.
  * تغيير أبعاد الصور (% Scale) تلقائياً.
* **📊 إحصائيات ذكية:** حساب وعرض مقدار المساحة الموفرة (بالميجابايت) ونسبة تقليص الحجم فور انتهاء التحويل.

---

## 🛠️ التقنيات المستخدمة (Technologies)

* **Python:** Core Logic & Multi-threading.
* **CustomTkinter:** Modern, Dark-mode first UI.
* **Pillow (PIL):** Advanced Image processing and WebP conversion engine.
* **io.BytesIO:** In-memory image processing for lightning-fast live previews.

---

## 💡 حالات الاستخدام (Use Cases)

* **تحسين محركات البحث (SEO):** تقليل أحجام الصور لرفع سرعة تحميل الصفحات وتحسين تقييمات (Core Web Vitals).
* **المتاجر الإلكترونية:** تجهيز صور المنتجات بدقة عالية وأحجام خفيفة جداً لتحسين تجربة العملاء وتقليل معدل الارتداد (Bounce Rate)، مما يساهم في رفع تقييم (Google Merchant Center).
* **تطوير الويب:** أداة محلية (Local Tool) تضمن خصوصية ملفاتك وتغنيك عن خدمات ضغط الصور السحابية المدفوعة.

---

## 🚀 التثبيت والتشغيل (Installation & Usage)

1. **استنساخ المستودع (Clone the repository):**
   ```bash
   git clone [https://github.com/yourusername/Pro-WebP-Optimizer.git](https://github.com/yourusername/Pro-WebP-Optimizer.git)
   cd Pro-WebP-Optimizer
