// 标志位
enable_tts = false;

// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//  第 1 部分: 工具函数
// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

function push_data_to_gradio_component(DAT, ELEM_ID, TYPE) {
    // type,               // type==="str" / type==="float"
    if (TYPE == "str") {
        // convert dat to string: do nothing
    }
    else if (TYPE == "obj") {
        // convert dat to string: do nothing
    }
    else if (TYPE == "no_conversion") {
        // no nothing
    }
    else if (TYPE == "float") {
        // convert dat to float
        DAT = parseFloat(DAT);
    }
    const myEvent = new CustomEvent('gpt_academic_update_gradio_component', {
        detail: {
            data: DAT,
            elem_id: ELEM_ID,
        }
    });
    window.dispatchEvent(myEvent);
}


async function get_gradio_component(ELEM_ID) {
    function waitFor(ELEM_ID) {
        return new Promise((resolve) => {
            const myEvent = new CustomEvent('gpt_academic_get_gradio_component_value', {
                detail: {
                    elem_id: ELEM_ID,
                    resolve,
                }
            });
            window.dispatchEvent(myEvent);
        });
    }
    result = await waitFor(ELEM_ID);
    return result;
}


async function get_data_from_gradio_component(ELEM_ID) {
    let comp = await get_gradio_component(ELEM_ID);
    return comp.props.value;
}


function update_array(arr, item, mode) {
    //   // Remove "输入清除键"
    //   p = updateArray(p, "输入清除键", "remove");
    //   console.log(p); // Should log: ["基础功能区", "函数插件区"]

    //   // Add "输入清除键"
    //   p = updateArray(p, "输入清除键", "add");
    //   console.log(p); // Should log: ["基础功能区", "函数插件区", "输入清除键"]

    const index = arr.indexOf(item);
    if (mode === "remove") {
        if (index !== -1) {
            // Item found, remove it
            arr.splice(index, 1);
        }
    } else if (mode === "add") {
        if (index === -1) {
            // Item not found, add it
            arr.push(item);
        }
    }
    return arr;
}


function gradioApp() {
    // https://github.com/GaiZhenbiao/ChuanhuChatGPT/tree/main/web_assets/javascript
    const elems = document.getElementsByTagName('gradio-app');
    const elem = elems.length == 0 ? document : elems[0];
    if (elem !== document) {
        elem.getElementById = function (id) {
            return document.getElementById(id);
        };
    }
    return elem.shadowRoot ? elem.shadowRoot : elem;
}


function setCookie(name, value, days) {
    var expires = "";

    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }

    document.cookie = name + "=" + value + expires + "; path=/";
}


function getCookie(name) {
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookies = decodedCookie.split(';');

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();

        if (cookie.indexOf(name + "=") === 0) {
            return cookie.substring(name.length + 1, cookie.length);
        }
    }

    return null;
}


let toastCount = 0;
function toast_push(msg, duration) {
    duration = isNaN(duration) ? 3000 : duration;
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => {
        toast.style.top = `${parseInt(toast.style.top, 10) - 70}px`;
    });
    const m = document.createElement('div');
    m.innerHTML = msg;
    m.classList.add('toast');
    m.style.cssText = `font-size: var(--text-md) !important; color: rgb(255, 255, 255); background-color: rgba(0, 0, 0, 0.6); padding: 10px 15px; border-radius: 4px; position: fixed; top: ${50 + toastCount * 70}%; left: 50%; transform: translateX(-50%); width: auto; text-align: center; transition: top 0.3s;`;
    document.body.appendChild(m);
    setTimeout(function () {
        m.style.opacity = '0';
        setTimeout(function () {
            document.body.removeChild(m);
            toastCount--;
        }, 500);
    }, duration);
    toastCount++;
}


function toast_up(msg) {
    var m = document.getElementById('toast_up');
    if (m) {
        document.body.removeChild(m); // remove the loader from the body
    }
    m = document.createElement('div');
    m.id = 'toast_up';
    m.innerHTML = msg;
    m.style.cssText = "font-size: var(--text-md) !important; color: rgb(255, 255, 255); background-color: rgba(0, 0, 100, 0.6); padding: 10px 15px; margin: 0 0 0 -60px; border-radius: 4px; position: fixed; top: 50%; left: 50%; width: auto; text-align: center;";
    document.body.appendChild(m);
}


function toast_down() {
    var m = document.getElementById('toast_up');
    if (m) {
        document.body.removeChild(m); // remove the loader from the body
    }
}


function begin_loading_status() {
    // Create the loader div and add styling
    var loader = document.createElement('div');
    loader.id = 'Js_File_Loading';
    var C1 = document.createElement('div');
    var C2 = document.createElement('div');
    // var C3 = document.createElement('span');
    // C3.textContent = '上传中...'
    // C3.style.position = "fixed";
    // C3.style.top = "50%";
    // C3.style.left = "50%";
    // C3.style.width = "80px";
    // C3.style.height = "80px";
    // C3.style.margin = "-40px 0 0 -40px";

    C1.style.position = "fixed";
    C1.style.top = "50%";
    C1.style.left = "50%";
    C1.style.width = "80px";
    C1.style.height = "80px";
    C1.style.borderLeft = "12px solid #00f3f300";
    C1.style.borderRight = "12px solid #00f3f300";
    C1.style.borderTop = "12px solid #82aaff";
    C1.style.borderBottom = "12px solid #82aaff"; // Added for effect
    C1.style.borderRadius = "50%";
    C1.style.margin = "-40px 0 0 -40px";
    C1.style.animation = "spinAndPulse 2s linear infinite";

    C2.style.position = "fixed";
    C2.style.top = "50%";
    C2.style.left = "50%";
    C2.style.width = "40px";
    C2.style.height = "40px";
    C2.style.borderLeft = "12px solid #00f3f300";
    C2.style.borderRight = "12px solid #00f3f300";
    C2.style.borderTop = "12px solid #33c9db";
    C2.style.borderBottom = "12px solid #33c9db"; // Added for effect
    C2.style.borderRadius = "50%";
    C2.style.margin = "-20px 0 0 -20px";
    C2.style.animation = "spinAndPulse2 2s linear infinite";

    loader.appendChild(C1);
    loader.appendChild(C2);
    // loader.appendChild(C3);
    document.body.appendChild(loader); // Add the loader to the body

    // Set the CSS animation keyframes for spin and pulse to be synchronized
    var styleSheet = document.createElement('style');
    styleSheet.id = 'Js_File_Loading_Style';
    styleSheet.textContent = `
    @keyframes spinAndPulse {
        0% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(90deg) scale(1.1); }
        50% { transform: rotate(180deg) scale(1); }
        75% { transform: rotate(270deg) scale(0.9); }
        100% { transform: rotate(360deg) scale(1); }
    }

    @keyframes spinAndPulse2 {
        0% { transform: rotate(-90deg);}
        25% { transform: rotate(-180deg);}
        50% { transform: rotate(-270deg);}
        75% { transform: rotate(-360deg);}
        100% { transform: rotate(-450deg);}
    }
    `;
    document.head.appendChild(styleSheet);
}


function cancel_loading_status() {
    // remove the loader from the body
    var loadingElement = document.getElementById('Js_File_Loading');
    if (loadingElement) {
        document.body.removeChild(loadingElement);
    }
    var loadingStyle = document.getElementById('Js_File_Loading_Style');
    if (loadingStyle) {
        document.head.removeChild(loadingStyle);
    }
    // create new listen event
    let clearButton = document.querySelectorAll('div[id*="elem_upload"] button[aria-label="Clear"]');
    for (let button of clearButton) {
        button.addEventListener('click', function () {
            setTimeout(function () {
                register_upload_event();
            }, 50);
        });
    }
}


// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//  第 2 部分: 复制按钮
// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// 解压缩函数
function decompressString(compressedString) {
    // 第1步：Base64解码
    const binaryString = atob(compressedString);

    // 第2步：将二进制字符串转换为Uint8Array
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }

    // 第3步：使用DecompressionStream (基于Web Streams API)进行gzip解压缩
    const ds = new DecompressionStream('gzip');
    const decompressedStream = new Response(new Blob([bytes])).body.pipeThrough(ds);

    // 第4步：获取解压后的数据并转换为字符串
    return new Response(decompressedStream).text();
}

var allow_auto_read_continously = true;
var allow_auto_read_tts_flag = false;
function addCopyButton(botElement, index, is_last_in_arr) {
    // https://github.com/GaiZhenbiao/ChuanhuChatGPT/tree/main/web_assets/javascript
    // Copy bot button
    const copiedIcon = '<span><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height=".8em" width=".8em" xmlns="http://www.w3.org/2000/svg"><polyline points="20 6 9 17 4 12"></polyline></svg></span>';
    const copyIcon = '<span><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height=".8em" width=".8em" xmlns="http://www.w3.org/2000/svg"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg></span>';
    // const audioIcon = '<span><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height=".8em" width=".8em" xmlns="http://www.w3.org/2000/svg"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg></span>';
    const audioIcon = '<span><svg t="1713628577799" fill="currentColor" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4587" width=".9em" height=".9em"><path d="M113.7664 540.4672c0-219.9552 178.2784-398.2336 398.2336-398.2336S910.2336 320.512 910.2336 540.4672v284.4672c0 31.4368-25.4976 56.9344-56.9344 56.9344h-56.9344c-31.4368 0-56.9344-25.4976-56.9344-56.9344V597.2992c0-31.4368 25.4976-56.9344 56.9344-56.9344h56.9344c0-188.5184-152.7808-341.2992-341.2992-341.2992S170.7008 351.9488 170.7008 540.4672h56.9344c31.4368 0 56.9344 25.4976 56.9344 56.9344v227.5328c0 31.4368-25.4976 56.9344-56.9344 56.9344h-56.9344c-31.4368 0-56.9344-25.4976-56.9344-56.9344V540.4672z" p-id="4588"></path></svg></span>';
    // const cancelAudioIcon = '<span><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height=".8em" width=".8em" xmlns="http://www.w3.org/2000/svg"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg></span>';

    // audio functionality
    if (allow_auto_read_continously && is_last_in_arr && allow_auto_read_tts_flag) {
        process_latest_text_output(botElement.innerText, index);
    }

    const messageBtnColumnElement = botElement.querySelector('.message-btn-row');
    if (messageBtnColumnElement) {
        // if .message-btn-column exists
        return;
    }

    // 原始文本拷贝
    var copyButtonOrig = document.createElement('button');
    copyButtonOrig.classList.add('copy-bot-btn');
    copyButtonOrig.setAttribute('aria-label', 'Copy');
    copyButtonOrig.innerHTML = copyIcon;
    copyButtonOrig.addEventListener('click', async () => {
        try {
            const base64gzipcode = botElement.getElementsByClassName('raw_text')[0].innerText;
            const textToCopy = await decompressString(base64gzipcode);
            // push_text_to_audio(textToCopy).catch(console.error);
            if ("clipboard" in navigator) {
                await navigator.clipboard.writeText(textToCopy);
                copyButtonOrig.innerHTML = copiedIcon;
                setTimeout(() => {
                    copyButtonOrig.innerHTML = copyIcon;
                }, 1500);
            } else {
                const textArea = document.createElement("textarea");
                textArea.value = textToCopy;
                document.body.appendChild(textArea);
                textArea.select();
                try {
                    document.execCommand('copy');
                    copyButtonOrig.innerHTML = copiedIcon;
                    setTimeout(() => {
                        copyButtonOrig.innerHTML = copyIcon;
                    }, 1500);
                } catch (error) {
                    console.error("Copy failed: ", error);
                }
                document.body.removeChild(textArea);
            }
        } catch (error) {
            console.error("Copy failed: ", error);
        }
    });

    if (enable_tts) {
        var audioButton = document.createElement('button');
        audioButton.classList.add('audio-toggle-btn');
        audioButton.innerHTML = audioIcon;
        audioButton.addEventListener('click', async () => {
            if (audioPlayer.isPlaying) {
                allow_auto_read_tts_flag = false;
                toast_push('自动朗读已禁用。', 3000);
                audioPlayer.stop();
                setCookie("js_auto_read_cookie", "False", 365);

            } else {
                allow_auto_read_tts_flag = true;
                toast_push('正在合成语音 & 自动朗读已开启 (再次点击此按钮可禁用自动朗读)。', 3000);
                // toast_push('正在合成语音', 3000);
                const readText = botElement.innerText;
                prev_chatbot_index = index;
                prev_text = readText;
                prev_text_already_pushed = readText;
                push_text_to_audio(readText);
                setCookie("js_auto_read_cookie", "True", 365);
            }
        });
    }

    var messageBtnColumn = document.createElement('div');
    messageBtnColumn.classList.add('message-btn-row');
    // messageBtnColumn.appendChild(copyButton);
    messageBtnColumn.appendChild(copyButtonOrig);
    if (enable_tts) {
        messageBtnColumn.appendChild(audioButton);
    }
    botElement.appendChild(messageBtnColumn);
}


let timeoutID = null;
let lastInvocationTime = 0;
let lastArgs = null;
function do_something_but_not_too_frequently(min_interval, func) {
    return function (...args) {
        lastArgs = args;
        const now = Date.now();
        if (!lastInvocationTime || (now - lastInvocationTime) >= min_interval) {
            lastInvocationTime = now;
            // 现在就执行
            setTimeout(() => {
                func.apply(this, lastArgs);
            }, 0);
        } else if (!timeoutID) {
            // 等一会执行
            timeoutID = setTimeout(() => {
                timeoutID = null;
                lastInvocationTime = Date.now();
                func.apply(this, lastArgs);
            }, min_interval - (now - lastInvocationTime));
        } else {
            // 压根不执行
        }
    }
}


function chatbotContentChanged(attempt = 1, force = false) {
    for (var i = 0; i < attempt; i++) {
        setTimeout(() => {
            const messages = gradioApp().querySelectorAll('#gpt-chatbot .message-wrap .message.bot');
            messages.forEach((message, index, arr) => {
                // Check if the current message is the last in the array
                const is_last_in_arr = index === arr.length - 1;

                // Now pass both the message element and the is_last_in_arr boolean to addCopyButton
                addCopyButton(message, index, is_last_in_arr);

                // if last message, add stop btn link
                addStopButton(message, index, is_last_in_arr);

                // save_conversation_history
                save_conversation_history_slow_down();
            });
            // gradioApp().querySelectorAll('#gpt-chatbot .message-wrap .message.bot').forEach(addCopyButton);
        }, i === 0 ? 0 : 200);
    }
    // we have moved mermaid-related code to gradio-fix repository: binary-husky/gradio-fix@32150d0

}

function addStopButton(botElement, index, is_last_in_arr) {
    function is_generating() {
        var statePanelElement = document.getElementById("state-panel");
        var generatingElement = statePanelElement.querySelector(".generating");
        if (generatingElement) {
            return true;
        } else {
            return false;
        }
    }
    function on_stop_btn_click() {
        let stopButton = document.getElementById("elem_stop");
        stopButton.click();
    }
    function remove_stop_generate_btn(messageTailElement) {
        // remove all child elements of messageTailElement
        while (messageTailElement.firstChild) {
            messageTailElement.removeChild(messageTailElement.firstChild);
        }
        messageTailElement.style.display = 'none';
        messageTailElement.classList.add('removed');
    }
    function add_stop_generate_btn() {
        // write here: add a beautiful stop btn `bottomElement` as child, when clicked execute on_stop_btn_click
        console.log("get_gradio_component")
        const bottomElement = document.createElement('button');
        bottomElement.className = 'ant-btn ant-btn-primary';
        bottomElement.innerHTML = `
            <span class="ant-btn-icon">
                <svg viewBox="64 64 896 896" focusable="false" data-icon="sync" width="1em" height="1em" fill="currentColor" aria-hidden="true" class="anticon anticon-sync anticon-spin">
                <path d="M168 504.2c1-43.7 10-86.1 26.9-126 17.3-41 42.1-77.7 73.7-109.4S337 212.3 378 195c42.4-17.9 87.4-27 133.9-27s91.5 9.1 133.8 27A341.5 341.5 0 01755 268.8c9.9 9.9 19.2 20.4 27.8 31.4l-60.2 47a8 8 0 003 14.1l175.7 43c5 1.2 9.9-2.6 9.9-7.7l.8-180.9c0-6.7-7.7-10.5-12.9-6.3l-56.4 44.1C765.8 155.1 646.2 92 511.8 92 282.7 92 96.3 275.6 92 503.8a8 8 0 008 8.2h60c4.4 0 7.9-3.5 8-7.8zm756 7.8h-60c-4.4 0-7.9 3.5-8 7.8-1 43.7-10 86.1-26.9 126-17.3 41-42.1 77.8-73.7 109.4A342.45 342.45 0 01512.1 856a342.24 342.24 0 01-243.2-100.8c-9.9-9.9-19.2-20.4-27.8-31.4l60.2-47a8 8 0 00-3-14.1l-175.7-43c-5-1.2-9.9 2.6-9.9 7.7l-.7 181c0 6.7 7.7 10.5 12.9 6.3l56.4-44.1C258.2 868.9 377.8 932 512.2 932c229.2 0 415.5-183.7 419.8-411.8a8 8 0 00-8-8.2z"></path>
                </svg>
            </span>
            <span>终止</span>
        `;
        bottomElement.classList.add('message_tail_stop');
        bottomElement.addEventListener('click', on_stop_btn_click);
        messageTailElement.appendChild(bottomElement);
    }

    // find a sub element of class `message_tail`
    const messageTailElement = botElement.querySelector('.message_tail');
    // if not is_last_in_arr, hide this elem (display none)
    if (!messageTailElement) {
        return;
    }
    if (messageTailElement.classList.contains('removed')) {
        return;
    }
    if (!is_last_in_arr) {
        remove_stop_generate_btn(messageTailElement);
        return;
    }
    messageTailElement.style.display = 'flex';
    const messageTailStopElem = messageTailElement.querySelector('.message_tail_stop');
    if(!is_generating()) {
        setTimeout(() => {
            if(!is_generating()) {
                remove_stop_generate_btn(messageTailElement);
                return;
            } else {
                if (!messageTailStopElem) {
                    add_stop_generate_btn()
                }
            }
        }, 500);
    } else {
        if (!messageTailStopElem) {
            add_stop_generate_btn()
        }
    }

}


// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//  第 3 部分: chatbot动态高度调整
// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
function chatbotAutoHeight() {
    // 自动调整高度：立即
    function update_height() {
        var { height_target, chatbot_height, chatbot } = get_elements(true);
        if (height_target != chatbot_height) {
            var pixelString = height_target.toString() + 'px';
            chatbot.style.maxHeight = pixelString; chatbot.style.height = pixelString;
        }
    }

    // 自动调整高度：缓慢
    function update_height_slow() {
        var { height_target, chatbot_height, chatbot } = get_elements();
        if (height_target != chatbot_height) {
            new_panel_height = (height_target - chatbot_height) * 0.5 + chatbot_height;
            if (Math.abs(new_panel_height - height_target) < 10) {
                new_panel_height = height_target;
            }
            var pixelString = new_panel_height.toString() + 'px';
            chatbot.style.maxHeight = pixelString; chatbot.style.height = pixelString;
        }
    }
    update_height();
    window.addEventListener('resize', function () { update_height(); });
    window.addEventListener('scroll', function () { update_height_slow(); });
    setInterval(function () { update_height_slow() }, 50); // 每50毫秒执行一次
}


swapped = false;
function swap_input_area() {
    // Get the elements to be swapped
    var element1 = document.querySelector("#input-panel");
    var element2 = document.querySelector("#basic-panel");

    // Get the parent of the elements
    var parent = element1.parentNode;

    // Get the next sibling of element2
    var nextSibling = element2.nextSibling;

    // Swap the elements
    parent.insertBefore(element2, element1);
    parent.insertBefore(element1, nextSibling);
    if (swapped) { swapped = false; }
    else { swapped = true; }
}


function get_elements(consider_state_panel = false) {
    var chatbot = document.querySelector('#gpt-chatbot > div.wrap.svelte-18telvq');
    if (!chatbot) {
        chatbot = document.querySelector('#gpt-chatbot');
    }
    const panel1 = document.querySelector('#input-panel').getBoundingClientRect();
    const panel2 = document.querySelector('#basic-panel').getBoundingClientRect();
    const panel3_elem = document.querySelector('#plugin-panel');
    const panel3 = panel3_elem ? panel3_elem.getBoundingClientRect() : { height: 0, bottom: 0 };
    // const panel4 = document.querySelector('#interact-panel').getBoundingClientRect();
    const panel_active = document.querySelector('#state-panel').getBoundingClientRect();
    if (consider_state_panel || panel_active.height < 25) {
        document.state_panel_height = panel_active.height;
    }
    // 25 是chatbot的label高度, 16 是右侧的gap
    var height_target = panel1.height + panel2.height + panel3.height + 0 + 0 - 25 + 16 * 2;
    // 禁止动态的state-panel高度影响
    height_target = height_target + (document.state_panel_height - panel_active.height)
    var height_target = parseInt(height_target);
    var chatbot_height = chatbot.style.height;
    // 交换输入区位置，使得输入区始终可用
    if (!swapped) {
        if (panel1.top != 0 && (0.9 * panel1.bottom + 0.1 * panel1.top) < 0) { swap_input_area(); }
    }
    else if (swapped) {
        if (panel2.top != 0 && panel2.top > 0) { swap_input_area(); }
    }
    // 调整高度
    const err_tor = 5;
    if (Math.abs(panel1.left - chatbot.getBoundingClientRect().left) < err_tor) {
        // 是否处于窄屏模式
        height_target = window.innerHeight * 0.6;
    } else {
        // 调整高度
        const chatbot_height_exceed = 15;
        const chatbot_height_exceed_m = 10;
        b_panel = Math.max(panel1.bottom, panel2.bottom, panel3.bottom)
        if (b_panel >= window.innerHeight - chatbot_height_exceed) {
            height_target = window.innerHeight - chatbot.getBoundingClientRect().top - chatbot_height_exceed_m;
        }
        else if (b_panel < window.innerHeight * 0.75) {
            height_target = window.innerHeight * 0.8;
        }
    }
    var chatbot_height = parseInt(chatbot_height);
    return { height_target, chatbot_height, chatbot };
}


// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//  第 4 部分: 顶栏自适应调整
// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
function minor_ui_adjustment() {
    var bar_btn_width = [];
    // 自动隐藏超出范围的toolbar按钮
    function auto_hide_toolbar() {
        // if chatbot hit upper page boarder, hide all
        const elem_chatbot = document.getElementById('gpt-chatbot');
        const chatbot_top = elem_chatbot.getBoundingClientRect().top;
        var tooltip = document.getElementById('tooltip');
        var tab_nav = tooltip.getElementsByClassName('tab-nav')[0];

        // 20 px 大概是一个字的高度
        if (chatbot_top < 20) {
            if (tab_nav.classList.contains('visible')) {tab_nav.classList.remove('visible');}
            if (!tab_nav.classList.contains('hidden')) {tab_nav.classList.add('hidden');}
            return;
        }
        if (tab_nav.classList.contains('hidden')) {tab_nav.classList.remove('hidden');}
        if (!tab_nav.classList.contains('visible')) {tab_nav.classList.add('visible');}
        if (tab_nav.length == 0) { return; }
        var btn_list = tab_nav.getElementsByTagName('button')
        if (btn_list.length == 0) { return; }
        // 获取页面宽度
        var page_width = document.documentElement.clientWidth;
        // 总是保留的按钮数量
        const always_preserve = 2;
        // 获取最后一个按钮的右侧位置
        var cur_right = btn_list[always_preserve - 1].getBoundingClientRect().right;
        if (bar_btn_width.length == 0) {
            // 首次运行，记录每个按钮的宽度
            for (var i = 0; i < btn_list.length; i++) {
                bar_btn_width.push(btn_list[i].getBoundingClientRect().width);
            }
        }
        // 处理每一个按钮
        for (var i = always_preserve; i < btn_list.length; i++) {
            var element = btn_list[i];
            var element_right = element.getBoundingClientRect().right;
            if (element_right != 0) { cur_right = element_right; }
            if (element.style.display === 'none') {
                if ((cur_right + bar_btn_width[i]) < (page_width * 0.37)) {
                    // 恢复显示当前按钮
                    element.style.display = 'block';
                    return;
                } else {
                    return;
                }
            } else {
                if (cur_right > (page_width * 0.38)) {
                    // 隐藏当前按钮以及右侧所有按钮
                    for (var j = i; j < btn_list.length; j++) {
                        if (btn_list[j].style.display !== 'none') {
                            btn_list[j].style.display = 'none';
                        }
                    }
                    return;
                }
            }
        }
    }

    setInterval(function () {
        auto_hide_toolbar();
    }, 200);
}

// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//  第 5 部分: 避免滑动
// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
let prevented_offset = 0;
function limit_scroll_position() {
    let scrollableDiv = document.querySelector('#gpt-chatbot > div.wrap');
    scrollableDiv.addEventListener('wheel', function (e) {
        let preventScroll = false;
        if (e.deltaX != 0) { prevented_offset = 0; return; }
        if (this.scrollHeight == this.clientHeight) { prevented_offset = 0; return; }
        if (e.deltaY < 0) { prevented_offset = 0; return; }
        if (e.deltaY > 0 && this.scrollHeight - this.clientHeight - this.scrollTop <= 1) { preventScroll = true; }

        if (preventScroll) {
            prevented_offset += e.deltaY;
            if (Math.abs(prevented_offset) > 499) {
                if (prevented_offset > 500) { prevented_offset = 500; }
                if (prevented_offset < -500) { prevented_offset = -500; }
                preventScroll = false;
            }
        } else {
            prevented_offset = 0;
        }
        if (preventScroll) {
            e.preventDefault();
            return;
        }
    }, { passive: false });
}


// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//  第 6 部分: JS初始化与会话缓存函数
// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

function get_checkbox_selected_items(elem_id) {
    display_panel_arr = [];
    document.getElementById(elem_id).querySelector('[data-testid="checkbox-group"]').querySelectorAll('label').forEach(label => {
        // Get the span text
        const spanText = label.querySelector('span').textContent;
        // Get the input value
        const checked = label.querySelector('input').checked;
        if (checked) {
            display_panel_arr.push(spanText)
        }
    });
    return display_panel_arr;
}


function gpt_academic_gradio_saveload(
    save_or_load,       // save_or_load==="save" / save_or_load==="load"
    elem_id,            // element id
    cookie_key,         // cookie key
    save_value = "",      // save value
    load_type = "str",  // type==="str" / type==="float"
    load_default = false, // load default value
    load_default_value = ""
) {
    if (save_or_load === "load") {
        let value = getCookie(cookie_key);
        if (value) {
            // console.log('加载cookie', elem_id, value)
            push_data_to_gradio_component(value, elem_id, load_type);
        }
        else {
            if (load_default) {
                // console.log('加载cookie的默认值', elem_id, load_default_value)
                push_data_to_gradio_component(load_default_value, elem_id, load_type);
            }
        }
    }
    if (save_or_load === "save") {
        setCookie(cookie_key, save_value, 365);
    }
}

function generateUUID() {
    // Generate a random number and convert it to a hexadecimal string
    function randomHexDigit() {
        return Math.floor((1 + Math.random()) * 0x10000).toString(16).slice(1);
    }

    // Construct the UUID using the randomHexDigit function
    return (
        randomHexDigit() + randomHexDigit() + '-' +
        randomHexDigit() + '-' +
        '4' + randomHexDigit().slice(0, 3) + '-' + // Version 4 UUID
        ((Math.floor(Math.random() * 4) + 8).toString(16)) + randomHexDigit().slice(0, 3) + '-' +
        randomHexDigit() + randomHexDigit() + randomHexDigit()
    );
}

function update_conversation_metadata() {
    // Create a conversation UUID and timestamp
    try {
        const conversationId = generateUUID();
        console.log('Create conversation ID:', conversationId);
        const timestamp = new Date().toISOString();
        const conversationMetaData = {
            id: conversationId,
            timestamp: timestamp
        };
        localStorage.setItem("conversation_metadata", JSON.stringify(conversationMetaData));
    } catch (e) {
        console.error('Error in updating conversation metadata:', e);
    }
}


// Helper function to generate conversation preview
function generatePreview(conversation, timestamp, maxLength = 100) {
    if (!conversation || conversation.length === 0) return "";
    // Join all messages with dash separator
    let preview = conversation.join("\n");
    const readableDate = new Date(timestamp).toLocaleString();
    preview = readableDate + "\n" + preview;
    if (preview.length <= maxLength) return preview;
    return preview.substring(0, maxLength) + "...";
}

async function save_conversation_history() {

    let chatbot = await get_data_from_gradio_component('gpt-chatbot');
    let history = await get_data_from_gradio_component('history-ng');
    let conversation = {};
    let conversation_metadata = localStorage.getItem("conversation_metadata");
    try {
        conversation_metadata = JSON.parse(conversation_metadata);
        conversation = {
            timestamp: conversation_metadata.timestamp,
            id: conversation_metadata.id,
            metadata: conversation_metadata,
            conversation: chatbot,
            history: history,
            preview: generatePreview(JSON.parse(history), conversation_metadata.timestamp)
        };
    } catch (e) {
        // console.error('Conversation metadata parse error, recreate conversation metadata');
        update_conversation_metadata();
        return;
    }

    // Get existing conversation history from local storage
    let conversation_history = [];
    try {
        const stored = localStorage.getItem('conversation_history');
        if (stored) {
            conversation_history = JSON.parse(stored);
        }
    } catch (e) {
        // console.error('Error reading conversation history from localStorage:', e);
    }

    // Find existing conversation with same ID
    const existingIndex = conversation_history.findIndex(c => c.id === conversation.id);

    if (existingIndex >= 0) {
        // Update existing conversation
        conversation_history[existingIndex] = conversation;
    } else {
        // Add new conversation
        conversation_history.push(conversation);
    }

    // Sort conversations by timestamp, newest first
    conversation_history.sort((a, b) => {
        const timeA = new Date(a.timestamp).getTime();
        const timeB = new Date(b.timestamp).getTime();
        return timeB - timeA;
    });

    const max_chat_preserve = 10;

    if (conversation_history.length >= max_chat_preserve + 1) {
        toast_push('对话时间线记录已满，正在移除最早的对话记录。您也可以点击左侧的记录点进行手动清理。', 3000);
        conversation_history = conversation_history.slice(0, max_chat_preserve);
    }

    // Save back to local storage
    try {
        localStorage.setItem('conversation_history', JSON.stringify(conversation_history));
        const LOCAL_STORAGE_UPDATED = "gptac_conversation_history_updated";
        window.dispatchEvent(
            new CustomEvent(LOCAL_STORAGE_UPDATED, {
                detail: conversation_history
            })
        );
    } catch (e) {
        console.error('Error saving conversation history to localStorage:', e);
    }
}

save_conversation_history_slow_down = do_something_but_not_too_frequently(300, save_conversation_history);

function restore_chat_from_local_storage(event) {
    let conversation = event.detail;
    push_data_to_gradio_component(conversation.conversation, "gpt-chatbot", "obj");
    push_data_to_gradio_component(conversation.history, "history-ng", "obj");
    const conversationId = conversation.id;
    const timestamp = conversation.timestamp;
    const conversationData = {
        id: conversationId,
        timestamp: timestamp
    };
    localStorage.setItem("conversation_metadata", JSON.stringify(conversationData));
}

async function clear_conversation(a, b, c) {
    await save_conversation_history();
    update_conversation_metadata();
    let stopButton = document.getElementById("elem_stop");
    stopButton.click();
    // Save back to local storage
    try {
        const EVENT_NAME = "gptac_reset_btn_clicked";
        window.dispatchEvent(
            new CustomEvent(EVENT_NAME, {
                detail: ""
            })
        );
    } catch (e) {}
    return reset_conversation(a, b);
}


function reset_conversation(a, b) {
    return [[], [], "已重置"];
}

async function duplicate_in_new_window() {
    var url = window.location.href;
    window.open(url, '_blank');
}

async function click_real_submit_btn() {
    document.getElementById("elem_submit").click();
}

async function persistent_cookie_init(web_cookie_cache, cookie) {
    return [localStorage.getItem('web_cookie_cache'), cookie];
}
