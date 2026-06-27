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
                st.success("📧 Listing also sent to your email!")
            else:
                st.warning("Email delivery unavailable right now. Use the download button instead.")
        except:
            st.warning("Email delivery unavailable right now. Use the download button instead.")
