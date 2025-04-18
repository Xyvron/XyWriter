import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
apikey= os.getenv("OPENROUTER_API_KEY")

client = openai.OpenAI(
    api_key=apikey,
    base_url="https://openrouter.ai/api/v1"
)

def reset_form():
    st.session_state.input_text = ""
    st.session_state.input_style = ""
    st.session_state.result = ""

if "history" not in st.session_state:
    st.session_state.history = []
st.set_page_config(page_title="Alvara AI", page_icon="https://github.com/Xyvron/Xyvron-Asset/blob/main/Xyvron_icon_64x64.png?raw=true")

st.image("https://github.com/Xyvron/Xyvron-Asset/blob/main/Xyvron_icon_64x64.png?raw=true", width=40)
st.title("XyWriter")
st.subheader("Smart Text Rewriter")

userinput = st.text_area("Input Text: ", height=150, key="input_text")
gaya = st.text_input("Choose Rewrite Style : ", placeholder="Example: Formal, Funny, Casual", key="input_style")
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "input_style" not in st.session_state:
    st.session_state.input_style = ""

if st.button("Transform") and userinput :
    prompt = f"Ubah atau ketik ulang text berikut ini dengan gaya {gaya.lower()}:\n\n{userinput}\n\nhasil:\n\nketik ulang kalimat tersebut agar bisa mendapatkan hasil seperti penulis yang profesional"

    try :
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        result = response.choices[0].message.content.strip()
        st.session_state.result = result
        st.session_state.history.append({
            "text": userinput,
            "style": gaya,
            "result": st.session_state.result
        })
        st.text_area("Result : ", value=result, height=200)

        if st.session_state.result:
            st.download_button(
                label="Download Result",
                data=st.session_state.result,
                file_name="XyWriter.txt",
                mime="text/plain"
            )
    
    except Exception as e : 
        st.error(f"Error : {str(e)}")

with st.sidebar.expander("Result History"):
    for i, item in enumerate(st.session_state.history[::-1]):  # terbaru di atas
        st.markdown(f"**{i+1}. Style: {item['style']}**")
        st.markdown(f"Kalimat Asli:\n {item['text']}")
        st.markdown(f"Result:\n```\n{item['result']}\n```")
        st.markdown("---")

    if st.button("Clear History"):
        st.session_state.history = []

st.button("Rewrite Another Text", on_click=reset_form)