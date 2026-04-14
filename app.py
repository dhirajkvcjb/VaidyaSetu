import streamlit as st
import pandas as pd
from groq import Groq

# Load your data
df = pd.read_csv("data.csv", encoding="utf-8")

# Build examples from your data to teach the AI
def build_examples():
    examples = ""
    for _, row in df.head(20).iterrows():
        examples += f"Marathi: {row['dialect_phrase']}\nEnglish: {row['medical_english']}\n\n"
    return examples

# Translate function
def translate(phrase, region):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    examples = build_examples()
    
    system_prompt = f"""You are a medical translator specialized in converting colloquial Marathi dialect phrases into clear medical English that a doctor can understand.

You understand regional Marathi dialects from areas like Pune, Nashik, Kolhapur, Vidarbha, Marathwada, and Konkan.

Here are some examples of how local Marathi phrases map to medical English:

{examples}

Rules:
- Translate the medical meaning, not just the literal words
- Keep the output clear and professional for a doctor
- If the phrase mentions a body part or symptom, make it medically precise
- Always mention the region context in your translation
- Keep response to 2-3 sentences maximum"""

    user_message = f"Region: {region}\nMarathi phrase: {phrase}\n\nTranslate this to medical English for a doctor."

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        max_tokens=200
    )
    
    return response.choices[0].message.content

# UI
st.set_page_config(page_title="VaidyaSetu", page_icon="🏥")

st.title("🏥 VaidyaSetu")
st.subheader("Bridging language gaps between patients and doctors")

st.divider()

region = st.selectbox(
    "Select Patient's Region",
    ["Pune", "Nashik", "Kolhapur", "Vidarbha", "Marathwada", "Konkan"]
)

phrase = st.text_area(
    "Enter Patient's Marathi Phrase",
    placeholder="e.g. माझ्या पोटात आग होतेय...",
    height=100
)

if st.button("Translate for Doctor", type="primary"):
    if phrase.strip() == "":
        st.warning("Please enter a phrase first.")
    else:
        with st.spinner("Translating..."):
            result = translate(phrase, region)
        st.success("Translation:")
        st.write(result)

st.divider()
st.caption("Built to bridge the communication gap between rural Marathi patients and doctors.")