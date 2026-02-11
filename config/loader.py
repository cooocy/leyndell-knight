import os
import re

import yaml


def load_yaml_configurations(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        yaml_content = f.read()

        def replace_env_var(match):
            var_name = match.group(1)
            default_val = match.group(2) if match.group(2) else ""
            # 从环境变量获取值, 没有则用默认值
            return os.getenv(var_name, default_val)

        # 替换所有环境变量占位符
        # 正则匹配 ${VAR_NAME:DEFAULT} 或 ${VAR_NAME} 格式的占位符
        # 匹配到占位符后, 从环境变量取值, 无则用默认值
        env_pattern = re.compile(r"\$\{([^}:-]+)(?::([^}]+))?}")
        replaced_content = env_pattern.sub(replace_env_var, yaml_content)
        # 解析替换后的 YAML 内容
        config = yaml.safe_load(replaced_content)
        return config
