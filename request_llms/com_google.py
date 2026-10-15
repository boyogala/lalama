import json
import os
import re
import requests
from typing import List, Dict, Tuple
from toolbox import get_conf, update_ui, encode_image, get_pictures_list

proxies, TIMEOUT_SECONDS = get_conf("proxies", "TIMEOUT_SECONDS")


def input_encode_handler(inputs, llm_kwargs):
    if llm_kwargs["most_recent_uploaded"].get("path"):
        image_paths = get_pictures_list(llm_kwargs["most_recent_uploaded"]["path"])
    md_encode = []
    for md_path in image_paths:
        type_ = os.path.splitext(md_path)[1].replace(".", "")
        type_ = "jpeg" if type_ == "jpg" else type_
        md_encode.append({"data": encode_image(md_path), "type": type_})
    return inputs, md_encode


def reverse_base64_from_input(inputs):
    pattern = re.compile(r'<br/><br/><div align="center"><img[^<>]+base64="([^"]+)"></div>')
    base64_strings = pattern.findall(inputs)
    return base64_strings

def contain_base64(inputs):
    base64_strings = reverse_base64_from_input(inputs)
    return len(base64_strings) > 0

class GoogleChatInit:
    def __init__(self, llm_kwargs):
        from .bridge_all import model_info
        endpoint = model_info[llm_kwargs['llm_model']]['endpoint']
        self.url_gemini = endpoint + "/%m:streamGenerateContent?key=%k"

    def generate_chat(self, inputs, llm_kwargs, history, system_prompt, image_base64_array:list=[], has_multimodal_capacity:bool=False):
        headers, payload = self.generate_message_payload(
            inputs, llm_kwargs, history, system_prompt, image_base64_array, has_multimodal_capacity
        )
        response = requests.post(
            url=self.url_gemini,
            headers=headers,
            data=json.dumps(payload),
            stream=True,
            proxies=proxies,
            timeout=TIMEOUT_SECONDS,
        )
        return response.iter_lines()

    def __conversation_user(self, user_input, llm_kwargs, enable_multimodal_capacity):
        what_i_have_asked = {"role": "user", "parts": []}
        from .bridge_all import model_info

        if enable_multimodal_capacity:
            input_, encode_img = input_encode_handler(user_input, llm_kwargs=llm_kwargs)
        else:
            input_ = user_input
            encode_img = []

        what_i_have_asked["parts"].append({"text": input_})
        if encode_img:
            for data in encode_img:
                what_i_have_asked["parts"].append(
                    {
                        "inline_data": {
                            "mime_type": f"image/{data['type']}",
                            "data": data["data"],
                        }
                    }
                )
        return what_i_have_asked

    def __conversation_history(self, history, llm_kwargs, enable_multimodal_capacity):
        messages = []
        conversation_cnt = len(history) // 2
        if conversation_cnt:
            for index in range(0, 2 * conversation_cnt, 2):
                what_i_have_asked = self.__conversation_user(history[index], llm_kwargs, enable_multimodal_capacity)
                what_gpt_answer = {
                    "role": "model",
                    "parts": [{"text": history[index + 1]}],
                }
                messages.append(what_i_have_asked)
                messages.append(what_gpt_answer)
        return messages

    def generate_message_payload(
        self, inputs, llm_kwargs, history, system_prompt, image_base64_array:list=[], has_multimodal_capacity:bool=False
    ) -> Tuple[Dict, Dict]:
        messages = [
            # {"role": "system", "parts": [{"text": system_prompt}]},  # gemini 不允许对话轮次为偶数，所以这个没有用，看后续支持吧。。。
            # {"role": "user", "parts": [{"text": ""}]},
            # {"role": "model", "parts": [{"text": ""}]}
        ]
        self.url_gemini = self.url_gemini.replace(
            "%m", llm_kwargs["llm_model"]
        ).replace("%k", get_conf("GEMINI_API_KEY"))
        header = {"Content-Type": "application/json"}

        if has_multimodal_capacity:
            enable_multimodal_capacity = (len(image_base64_array) > 0) or any([contain_base64(h) for h in history])
        else:
            enable_multimodal_capacity = False

        if not enable_multimodal_capacity:
            messages.extend(
                self.__conversation_history(history, llm_kwargs, enable_multimodal_capacity)
            )  # 处理 history

        messages.append(self.__conversation_user(inputs, llm_kwargs, enable_multimodal_capacity))  # 处理用户对话
        stop_sequences = str(llm_kwargs.get("stop", "")).split(" ")
        # 过滤空字符串并确保至少有一个停止序列
        stop_sequences = [s for s in stop_sequences if s]
        if not stop_sequences:
            payload = {
                "contents": messages,
                "generationConfig": {
                    "temperature": llm_kwargs.get("temperature", 1),
                    "topP": llm_kwargs.get("top_p", 0.8),
                    "topK": 10,
                },
            }
        else:
            payload = {
                "contents": messages,
                "generationConfig": {
                    # "maxOutputTokens": llm_kwargs.get("max_token", 1024),
                    "stopSequences": stop_sequences,
                    "temperature": llm_kwargs.get("temperature", 1),
                    "topP": llm_kwargs.get("top_p", 0.8),
                    "topK": 10,
                },
            }

        return header, payload


if __name__ == "__main__":
    google = GoogleChatInit()
