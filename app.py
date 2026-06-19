import os
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# المجلدات الأساسية لحفظ البيانات
DATA_DIR = "employees_data"
IMAGES_DIR = "employees_images"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

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

# واجهة المستخدم (HTML المعروضة في المتصفح)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام تسجيل الموظفين</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .container { background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 500px; text-align: center; }
        h2 { color: #333; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; text-align: right; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        input[type="text"], input[type="tel"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        #camera-container { margin: 20px 0; background: #eee; border-radius: 8px; overflow: hidden; position: relative; height: 240px; }
        video, canvas { width: 100%; height: 100%; object-fit: cover; }
        canvas { display: none; }
        button { background-color: #4CAF50; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; }
        button:hover { background-color: #45a049; }
        .status { margin-top: 15px; font-weight: bold; color: #2c3e50; }
    </style>
</head>
<body>

<div class="container">
    <h2>تسجيل موظف جديد</h2>
    
    <div class="form-group">
        <label>الاسم الأول:</label>
        <input type="text" id="firstName" required>
    </div>
    
    <div class="form-group">
        <label>الاسم المستعار:</label>
        <input type="text" id="nickname">
    </div>
    
    <div class="form-group">
        <label>رقم الهاتف:</label>
        <input type="tel" id="phone" required>
    </div>

    <div id="camera-container">
        <video id="video" autoplay playsinline></video>
        <canvas id="canvas"></canvas>
    </div>

    <button type="button" onclick="captureAndSubmit()">التقاط الصورة وحفظ البيانات</button>
    
    <div class="status" id="statusMsg"></div>
</div>

<script>
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const statusMsg = document.getElementById('statusMsg');

    // تشغيل الكاميرا فور فتح الصفحة
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => { video.srcObject = stream; })
        .catch(err => {
            console.error("خطأ في تشغيل الكاميرا: ", err);
            statusMsg.innerText = "تنبيه: لم نتمكن من تشغيل الكاميرا، يرجى إعطاء الصلاحية.";
            statusMsg.style.color = "red";
        });

    function captureAndSubmit() {
        const firstName = document.getElementById('firstName').value.trim();
        const nickname = document.getElementById('nickname').value.trim();
        const phone = document.getElementById('phone').value.trim();

        if (!firstName || !phone) {
            alert("الرجاء ملء حقول الاسم الأول ورقم الهاتف!");
            return;
        }

        statusMsg.innerText = "جاري الحفظ والالتقاط...";
        statusMsg.style.color = "#333";

        // التقاط الصورة من الفيديو ورسمها على الـ Canvas
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // تحويل الصورة إلى صيغة Base64 لإرسالها للسيرفر
        const imageData = canvas.toDataURL('image/jpeg');

        // إرسال البيانات عبر Ajax (Fetch API) إلى السيرفر
        fetch('/save_employee', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                first_name: firstName,
                nickname: nickname,
                phone: phone,
                image: imageData
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                statusMsg.innerText = `تم تسجيل الموظف بنجاح برقم: ${data.emp_id}`;
                statusMsg.style.color = "green";
                // تفريغ الحقول بعد النجاح
                document.getElementById('firstName').value = '';
                document.getElementById('nickname').value = '';
                document.getElementById('phone').value = '';
            } else {
                statusMsg.innerText = "حدث خطأ أثناء حفظ البيانات.";
                statusMsg.style.color = "red";
            }
        })
        .catch(err => {
            statusMsg.innerText = "خطأ في الاتصال بالسيرفر.";
            statusMsg.style.color = "red";
            console.error(err);
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
        image_data = data.get('image')

        # الحصول على المعرّف التلقائي للموظف
        emp_id = get_next_employee_id()

        # معالجة الصورة وحفظها (تحويل من base64 إلى ملف jpg)
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        
        image_filename = f"employee_{emp_id}.jpg"
        image_path = os.path.join(IMAGES_DIR, image_filename)
        with open(image_path, "wb") as f:
            f.write(image_bytes)

        # حفظ البيانات النصية في ملف مرقم تلقائياً
        text_filename = f"employee_{emp_id}.txt"
        text_path = os.path.join(DATA_DIR, text_filename)
        with open(text_path, "w", encoding="utf-8") as file:
            file.write(f"رقم الموظف: {emp_id}\n")
            file.write(f"الاسم الأول: {first_name}\n")
            file.write(f"الاسم المستعار: {nickname}\n")
            file.write(f"رقم الهاتف: {phone}\n")
            file.write(f"اسم ملف الصورة: {image_filename}\n")

        return jsonify({"success": True, "emp_id": emp_id})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    # تشغيل السيرفر ليكون متاحاً عبر الشبكة المحلية أو الخادم
    app.run(host='0.0.0.0', port=5000, debug=True)