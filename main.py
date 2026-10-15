import os; os.environ['no_proxy'] = '*' # 避免代理网络产生意外污染

help_menu_description = \
"""Github源代码开源和更新[LaLaMa, Large Language Model for Academic](https://github.com/boyogala/lalama)."""

from loguru import logger
def enable_log(PATH_LOGGING):
    from shared_utils.logging import setup_logging
    setup_logging(PATH_LOGGING)

def main():
    import gradio as gr
    if gr.__version__ not in ['3.32.15']:
        raise ModuleNotFoundError("使用项目内置Gradio获取最优体验! 请运行 `pip install -r requirements.txt` 指令安装内置Gradio及其他依赖, 详情信息见requirements.txt.")

    # 一些基础工具
    from toolbox import format_io, find_free_port, get_conf, ArgsGeneralWrapper, DummyWith

    # 对话、日志记录
    enable_log(get_conf("PATH_LOGGING"))

    # 对话句柄
    from request_llms.bridge_all import predict

    # 读取配置
    proxies, WEB_PORT, LLM_MODEL, CONCURRENT_COUNT, AUTHENTICATION = get_conf('proxies', 'WEB_PORT', 'LLM_MODEL', 'CONCURRENT_COUNT', 'AUTHENTICATION')
    CHATBOT_HEIGHT, LAYOUT, AVAIL_LLM_MODELS, AUTO_CLEAR_TXT = get_conf('CHATBOT_HEIGHT', 'LAYOUT', 'AVAIL_LLM_MODELS', 'AUTO_CLEAR_TXT')
    ENABLE_AUDIO, AUTO_CLEAR_TXT, AVAIL_FONTS, AVAIL_THEMES, THEME, ADD_WAIFU = get_conf('ENABLE_AUDIO', 'AUTO_CLEAR_TXT', 'AVAIL_FONTS', 'AVAIL_THEMES', 'THEME', 'ADD_WAIFU')
    NUM_CUSTOM_BASIC_BTN, SSL_KEYFILE, SSL_CERTFILE = get_conf('NUM_CUSTOM_BASIC_BTN', 'SSL_KEYFILE', 'SSL_CERTFILE')
    DARK_MODE, INIT_SYS_PROMPT, ADD_WAIFU, TTS_TYPE = get_conf('DARK_MODE', 'INIT_SYS_PROMPT', 'ADD_WAIFU', 'TTS_TYPE')
    if LLM_MODEL not in AVAIL_LLM_MODELS: AVAIL_LLM_MODELS += [LLM_MODEL]

    # 如果WEB_PORT是-1, 则随机选取WEB端口
    PORT = find_free_port() if WEB_PORT <= 0 else WEB_PORT
    from themes.theme import adjust_theme, advanced_css, js_code_clear, js_code_show_or_hide
    from themes.theme import js_code_for_toggle_darkmode
    from themes.theme import load_dynamic_theme, assign_user_uuid

    # 一些普通功能模块
    from core_functional import get_core_functions
    functional = get_core_functions()

    # 处理markdown文本格式的转变
    gr.Chatbot.postprocess = format_io

    # 做一些外观色彩上的调整
    set_theme = adjust_theme()

    # 预热模块
    from check_proxy import warm_up_modules

    # 切换布局
    gr_L1 = lambda: gr.Row().style()
    gr_L2 = lambda scale, elem_id: gr.Column(scale=scale, elem_id=elem_id, min_width=400)
    if LAYOUT == "TOP-DOWN":
        gr_L1 = lambda: DummyWith()
        gr_L2 = lambda scale, elem_id: gr.Row()
        CHATBOT_HEIGHT /= 2

    cancel_handles = []
    customize_btns = {}
    predefined_btns = {}
    from shared_utils.cookie_manager import make_cookie_cache, make_history_cache
    with gr.Blocks(title="LaLaMa", theme=set_theme, analytics_enabled=False, css=advanced_css) as app_block:
        gr.HTML("<div style=\"height: 28px;\"></div>")
        secret_css = gr.Textbox(visible=False, elem_id="secret_css")
        plugin_advanced_arg = gr.Textbox(show_label=True, label="高级参数输入区", visible=False, elem_id="advance_arg_input_legacy").style(container=False)

        cookies, web_cookie_cache = make_cookie_cache() # 定义 后端state（cookies）、前端（web_cookie_cache）两兄弟
        with gr_L1():
            with gr_L2(scale=2, elem_id="gpt-chat"):
                chatbot = gr.Chatbot(label=f"当前模型：{LLM_MODEL}", elem_id="gpt-chatbot")
                if LAYOUT == "TOP-DOWN":  chatbot.style(height=CHATBOT_HEIGHT)
                history, _, _ = make_history_cache() # 定义 后端state（history）、前端（history_cache）、后端setter（history_cache_update）三兄弟
            with gr_L2(scale=1, elem_id="gpt-panel"):
                with gr.Accordion("输入区", open=True, elem_id="input-panel") as area_input_primary:
                    with gr.Row():
                        txt = gr.Textbox(show_label=False, placeholder="Input question here.", elem_id='user_input_main').style(container=False)
                    with gr.Row():
                        submit_btn = gr.Button("提交", elem_id="elem_submit", variant="primary")
                    with gr.Row():
                        resetBtn = gr.Button("重置", elem_id="elem_reset", variant="secondary"); resetBtn.style(size="sm")
                        stopBtn = gr.Button("停止", elem_id="elem_stop", variant="secondary"); stopBtn.style(size="sm")
                        clearBtn = gr.Button("清除", elem_id="elem_clear", variant="secondary", visible=False); clearBtn.style(size="sm")
                    with gr.Row():
                        status = gr.Markdown(f"Tip: 按Enter提交, 按Shift+Enter换行。", elem_id="state-panel")

                with gr.Accordion("基础功能区", open=True, elem_id="basic-panel") as area_basic_fn:
                    with gr.Row():
                        for k in range(NUM_CUSTOM_BASIC_BTN):
                            customize_btn = gr.Button("自定义按钮" + str(k+1), visible=False, variant="secondary", info_str=f'基础功能区: 自定义按钮')
                            customize_btn.style(size="sm")
                            customize_btns.update({"自定义按钮" + str(k+1): customize_btn})
                        for k in functional:
                            if ("Visible" in functional[k]) and (not functional[k]["Visible"]): continue
                            variant = functional[k]["Color"] if "Color" in functional[k] else "secondary"
                            functional[k]["Button"] = gr.Button(k, variant=variant, info_str=f'基础功能区: {k}')
                            functional[k]["Button"].style(size="sm")
                            predefined_btns.update({k: functional[k]["Button"]})

        # 左上角工具栏定义
        from themes.gui_toolbar import define_gui_toolbar
        checkboxes, max_length_sl, theme_dropdown, system_prompt, md_dropdown, top_p, temperature = \
            define_gui_toolbar(AVAIL_LLM_MODELS, LLM_MODEL, INIT_SYS_PROMPT, THEME, AVAIL_THEMES, AVAIL_FONTS, ADD_WAIFU, help_menu_description, js_code_for_toggle_darkmode)

        # 浮动菜单定义（隐藏状态，保留以维护参数链路及基础功能区按钮缓存初始化）
        from themes.gui_floating_menu import define_gui_floating_menu
        area_input_secondary, txt2, area_customize, _, resetBtn2, clearBtn2, stopBtn2 = \
            define_gui_floating_menu(customize_btns, functional, predefined_btns, cookies, web_cookie_cache)

        # 浮动时间线定义
        gr.Spark()

        # 功能区显示开关与功能区的互动
        checkboxes.select(None, [checkboxes], None, _js=js_code_show_or_hide)

        # 整理反复出现的控件句柄组合
        input_combo = [cookies, max_length_sl, md_dropdown, txt, txt2, top_p, temperature, chatbot, history, system_prompt, plugin_advanced_arg]
        output_combo = [cookies, chatbot, history, status]
        predict_args = dict(fn=ArgsGeneralWrapper(predict), inputs=[*input_combo, gr.State(True)], outputs=output_combo)

        # 提交按钮、重置按钮
        cancel_handles.append(submit_btn.click(**predict_args))
        cancel_handles.append(txt.submit(**predict_args))
        resetBtn.click(None, None, [chatbot, history, status], _js="""clear_conversation""")   # 先在前端快速清除chatbot&status
        resetBtn2.click(None, None, [chatbot, history, status], _js="""clear_conversation""")  # 先在前端快速清除chatbot&status
        clearBtn.click(None, None, [txt, txt2], _js=js_code_clear)
        clearBtn2.click(None, None, [txt, txt2], _js=js_code_clear)
        if AUTO_CLEAR_TXT:
            submit_btn.click(None, None, [txt, txt2], _js=js_code_clear)
            txt.submit(None, None, [txt, txt2], _js=js_code_clear)

        # 基础功能区的回调函数注册
        for k in functional:
            if ("Visible" in functional[k]) and (not functional[k]["Visible"]): continue
            click_handle = functional[k]["Button"].click(fn=ArgsGeneralWrapper(predict), inputs=[*input_combo, gr.State(True), gr.State(k)], outputs=output_combo)
            cancel_handles.append(click_handle)
        for btn in customize_btns.values():
            click_handle = btn.click(fn=ArgsGeneralWrapper(predict), inputs=[*input_combo, gr.State(True), gr.State(btn.value)], outputs=output_combo)
            cancel_handles.append(click_handle)

        # 模型切换时的回调
        def on_md_dropdown_changed(k):
            return {chatbot: gr.update(label="当前模型："+k)}
        md_dropdown.select(on_md_dropdown_changed, [md_dropdown], [chatbot])

        # 主题修改
        def on_theme_dropdown_changed(theme, secret_css):
            adjust_theme, css_part1, _, adjust_dynamic_theme = load_dynamic_theme(theme)
            if adjust_dynamic_theme:
                css_part2 = adjust_dynamic_theme._get_theme_css()
            else:
                css_part2 = adjust_theme()._get_theme_css()
            return css_part2 + css_part1
        theme_handle = theme_dropdown.select(on_theme_dropdown_changed, [theme_dropdown, secret_css], [secret_css])
        theme_handle.then(None, [theme_dropdown, secret_css], None, _js="""change_theme""")

        # 终止按钮的回调函数注册
        stopBtn.click(fn=None, inputs=None, outputs=None, cancels=cancel_handles)
        stopBtn2.click(fn=None, inputs=None, outputs=None, cancels=cancel_handles)

        # 生成当前浏览器窗口的uuid（刷新失效）
        app_block.load(assign_user_uuid, inputs=[cookies], outputs=[cookies])

        # 初始化（前端）
        from shared_utils.cookie_manager import load_web_cookie_cache__fn_builder
        load_web_cookie_cache = load_web_cookie_cache__fn_builder(customize_btns, cookies, predefined_btns)
        app_block.load(load_web_cookie_cache, inputs = [web_cookie_cache, cookies],
            outputs = [web_cookie_cache, cookies, *customize_btns.values(), *predefined_btns.values()], _js="""persistent_cookie_init""")
        app_block.load(None, inputs=[], outputs=None, _js=f"""()=>GptAcademicJavaScriptInit("{DARK_MODE}","{INIT_SYS_PROMPT}","{ADD_WAIFU}","{LAYOUT}","{TTS_TYPE}")""")    # 配置暗色主题或亮色主题

    # 后台运行浏览器自动打开与分词器预热
    def run_delayed_tasks():
        import threading, webbrowser, time
        logger.info(f"如果浏览器没有自动打开，请复制并转到以下URL：")
        if DARK_MODE:   logger.info(f"\t「暗色主题已启用（支持动态切换主题）」: http://127.0.0.1:{PORT}")
        else:           logger.info(f"\t「亮色主题已启用（支持动态切换主题）」: http://127.0.0.1:{PORT}")

        def open_browser(): time.sleep(2); webbrowser.open_new_tab(f"http://127.0.0.1:{PORT}")
        def warm_up_mods(): time.sleep(4); warm_up_modules()

        threading.Thread(target=warm_up_mods, name="warm-up", daemon=True).start() # 预热tiktoken模块
        if get_conf('AUTO_OPEN_BROWSER'):
            threading.Thread(target=open_browser, name="open-browser", daemon=True).start() # 打开浏览器页面

    run_delayed_tasks()

    # 最后，正式开始服务
    from shared_utils.fastapi_server import start_app
    start_app(app_block, CONCURRENT_COUNT, AUTHENTICATION, PORT, SSL_KEYFILE, SSL_CERTFILE)


if __name__ == "__main__":
    main()
