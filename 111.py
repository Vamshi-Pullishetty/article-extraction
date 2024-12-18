import streamlit as st
import openai
from newspaper import Article

# Set your OpenAI API key
openai.api_key = "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"
def fetch_article(url):
    """Fetch and parse the article using the Newspaper library."""
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def generate_title_slug_tags_focus(content):
    """Generate a title, slug, tags, and focus keyphrase based on the content."""
    prompt = f"""
    Analyze the following content and generate:
    1. A concise and meaningful title (within 60 characters).
    2. A URL-friendly slug derived from the title.
    3. 50 SEO-friendly tags relevant to the content, separated by commas.
    4. A single focus keyphrase that best represents the central idea of the content.

    Content: {content}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.5
    )
    result = response.choices[0].message["content"].strip()
    
    # Extract title, slug, tags, and focus keyphrase
    lines = result.split("\n")
    title = lines[0].replace("Title:", "").strip()
    slug = lines[1].replace("Slug:", "").strip()
    tags = lines[2].replace("Tags:", "").strip()
    focus_keyphrase = lines[3].replace("Focus Keyphrase:", "").strip()
    return title, slug, tags, focus_keyphrase

def enhance_content(content, inbound_link, outbound_link):
    """Use OpenAI API to enhance content with SEO optimizations."""
    prompt = f"""
    Improve the following content to meet SEO standards:
    - Distribute relevant keywords evenly and naturally throughout the content.
    - Add at least one internal link: {inbound_link}.
    - Add at least one external link: {outbound_link}.
    - Expand the content to over 350 words without repeating information.
    - Make the text user-friendly and engaging while keeping it SEO optimized.

    Content: {content}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.7
    )
    return response.choices[0].message["content"]

def generate_meta_description(content):
    """Generate a meta description from the content."""
    prompt = f"Create a concise, 120-character meta description for the following content:\n\n{content}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.5
    )
    return response.choices[0].message["content"]

# Streamlit UI
st.title("SEO Content Enhancer")

# User Inputs
url = st.text_input("Enter the website URL:")
inbound_link = st.text_input("Enter an inbound link:")
outbound_link = st.text_input("Enter an outbound link:")

if st.button("Generate Article"):
    if url and inbound_link and outbound_link:
        with st.spinner("Fetching and processing content..."):
            # Fetch article content using Newspaper library
            try:
                content = fetch_article(url)
                # Generate title, slug, tags, and focus keyphrase
                title, slug, tags, focus_keyphrase = generate_title_slug_tags_focus(content)
                # Enhance content
                enhanced_content = enhance_content(content, inbound_link, outbound_link)
                # Generate meta description
                meta_description = generate_meta_description(enhanced_content)
                
                # Display Results
                st.subheader("Title")
                st.write(title)
                st.subheader("Slug")
                st.write(slug)
                st.subheader("Focus Keyphrase")
                st.write(focus_keyphrase)
                st.subheader("Tags")
                st.write(tags)
                st.subheader("Enhanced Content")
                st.write(enhanced_content)
                st.subheader("Meta Description")
                st.write(meta_description)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide all required inputs!")
