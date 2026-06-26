import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
import io

# ---- CONFIGURATION ----
# Reads your API key from Streamlit secrets (safe, never in code)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"API Configuration Error: {e}")
    st.stop()

# ---- PAGE SETUP ----
st.set_page_config(page_title="Artisan Nexus", page_icon="🧵")
st.title("🧵 Artisan Nexus")
st.caption("Transform your product into a professional marketplace listing")

# ---- INPUT FORM ----
st.subheader("Tell us about your product")

product_name = st.text_input("Product Name *", 
    placeholder="e.g. Hand Embroidered Shawl")

col1, col2 = st.columns(2)
with col1:
    material = st.text_input("Material *", 
        placeholder="e.g. Pure Wool")
    region = st.text_input("Region of Origin", 
        placeholder="e.g. Swat, KPK")
with col2:
    technique = st.text_input("Production Technique", 
        placeholder="e.g. Hand Embroidery")
    price = st.text_input("Your Price (PKR or USD) *", 
        placeholder="e.g. PKR 2500")

marketplace = st.selectbox(
    "Target Marketplace *",
    ["Daraz", "Etsy", "Amazon", "Instagram"]
)

additional_notes = st.text_area("Additional Notes (optional)", 
    placeholder="Any other details about your product...")

uploaded_image = st.file_uploader(
    "Upload Product Photo *", 
    type=["jpg", "jpeg", "png", "webp"]
)

# Show preview of uploaded image
if uploaded_image:
    st.image(uploaded_image, caption="Your product", width=300)

# ---- GENERATE BUTTON ----
generate = st.button("✨ Generate My Listing", 
    type="primary", 
    use_container_width=True)

# ---- GENERATION LOGIC ----
if generate:
    # Validate required fields
    if not product_name or not material or not price or not uploaded_image:
        st.error("Please fill in all required fields (*) and upload an image.")
    else:
        with st.spinner("Analyzing your product and generating content..."):

            # -- CALL 1: VISION --
            # We only ask Gemini to describe what it SEES
            # Never to identify, name, or assume anything
            image = Image.open(uploaded_image)
            
            vision_prompt = """
            Describe only the visible characteristics of this product image.
            Include: colors present, patterns visible, texture appearance, 
            approximate size, decorative elements, and overall condition.
            Do NOT identify, name, assume origin, material, or cultural background.
            Only describe what you can literally see.
            """
            
            vision_response = model.generate_content([vision_prompt, image])
            visual_description = vision_response.text

            # -- CALL 2: GENERATION --
            # All facts come from seller
            # Visual description only adds what AI saw
            generation_prompt = f"""
You are an expert e-commerce content strategist specializing in 
South Asian marketplace listings.

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

Generate ALL of the following sections clearly labeled:

[TITLE]
A professional SEO-optimized product title. Include material, 
technique and region if provided.

[DESCRIPTION]
3 professional paragraphs. Use seller facts as truth. 
Reference visual description for appearance details only.
Do not invent history, certifications, or claims not provided.

[SEO KEYWORDS]
10 English keywords and 5 Urdu keywords relevant to this product.

[HASHTAGS]
20 Instagram hashtags and 5 Twitter/X hashtags.

[PRICE SUGGESTION]
Based on the seller's stated price of {price}, suggest a price range 
for {marketplace}. If selling on Etsy/Amazon, also suggest an 
international USD price. Explain your reasoning briefly.

[MARKETING CAPTION]
A compelling Instagram/social media caption with emojis 
and a call to action.

[ENGLISH LISTING]
A complete {marketplace}-ready listing in English with title, 
description and key details formatted for that platform.

[URDU LISTING]
Translate the title and description into proper Urdu script. 
Translate naturally, not literally.

RULES:
- Never invent specifications, history, certifications or dimensions
- Only reference cultural/origin details if seller provided them
- Keep tone professional, trustworthy, and customer-friendly
"""

            listing_response = model.generate_content(generation_prompt)
            full_output = listing_response.text

            # -- PARSE OUTPUT INTO SECTIONS --
            def extract_section(text, section_name, next_section=None):
                try:
                    start = text.find(f"[{section_name}]") + len(f"[{section_name}]")
                    if next_section:
                        end = text.find(f"[{next_section}]")
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
            caption = extract_section(full_output, "MARKETING CAPTION", "ENGLISH LISTING")
            english_listing = extract_section(full_output, "ENGLISH LISTING", "URDU LISTING")
            urdu_listing = extract_section(full_output, "URDU LISTING")

        # ---- OUTPUT TABS ----
        st.success("✅ Your listing package is ready!")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📝 Listing", 
            "🔍 SEO & Hashtags", 
            "💰 Pricing",
            "📱 Social Media",
            "🌐 Urdu Version"
        ])

        with tab1:
            st.subheader("Product Title")
            st.info(title)
            st.subheader("Product Description")
            st.write(description)
            st.subheader(f"{marketplace} Ready Listing")
            st.write(english_listing)

        with tab2:
            st.subheader("SEO Keywords")
            st.write(seo)
            st.subheader("Hashtags")
            st.write(hashtags)

        with tab3:
            st.subheader("Price Suggestion")
            st.write(price_suggestion)

        with tab4:
            st.subheader("Marketing Caption")
            st.write(caption)

        with tab5:
            st.subheader("Urdu Listing")
            st.write(urdu_listing)

        # ---- DOWNLOAD BUTTON ----
        full_package = f"""
ARTISAN NEXUS - COMPLETE LISTING PACKAGE
Product: {product_name}
Generated for: {marketplace}
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

ENGLISH LISTING:
{english_listing}

URDU LISTING:
{urdu_listing}
"""
        st.download_button(
            label="📥 Download Full Package",
            data=full_package,
            file_name=f"artisan_nexus_{product_name.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

        # ---- SEND TO N8N (optional) ----
        # Uncomment this when you have your n8n webhook URL ready
        # n8n_webhook = "YOUR_N8N_WEBHOOK_URL"
        # payload = {
        #     "product_name": product_name,
        #     "marketplace": marketplace,
        #     "title": title,
        #     "description": description,
        #     "seo": seo,
        #     "hashtags": hashtags,
        #     "price_suggestion": price_suggestion,
        #     "caption": caption,
        #     "english_listing": english_listing,
        #     "urdu_listing": urdu_listing
        # }
        # requests.post(n8n_webhook, json=payload)
