import re
import os
import requests


def start_with_url(inputs: str):
    """
    检查输入是否以 http:// 或 https:// 开头，且为有效的网址
    """
    if not ("http://" in inputs or "https://" in inputs):
        return False
    try:
        text = inputs.strip(',.!?，。！？ \t\n\r')
        words = text.split()
        if len(words) != 1:
            return False
        from urllib.parse import urlparse
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except:
        return False


def _extract_web_text(url: str) -> str:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    html_content = response.text
    try:
        import trafilatura
        extracted_text = trafilatura.extract(
            html_content,
            include_comments=False,
            include_tables=True,
            include_links=False,
            no_fallback=False,
        )
        if extracted_text:
            return ' '.join(extracted_text.split()).strip()
    except ImportError:
        pass
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    return ' '.join(text.split()).strip()


def load_web_content(inputs: str, chatbot_with_cookie, history: list):
    from toolbox import update_ui

    try:
        chatbot_with_cookie.append([None, "正在提取网页内容，请稍作等待..."])
        yield from update_ui(chatbot=chatbot_with_cookie, history=history)
        web_content = _extract_web_text(inputs.strip(',.!?，。！？ \t\n\r'))
        chatbot_with_cookie.pop()
        chatbot_with_cookie.append([None, f"网页{inputs}的文本内容如下：" + web_content])
        history.extend([f"网页{inputs}的文本内容如下：" + web_content])
        yield from update_ui(chatbot=chatbot_with_cookie, history=history)
    except Exception as e:
        if len(chatbot_with_cookie) > 0 and chatbot_with_cookie[-1][-1] == "正在提取网页内容，请稍作等待...":
            chatbot_with_cookie.pop()
        chatbot_with_cookie.append([inputs, f"网页内容提取失败: {str(e)}"])
        yield from update_ui(chatbot=chatbot_with_cookie, history=history)
