<div align="center">
  <h1>🥷 WEBHOOK-HUNTER</h1>
  <p><strong>Shadow Username Hunter — إصطياد اليوزرات النادرة + إرسال إلى Webhook</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
    <img src="https://img.shields.io/badge/Termux-Compatible-brightgreen?style=for-the-badge&logo=android">
    <img src="https://img.shields.io/badge/License-NINJA%20%E2%84%A2-red?style=for-the-badge">
    <img src="https://img.shields.io/badge/Discord-in7j-7289DA?style=for-the-badge&logo=discord">
  </p>
</div>

---

## 🎯 ما هي الأداة؟

**WEBHOOK-HUNTER** هي أداة متخصصة في **إصطياد اليوزرنيمات النادرة** (ثلاثية، رباعية، خماسية) على أشهر المنصات، مع إرسال النتائج **فوراً إلى Webhook** (Discord/Telegram).

---

## 🚀 الميزات

| الميزة | الوصف |
|--------|-------|
| ✅ **يعمل على Termux** | متوافق مع Android بالكامل |
| ✅ **10+ منصة** | Instagram, Twitter, GitHub, TikTok, Snapchat, Reddit, Pinterest, Twitch, YouTube, Telegram |
| ✅ **يوزرات ثلاثية** | 3 أحرف — نادرة جداً |
| ✅ **يوزرات رباعية** | 4 أحرف — نادرة |
| ✅ **يوزرات خماسية** | 5 أحرف — متوسطة الندرة |
| ✅ **إرسال إلى Webhook** | Discord / Telegram Webhook |
| ✅ **توليد ذكي** | يمنع الرموز المتتالية |
| ✅ **حفظ النتائج** | JSON + TXT محلياً |
| ✅ **واجهة فخمة** | أنيميشن + ألوان جذابة |

---

## 📦 التثبيت على Termux

```bash
# تحديث الحزم
pkg update && pkg upgrade -y

# تثبيت الأدوات الأساسية
pkg install git python python-pip -y

# تحميل الأداة
git clone https://github.com/in7j/WEBHOOK-HUNTER.git
cd WEBHOOK-HUNTER

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل الأداة
python3 webhook_hunter.py 