from functools import lru_cache
from toolbox import get_conf
CODE_HIGHLIGHT, ADD_WAIFU, LAYOUT = get_conf("CODE_HIGHLIGHT", "ADD_WAIFU", "LAYOUT")


def minimize_js(common_js_path):
    try:
        import rjsmin, hashlib, glob, os
        for old_min_js in glob.glob(common_js_path + '.min.*.js'):
            os.remove(old_min_js)
        c_jsmin = rjsmin.jsmin
        with open(common_js_path, "r", encoding='utf-8') as f:
            js_content = f.read()
        minimized_js_content = c_jsmin(js_content)
        sha_hash = hashlib.sha256(minimized_js_content.encode()).hexdigest()[:8]
        minimized_js_path = common_js_path + '.min.' + sha_hash + '.js'
        with open(minimized_js_path, "w", encoding='utf-8') as f:
            f.write(minimized_js_content)
        return minimized_js_path
    except:
        return common_js_path


@lru_cache
def get_common_html_javascript_code():
    js = "\n"
    common_js_path_list = [
        "themes/common.js",
        "themes/theme.js",
        "themes/tts.js",
        "themes/init.js",
        "themes/welcome.js",
    ]

    for common_js_path in common_js_path_list:
        minimized_js_path = minimize_js(common_js_path) if '.min.' not in common_js_path else common_js_path
        jsf = f"file={minimized_js_path}"
        js += f"""<script src="{jsf}"></script>\n"""

    return js
