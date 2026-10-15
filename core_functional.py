# 'primary' 颜色对应 theme.py 中的 primary_hue
# 'secondary' 颜色对应 theme.py 中的 neutral_hue
# 'stop' 颜色对应 theme.py 中的 color_er
import importlib
from toolbox import clear_line_break
from toolbox import apply_gpt_academic_string_mask_langbased
from toolbox import build_gpt_academic_masked_string_langbased
from textwrap import dedent

def get_core_functions():
    return {

        "学术语料润色": {
            # [1*] 前缀字符串，会被加在你的输入之前。例如，用来描述你的要求，例如翻译、中文学术润色、润色等等。
            #      这里填一个提示词字符串就行了，这里为了区分中英文情景搞复杂了一点
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_english=
                                r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, "
                                r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. "
                                r"Firstly, you should provide the polished paragraph (in English). "
                                r"Secondly, you should list all your modification and explain the reasons to do so in markdown table.",
                            text_show_chinese=
                                r"作为一名中文学术论文写作改进助理，你的任务是改进所提供文本的拼写、语法、清晰、简洁和整体可读性，"
                                r"同时分解长句，减少重复，并提供改进建议。请先提供文本的更正版本，然后在markdown表格中列出修改的内容，并给出修改的理由:"
                        ) + "\n\n",
            # [2*] 后缀字符串，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix":   r"",
            # [3] 按钮颜色 (可选参数，默认 secondary)
            "Color":    r"secondary",
            # [4] 按钮是否可见 (可选参数，默认 True，即可见)
            "Visible": True,
            # [5] 是否在触发时清除历史 (可选参数，默认 False，即不处理之前的对话历史)
            "AutoClearHistory": False,
            # [6] 文本预处理 （可选参数，默认 None，举例：写个函数移除所有的换行符）
            "PreProcess": None,
            # [7] 模型选择 （可选参数。如不设置，则使用当前全局模型；如设置，则用指定模型覆盖全局模型。）
            # "ModelOverride": "gpt-6-astra", # 主要用途：强制点击此基础功能按钮时，使用指定的模型。
        },


        "英文学术润色": {
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_english=
                                r"You are a professional English language expert, serving as an English academic paper writing improvement assistant. "
                                r"Your task is to enhance the spelling, grammar, clarity, conciseness, and overall readability of the provided text. "
                                r"This includes breaking down long sentences, reducing repetition, and offering suggestions for improvement. "
                                r"If the input and output contain text in TeX format, please ensure that the TeX format is preserved for easy copying and reading. "
                                r"Please first provide the corrected version of the text, and then list the modifications in a Markdown table, along with the reasons for the changes.",
                            text_show_chinese=
                                r"你是一名专业的英语语言专家，担任英文学术论文写作改进助理。你的任务是改进所提供文本的拼写、语法、清晰度、简洁性和整体可读性，"
                                r"包括分解长句、减少重复并提供改进建议。如果输入和输出包含TeX格式的文本，请确保保留TeX格式以便于复制和阅读。"
                                r"请先提供文本的更正版本，然后在Markdown表格中列出修改的内容，并给出修改的理由："
                        ) + "\n\n",
            "Suffix":   r"",
        },


        "中文译英文": {
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_english=
                                r"You are a highly professional linguistic translation assistant. Please translate my Chinese text into English, and translate all non-Chinese text into Chinese. "
                                r"All the content I send to you requires translation, and you only need to provide the translated result. "
                                r"The translation should conform to the conventions of academic writing, not only accurately conveying complex concepts and specialized terminology, "
                                r"but also maintaining the professionalism and rigor characteristic of academic English. "
                                r"In particular, the original meaning must remain unchanged, while enhancing its academic quality.",
                            text_show_chinese=
                                r"你是一名高度专业的语言翻译助理。请将我的中文文本翻译成英文，并将所有非中文文本翻译成中文。"
                                r"我发送给你的所有内容都需要翻译，你只需提供翻译结果。"
                                r"翻译应符合学术写作规范，不仅要准确传达复杂的概念和专业术语，还要保持学术英语的专业性和严谨性。"
                                r"特别是必须保持原意不变，同时提升其学术质量："
                        ) + "\n\n",
            "Suffix":   r"",
        },


        "英文译中文": {
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_english=
                                r"You are a highly professional linguistic translation assistant. Kindly translate my English content into Chinese, encompassing individual words, sentences, or even extended passages, while also rendering all non-Chinese elements into Chinese. "
                                r"All textual material provided to you necessitates translation, with the resultant output adhering to idiomatic conventions of the Chinese language. "
                                r"In the case of a solitary word, please furnish a comprehensive enumeration including its phonetic transcription and Chinese signification, "
                                r"supplemented by a selection of pertinent common English phrases and illustrative English sentences associated with the word, accompanied by their respective Chinese translations.",
                            text_show_chinese=
                                r"你是一名高度专业的语言翻译助理。请将我的英文内容翻译成中文，无论是单个单词、句子还是较长的段落，同时也将所有非中文内容翻译成中文。"
                                r"提供给你的所有文本材料都需要翻译，且翻译结果应符合地道中文的表达习惯。"
                                r"如果是单个单词，请提供全面的解释，包括其音标和中文释义，并补充与该单词相关的常见英文短语和英文例句及其对应的中文翻译："
                        ) + "\n\n",
            "Suffix":   r"",
        },


        "查英语汉语": {
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_english=dedent(r"""
                                **Role Definition**

                                You are a professional bilingual language-learning assistant with expertise in the lexicology, etymology, cultural linguistics, and academic writing of both English and Chinese. Your task is to provide users with comprehensive, detailed, and accurate word/phrase/sentence lookup services.

                                **Workflow**

                                Whenever a user inputs any English or Chinese word, phrase, or sentence, please respond strictly in accordance with the following three parts:

                                **Part One: Pronunciation and Translation**

                                Pronunciation Annotation

                                - If the input is English: provide the British phonetic transcription /UK/ and the American phonetic transcription /US/
                                - If the input is Chinese: provide Hanyu Pinyin (with tone marks) or Zhuyin (phonetic symbols)
                                - If it is a phrase or sentence: provide pronunciation annotation for the key words or for the whole

                                Translation Comparison

                                - English → provide an accurate and idiomatic Chinese translation (if there are multiple senses, list them one by one)
                                - Chinese → provide an accurate and idiomatic English translation (if there are multiple senses, list them one by one)
                                - Annotate the part of speech (noun/verb/adjective, etc.)

                                **Part Two: Knowledge Retrieval and Detailed Introduction**

                                Please conduct an in-depth search and analysis of the input content, including but not limited to:

                                Historical Origin and Development (Etymology)

                                - The origin of the word/phrase (e.g., Latin, Greek, Old English, Classical Chinese, etc.)
                                - Word-formation analysis (roots, affixes, evolution of character forms, etc.)
                                - The process of historical semantic change and its key milestones

                                Cultural Background and Connotation

                                - Related cultural allusions, historical events, and literary sources
                                - Symbolic meaning or emotional coloring within the culture of the target language
                                - A comparison of Chinese and Western cultural differences (where culture-specific concepts are involved)

                                Semantic Extension

                                - Common collocations, idiomatic expressions, and fixed usages
                                - Discrimination of synonyms/antonyms
                                - Idioms, proverbs, and slang (where applicable)

                                **Part Three: Summary of Usage Notes**

                                Scope of Academic Use

                                - The register to which the word/phrase/sentence is suited (formal/informal/colloquial/written/academic)
                                - Appropriate usage in academic writing, with typical example sentences

                                Usage Precautions

                                - Points of confusion, common errors, and prohibited usages
                                - Reminders regarding tone and emotional coloring (commendatory/derogatory/neutral)
                                - Usage suggestions and alternative expressions

                                **Output Requirements**

                                - Information should be detailed, specific, and accurate, avoiding vague generalities
                                - Use a clear hierarchical structure (headings, lists, bullet points)
                                - Provide example sentences where appropriate to aid comprehension
                                - If the user's input has multiple meanings, cover them comprehensively
                            """).strip(),
                            text_show_chinese=dedent(r"""
                                **角色定义**

                                你是一名专业的双语语言学习助手，精通中英文的词汇学、词源学、文化语言学及学术写作。你的任务是为用户提供全面、详尽、准确的单词/短语/句子查询服务。

                                **工作流程**

                                每当用户输入任何英文或中文单词、短语或句子时，请严格按照以下三个部分进行回复：

                                **第一部分：发音与翻译**

                                发音标注

                                - 若输入为英文：提供英式音标 /UK/ 和美式音标 /US/
                                - 若输入为中文：提供汉语拼音（带声调）或注音符号
                                - 若为短语或句子：提供重点词汇或整体的发音标注

                                翻译对照

                                - 英文 → 提供准确地道的中文翻译（如有多个义项请逐一列出）
                                - 中文 → 提供准确地道的英文翻译（如有多个义项请逐一列出）
                                - 标注词性（名词/动词/形容词等）

                                **第二部分：知识检索与详细介绍**

                                请对输入内容进行深入检索与剖析，包括但不限于：

                                历史渊源与发展（词源）

                                - 词汇/短语的来源（如拉丁语、希腊语、古英语、文言文等）
                                - 构词法分析（词根、词缀、字形演变等）
                                - 历史词义流变过程及关键节点

                                文化背景与内涵

                                - 相关的文化典故、历史事件与文学出处
                                - 在目标语言文化中的象征意义或感情色彩
                                - 中西文化差异对比（如涉及特定文化概念）

                                语义拓展

                                - 常见搭配、惯用表达与固定用法
                                - 近义词/反义词辨析
                                - 习语、谚语与俚语（如适用）

                                **第三部分：用法总结与注意事项**

                                学术使用范围

                                - 该词/短语/句子适用的语域（正式/非正式/口语/书面语/学术）
                                - 在学术写作中的恰当用法及典型例句

                                使用注意事项

                                - 易混淆点、常见错误与禁忌用法
                                - 语气与感情色彩提示（褒义/贬义/中性）
                                - 使用建议与替代性表达

                                **输出要求**

                                - 信息需详实、具体、准确，避免笼统泛谈
                                - 使用清晰的层级结构（标题、列表、要点）
                                - 在适当位置提供例句以辅助理解
                                - 若用户输入有多种含义，请全面涵盖
                            """).strip()
                        ) + "\n\n",
            "Suffix":   r"",
        },


        "英译中": {
            "Prefix":   r"翻译成地道的中文：" + "\n\n",
            "Suffix":   r"",
            "Visible":  False,
        },


        "找图片": {
            "Prefix":   r"我需要你找一张网络图片。使用Unsplash API(https://source.unsplash.com/960x640/?<英语关键词>)获取图片URL，"
                        r"然后请使用Markdown格式封装，并且不要有反斜线，不要用代码块。现在，请按以下描述给我发送图片：" + "\n\n",
            "Suffix":   r"",
            "Visible":  False,
        },


        "中文学术润色": {
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_english=
                                r"You are a professional expert in the Chinese language, serving as an assistant for improving the writing of academic papers in Chinese. "
                                r"Your task is to improve the spelling, grammar, clarity, conciseness, and overall readability of the provided text, "
                                r"while breaking down long sentences, reducing repetition, and offering suggestions for improvement. "
                                r"If the input and output contain text in TeX format, please be sure to preserve the display of the TeX source file format, so as to facilitate copying and reading. "
                                r"Please first provide a corrected version of the text, and then list the modifications in a markdown table, giving the reasons for each change.",
                            text_show_chinese=
                                r"你是一名专业的中文语言专家，担任中文学术论文写作改进助理。你的任务是改进所提供文本的拼写、语法、清晰度、简洁性和整体可读性，"
                                r"同时分解长句，减少重复，并提供改进建议。如果输入和输出包含TeX格式的文本，请务必保留TeX源文件格式的显示，以便于复制和阅读。"
                                r"请先提供文本的更正版本，然后在markdown表格中列出修改的内容，并给出每处修改的理由："
                        ) + "\n\n",
            "Suffix":   r"",
        },


        "参考文献转Bib": {
            "Prefix":   r"Here are some bibliography items, please transform them into bibtex style."
                        r"Note that, reference styles maybe more than one kind, you should transform each item correctly."
                        r"Items need to be transformed:" + "\n\n",
            "Visible":  False,
            "Suffix":   r"",
        }
    }


_CORE_FUNCTIONS_CACHE = None

def handle_core_functionality(additional_fn, inputs, history, chatbot):
    global _CORE_FUNCTIONS_CACHE
    from toolbox import get_conf
    if get_conf("PLUGIN_HOT_RELOAD"):
        import core_functional
        importlib.reload(core_functional)    # 热更新prompt
        core_functional_dict = core_functional.get_core_functions()
    else:
        if _CORE_FUNCTIONS_CACHE is None:
            _CORE_FUNCTIONS_CACHE = get_core_functions()
        core_functional_dict = _CORE_FUNCTIONS_CACHE
    addition = chatbot._cookies['customize_fn_overwrite']
    if additional_fn in addition:
        # 自定义功能
        inputs = addition[additional_fn]["Prefix"] + inputs + addition[additional_fn]["Suffix"]
        return inputs, history
    else:
        # 预制功能
        if "PreProcess" in core_functional_dict[additional_fn]:
            if core_functional_dict[additional_fn]["PreProcess"] is not None:
                inputs = core_functional_dict[additional_fn]["PreProcess"](inputs)  # 获取预处理函数（如果有的话）
        # 为字符串加上上面定义的前缀和后缀。
        inputs = apply_gpt_academic_string_mask_langbased(
            string = core_functional_dict[additional_fn]["Prefix"] + inputs + core_functional_dict[additional_fn]["Suffix"],
            lang_reference = inputs,
        )
        if core_functional_dict[additional_fn].get("AutoClearHistory", False):
            history = []
        return inputs, history

if __name__ == "__main__":
    t = get_core_functions()["英文学术润色"]
    print(t["Prefix"] + t["Suffix"])
