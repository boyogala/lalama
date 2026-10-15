"""
    以下所有配置也都支持利用环境变量覆写，环境变量配置格式见docker-compose.yml。
    读取优先级：环境变量 > config_private.py > config.py
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    All the following configurations also support using environment variables to override,
    and the environment variable configuration format can be seen in docker-compose.yml.
    Configuration reading priority: environment variable > config_private.py > config.py
"""

# [step 1-1]>> ( 接入OpenAI模型家族: gpt-6-astra, gpt-6.1-sol, gpt-6-luna, gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna )
API_KEY = "在此处填写APIKEY"    # 可同时填写多个API-KEY，用英文逗号分割

# [step 1-2]>> ( 接入通义家族 & 大模型服务平台百炼 ) 接入通义千问在线大模型，api-key获取地址 https://dashscope.console.aliyun.com/
DASHSCOPE_API_KEY = "" # 阿里灵积云API_KEY（用于接入qwen-max，dashscope-qwen3-14b等）

# [step 1-3]>> ( 接入 DeepSeek 模型: deepseek-flash, deepseek-v4-pro ) 深度求索(DeepSeek) API KEY，默认请求地址为"https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = ""

# [step 2]>> 改为True应用代理。如果使用本地或无地域限制的大模型时，此处不修改；如果直接在海外服务器部署，此处不修改
USE_PROXY = False
if USE_PROXY:
    proxies = {
        # "http":  "http://127.0.0.1:10808",
        # "https": "http://127.0.0.1:10808",
    }
else:
    proxies = None

# [step 3]>> 模型选择是 (注意: LLM_MODEL是默认选中的模型, 它*必须*被包含在AVAIL_LLM_MODELS列表中 )
LLM_MODEL = "deepseek-flash" # 可选 ↓↓↓
AVAIL_LLM_MODELS = [
    "deepseek-flash", "deepseek-v4-pro",
    "grok-4.7", "grok-4.3", "grok-imagine-image-2.0", "grok-build-0.1", "grok-4.20-0309-reasoning",
    "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3.1-pro-preview", "gemini-pro-latest", "gemini-flash-latest", "gemini-4-argon",
    "gpt-6-astra", "gpt-6.1-sol", "gpt-6-luna", "gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna",
    "qwen-max", "dashscope-qwen3-14b", "dashscope-qwen3-235b-a22b", "dashscope-qwen3-32b",
    "glm-4", "glm-4v", "glm-3-turbo", "chatglm3", "chatglm4",
]

EMBEDDING_MODEL = "text-embedding-3-small"

# --------------- 以下配置可以优化体验 ---------------

# 重新URL重新定向，实现更换API_URL的作用（常规情况下不要修改）
API_URL_REDIRECT = {}

# 色彩主题, 可选 ["Default", "Chuanhu-Small-and-Beautiful", "High-Contrast"]
THEME = "Default"
AVAIL_THEMES = ["Default", "Chuanhu-Small-and-Beautiful", "High-Contrast", "Gstaff/Xkcd", "NoCrypt/Miku"]

FONT = "Theme-Default-Font"
AVAIL_FONTS = [
    "默认值(Theme-Default-Font)",
    "宋体(SimSun)",
    "黑体(SimHei)",
    "楷体(KaiTi)",
    "仿宋(FangSong)",
    "华文细黑(STHeiti Light)",
    "华文楷体(STKaiti)",
    "华文仿宋(STFangsong)",
    "华文宋体(STSong)",
    "华文中宋(STZhongsong)",
    "华文新魏(STXinwei)",
    "华文隶书(STLiti)",
    "思源宋体(Source Han Serif CN VF@https://chinese-fonts-cdn.deno.dev/packages/syst/dist/SourceHanSerifCN/result.css)",
    "月星楷(Moon Stars Kai HW@https://chinese-fonts-cdn.deno.dev/packages/moon-stars-kai/dist/MoonStarsKaiHW-Regular/result.css)",
    "珠圆体(MaokenZhuyuanTi@https://chinese-fonts-cdn.deno.dev/packages/mkzyt/dist/猫啃珠圆体/result.css)",
    "平方萌萌哒(PING FANG MENG MNEG DA@https://chinese-fonts-cdn.deno.dev/packages/pfmmd/dist/平方萌萌哒/result.css)",
    "Helvetica",
    "ui-sans-serif",
    "sans-serif",
    "system-ui"
]

# 默认的系统提示词（system prompt）
INIT_SYS_PROMPT = "Serve me as a writing and programming assistant."

# 对话窗的高度 （仅在LAYOUT="TOP-DOWN"时生效）
CHATBOT_HEIGHT = 1115

# 代码高亮
CODE_HIGHLIGHT = True

# 窗口布局
LAYOUT = "LEFT-RIGHT"   # "LEFT-RIGHT"（左右布局） # "TOP-DOWN"（上下布局）

# 暗色模式 / 亮色模式
DARK_MODE = True

# 发送请求到LLM后，等待多久判定为超时
TIMEOUT_SECONDS = 30

# 网页的端口, -1代表随机端口
WEB_PORT = -1

# 是否自动打开浏览器页面
AUTO_OPEN_BROWSER = True

# 如果LLM不响应（网络卡顿、代理失败、KEY失效），重试的次数限制
MAX_RETRY = 2

# 选择本地模型变体（只有当AVAIL_LLM_MODELS包含了对应本地模型时，才会起作用）
QWEN_LOCAL_MODEL_SELECTION = "Qwen/Qwen-1_8B-Chat-Int8"
CHATGLM_LOCAL_MODEL_PATH = "THUDM/glm-4-9b-chat"
CHATGLM_PTUNING_CHECKPOINT = ""

# 本地LLM模型如ChatGLM的执行方式 CPU/GPU
LOCAL_MODEL_DEVICE = "cpu" # 可选 "cuda"
LOCAL_MODEL_QUANT = "FP16" # 默认 "FP16" "INT4" 启用量化INT4版本 "INT8" 启用量化INT8版本

# 设置gradio的并行线程数（不需要修改）
CONCURRENT_COUNT = 100

# 是否在提交时自动清空输入框
AUTO_CLEAR_TXT = False

# 加一个live2d装饰
ADD_WAIFU = False

# 设置用户名和密码（不需要修改）
AUTHENTICATION = []

# 如果需要在二级路径下运行（常规情况下，不要修改!!）
CUSTOM_PATH = "/"

# HTTPS 秘钥和证书（不需要修改）
SSL_KEYFILE = ""
SSL_CERTFILE = ""

# 极少数情况下，openai的官方KEY需要伴随组织编码（格式如org-xxxxxxxxxxxxxxxxxxxxxxxx）使用
API_ORG = ""

# Slack Claude
SLACK_CLAUDE_BOT_ID = ''
SLACK_CLAUDE_USER_TOKEN = ''

# AZURE
AZURE_ENDPOINT = "https://你亲手写的api名称.openai.azure.com/"
AZURE_API_KEY = "填入azure openai api的密钥"
AZURE_ENGINE = "填入你亲手写的部署名"
AZURE_CFG_ARRAY = {}

# 实时语音识别开关
ENABLE_AUDIO = False

# GPT-SOVITS / Edge-TTS 文本转语音服务的运行地址
TTS_TYPE = "EDGE_TTS" # EDGE_TTS / LOCAL_SOVITS_API / DISABLE
GPT_SOVITS_URL = ""
EDGE_TTS_VOICE = "zh-CN-XiaoxiaoNeural"

# 接入智谱大模型
ZHIPUAI_API_KEY = ""
ZHIPUAI_MODEL = ""

# Claude API KEY
ANTHROPIC_API_KEY = ""

# Grok API KEY
GROK_API_KEY = ""

# 自定义API KEY格式
CUSTOM_API_KEY_PATTERN = ""

# Google Gemini API-Key
GEMINI_API_KEY = ""

# HUGGINGFACE的TOKEN，下载LLAMA时起作用
HUGGINGFACE_ACCESS_TOKEN = ""

# 临时的上传文件夹位置，请尽量不要修改
PATH_PRIVATE_UPLOAD = "private_upload"

# 日志文件夹的位置，请尽量不要修改
PATH_LOGGING = "gpt_log"

# 允许使用代理的场合
WHEN_TO_USE_PROXY = ["Connect_OpenAI", "Download_LLM", "Download_Gradio_Theme", "Warmup_Modules"]

# 启用热加载
PLUGIN_HOT_RELOAD = False

# 自定义按钮的最大数量限制
NUM_CUSTOM_BASIC_BTN = 4

# 是否自动裁剪上下文长度（是否启动，默认不启动）
AUTO_CONTEXT_CLIP_ENABLE = False
AUTO_CONTEXT_CLIP_TRIGGER_TOKEN_LEN = 30*1000
AUTO_CONTEXT_MAX_ROUND = 64
AUTO_CONTEXT_MAX_CLIP_RATIO = [0.80, 0.60, 0.45, 0.25, 0.20, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]


"""
--------------- 配置关联关系说明 ---------------

在线大模型配置关联关系示意图
│
├── "gpt-6-astra" 等openai模型
│   ├── API_KEY
│   ├── CUSTOM_API_KEY_PATTERN（不常用）
│   ├── API_ORG（不常用）
│   └── API_URL_REDIRECT（不常用）
│
├── "azure-gpt-3.5" 等azure模型（单个azure模型，不需要动态切换）
│   ├── API_KEY
│   ├── AZURE_ENDPOINT
│   ├── AZURE_API_KEY
│   ├── AZURE_ENGINE
│   └── API_URL_REDIRECT
│
├── "azure-gpt-3.5" 等azure模型（多个azure模型，需要动态切换，高优先级）
│   └── AZURE_CFG_ARRAY
│
├── "claude-3-opus-20240229" 等claude模型
│   └── ANTHROPIC_API_KEY
│
├── "stack-claude"
│   ├── SLACK_CLAUDE_BOT_ID
│   └── SLACK_CLAUDE_USER_TOKEN
│
├── "glm-4", "glm-3-turbo", "zhipuai" 智谱AI大模型
│   └── ZHIPUAI_API_KEY
│
├── "qwen-turbo" 等通义千问大模型
│   └──  DASHSCOPE_API_KEY
│
├── "deepseek-flash", "deepseek-v4-pro" 等DeepSeek大模型
│   └──  DEEPSEEK_API_KEY
│
├── "grok-4.7" 等xAI大模型
│   └──  GROK_API_KEY
│
├── "Gemini"
│   └──  GEMINI_API_KEY
│
└── "one-api-...(max_token=...)" 用一种更方便的方式接入one-api多模型管理界面
    ├── AVAIL_LLM_MODELS
    ├── API_KEY
    └── API_URL_REDIRECT


本地大模型示意图
│
├── "chatglm4"
├── "chatglm3"
├── "chatglm"
├── "chatglm_onnx"
├── "chatglmft"
├── "qwen-local"
└── "llama2"


用户图形界面布局依赖关系示意图
│
├── CHATBOT_HEIGHT 对话窗的高度
├── CODE_HIGHLIGHT 代码高亮
├── LAYOUT 窗口布局
├── DARK_MODE 暗色模式 / 亮色模式
├── DEFAULT_FN_GROUPS 插件分类默认选项
├── THEME 色彩主题
├── AUTO_CLEAR_TXT 是否在提交时自动清空输入框
├── ADD_WAIFU 加一个live2d装饰
└── ALLOW_RESET_CONFIG 是否允许通过自然语言描述修改本页的配置，该功能具有一定的危险性


插件在线服务配置依赖关系示意图
│
├── 互联网检索
│   └── SEARXNG_URLS
│
├── 语音功能
│   ├── ENABLE_AUDIO
│   ├── ALIYUN_TOKEN
│   ├── ALIYUN_APPKEY
│   ├── ALIYUN_ACCESSKEY
│   └── ALIYUN_SECRET
│
└── PDF文档精准解析
    ├── GROBID_URLS
    ├── MATHPIX_APPID
    └── MATHPIX_APPKEY


"""
