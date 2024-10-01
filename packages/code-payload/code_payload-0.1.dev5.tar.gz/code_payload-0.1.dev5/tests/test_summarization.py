from src.code_payload.summarization import summarize_content, truncate_content


def test_truncate_content_empty_string():
    """Test truncate_content when the input string is empty."""
    content = ""
    truncated = truncate_content(content, max_length=20)
    assert truncated == ""

def test_summarize_content_with_empty_string():
    """Test summarize_content with an empty string."""
    content = ""
    summarized = summarize_content(content, max_tokens=5)
    assert summarized == ""

def test_summarize_content_with_large_content():
    """Test summarize_content with content larger than max tokens."""
    content = "This is a long piece of content that needs summarizing." * 100
    summarized = summarize_content(content, max_tokens=5)
    assert len(summarized.split()) <= 5

def test_summarize_content_at_token_limit():
    content = "This is exactly five tokens."
    summarized = summarize_content(content, max_tokens=5)
    assert summarized == content

def test_summarize_content_with_exact_token_limit():
    content = "This is exactly five tokens."
    summarized = summarize_content(content, max_tokens=5)
    assert summarized == content

def test_summarize_content_edge_cases():
    content = "This is exactly five tokens."
    summarized = summarize_content(content, max_tokens=5)
    assert summarized == content
