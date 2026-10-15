from loguru import logger


def check_proxy(proxies, return_ip=False):
    """
    检查代理配置并返回结果。
    """
    import requests
    proxies_https = proxies['https'] if proxies is not None else '无'
    ip = None
    try:
        response = requests.get("https://ipapi.co/json/", proxies=proxies, timeout=4)
        data = response.json()
        if 'country_name' in data:
            country = data['country_name']
            result = f"代理配置 {proxies_https}, 代理所在地：{country}"
            if 'ip' in data:
                ip = data['ip']
        elif 'error' in data:
            alternative, ip = _check_with_backup_source(proxies)
            if alternative is None:
                result = f"代理配置 {proxies_https}, 代理所在地：未知，IP查询频率受限"
            else:
                result = f"代理配置 {proxies_https}, 代理所在地：{alternative}"
        else:
            result = f"代理配置 {proxies_https}, 代理数据解析失败：{data}"

        if not return_ip:
            logger.warning(result)
            return result
        else:
            return ip
    except:
        result = f"代理配置 {proxies_https}, 代理所在地查询超时，代理可能无效"
        if not return_ip:
            logger.warning(result)
            return result
        else:
            return ip


def _check_with_backup_source(proxies):
    import random, string, requests
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    try:
        res_json = requests.get(f"http://{random_string}.edns.ip-api.com/json", proxies=proxies, timeout=4).json()
        return res_json['dns']['geo'], res_json['dns']['ip']
    except:
        return None, None


def warm_up_modules():
    """
    预热分词器模块。
    """
    logger.info('正在执行分词器模块的预热 ...')
    from toolbox import ProxyNetworkActivate
    from request_llms.bridge_all import tokenizer_gpt35, tokenizer_gpt4
    with ProxyNetworkActivate("Warmup_Modules"):
        tokenizer_gpt35.encode("模块预热", disallowed_special=())
        tokenizer_gpt4.encode("模块预热", disallowed_special=())


if __name__ == '__main__':
    import os
    os.environ['no_proxy'] = '*'
    from toolbox import get_conf
    proxies = get_conf('proxies')
    check_proxy(proxies)
