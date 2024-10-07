#1import os
import requests
import fitz  # PyMuPDF
import streamlit as st
import yaml
from config import GPT4V_KEY, GPT4V_ENDPOINT

# Define headers for API requests
headers = {
    "Content-Type": "application/json",
    "api-key": GPT4V_KEY,
}

def load_prompts():
    """Load prompts from the prompts.yaml file."""
    with open('prompts.yaml', 'r') as file:
        prompts = yaml.safe_load(file)
    return prompts

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def analyze_with_openai(prompt):
    """Send a prompt to OpenAI API and get the response."""
    data = {
        "model": "gpt-4",  # Specify the model name
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1500,
        "temperature": 0.7
    }
    
    response = requests.post(GPT4V_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return ""

def summarize_paper(text, prompt_template):
    """Generate a summary of the research paper."""
    prompt = prompt_template.format(paper_text=text)
    return analyze_with_openai(prompt)

def main():
    st.title("Research Paper Analyzer")
    
    # Load prompts from YAML file
    prompts = load_prompts()
    
    # File uploader for PDF files
    uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        pdf_path = os.path.join("papers", uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extract text from the PDF
        paper_text = extract_text_from_pdf(pdf_path)

        # Summarize the paper
        if paper_text:
            summary = summarize_paper(paper_text, prompts['summarize_paper'])
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.warning("No text extracted from the paper.")

if __name__ == "__main__":
    main()



#2222222
import os
import requests
import fitz  # PyMuPDF
import streamlit as st
import yaml
from config import GPT4V_KEY, GPT4V_ENDPOINT

# Define headers for API requests
headers = {
    "Content-Type": "application/json",
    "api-key": GPT4V_KEY,
}

def load_prompts():
    """Load prompts from the prompts.yaml file."""
    with open('prompts.yaml', 'r') as file:
        prompts = yaml.safe_load(file)
    return prompts

def extract_text_and_images_from_pdf(pdf_path):
    """Extract text and images from a PDF file."""
    text = ""
    images = []
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
            # Extract images
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                images.append((f"page_{page_num + 1}_img_{img_index + 1}.png", image_bytes))
    return text, images

def analyze_with_openai(prompt):
    """Send a prompt to OpenAI API and get the response."""
    data = {
        "model": "gpt-4",  # Specify the model name
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1500,
        "temperature": 0.7
    }
    
    response = requests.post(GPT4V_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return ""

def summarize_paper(text, prompt_template):
    """Generate a summary of the research paper."""
    prompt = prompt_template.format(paper_text=text)
    return analyze_with_openai(prompt)

def main():
    st.title("Research Paper Analyzer")
    
    # Load prompts from YAML file
    prompts = load_prompts()
    
    # File uploader for PDF files
    uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        pdf_path = os.path.join("papers", uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extract text and images from the PDF
        paper_text, images = extract_text_and_images_from_pdf(pdf_path)

        # Summarize the paper
        if paper_text:
            summary = summarize_paper(paper_text, prompts['summarize_paper'])
            st.subheader("Summary:")
            st.write(summary)

            # Display images
            st.subheader("Extracted Images:")
            for img_name, img_bytes in images:
                st.image(img_bytes, caption=img_name, use_column_width=True)

        else:
            st.warning("No text extracted from the paper.")

if __name__ == "__main__":
    main()
