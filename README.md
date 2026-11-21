# 🛡️ Shield — Privacy Screen Protector

> BFB.AI · Built For Benefits, by AI

تطبيق أندرويد خفيف يوفّر طبقة خصوصية فوق الشاشة (Privacy Overlay) تُفعَّل بضغطة واحدة من **الإعدادات السريعة** (Quick Settings Tile).

## ✨ المميزات
- ⚡ **تشغيل بضغطة واحدة** من Quick Settings Tile
- 🎨 **4 أنماط للخصوصية**: ستارة كاملة، شبكة خطية، شبكة نقطية، منطقة تركيز
- 🌈 **تخصيص كامل للألوان** والشفافية والكثافة
- 🎭 **6 ثيمات جاهزة** + تصدير/استيراد ثيمات `.bfbtheme`
- 🌙 **دعم الوضع الليلي والنهاري + AMOLED**
- 🌐 **دعم العربية (RTL) والإنجليزية (LTR)**
- 📱 **يعمل على Android 7.0+ و HarmonyOS**
- 🚫 **بدون Google Play Services** — مستقل تماماً
- 🔒 **توقيع BFB.AI** في كل مكان

## 📲 التثبيت
حمّل APK من **Actions → Artifacts** بعد نجاح الـ workflow.

## 🛠️ البناء من المصدر
```bash
git clone https://github.com/Mohammedazizhedia/Shield.git
cd Shield
./gradlew assembleDebug
```

## 📖 الاستخدام
1. افتح التطبيق → امنح صلاحية **"الظهور فوق التطبيقات"**
2. اسحب شريط الإعدادات السريعة → أضف بلاطة **"درع الخصوصية"**
3. اضغط البلاطة لتفعيل/إيقاف الطبقة فوراً

## 🔐 الأمان
- ProGuard/R8 مفعّل في Release
- كشف Root/Debugger (تنبيه فقط)
- Smart Crash Reporter مع تحكم كامل من المستخدم
- 0 اعتماد على GMS

## 📜 الترخيص
MIT License

---
*Built with BFB.AI — Built For Benefits, by AI*
