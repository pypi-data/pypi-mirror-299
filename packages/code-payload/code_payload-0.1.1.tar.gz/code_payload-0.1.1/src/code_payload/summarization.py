# src/code_payload/summarization.py

import tiktoken


def truncate_content(content: str, max_length: int) -> str:
    """
    Truncate the content to a specified maximum length.

    If the content exceeds the specified `max_length`, it is truncated and an ellipsis is appended.

    Args:
        content (str): The content to be truncated.
        max_length (int): The maximum length of the content after truncation.

    Returns:
        str: The truncated content, with an ellipsis appended if truncation occurred.

    Example:
        ```python
        from code_payload.summarization import truncate_content

        long_content = "This is a long piece of content that needs truncating."
        truncated = truncate_content(long_content, max_length=20)
        print(truncated)  # Outputs: "This is a long piec..."
        ```

    <!-- Example Test:
    >>> from code_payload.summarization import truncate_content
    >>> content = "This is a long piece of content that needs truncating."
    >>> truncated = truncate_content(content, max_length=20)
    >>> assert truncated == "This is a long piec..."
    -->
    """
    if len(content) <= max_length:
        return content
    return content[:max_length] + "..."

def summarize_content(content: str, max_tokens: int) -> str:
    """
    Summarize the content by truncating it to a specified token limit.

    This function uses a tokenization method to count the number of tokens in the content.
    If the content exceeds `max_tokens`, it is truncated.

    Args:
        content (str): The content to be summarized.
        max_tokens (int): The maximum number of tokens allowed in the summarized content.

    Returns:
        str: The summarized content.

    Example:
        ```python
        from code_payload.summarization import summarize_content

        long_content = "This is a long piece of content that needs summarizing."
        summarized = summarize_content(long_content, max_tokens=5)
        print(summarized)  # Outputs a truncated version within the token limit
        ```

    <!-- Example Test:
    >>> from code_payload.summarization import summarize_content
    >>> content = "This is a long piece of content that needs summarizing."
    >>> summarized = summarize_content(content, max_tokens=5)
    >>> assert len(tiktoken.get_encoding("gpt2").encode(summarized)) <= 5
    -->
    """
    tokens = tiktoken.get_encoding("gpt2").encode(content)

    if len(tokens) <= max_tokens:
        return content

    truncated_tokens = tokens[:max_tokens]
    truncated_content = tiktoken.get_encoding("gpt2").decode(truncated_tokens)

    return truncated_content + "...\n"
