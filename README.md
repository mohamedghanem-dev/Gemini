# Gemini WebView (Android)

تطبيق أندرويد بسيط بيفتح https://gemini.google.com/ جوه WebView، وبيتبني APK أوتوماتيك بـ GitHub Actions.

## البناء
1. ارفع المحتوى كله على مستودع GitHub (فرع `main`).
2. افتح تبويب **Actions** ← **Build Gemini APK** ← (بيشتغل لوحده مع أي push أو دوس *Run workflow*).
3. بعد ما يخلص، نزّل الـ artifact اسمه **Gemini-Android-APK** (جواه `app-debug.apk`).

## الأيقونة
متولدة من `assets-src/icon-source.jpg`. لو غيرتها شغّل:
`pip install Pillow numpy && python3 tools/make_icons.py`
