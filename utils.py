import fitz  # PyMuPDF
import requests
import yaml

def load_prompts():
    """Load prompts from the prompts.yaml file."""
    with open('prompts.yaml', 'r') as file:
        prompts = yaml.safe_load(file)
    return prompts

def extract_text_and_images_from_pdf(pdf_bytes):
    """Extract text and images from a PDF file."""
    text = ""
    images = []
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text += page.get_text()
        # Extract images
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            images.append((f"page_{page_num + 1}_img_{img_index + 1}.png", image_bytes))
    
    return text, images

def analyze_with_openai(prompt, endpoint, headers):
    """Send a prompt to OpenAI API and get the response."""
    data = {
        "model": "gpt-4",  # Specify the model name
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1500,
        "temperature": 0.7
    }
    
    response = requests.post(endpoint, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        return None, f"Error: {response.status_code}, {response.text}"

def summarize_and_explain_paper(text, prompt_template, endpoint, headers):
    """Generate a summary and explanations for images/graphs in the research paper."""
    prompt = prompt_template.format(paper_text=text)
    return analyze_with_openai(prompt, endpoint, headers)
