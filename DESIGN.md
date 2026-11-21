# Shield — Design Document
> BFB.AI · Built For Benefits, by AI

## الهوية
- **فئة التطبيق:** أمان/خصوصية
- **المزاج:** Cyber + Glassmorphism خفيف + إحساس بالثقة
- **جملة الهوية:** "هادئ، دقيق، يبعث على الثقة — درع رقمي أنيق"

## وضع جوجل
**A) بدون خدمات جوجل (Open)** — لا SDK لجوجل في الكود إطلاقاً.

## Design Tokens
- **Primary:** #00A6A6 (سماوي نيون)
- **Secondary:** #0B1B3A (أزرق ليلي)
- **Accent:** #00D4AA (أخضر نيون)
- **Background Light:** #F5F7FA / **Dark:** #0B1B3A / **AMOLED:** #000000
- **Surface Light:** #FFFFFF / **Dark:** #13264D
- **Error:** #FF5A5F / **Success:** #2ECC71 / **Warning:** #F5A623

## الخطوط
- عربي عناوين: Cairo Bold 700
- عربي نصوص: IBM Plex Sans Arabic 400/500
- لاتيني: Inter
- أكواد: JetBrains Mono
- **ممنوع:** DejaVu Sans

## الأشكال
- بطاقات: 16dp / أزرار: 12dp / شبكة: 8dp
- ظل: elevation 2dp

## الحركة
- Duration: 250ms / Easing: cubic-bezier(0.4, 0.0, 0.2, 1)
- تحترم "تقليل الحركة"

## الأيقونة
- درع هندسي + نقطة مركزية مضيئة
- خلفية: تدرج #0B1B3A → #1E3A5F
- رمز: #4DE1E1 سماوي نيون
- Adaptive Icon + Monochrome لـ Themed Icons

## شاشة Appearance (4.9)
- 6 ثيمات جاهزة: Default, Light, Dark, AMOLED, High Contrast, Midnight Gold
- تخصيص كامل: Primary/Secondary/Accent/Background/Surface
- استيراد/تصدير `.bfbtheme` (JSON, schema 1, حد 64KB)
- فحص التباين ≥ 4.5:1 تلقائياً
- مصدر واحد للحقيقة: ThemeRepository (DataStore)

## توقيع BFB.AI
- **About:** سطر "Built with BFB.AI" + المعنى بالعربي والإنجليزي
- **Splash:** توقيع صغير أسفل الشاشة (مستقبل)
- **README/Changelog/تقرير أمني:** ترويسة `BFB.AI · Built For Benefits, by AI`
- **كل ملف Kotlin:** تعليق `// Built with BFB.AI — Built For Benefits, by AI`
- **ملفات الشعار:** `assets/brand/BFB_light.svg`, `BFB_dark.svg`, `BFB_mono.svg`
- **ملفات ZIP:** `BFB.txt` داخل كل حزمة
