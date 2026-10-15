function remove_legacy_cookie() {
    setCookie("web_cookie_cache", "", -1);
    setCookie("js_previous_chat_cookie", "", -1);
    setCookie("js_previous_history_cookie", "", -1);
}


function processFontFamily(fontfamily) {
    // 检查是否包含括号
    if (fontfamily.includes('(')) {
        // 分割字符串
        const parts = fontfamily.split('(');
        const fontNamePart = parts[1].split(')')[0].trim(); // 获取括号内的部分

        // 检查是否包含 @
        if (fontNamePart.includes('@')) {
            const [fontName, fontUrl] = fontNamePart.split('@').map(part => part.trim());
            return { fontName, fontUrl };
        } else {
            return { fontName: fontNamePart, fontUrl: null };
        }
    } else {
        return { fontName: fontfamily, fontUrl: null };
    }
}

// 检查字体是否存在
function checkFontAvailability(fontfamily) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');

        // 设置两个不同的字体进行比较
        const testText = 'abcdefghijklmnopqrstuvwxyz0123456789';
        context.font = `16px ${fontfamily}, sans-serif`;
        const widthWithFont = context.measureText(testText).width;

        context.font = '16px sans-serif';
        const widthWithFallback = context.measureText(testText).width;

        // 如果宽度相同，说明字体不存在
        resolve(widthWithFont !== widthWithFallback);
    });
}
async function checkFontAvailabilityV2(fontfamily) {
    fontName = fontfamily;
    console.log('Checking font availability:', fontName);
    if ('queryLocalFonts' in window) {
        try {
            const fonts = await window.queryLocalFonts();
            const fontExists = fonts.some(font => font.family === fontName);
            console.log(`Local Font "${fontName}" exists:`, fontExists);
            return fontExists;
        } catch (error) {
            console.error('Error querying local fonts:', error);
            return false;
        }
    } else {
        console.error('queryLocalFonts is not supported in this browser.');
        return false;
    }
}
// 动态加载字体
function loadFont(fontfamily, fontUrl) {
    return new Promise((resolve, reject) => {
        // 使用 Google Fonts 或其他字体来源
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = fontUrl;
        link.onload = () => {
            toast_push(`字体 "${fontfamily}" 已成功加载`, 3000);
            resolve();
        };
        link.onerror = (error) => {
            reject(error);
        };
        document.head.appendChild(link);
    });
}
function gpt_academic_change_chatbot_font(fontfamily, fontsize, fontcolor) {
    const chatbot = document.querySelector('#gpt-chatbot');
    // 检查元素是否存在
    if (chatbot) {
        if (fontfamily != null) {
            // 更改字体
            const result = processFontFamily(fontfamily);
            if (result.fontName == "Theme-Default-Font") {
                chatbot.style.fontFamily = result.fontName;
                return;
            }
            // 检查字体是否存在
            checkFontAvailability(result.fontName).then((isAvailable) => {
                if (isAvailable) {
                    // 如果字体存在，直接应用
                    chatbot.style.fontFamily = result.fontName;
                } else {
                    if (result.fontUrl == null) {
                        // toast_push('无法加载字体，本地字体不存在，且URL未提供', 3000);
                        // 直接把失效的字体放上去，让系统自动fallback
                        chatbot.style.fontFamily = result.fontName;
                        return;
                    } else {
                        toast_push('正在下载字体', 3000);
                        // 如果字体不存在，尝试加载字体
                        loadFont(result.fontName, result.fontUrl).then(() => {
                            chatbot.style.fontFamily = result.fontName;
                        }).catch((error) => {
                            console.error(`无法加载字体 "${result.fontName}":`, error);
                        });
                    }
                }
            });

        }
        if (fontsize != null) {
            // 修改字体大小
            document.documentElement.style.setProperty(
                '--gpt-academic-message-font-size',
                `${fontsize}px`
            );
        }
        if (fontcolor != null) {
            // 更改字体颜色
            chatbot.style.color = fontcolor;
        }
    } else {
        console.error('#gpt-chatbot is missing');
    }
}

function footer_show_hide(show) {
    if (show) {
        document.querySelector('footer').style.display = '';
    } else {
        document.querySelector('footer').style.display = 'none';
    }
}

async function GptAcademicJavaScriptInit(dark, prompt, live2d, layout, tts) {
    // 第一部分，布局初始化
    remove_legacy_cookie();
    minor_ui_adjustment();
    update_conversation_metadata();
    window.addEventListener("gptac_restore_chat_from_local_storage", restore_chat_from_local_storage);

    // 加载欢迎页面
    const welcomeMessage = new WelcomeMessage();
    welcomeMessage.begin_render();
    chatbotIndicator = gradioApp().querySelector('#gpt-chatbot > div.wrap');
    var chatbotObserver = new MutationObserver(() => {
        chatbotContentChanged(1);
        welcomeMessage.update();
    });
    chatbotObserver.observe(chatbotIndicator, { attributes: true, childList: true, subtree: true });

    if (layout === "LEFT-RIGHT") { chatbotAutoHeight(); }
    if (layout === "LEFT-RIGHT") { limit_scroll_position(); }

    // 第二部分，读取Cookie，初始化界面
    //  darkmode 深色模式
    if (getCookie("js_darkmode_cookie")) {
        dark = getCookie("js_darkmode_cookie")
    }
    dark = dark == "True";
    if (document.querySelectorAll('.dark').length) {
        if (!dark) {
            document.querySelectorAll('.dark').forEach(el => el.classList.remove('dark'));
        }
    } else {
        if (dark) {
            document.querySelector('body').classList.add('dark');
        }
    }

    //  自动朗读
    if (tts != "DISABLE") {
        enable_tts = true;
        if (getCookie("js_auto_read_cookie")) {
            auto_read_tts = getCookie("js_auto_read_cookie")
            auto_read_tts = auto_read_tts == "True";
            if (auto_read_tts) {
                allow_auto_read_tts_flag = true;
            }
        }
    }

    // 字体
    gpt_academic_gradio_saveload("load", "elem_fontfamily", "js_fontfamily", null, "str");
    gpt_academic_change_chatbot_font(getCookie("js_fontfamily"), null, null);
    gpt_academic_gradio_saveload("load", "elem_fontsize", "js_fontsize", null, "str");
    gpt_academic_change_chatbot_font(null, getCookie("js_fontsize"), null);
    // SysPrompt 系统静默提示词
    gpt_academic_gradio_saveload("load", "elem_prompt", "js_system_prompt_cookie", null, "str");
    // Temperature 大模型温度参数
    gpt_academic_gradio_saveload("load", "elem_temperature", "js_temperature_cookie", null, "float");
    // md_dropdown 大模型类型选择
    if (getCookie("js_md_dropdown_cookie")) {
        const cached_model = getCookie("js_md_dropdown_cookie");
        var model_sel = await get_gradio_component("elem_model_sel");
        // determine whether the cached model is in the choices
        if (model_sel.props.choices.includes(cached_model)) {
            // change dropdown
            gpt_academic_gradio_saveload("load", "elem_model_sel", "js_md_dropdown_cookie", null, "str");
            // 连锁修改chatbot的label
            push_data_to_gradio_component({
                label: '当前模型：' + getCookie("js_md_dropdown_cookie"),
                __type__: 'update'
            }, "gpt-chatbot", "obj")
        }
    }

    // 主题加载（恢复到上次）
    change_theme("", "")

}
