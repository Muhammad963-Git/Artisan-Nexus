import streamlit as st
import requests
import base64
from PIL import Image
import io
import time

# ================================================================
# LANGUAGE CONFIGURATION — UI LABELS
# ================================================================
UI_LANGUAGES = {
    "English": {
        "page_title": "Artisan Nexus",
        "tagline_head": "Your product. Professional listings. In seconds.",
        "tagline_body": "Upload a photo, fill in a few details, and Artisan Nexus instantly generates a complete marketplace listing — product title, description, SEO keywords, hashtags, pricing suggestion, and social media caption — ready for Daraz, Etsy, Amazon, Instagram and more. In any language. For free.",
        "ui_lang_label": "🌐 Interface Language",
        "output_lang_label": "📄 Output Language",
        "form_header": "Tell us about your product",
        "product_type_label": "What are you selling?",
        "product_name_label": "Product Name *",
        "product_name_placeholder": "e.g. Handmade Swati Shawl",
        "field1_label": "What is it made of? *",
        "field1_placeholder": "e.g. Pure Wool, Cotton, Glass, Steel...",
        "field2_label": "How is it made or what does it do?",
        "field2_placeholder": "e.g. Hand embroidered, Machine pressed, Moisturizes skin...",
        "region_label": "Region or Brand Origin (optional)",
        "region_placeholder": "e.g. Swat KPK, Lahore, Seoul...",
        "price_label": "Your Price (PKR or USD) *",
        "price_placeholder": "e.g. PKR 2500 or $12",
        "marketplace_label": "Target Marketplace *",
        "notes_label": "Additional Details (optional)",
        "notes_placeholder": "Anything else that makes your product special...",
        "upload_label": "Upload Product Photo *",
        "generate_btn": "✨ Generate My Listing",
        "error_msg": "Please fill in all required fields (*) and upload a photo.",
        "spinner_msg": "Analyzing your product and generating content...",
        "success_msg": "✅ Your listing package is ready!",
        "tab_listing": "📝 Listing",
        "tab_seo": "🔍 SEO & Hashtags",
        "tab_pricing": "💰 Pricing",
        "tab_social": "📱 Social Media",
        "title_header": "Product Title",
        "desc_header": "Product Description",
        "listing_header": "Marketplace Ready Listing",
        "seo_header": "SEO Keywords",
        "hashtags_header": "Hashtags",
        "price_header": "Price Suggestion",
        "caption_header": "Marketing Caption",
        "download_btn": "📥 Download Full Package",
        "photo_caption": "Your product photo",
        "email_label": "📧 Your Email (optional)",
        "email_placeholder": "yourname@gmail.com",
        "email_help": "Leave blank if you prefer to just download your listing manually",
    },
    "اردو": {
        "page_title": "آرٹیزن نیکسس",
        "tagline_head": "آپ کی مصنوعات۔ پیشہ ورانہ لسٹنگ۔ چند سیکنڈوں میں۔",
        "tagline_body": "ایک تصویر اپ لوڈ کریں، چند تفصیلات بھریں، اور آرٹیزن نیکسس فوری طور پر مکمل مارکیٹ پلیس لسٹنگ بناتا ہے — عنوان، تفصیل، SEO کلیدی الفاظ، ہیش ٹیگز، قیمت کی تجویز اور سوشل میڈیا کیپشن۔ مفت۔",
        "ui_lang_label": "🌐 انٹرفیس زبان",
        "output_lang_label": "📄 آؤٹ پٹ زبان",
        "form_header": "اپنی مصنوعات کے بارے میں بتائیں",
        "product_type_label": "آپ کیا فروخت کر رہے ہیں؟",
        "product_name_label": "مصنوع کا نام *",
        "product_name_placeholder": "مثال: ہاتھ سے بنی سواتی شال",
        "field1_label": "یہ کس چیز سے بنا ہے؟ *",
        "field1_placeholder": "مثال: خالص اون، کپاس، شیشہ...",
        "field2_label": "یہ کیسے بنایا گیا یا یہ کیا کرتا ہے؟",
        "field2_placeholder": "مثال: ہاتھ سے کڑھائی، جلد کو نمی دیتا ہے...",
        "region_label": "علاقہ یا برانڈ کی اصل (اختیاری)",
        "region_placeholder": "مثال: سوات کے پی کے، لاہور...",
        "price_label": "آپ کی قیمت (PKR یا USD) *",
        "price_placeholder": "مثال: PKR 2500",
        "marketplace_label": "ہدف مارکیٹ پلیس *",
        "notes_label": "اضافی تفصیلات (اختیاری)",
        "notes_placeholder": "کوئی اور چیز جو آپ کی مصنوع کو خاص بناتی ہے...",
        "upload_label": "مصنوع کی تصویر اپ لوڈ کریں *",
        "generate_btn": "✨ میری لسٹنگ بنائیں",
        "error_msg": "براہ کرم تمام ضروری فیلڈز (*) پُر کریں اور تصویر اپ لوڈ کریں۔",
        "spinner_msg": "آپ کی مصنوع کا تجزیہ ہو رہا ہے...",
        "success_msg": "✅ آپ کا لسٹنگ پیکیج تیار ہے!",
        "tab_listing": "📝 لسٹنگ",
        "tab_seo": "🔍 SEO اور ہیش ٹیگز",
        "tab_pricing": "💰 قیمت",
        "tab_social": "📱 سوشل میڈیا",
        "title_header": "مصنوع کا عنوان",
        "desc_header": "مصنوع کی تفصیل",
        "listing_header": "مارکیٹ پلیس لسٹنگ",
        "seo_header": "SEO کلیدی الفاظ",
        "hashtags_header": "ہیش ٹیگز",
        "price_header": "قیمت کی تجویز",
        "caption_header": "مارکیٹنگ کیپشن",
        "download_btn": "📥 مکمل پیکیج ڈاؤن لوڈ کریں",
        "photo_caption": "آپ کی مصنوع کی تصویر",
        "email_label": "📧 آپ کی ای میل (اختیاری)",
        "email_placeholder": "yourname@gmail.com",
        "email_help": "اگر آپ صرف ڈاؤن لوڈ کرنا چاہتے ہیں تو خالی چھوڑ دیں",
    },
    "العربية": {
        "page_title": "آرتيزان نيكسس",
        "tagline_head": "منتجك. قوائم احترافية. في ثوانٍ.",
        "tagline_body": "ارفع صورة، أدخل بعض التفاصيل، وسيقوم آرتيزان نيكسس بإنشاء قائمة متكاملة — عنوان، وصف، كلمات SEO، وسوم، اقتراح سعر، وتعليق للتواصل الاجتماعي. مجاناً.",
        "ui_lang_label": "🌐 لغة الواجهة",
        "output_lang_label": "📄 لغة المخرجات",
        "form_header": "أخبرنا عن منتجك",
        "product_type_label": "ماذا تبيع؟",
        "product_name_label": "اسم المنتج *",
        "product_name_placeholder": "مثال: شال مطرز يدويًا",
        "field1_label": "مم صُنع؟ *",
        "field1_placeholder": "مثال: صوف نقي، قطن، زجاج...",
        "field2_label": "كيف صُنع أو ماذا يفعل؟",
        "field2_placeholder": "مثال: تطريز يدوي، يرطب البشرة...",
        "region_label": "المنطقة أو أصل العلامة (اختياري)",
        "region_placeholder": "مثال: باكستان، القاهرة...",
        "price_label": "سعرك (بكر أو دولار) *",
        "price_placeholder": "مثال: PKR 2500",
        "marketplace_label": "السوق المستهدف *",
        "notes_label": "تفاصيل إضافية (اختياري)",
        "notes_placeholder": "أي شيء آخر يميز منتجك...",
        "upload_label": "رفع صورة المنتج *",
        "generate_btn": "✨ إنشاء قائمتي",
        "error_msg": "يرجى ملء جميع الحقول المطلوبة (*) ورفع صورة.",
        "spinner_msg": "جارٍ تحليل منتجك وإنشاء المحتوى...",
        "success_msg": "✅ حزمة القائمة جاهزة!",
        "tab_listing": "📝 القائمة",
        "tab_seo": "🔍 SEO والوسوم",
        "tab_pricing": "💰 التسعير",
        "tab_social": "📱 وسائل التواصل",
        "title_header": "عنوان المنتج",
        "desc_header": "وصف المنتج",
        "listing_header": "قائمة السوق",
        "seo_header": "كلمات SEO",
        "hashtags_header": "الوسوم",
        "price_header": "اقتراح السعر",
        "caption_header": "تعليق تسويقي",
        "download_btn": "📥 تحميل الحزمة الكاملة",
        "photo_caption": "صورة منتجك",
        "email_label": "📧 بريدك الإلكتروني (اختياري)",
        "email_placeholder": "yourname@gmail.com",
        "email_help": "اتركه فارغاً إذا كنت تفضل تنزيل القائمة يدوياً",
    },
    "中文": {
        "page_title": "工匠枢纽",
        "tagline_head": "您的产品。专业列表。即刻生成。",
        "tagline_body": "上传照片，填写几个细节，工匠枢纽立即生成完整的市场列表——标题、描述、SEO关键词、话题标签、定价建议和社交媒体文案。免费。",
        "ui_lang_label": "🌐 界面语言",
        "output_lang_label": "📄 输出语言",
        "form_header": "告诉我们您的产品",
        "product_type_label": "您在销售什么？",
        "product_name_label": "产品名称 *",
        "product_name_placeholder": "例如：手工刺绣披肩",
        "field1_label": "由什么制成？*",
        "field1_placeholder": "例如：纯羊毛、棉花、玻璃...",
        "field2_label": "如何制作或有什么功能？",
        "field2_placeholder": "例如：手工刺绣、保湿皮肤...",
        "region_label": "地区或品牌来源（可选）",
        "region_placeholder": "例如：巴基斯坦、上海...",
        "price_label": "您的价格（PKR或USD）*",
        "price_placeholder": "例如：PKR 2500",
        "marketplace_label": "目标市场 *",
        "notes_label": "补充说明（可选）",
        "notes_placeholder": "任何让您的产品与众不同的细节...",
        "upload_label": "上传产品照片 *",
        "generate_btn": "✨ 生成我的列表",
        "error_msg": "请填写所有必填字段 (*) 并上传照片。",
        "spinner_msg": "正在分析您的产品并生成内容...",
        "success_msg": "✅ 您的列表包已准备好！",
        "tab_listing": "📝 列表",
        "tab_seo": "🔍 SEO和标签",
        "tab_pricing": "💰 定价",
        "tab_social": "📱 社交媒体",
        "title_header": "产品标题",
        "desc_header": "产品描述",
        "listing_header": "市场列表",
        "seo_header": "SEO关键词",
        "hashtags_header": "话题标签",
        "price_header": "价格建议",
        "caption_header": "营销文案",
        "download_btn": "📥 下载完整包",
        "photo_caption": "您的产品照片",
        "email_label": "📧 您的邮箱（可选）",
        "email_placeholder": "yourname@gmail.com",
        "email_help": "如果您只想手动下载列表，请留空",
    },
}

# ================================================================
# OUTPUT LANGUAGE OPTIONS
# ================================================================
OUTPUT_LANGUAGES = {
    "English": "Write all generated content in English.",
    "اردو": "تمام مواد اردو میں لکھیں۔ SEO keywords انگریزی میں بھی شامل کریں۔",
    "العربية": "اكتب جميع المحتوى باللغة العربية. أضف كلمات SEO بالإنجليزية أيضًا.",
    "中文": "用中文写所有内容。同时用英文提供SEO关键词。",
    "Français": "Écrivez tout le contenu en français. Incluez également les mots-clés SEO en anglais.",
    "Español": "Escribe todo el contenido en español. Incluye también palabras clave SEO en inglés.",
}

# ================================================================
# PRODUCT TYPE FIELD CONFIGURATIONS
# ================================================================
PRODUCT_TYPES = {
    "🧵 Handcrafted / Artisan": {
        "field1_override": None,
        "field2_override": None,
    },
    "💄 Beauty & Personal Care": {
        "field1_override": "Key Ingredients *",
        "field1_placeholder_override": "e.g. Shea Butter, Aloe Vera, Vitamin E...",
        "field2_override": "What does it do?",
        "field2_placeholder_override": "e.g. Moisturizes skin, reduces dark spots, repairs hair...",
    },
    "🍱 Food & Grocery": {
        "field1_override": "Main Ingredients *",
        "field1_placeholder_override": "e.g. Wheat flour, Desi Ghee, Organic Honey...",
        "field2_override": "How is it prepared / Shelf life?",
        "field2_placeholder_override": "e.g. Stone ground, sun dried, 6 months shelf life...",
    },
    "👗 Clothing & Accessories": {
        "field1_override": "Fabric / Material *",
        "field1_placeholder_override": "e.g. 100% Cotton, Chiffon, Leather...",
        "field2_override": "Style / Cut / Feature",
        "field2_placeholder_override": "e.g. Flared sleeves, embroidered neckline, unstitched...",
    },
    "🏠 Home & Living": {
        "field1_override": "Material / Finish *",
        "field1_placeholder_override": "e.g. Solid Wood, Ceramic, Stainless Steel...",
        "field2_override": "Function / Feature",
        "field2_placeholder_override": "e.g. Storage basket, decorative centerpiece, non-stick...",
    },
    "📦 Other": {
        "field1_override": "What is it made of or contains? *",
        "field1_placeholder_override": "e.g. Plastic, Metal, Mixed materials...",
        "field2_override": "What does it do or how is it used?",
        "field2_placeholder_override": "e.g. Used for cooking, worn on head, applied on skin...",
    },
}

# ================================================================
# GEMINI CONFIGURATION
# ================================================================
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

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
        # Strip all asterisks and markdown bold/italic
        clean = raw.replace("**", "").replace("* ", "").replace("*", "")
        return clean
    else:
        st.error(f"API Error {response.status_code}: {response.json()}")
        st.stop()

# ================================================================
# PAGE SETUP
# ================================================================
st.set_page_config(page_title="Artisan Nexus", page_icon="🧵", layout="centered")

# ================================================================
# LANGUAGE SELECTORS — TOP OF PAGE
# ================================================================
# Initialize session state for language tracking
if "prev_ui_lang" not in st.session_state:
    st.session_state.prev_ui_lang = "English"

col_lang1, col_lang2 = st.columns(2)
with col_lang1:
    selected_ui_lang = st.selectbox(
        "🌐 Interface Language / زبان / اللغة / 语言",
        list(UI_LANGUAGES.keys()),
        index=0
    )
with col_lang2:
    selected_output_lang = st.selectbox(
        "📄 Output Language / آؤٹ پٹ / لغة المخرجات / 输出语言",
        list(OUTPUT_LANGUAGES.keys()),
        index=0
    )

# Force rerun when UI language changes so placeholders update
if selected_ui_lang != st.session_state.prev_ui_lang:
    st.session_state.prev_ui_lang = selected_ui_lang
    st.rerun()

L = UI_LANGUAGES[selected_ui_lang]
output_instruction = OUTPUT_LANGUAGES[selected_output_lang]
# ================================================================
# HERO SECTION — MORE NOTICEABLE TAGLINE
# ================================================================
st.markdown("---")
st.markdown(f"## 🧵 {L['page_title']}")
st.markdown(f"### _{L['tagline_head']}_")
st.info(f"💡 {L['tagline_body']}")
st.markdown("---")

# ================================================================
# INPUT FORM
# ================================================================
st.subheader(L["form_header"])

# Product Type Selector
product_type = st.selectbox(
    L["product_type_label"],
    list(PRODUCT_TYPES.keys())
)
type_config = PRODUCT_TYPES[product_type]

# Product Name
product_name = st.text_input(
    L["product_name_label"],
    placeholder=L["product_name_placeholder"]
)

col1, col2 = st.columns(2)
with col1:
    # Dynamic field 1 label based on product type
    field1_label = type_config.get("field1_override") or L["field1_label"]
    field1_placeholder = type_config.get("field1_placeholder_override") or L["field1_placeholder"]
    field1 = st.text_input(field1_label, placeholder=field1_placeholder)

    region = st.text_input(
        L["region_label"],
        placeholder=L["region_placeholder"]
    )

with col2:
    # Dynamic field 2 label based on product type
    field2_label = type_config.get("field2_override") or L["field2_label"]
    field2_placeholder = type_config.get("field2_placeholder_override") or L["field2_placeholder"]
    field2 = st.text_input(field2_label, placeholder=field2_placeholder)

    price = st.text_input(
        L["price_label"],
        placeholder=L["price_placeholder"]
    )

# Marketplace — includes None option
marketplace = st.selectbox(
    L["marketplace_label"],
    ["Daraz", "Etsy", "Amazon", "Instagram", "None / Not decided yet"]
)

additional_notes = st.text_area(
    L["notes_label"],
    placeholder=L["notes_placeholder"]
)
seller_email = st.text_input(
    L["email_label"],
    placeholder=L["email_placeholder"],
    help=L["email_help"]
)
uploaded_image = st.file_uploader(
    L["upload_label"],
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_image:
    st.image(uploaded_image, caption=L["photo_caption"], width=300)

# ================================================================
# GENERATE BUTTON
# ================================================================
st.markdown("---")
generate = st.button(
    L["generate_btn"],
    type="primary",
    use_container_width=True
)

# ================================================================
# GENERATION LOGIC
# ================================================================
if generate:
    if not product_name or not field1 or not price or not uploaded_image:
        st.error(L["error_msg"])
    else:
        with st.spinner(L["spinner_msg"]):

            # CALL 1 — VISION
            image = Image.open(uploaded_image)
            vision_prompt = """
            Describe only the visible characteristics of this product image.
            Include: colors present, patterns visible, texture appearance,
            approximate size, decorative elements, and overall condition.
            Do NOT identify, name, assume origin, material, or cultural background.
            Only describe what you can literally see.
            Do not use asterisks or any markdown formatting.
            """
            visual_description = call_gemini(vision_prompt, image)

            time.sleep(3)

            # Marketplace context
            marketplace_context = (
                "The seller has not chosen a specific marketplace yet. "
                "Generate a general listing suitable for any platform."
                if marketplace == "None / Not decided yet"
                else f"Target marketplace: {marketplace}. Format listing accordingly."
            )

            # CALL 2 — GENERATION
            generation_prompt = f"""
You are an expert e-commerce content strategist.

LANGUAGE INSTRUCTION:
{output_instruction}

PRODUCT CATEGORY: {product_type}

SELLER-PROVIDED FACTS (treat as absolute truth — never contradict these):
- Product Name: {product_name}
- Composition / Ingredients / Material: {field1}
- Function / Technique / Feature: {field2 if field2 else 'Not specified'}
- Region or Brand Origin: {region if region else 'Not specified'}
- Price: {price}
- Additional Details: {additional_notes if additional_notes else 'None'}

MARKETPLACE:
{marketplace_context}

VISUAL DESCRIPTION FROM IMAGE (visible characteristics only — do not treat as facts about material or origin):
{visual_description}

Generate ALL sections below. Use the exact labels in square brackets.
Do NOT use asterisks, bullet dashes, or markdown formatting anywhere.
Write in plain readable text only.

[TITLE]
One professional SEO-optimized product title.
Include the most important keywords naturally.

[DESCRIPTION]
Three professional paragraphs.
First paragraph: what it is and what makes it special.
Second paragraph: appearance based on visual description.
Third paragraph: who it is for and why they should buy it.
Never invent claims, certifications, history, or dimensions not provided.

[SEO KEYWORDS]
10 keywords in the output language.
5 keywords in English (always include regardless of output language).

[HASHTAGS]
20 Instagram hashtags.
5 Twitter/X hashtags.
Keep hashtags in English for maximum reach.

[PRICE SUGGESTION]
Based on the seller price of {price}, suggest a competitive price range.
If marketplace is Etsy or Amazon, also suggest a USD equivalent.
Give one sentence of reasoning.

[MARKETING CAPTION]
One compelling social media caption.
Include relevant emojis and a clear call to action.
Keep it under 150 words.

[MARKETPLACE LISTING]
{marketplace_context}
Format the listing appropriately for the platform.
Include title, key features, description, and any platform-specific details.
If no marketplace selected, write a clean universal listing.

RULES:
- Never use asterisks or any markdown symbols
- Never invent specifications, history, certifications or dimensions
- Only reference cultural or origin details if the seller provided them
- Keep tone professional, trustworthy, and customer-friendly
- If product type is beauty or food, always include a disclaimer:
  "Please verify all ingredients before use."
"""
            full_output = call_gemini(generation_prompt)

            # PARSE SECTIONS
            def extract_section(text, section_name, next_section=None):
                try:
                    start = text.find(f"[{section_name}]") + len(f"[{section_name}]")
                    if next_section:
                        end = text.find(f"[{next_section}]")
                        if end == -1:
                            return text[start:].strip()
                        return text[start:end].strip()
                    else:
                        return text[start:].strip()
                except:
                    return "Could not generate this section. Please try again."

            title = extract_section(full_output, "TITLE", "DESCRIPTION")
            description = extract_section(full_output, "DESCRIPTION", "SEO KEYWORDS")
            seo = extract_section(full_output, "SEO KEYWORDS", "HASHTAGS")
            hashtags = extract_section(full_output, "HASHTAGS", "PRICE SUGGESTION")
            price_suggestion = extract_section(full_output, "PRICE SUGGESTION", "MARKETING CAPTION")
            caption = extract_section(full_output, "MARKETING CAPTION", "MARKETPLACE LISTING")
            marketplace_listing = extract_section(full_output, "MARKETPLACE LISTING")

        # ================================================================
        # OUTPUT DISPLAY
        # ================================================================
        st.success(L["success_msg"])

        tab1, tab2, tab3, tab4 = st.tabs([
            L["tab_listing"],
            L["tab_seo"],
            L["tab_pricing"],
            L["tab_social"]
        ])

        with tab1:
            st.subheader(L["title_header"])
            st.info(title)
            st.subheader(L["desc_header"])
            st.write(description)
            st.subheader(L["listing_header"])
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
        # ---- HOW TO SELL GUIDE ----
        st.markdown("---")
        st.subheader("📖 How To List & Sell Your Product")
        st.caption("A step-by-step guide for first-time sellers")

        SELLING_GUIDES = {
            "Daraz": {
                "intro": "Daraz is Pakistan's largest online marketplace with over 20 million active users. Registration is free and there are no monthly fees — Daraz only charges a small commission when you make a sale.",
                "requirements": [
                    "Valid CNIC (front and back photo)",
                    "Active Pakistani mobile number",
                    "Valid email address",
                    "Bank account with IBAN number",
                    "At least 3 high-quality product photos (white background preferred)",
                ],
                "steps": [
                    ("Create Your Account", "Go to sellercenter.daraz.pk and click 'Create New Account'. You can also SMS 'Daraz [Your Name]' to 7575 to get started via mobile."),
                    ("Choose Account Type", "Select 'Local Seller' if you are an individual. Select 'Corporate Seller' if you have a registered business with NTN. Most artisans and small sellers choose Local Seller."),
                    ("Verify Your Identity", "Upload a clear photo of the front and back of your CNIC. Fill in your full name, mobile number, email, and shop name. Set a password and accept the terms."),
                    ("Complete Your Profile", "Inside Seller Center, find the to-do list and complete it. Add your warehouse address — this is where Daraz riders will come to pick up your orders. Be as specific as possible with house number, street, and nearest landmark."),
                    ("Add Your Bank Details", "Enter your IBAN number carefully. Double-check every digit — a single wrong number means your payment goes to the wrong account."),
                    ("Wait For Verification", "Daraz typically verifies accounts within 24 to 48 hours. You will receive a confirmation email."),
                    ("List Your Product", "In Seller Center, go to Products and click Add Products. Enter your product name, select the correct category, add your description, set your price, and upload at least 3 photos. Click Publish."),
                    ("Receive & Ship Orders", "When a customer orders, pack it well and wait for the Daraz Express rider to pick it up. You can also drop it off at a Daraz hub near you."),
                    ("Get Paid", "Daraz pays sellers every 14 days. Orders delivered between the 1st and 15th are paid by the 25th. Payments go directly to your linked bank account."),
                ],
                "tips": [
                    "Use a white background for product photos — listings with clean photos rank higher in search",
                    "Include the brand, material, and key feature in your product title for better SEO",
                    "Select the most accurate category — wrong categories mean your product never appears in search filters",
                    "Daraz commission varies by category — check the Commission Structure in Daraz University inside your Seller Center",
                    "Join Daraz campaigns like 11.11 or 12.12 for massive traffic boosts",
                    "Aim for at least a 30-40% profit margin to stay profitable after commission and packaging costs",
                ],
                "fees": "Registration: Free. Monthly fee: None. Commission: 5-20% per sale depending on category. Payment cycle: Every 14 days.",
                "link": "https://sellercenter.daraz.pk",
            },
            "Etsy": {
                "intro": "Etsy is a global marketplace with over 96 million buyers specifically looking for handmade, vintage, and unique items. It is ideal for artisan products, crafts, and culturally unique goods. Etsy connects Pakistani sellers directly with international buyers.",
                "requirements": [
                    "Valid email address",
                    "Payoneer account (for Pakistani sellers to receive payments)",
                    "At least one product photo to complete shop setup",
                    "A unique shop name (under 20 characters, no spaces)",
                    "Bank account linked to Payoneer",
                ],
                "steps": [
                    ("Create An Etsy Account", "Go to etsy.com and click 'Sign in' then 'Register'. Enter your name and email address and create a password. You can also sign up with Google."),
                    ("Open Your Shop", "Click your account icon and select 'Sell on Etsy' or go directly to etsy.com/sell. Click 'Open your Etsy shop'. This starts the guided setup wizard."),
                    ("Set Shop Preferences", "Choose your language, country (Pakistan), and currency. Click Save and Continue."),
                    ("Choose Your Shop Name", "Pick a unique name under 20 characters with no spaces or special characters. You can change it once later if needed. Include relevant keywords if possible."),
                    ("Create Your First Listing", "Etsy requires at least one listing to complete setup. Upload your product photos, write a title using keywords, add a description, set your price, and choose a category. Use all 13 tags Etsy allows — these are critical for search visibility."),
                    ("Set Up Payments", "Pakistani sellers use Etsy Payments via Payoneer. Create a free Payoneer account at payoneer.com if you don't have one. Link it to your Etsy shop. Funds from sales are deposited into your Payoneer account and can be transferred to your Pakistani bank."),
                    ("Set Up Billing", "Add a credit or debit card to pay for Etsy fees. Each listing costs $0.20 and is active for 4 months."),
                    ("Publish Your Shop", "Once billing is set up your shop goes live immediately. Your first listing is now visible to buyers worldwide."),
                    ("Customize Your Shop", "Add a shop logo, banner, and About section. Tell your story — where you are from, how you make your products. Buyers on Etsy love authentic stories and are more likely to buy from sellers with complete profiles."),
                    ("Ship Your Orders", "When an order arrives, pack it carefully and ship via Pakistan Post or a courier like TCS or Leopards for international orders. Update the tracking number in your Etsy orders dashboard."),
                ],
                "tips": [
                    "Etsy buyers love cultural stories — mention Swat, Multan, KPK or your region in your shop description",
                    "Use all 13 tags per listing — Etsy's search algorithm relies heavily on tags",
                    "Launch with at least 10-20 listings — more listings means more chances to be found",
                    "High quality photos are everything on Etsy — invest in good lighting before anything else",
                    "Complete your About Me page fully — buyers trust sellers who share their story",
                    "Reply to messages within 24 hours — fast replies improve your search ranking",
                    "Etsy automatically runs Offsite Ads for your products — you only pay a 15% fee if a sale comes from those ads",
                ],
                "fees": "Listing fee: $0.20 per item (active for 4 months). Transaction fee: 6.5% per sale. Payment processing: ~3% + $0.25 per transaction. Offsite Ads: 15% only if sale comes from an ad.",
                "link": "https://www.etsy.com/sell",
            },
            "Amazon": {
                "intro": "Amazon is the world's largest online marketplace with over 300 million active customers. It gives your product access to a global audience. Amazon is best suited for sellers who can produce consistent stock and want to scale internationally.",
                "requirements": [
                    "Valid email address",
                    "Government-issued ID (passport or national ID)",
                    "Credit or debit card",
                    "Bank account that can receive international transfers",
                    "Phone number for verification",
                    "Tax information (varies by country)",
                ],
                "steps": [
                    ("Choose A Selling Plan", "Go to sell.amazon.com. Individual Plan: No monthly fee, pay $0.99 per item sold. Best if you sell fewer than 40 items per month. Professional Plan: $39.99 per month, unlimited sales. Best for serious sellers who want advertising tools and bulk listing."),
                    ("Create Your Seller Account", "Go to sellercentral.amazon.com and click 'Sign up'. Enter your email and create a password. Provide your legal name, address, and contact details."),
                    ("Verify Your Identity", "Upload a government-issued photo ID and a recent bank statement or credit card statement. Amazon may schedule a short video verification call. Account approval typically takes 1 to 3 business days."),
                    ("Set Up Your Account", "Add your bank account details for receiving payments. Add a credit card for paying Amazon fees. Configure your display name and seller profile."),
                    ("List Your Product", "In Seller Central go to Inventory and click Add a Product. If your product already exists on Amazon search for it and add your offer. If it is brand new click Create a new product listing. Fill in the product title, category, description, bullet points, photos, price, and quantity."),
                    ("Choose Your Fulfillment Method", "FBM (Fulfilled by Merchant): You store, pack, and ship orders yourself. More control, lower fees. FBA (Fulfilled by Amazon): You ship your stock to Amazon's warehouse and they handle everything including returns. More expensive but products get the Prime badge which increases sales by 20-30%."),
                    ("Set Your Price", "Research similar products and price competitively. Account for Amazon's referral fee (8-20% depending on category) plus any FBA fees if applicable."),
                    ("Launch & Promote", "Once live, consider running Sponsored Products ads (pay per click) to get initial visibility. Ask satisfied customers to leave honest reviews — reviews are critical for Amazon ranking."),
                    ("Get Paid", "Amazon pays every 14 days directly to your bank account after deducting fees."),
                ],
                "tips": [
                    "Your product title should include brand, material, key feature, size or quantity, and main keyword — keep it under 200 characters",
                    "Use all 5 bullet points to highlight benefits not just features — lead with the benefit",
                    "Professional photography significantly increases conversion — cell phone photos on a white background is the minimum",
                    "FBA gives your product the Prime badge which dramatically increases sales for most categories",
                    "Never pay for reviews — it violates Amazon's terms and can result in account suspension",
                    "Factor all fees into your price: referral fee (8-20%) + FBA fees + packaging + shipping",
                    "Amazon's Individual plan becomes more expensive than Professional once you sell more than 40 items per month",
                ],
                "fees": "Individual plan: $0.99 per item sold. Professional plan: $39.99 per month. Referral fee: 8-20% per sale depending on category. FBA fees: vary by product size and weight.",
                "link": "https://sellercentral.amazon.com",
            },
            "Instagram": {
                "intro": "Instagram has over 2 billion monthly active users and 130 million users tap on shopping posts every single month. It is ideal for visually appealing products like crafts, clothing, beauty, and home goods. Setting up Instagram Shopping is free.",
                "requirements": [
                    "Instagram Business or Creator account (not a personal account)",
                    "Facebook Business Page linked to your Instagram",
                    "Physical products only (services and digital products are not eligible)",
                    "A website you own (for catalog verification in most regions)",
                    "Products must comply with Instagram Commerce Policies",
                ],
                "steps": [
                    ("Switch To A Business Account", "Open Instagram, go to Settings, tap Account, then tap Switch to Professional Account. Choose Business. This is required before you can access shopping features."),
                    ("Create A Facebook Business Page", "Go to facebook.com and create a Business Page for your shop. Link it to your Instagram in Settings under Linked Accounts. This is required even if you do not plan to sell on Facebook."),
                    ("Open Commerce Manager", "Go to facebook.com/commerce_manager on a computer. Click Get Started then Create a Shop. This is the control center for your Instagram shop."),
                    ("Choose Your Selling Platform", "If you use Shopify, select it for automatic sync. If not, choose I don't use these platforms and Instagram will create a product catalog for you manually."),
                    ("Add Your Products", "In Commerce Manager click Add Products. For each product add a name, description, price, and at least one photo. This becomes your product catalog."),
                    ("Link Your Instagram Account", "In Commerce Manager select your Instagram Business account. Choose your Facebook Page. Select or confirm your product catalog."),
                    ("Submit For Review", "Add your business details including customer support email, shipping information, and return policy. Agree to Meta's seller terms. Click Finish Setup and submit for review. Review typically takes a few days."),
                    ("Start Tagging Products", "Once approved go to your Instagram profile and tap the shopping bag icon. Now when you create a post, Reel, or Story you can tag your products directly. Viewers tap the tag to see the product and price."),
                    ("Receive Payments", "Outside the US customers are redirected to your website to complete purchase. Inside the US Instagram Checkout is available and handles payment within the app."),
                ],
                "tips": [
                    "Reels get the most organic reach on Instagram in 2026 — show your product being made or used in short videos",
                    "Tag products in every relevant post, Reel, and Story — each tag is a direct path to purchase",
                    "Post consistently — 3 to 5 times per week minimum to stay visible in the algorithm",
                    "Use your generated hashtags in every post — they dramatically increase discoverability",
                    "Respond to every comment and DM quickly — fast responses build trust and lead to sales",
                    "Add your WhatsApp number to your bio so local customers can contact you directly",
                    "Collaborate with micro-influencers in your niche — even 1000 follower accounts can drive real sales",
                    "Instagram Shopping may not be available in all regions of Pakistan — if unavailable use the link in bio strategy instead",
                ],
                "fees": "Setting up Instagram Shop: Free. No listing fees. No monthly fees. Instagram takes a selling fee only for US-based Instagram Checkout. For most sellers outside the US it is completely free.",
                "link": "https://facebook.com/commerce_manager",
            },
            "None / Not decided yet": {
                "intro": "Not sure which platform to sell on yet? Here is a quick comparison to help you decide based on your product type and goals.",
                "requirements": [],
                "steps": [
                    ("Daraz", "Best for: Pakistani market. Reaches millions of local buyers. Free to register. Requires CNIC. Commission 5-20% per sale. Visit: sellercenter.daraz.pk"),
                    ("Etsy", "Best for: Handmade, artisan, culturally unique products. International buyers. $0.20 per listing + 6.5% commission. Pakistani sellers use Payoneer. Visit: etsy.com/sell"),
                    ("Amazon", "Best for: Scaling internationally with consistent stock. Massive global reach. Individual plan $0.99/item or Professional $39.99/month. Visit: sellercentral.amazon.com"),
                    ("Instagram", "Best for: Visual products with a strong story. Building a brand and loyal following. Free to set up. Best combined with Daraz or Etsy for actual checkout. Visit: instagram.com"),
                    ("WhatsApp Business", "Best for: Direct local sales with zero fees. Create a catalog in WhatsApp Business app, share your product photos and price, and receive orders directly. Completely free and requires no technical setup."),
                ],
                "tips": [
                    "Start with Daraz if your primary market is Pakistan — lowest barrier to entry",
                    "Start with Etsy if your product is handmade and has cultural uniqueness — international buyers pay premium prices for authentic crafts",
                    "Use Instagram alongside any platform — it drives awareness and sends buyers to your actual shop",
                    "WhatsApp Business is completely free and requires zero technical knowledge — ideal for absolute beginners",
                    "You do not have to choose just one — many successful sellers use Daraz + Instagram + WhatsApp together",
                ],
                "fees": "Varies by platform. Daraz and Instagram are free to start. Etsy charges $0.20 per listing. Amazon charges $0.99 per item or $39.99/month.",
                "link": "",
            },
        }

        guide = SELLING_GUIDES.get(marketplace, SELLING_GUIDES["None / Not decided yet"])
        
        with st.expander("📖 Click to view your complete selling guide", expanded=False):
            st.markdown(f"### About {marketplace}")
            st.info(guide["intro"])

            if guide["requirements"]:
                st.markdown("#### ✅ What You Need Before You Start")
                for req in guide["requirements"]:
                    st.markdown(f"- {req}")

            st.markdown("#### 🪜 Step-by-Step Guide")
            for i, (step_title, step_desc) in enumerate(guide["steps"], 1):
                st.markdown(f"**Step {i}: {step_title}**")
                st.markdown(f"{step_desc}")
                st.markdown("")

            st.markdown("#### 💡 Tips For Success")
            for tip in guide["tips"]:
                st.markdown(f"- {tip}")

            st.markdown(f"#### 💰 Fees Summary")
            st.markdown(guide["fees"])

            if guide["link"]:
                st.markdown(f"#### 🔗 Get Started")
                st.markdown(f"[Click here to go to {marketplace} →]({guide['link']})")

        # ================================================================
        # DOWNLOAD BUTTON
        # ================================================================
        full_package = f"""
ARTISAN NEXUS — COMPLETE LISTING PACKAGE
Product: {product_name}
Category: {product_type}
Marketplace: {marketplace}
Output Language: {selected_output_lang}
{"=" * 50}

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
# ---- SEND TO N8N ----
        if seller_email and "@" in seller_email and "." in seller_email:
            n8n_webhook = "https://muhammad963.app.n8n.cloud/webhook/7c195f67-3083-4bd2-ae84-b726ce4431c3"
            payload = {
                "email": seller_email,
                "product_name": product_name,
                "marketplace": marketplace,
                "title": title,
                "description": description,
                "seo": seo,
                "hashtags": hashtags,
                "price_suggestion": price_suggestion,
                "caption": caption,
                "marketplace_listing": marketplace_listing
            }
            try:
                n8n_response = requests.post(n8n_webhook, json=payload, timeout=10)
                if n8n_response.status_code == 200:
                    st.success("📧 Listing sent to your email!")
                else:
                    st.warning("Email delivery unavailable. Use the download button instead.")
            except:
                st.warning("Email delivery unavailable. Use the download button instead.")
