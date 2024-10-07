import streamlit as st
import yaml
from config import GPT4V_KEY, GPT4V_ENDPOINT
from utils import load_prompts, extract_text_and_images_from_pdf, analyze_with_openai, summarize_and_explain_paper

headers = {
    "Content-Type": "application/json",
    "api-key": GPT4V_KEY,
}

def main():
    st.title("Research Paper Analyzer")
    
    prompts = load_prompts()
    
    uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type="pdf")

    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        
        if st.button("Analyze Research paper"):
            paper_text, images = extract_text_and_images_from_pdf(pdf_bytes)

            if paper_text:
                summary_and_explanation = summarize_and_explain_paper(
                    paper_text, 
                    prompts['summarize_paper'],
                    GPT4V_ENDPOINT, 
                    headers
                )
                st.subheader("Summary and Image Explanations:")
                st.write(summary_and_explanation)

                st.subheader("Extracted Images:")
                for img_name, img_bytes in images:
                    st.image(img_bytes, caption=img_name, use_column_width=True)
            else:
                st.warning("No text extracted from the paper.")

if __name__ == "__main__":
    main()
