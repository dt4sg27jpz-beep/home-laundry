if "global_bookings" not in st.session_state:
    st.session_state["global_bookings"] = []
import streamlit as st
import datetime
import pandas as pd

# إعدادات المظهر الفخم والواجهة الاحترافية
st.set_page_config(
    page_title="المنظم الذكي | غسيل وتجفيف البيت", 
    page_icon="🧺", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# تحسين المظهر باستخدام CSS مخصص لجعله فخماً ومريحاً للعين
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        background-color: #4A90E2;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #357ABD; }
    .reportview-container .sidebar-content { background-color: #1E293B; color: white; }
    h1 { color: #1E293B; font-family: 'Cairo', sans-serif; text-align: center; }
    h2, h3 { color: #2C3E50; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ نظام إدارة الغسالة والنشافة الذكي")
st.markdown("<p style='text-align: center; color: #7F8C8D;'>المنصة الفخمة لتنظيم أوقات الغسيل والتجفيف العائلي بكل سهولة وبدون تضارب بتوقيت الرياض</p>", unsafe_allow_html=True)

# قاعدة بيانات خفيفة وسريعة في ذاكرة المتصفح لمنع التعليق
if 'bookings' not in st.session_state:
   st.session_state.bookings = st.session_state["global_bookings"] 
if 'is_coming' not in st.session_state:
    st.session_state.is_coming = {}
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_password' not in st.session_state:
    st.session_state.user_password = None

# ----------------- 🔑 شاشة تسجيل الدخول الفخمة -----------------
if st.session_state.user_name is None:
    st.markdown("<div style='background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
    st.subheader("🔒 تسجيل الدخول السريع")
    with st.form("login_form"):
        login_name = st.text_input("👤 اكتب اسمك الكريم:")
        login_pass = st.text_input("🔑 ضع رمزك السري الخاص (لحماية حجوزاتك):", type="password")
        login_submit = st.form_submit_button("دخول آمن إلى النظام ←")
        
    if login_submit:
        if not login_name or not login_pass:
            st.warning("⚠️ الرجاء إدخال الاسم والرمز السري للدخول")
    else:
            # إنشاء صندوق حفظ عام لأسماء العائلة الممسجلة إذا لم يكن موجوداً
            if "registered_users" not in st.session_state["global_bookings"]:
                if "family_accounts" not in st.session_state:
                    st.session_state["family_accounts"] = {
                        "turki": {"name": "تركي", "password": "123"},
                        "abdullah": {"name": "عبد الله", "password": "456"}
                    }

            # خيار إضافي لإنشاء حساب جديد بنفس الشاشة
            st.markdown("---")
            action = st.radio("هل لديك حساب؟", ["تسجيل الدخول 🔒", "إنشاء حساب جديد 👥"], horizontal=True)
            
            if action == "إنشاء حساب جديد 👥":
                new_user = st.text_input("اختر اسم مستخدم (بالإنجليزي):", key="reg_user").strip().lower()
                new_name = st.text_input("اكتب اسمك الكريم (بالعربي):", key="reg_name").strip()
                new_pass = st.text_input("اختر رمزك السري الجديد:", type="password", key="reg_pass")
                
                if st.form_submit_button("🚀 تسجيل حسابي الجديد"):
                    if not new_user or not new_name or not new_pass:
                        st.error("⚠️ يرجى تعبئة جميع الخانات!")
                    elif new_user in st.session_state["family_accounts"]:
                        st.error("❌ اسم المستخدم هذا محجوز لشخص آخر في البيت!")
                    else:
                        st.session_state["family_accounts"][new_user] = {"name": new_name, "password": new_pass}
                        st.success(f"✅ تم إنشاء حسابك بنجاح يا {new_name}! اختر الآن 'تسجيل الدخول' للدخول.")
            
            else:
                user_key = login_name.strip().lower()
                if user_key in st.session_state["family_accounts"] and st.session_state["family_accounts"][user_key]["password"] == login_pass:
                    st.session_state.user_name = st.session_state["family_accounts"][user_key]["name"]
                    st.session_state.user_password = login_pass
                    st.success(f"✨ مرحباً بك يا {st.session_state.user_name}! يتم الآن تحميل لوحة التحكم...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو الرمز السري غير صحيح!")
    st.stop()

# ----------------- 📖 شريط التحكم ودليل الاستخدام الفخم (Sidebar) -----------------
st.sidebar.markdown(f"<h2 style='color: #4A90E2; text-align:center;'>👑 لوحة التحكم</h2>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='text-align:center;'>المستخدم الحالي: <b>{st.session_state.user_name}</b></p>", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("### 📖 دليل الاستخدام السريع")
with st.sidebar.expander("💡 اضغط لقراءة القوانين"):
    st.markdown("""
    * **🔐 أمان حجزك:** اسمك ورقمك السري يحميان حجزك تلقائياً من الحذف بواسطة الآخرين.
    * **⚠️ وقت الذروة (1-6 مساءً):** يفرض النظام **45 دقيقة كحد أقصى** للحجز الواحد لضمان العدالة للجميع.
    * **🏃‍♂️ زر أنا قادم:** اضغط عليه فور وصولك للجهاز لتثبيت نوبتك.
    * **⏱️ مهلة الـ 15 دقيقة:** إذا تأخرت 15 دقيقة دون الضغط على (أنا قادم)، يحق للشخص التالي إلغاء حجزك واستغلال الوقت.
    """)

st.sidebar.divider()
if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.user_name = None
    st.session_state.user_password = None
    st.rerun()

# الأوقات الحالية المسندة بدقة لمنع التعليق
now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3)
current_time = now.time()
current_date = now.date()

# ----------------- 1. عرض حالة الأجهزة والعداد التنازلي بفخامة -----------------
st.markdown("### 🤖 مراقبة الأجهزة مباشرة")

col_wash, col_dry = st.columns(2)

busy_wash = False
booking_wash = None
for b in st.session_state.bookings:
    if b['device'] == "الغسالة" and b['date'] == current_date and b['start_time'] <= current_time <= b['end_time']:
        busy_wash = True
        booking_wash = b
        break

busy_dry = False
booking_dry = None
for b in st.session_state.bookings:
    if b['device'] == "النشافة" and b['date'] == current_date and b['start_time'] <= current_time <= b['end_time']:
        busy_dry = True
        booking_dry = b
        break

# بطاقة الغسالة الفخمة
with col_wash:
    st.markdown("<div style='background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); border-top: 4px solid #2ECC71;'>", unsafe_allow_html=True)
    st.markdown("<h4>🧼 حالة الغسالة</h4>", unsafe_allow_html=True)
    if busy_wash:
        wash_id = f"{booking_wash['name']}_{booking_wash['start_time']}_wash"
        wash_confirmed = st.session_state.is_coming.get(wash_id, False)
        
        if wash_confirmed:
            st.warning(f"🏃‍♂️ **{booking_wash['name']}** موجود عند الغسالة")
        else:
            st.error(f"🔴 مشغولة بواسطة: **{booking_wash['name']}**")
            
        end_dt_wash = datetime.datetime.combine(current_date, booking_wash['end_time'])
        rem_wash = int((end_dt_wash - now).total_seconds() / 60)
        st.metric(label="الوقت المتبقي", value=f"{max(0, rem_wash)} دقيقة")
        
        start_dt_wash = datetime.datetime.combine(current_date, booking_wash['start_time'])
        if ((now - start_dt_wash).total_seconds() / 60) > 15 and not wash_confirmed:
            st.error("⏱️ متأخر عن النوبة (+15 دقيقة)!")
            
        if not wash_confirmed and st.session_state.user_name == booking_wash['name']:
            if st.button("🏃‍♂️ أنا عند الغسالة الآن", key="btn_wash_come"):
                st.session_state.is_coming[wash_id] = True
                st.rerun()
    else:
        st.success("🟢 متاحة وجاهزة فوراً")
    st.markdown("</div>", unsafe_allow_html=True)

# بطاقة النشافة الفخمة
with col_dry:
    st.markdown("<div style='background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); border-top: 4px solid #3498DB;'>", unsafe_allow_html=True)
    st.markdown("<h4>💨 حالة النشافة</h4>", unsafe_allow_html=True)
    if busy_dry:
        dry_id = f"{booking_dry['name']}_{booking_dry['start_time']}_dry"
        dry_confirmed = st.session_state.is_coming.get(dry_id, False)
        
        if dry_confirmed:
            st.warning(f"🏃‍♂️ **{booking_dry['name']}** موجود عند النشافة")
        else:
            st.error(f"🔴 مشغولة بواسطة: **{booking_dry['name']}**")
            
        end_dt_dry = datetime.datetime.combine(current_date, booking_dry['end_time'])
        rem_dry = int((end_dt_dry - now).total_seconds() / 60)
        st.metric(label="الوقت المتبقي", value=f"{max(0, rem_dry)} دقيقة")
        
        start_dt_dry = datetime.datetime.combine(current_date, booking_dry['start_time'])
        if ((now - start_dt_dry).total_seconds() / 60) > 15 and not dry_confirmed:
            st.error("⏱️ متأخر عن النوبة (+15 دقيقة)!")
            
        if not dry_confirmed and st.session_state.user_name == booking_dry['name']:
            if st.button("🏃‍♂️ أنا عند النشافة الآن", key="btn_dry_come"):
                st.session_state.is_coming[dry_id] = True
                st.rerun()
    else:
        st.success("🟢 متاحة وجاهزة فوراً")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ----------------- 2. قسم الحجز الجديد السلس -----------------
st.markdown("### 📅 حجز دور جديد سريع")
with st.form("booking_form", clear_on_submit=True):
    device = st.selectbox("اختر الجهاز المطلوب:", ["الغسالة", "النشافة"])
    booking_date = st.date_input("📅 اختر تاريخ اليوم أو الغد:", min_value=now.date())
    
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.time_input("⏰ وقت البدء:")
    with col2:
        end_time = st.time_input("⏳ وقت الانتهاء:")
        
    submit = st.form_submit_button("✨ تأكيد الحجز وإدراجه في الجدول")

if submit:
    if start_time >= end_time:
        st.error("خطأ: وقت الانتهاء يجب أن يكون بعد وقت البدء!")
    else:
        start_dt = datetime.datetime.combine(booking_date, start_time)
        end_dt = datetime.datetime.combine(booking_date, end_time)
        duration_minutes = (end_dt - start_dt).total_seconds() / 60
        
        rush_start = datetime.time(13, 0)
        rush_end = datetime.time(18, 0)
        
        is_in_rush_hour = False
        if (rush_start <= start_time <= rush_end) or (rush_start <= end_time <= rush_end):
            is_in_rush_hour = True
            
        if is_in_rush_hour and duration_minutes > 45:
            st.error(f"⚠️ تنبيه الذروة: الفترة بين 1 ظهراً و 6 مساءً مخصصة للغسيل السريع فقط، الحد الأقصى المسموح به هو 45 دقيقة للحفاظ على انسيابية الأدوار.")
        else:
            overlap = False
            for b in st.session_state.bookings:
                if b['device'] == device and b['date'] == booking_date:
                    if not (end_time <= b['start_time'] or start_time >= b['end_time']):
                        overlap = True
                        st.error(f"❌ هذا الوقت مشغول مسبقاً في {device} بواسطة: {b['name']} (من {b['start_time'].strftime('%I:%M %p')} إلى {b['end_time'].strftime('%I:%M %p')})")
                        break
            
            if not overlap:
                st.session_state.bookings.append({
                    'name': st.session_state.user_name,
                    'device': device,
                    'date': booking_date,
                    'start_time': start_time,
                    'end_time': end_time,
                    'password': st.session_state.user_password
                })
                st.success(f"✅ تم حجز {device} بنجاح يا {st.session_state.user_name}! المدة المجدولة: {int(duration_minutes)} دقيقة.")
                time.sleep(0.5)
                st.rerun()
                # 📊 3️⃣ قسم عرض الحجوزات النشطة وإلغائها في أي وقت لجميع العائلة
                st.markdown("---")
                st.subheader("📊 جدول الحجوزات النشطة في البيت")

                if not st.session_state.bookings:
                st.info("🎉 الأجهزة متاحة حالياً ولا توجد أي حجوزات نشطة!")
else:
    # عرض كل حجز مسجل في الصندوق الموحد
    for idx, b in enumerate(st.session_state.bookings):
        # تصميم بطاقة فخمة لكل حجز
        st.info(f"👤 **المستفيد:** {b['name']} | 📱 **الجهاز:** {b['device']} \n\n 📅 **التاريخ:** {b['date']} | ⏰ **الوقت:** من {b['start_time'].strftime('%H:%M')} إلى {b['end_time'].strftime('%H:%M')}")
        
        # إظهار زر الإلغاء للشخص صاحب الحجز فقط لحمايته من تلاعب الآخرين
        if st.session_state.user_name == b['name']:
            if st.button(f"❌ إلغاء حجزي لـ ({b['device']})", key=f"cancel_{idx}"):
                # حذف الحجز من الصندوق الموحد فوراً وفي أي وقت
                st.session_state.bookings.pop(idx)
                st.success("✅ تم إلغاء حجزك بنجاح وتحرير الجهاز للجميع!")
                time.sleep(0.5)
                st.rerun()                

