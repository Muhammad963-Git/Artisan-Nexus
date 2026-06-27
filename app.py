import streamlit as st
import requests
import base64
from PIL import Image
import io
import time

# ---- LANGUAGE CONFIGURATION ----
LANGUAGES = {
    "English": {
        "page_title": "Artisan Nexus",
        "caption": "Transform your product into a professional marketplace listing",
        "form_header": "Tell us about your product",
        "product_name": "Product Name *",
        "product_name_placeholder": "e.g. Hand Embroidered Shawl",
        "material": "Material *",
        "material_placeholder": "e.g. Pure Wool",
        "region": "Region of Origin",
        "region_placeholder": "e.g. Swat, KPK",
        "technique": "Production Technique",
        "technique_placeholder": "e.g. Hand Embroidery",
        "price": "Your Price (PKR or USD) *",
        "price_placeholder": "e.g. PKR 2500",
        "marketplace": "Target Marketplace *",
        "notes": "Additional Notes (optional)",
        "notes_placeholder": "Any other details about your product...",
        "upload": "Upload Product Photo *",
        "generate_btn": "✨ Generate My Listing",
        "error_fields": "Please fill in all required fields (*) and upload an image.",
        "spinner": "Analyzing your product and generating content...",
        "success": "✅ Your listing package is ready!",
        "tab1": "📝 Listing",
        "tab2": "🔍 SEO & Hashtags",
        "tab3": "💰 Pricing",
        "tab4": "📱 Social Media",
        "product_title_header": "Product Title",
        "product_desc_header": "Product Description",
        "seo_header": "SEO Keywords",
        "hashtags_header": "Hashtags",
        "price_header": "Price Suggestion",
        "caption_header": "Marketing Caption",
        "download_btn": "📥 Download Full Package",
        "output_language_instruction": "Generate all content in English.",
    },
    "اردو": {
        "page_title": "آرٹیزن نیکسس",
        "caption": "اپنی مصنوعات کو پیشہ ورانہ مارکیٹ پلیس لسٹنگ میں تبدیل کریں",
        "form_header": "اپنی مصنوعات کے بارے میں بتائیں",
        "product_name": "مصنوع کا نام *",
        "product_name_placeholder": "مثال: ہاتھ سے کڑھائی کی گئی شال",
        "technique": "پیداواری تکنیک",
        "technique_placeholder": "مثال: ہاتھ کی کڑھائی",
        "material": "مواد *",
        "material_placeholder": "مثال: خالص اون",
        "region": "اصل علاقہ",
        "region_placeholder": "مثال: سوات، کے پی کے",
        "price": "آپ کی قیمت (PKR یا USD) *",
        "price_placeholder": "مثال: PKR 2500",
        "marketplace": "ہدف مارکیٹ پلیس *",
        "notes": "اضافی نوٹس (اختیاری)",
        "notes_placeholder": "اپنی مصنوع کے بارے میں کوئی اور تفصیلات...",
        "upload": "مصنوع کی تصویر اپ لوڈ کریں *",
        "generate_btn": "✨ میری لسٹنگ بنائیں",
        "error_fields": "براہ کرم تمام ضروری فیلڈز (*) پُر کریں اور تصویر اپ لوڈ کریں۔",
        "spinner": "آپ کی مصنوع کا تجزیہ کیا جا رہا ہے...",
        "success": "✅ آپ کا لسٹنگ پیکیج تیار ہے!",
        "tab1": "📝 لسٹنگ",
        "tab2": "🔍 SEO اور ہیش ٹیگز",
        "tab3": "💰 قیمت",
        "tab4": "📱 سوشل میڈیا",
        "product_title_header": "مصنوع کا عنوان",
        "product_desc_header": "مصنوع کی تفصیل",
        "seo_header": "SEO کلیدی الفاظ",
        "hashtags_header": "ہیش ٹیگز",
        "price_header": "قیمت کی تجویز",
        "caption_header": "مارکیٹنگ کیپشن",
        "download_btn": "📥 مکمل پیکیج ڈاؤن لوڈ کریں",
        "output_language_instruction": "تمام مواد اردو میں لکھیں۔ SEO keywords انگریزی میں بھی شامل کریں۔",
    },
    "العربية": {
        "page_title": "آرتيزان نيكسس",
        "caption": "حوّل منتجك إلى قائمة احترافية في السوق",
        "form_header": "أخبرنا عن منتجك",
        "product_name": "اسم المنتج *",
        "product_name_placeholder": "مثال: شال مطرز يدويًا",
        "material": "المادة *",
        "material_placeholder": "مثال: صوف نقي",
        "region": "منطقة المنشأ",
        "region_placeholder": "مثال: سوات، خيبر بختونخوا",
        "technique": "تقنية الإنتاج",
        "technique_placeholder": "مثال: تطريز يدوي",
        "price": "سعرك (بكر أو دولار) *",
        "price_placeholder": "مثال: PKR 2500",
        "marketplace": "السوق المستهدف *",
        "notes": "ملاحظات إضافية (اختياري)",
        "notes_placeholder": "أي تفاصيل أخرى عن منتجك...",
        "upload": "رفع صورة المنتج *",
        "generate_btn": "✨ إنشاء قائمتي",
        "error_fields": "يرجى ملء جميع الحقول المطلوبة (*) ورفع صورة.",
        "spinner": "جارٍ تحليل منتجك وإنشاء المحتوى...",
        "success": "✅ حزمة القائمة جاهزة!",
        "tab1": "📝 القائمة",
        "tab2": "🔍 SEO والوسوم",
        "tab3": "💰 التسعير",
        "tab4": "📱 وسائل التواصل",
        "product_title_header": "عنوان المنتج",
        "product_desc_header": "وصف المنتج",
        "seo_header": "كلمات SEO",
        "hashtags_header": "الوسوم",
        "price_header": "اقتراح السعر",
        "caption_header": "تعليق تسويقي",
        "download_btn": "📥 تحميل الحزمة الكاملة",
        "output_language_instruction": "اكتب جميع المحتوى باللغة العربية. أضف كلمات SEO بالإنجليزية أيضًا.",
    },
    "中文": {
        "page_title": "工匠枢纽",
        "caption": "将您的产品转化为专业的市场列表",
        "form_header": "告诉我们您的产品",
        "product_name": "产品名称 *",
        "product_name_placeholder": "例如：手工刺绣披肩",
        "material": "材料 *",
        "material_placeholder": "例如：纯羊毛",
        "region": "原产地区",
        "region_placeholder": "例如：巴基斯坦斯瓦特",
        "technique": "生产工艺",
        "technique_placeholder": "例如：手工刺绣",
        "price": "您的价格 (PKR或USD) *",
        "price_placeholder": "例如：PKR 2500",
        "marketplace": "目标市场 *",
        "notes": "补充说明（可选）",
        "notes_placeholder": "关于您产品的其他详情...",
        "upload": "上传产品照片 *",
        "generate_btn": "✨ 生成我的列表",
        "error_fields": "请填写所有必填字段 (*) 并上传图片。",
        "spinner": "正在分析您的产品并生成内容...",
        "success": "✅ 您的列表包已准备好！",
        "tab1": "📝 列表",
        "tab2": "🔍 SEO和标签",
        "tab3": "💰 定价",
        "tab4": "📱 社交媒体",
        "product_title_header": "产品标题",
        "product_desc_header": "产品描述",
        "seo_header": "SEO关键词",
        "hashtags_header": "话题标签",
        "price_header": "价格建议",
        "caption_header": "营销文案",
        "download_btn": "📥 下载完整包",
        "output_language_instruction": "用中文写所有内容。同时用英文提供SEO关键词。",
    },
}

# ---- CONFIGURATION ----
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={GEMINI_API_KEY}"

def call_gemini(prompt_text, image=None):
    parts = []
    if image:
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": img_base64
            }
        })
    parts.append({"text": prompt_text})
    payload = {"contents": [{"parts": parts}]}
    response = requests.post(GEMINI_URL, json=payload)
    if response.status_code == 200:
        raw = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        # ---- REMOVE ASTERISKS ----
        clean = raw.replace("**", "").replace("* ", "").replace("*", "")
        return clean
    else:
        st.error(f"API Error {response.status_code}: {response.json()}")
        st.stop()

# ---- PAGE SETUP ----
st.set_page_config(page_title="Artisan Nexus", page_icon="🧵")

# ---- LANGUAGE SELECTOR (TOP OF PAGE) ----
selected_lang = st.selectbox(
    "🌐 Language / زبان / اللغة / 语言",
    list(LANGUAGES.keys()),
    index=0
)
L = LANGUAGES[selected_lang]

st.title(f"🧵 {L['page_title']}")
st.caption(L["caption"])

# ---- INPUT FORM ----
st.subheader(L["form_header"])

product_name = st.text_input(L["product_name"],
    placeholder=L["product_name_placeholder"])

col1, col2 = st.columns(2)
with col1:
    material = st.text_input(L["material"],
        placeholder=L["material_placeholder"])
    region = st.text_input(L["region"],
        placeholder=L["region_placeholder"])
with col2:
    technique = st.text_input(L["technique"],
        placeholder=L["technique_placeholder"])
    price = st.text_input(L["price"],
        placeholder=L["price_placeholder"])

marketplace = st.selectbox(L["marketplace"],
    ["Daraz", "Etsy", "Amazon", "Instagram"])

additional_notes = st.text_area(L["notes"],
    placeholder=L["notes_placeholder"])

uploaded_image = st.file_uploader(L["upload"],
    type=["jpg", "jpeg", "png", "webp"])

if uploaded_image:
    st.image(uploaded_image, caption="📸", width=300)

# ---- GENERATE BUTTON ----
generate = st.button(L["generate_btn"],
    type="primary",
    use_container_width=True)

# ---- GENERATION LOGIC ----
if generate:
    if not product_name or not material or not price or not uploaded_image:
        st.error(L["error_fields"])
    else:
        with st.spinner(L["spinner"]):

            # -- CALL 1: VISION --
            image = Image.open(uploaded_image)
            vision_prompt = """
            Describe only the visible characteristics of this product image.
            Include: colors present, patterns visible, texture appearance,
            approximate size, decorative elements, and overall condition.
            Do NOT identify, name, assume origin, material, or cultural background.
            Only describe what you can literally see.
            """
            visual_description = call_gemini(vision_prompt, image)

            time.sleep(3)

            # -- CALL 2: GENERATION --
            generation_prompt = f"""
You are an expert e-commerce content strategist specializing in
South Asian marketplace listings.

{L['output_language_instruction']}

SELLER-PROVIDED FACTS (treat these as absolute truth):
- Product Name: {product_name}
- Material: {material}
- Region of Origin: {region if region else 'Not specified'}
- Production Technique: {technique if technique else 'Not specified'}
- Price: {price}
- Target Marketplace: {marketplace}
- Additional Notes: {additional_notes if additional_notes else 'None'}

VISUAL DESCRIPTION FROM IMAGE (visible characteristics only):
{visual_description}

Generate ALL of the following sections clearly labeled.
Do NOT use asterisks or markdown formatting in your response.
Write in plain text only.

[TITLE]
A professional SEO-optimized product title. Include material,
technique and region if provided.

[DESCRIPTION]
3 professional paragraphs. Use seller facts as truth.
Reference visual description for appearance details only.
Do not invent history, certifications, or claims not provided.

[SEO KEYWORDS]
10 English keywords and 5 keywords in the output language.

[HASHTAGS]
20 Instagram hashtags and 5 Twitter/X hashtags.

[PRICE SUGGESTION]
Based on the seller's stated price of {price}, suggest a price range
for {marketplace}. Explain briefly.

[MARKETING CAPTION]
A compelling social media caption with emojis and a call to action.

[MARKETPLACE LISTING]
A complete {marketplace}-ready listing formatted for that platform.

RULES:
- Never use asterisks or markdown symbols
- Never invent specifications, history or certifications
- Only reference cultural details if seller provided them
- Keep tone professional, trustworthy, and customer-friendly
"""
            full_output = call_gemini(generation_prompt)

            # -- PARSE SECTIONS --
            def extract_section(text, section_name, next_section=None):
                try:
                    start = text.find(f"[{section_name}]") + len(f"[{section_name}]")
                    if next_section:
                        end = text.find(f"[{next_section}]")
                        return text[start:end].strip()
                    else:
                        return text[start:].strip()
                except:
                    return "Could not generate this section."

            title = extract_section(full_output, "TITLE", "DESCRIPTION")
            description = extract_section(full_output, "DESCRIPTION", "SEO KEYWORDS")
            seo = extract_section(full_output, "SEO KEYWORDS", "HASHTAGS")
            hashtags = extract_section(full_output, "HASHTAGS", "PRICE SUGGESTION")
            price_suggestion = extract_section(full_output, "PRICE SUGGESTION", "MARKETING CAPTION")
            caption = extract_section(full_output, "MARKETING CAPTION", "MARKETPLACE LISTING")
            marketplace_listing = extract_section(full_output, "MARKETPLACE LISTING")

        # ---- OUTPUT TABS ----
        st.success(L["success"])

        tab1, tab2, tab3, tab4 = st.tabs([
            L["tab1"], L["tab2"], L["tab3"], L["tab4"]
        ])

        with tab1:
            st.subheader(L["product_title_header"])
            st.info(title)
            st.subheader(L["product_desc_header"])
            st.write(description)
            st.subheader(f"{marketplace} Listing")
            st.write(marketplace_listing)

        with tab2:
            st.subheader(L["seo_header"])
            st.write(seo)
            st.subheader(L["hashtags_header"])
            st.write(hashtags)

        with tab3:
            st.subheader(L["price_header"])
            st.write(price_suggestion)

        with tab4:
            st.subheader(L["caption_header"])
            st.write(caption)

        # ---- DOWNLOAD BUTTON ----
        full_package = f"""
ARTISAN NEXUS - COMPLETE LISTING PACKAGE
Product: {product_name}
Generated for: {marketplace}
Language: {selected_lang}
{'='*50}

TITLE:
{title}

DESCRIPTION:
{description}

SEO KEYWORDS:
{seo}

HASHTAGS:
{hashtags}

PRICE SUGGESTION:
{price_suggestion}

MARKETING CAPTION:
{caption}

MARKETPLACE LISTING:
{marketplace_listing}
"""
        st.download_button(
            label=L["download_btn"],
            data=full_package,
            file_name=f"artisan_nexus_{product_name.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
