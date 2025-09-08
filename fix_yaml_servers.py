#!/usr/bin/env python3
"""
修复 YAML 文件中的 servers 引用问题
"""

import os
import re
from pathlib import Path

def fix_yaml_file(yaml_path):
    """修复单个 YAML 文件中的 servers 引用"""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换错误的 servers 引用
        old_servers = """servers:
  $ref: '../shared-components.yaml#/servers'"""
        
        new_servers = """servers:
  - url: https://zim-api.zego.im
    description: ZIM 服务端 API 地址"""
        
        if old_servers in content:
            content = content.replace(old_servers, new_servers)
            
            with open(yaml_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {yaml_path}")
            return True
        else:
            print(f"No fix needed for {yaml_path}")
            return False
            
    except Exception as e:
        print(f"Error fixing {yaml_path}: {e}")
        return False

def main():
    """主函数"""
    base_path = Path("core_products/zim/zh/docs_zim_server_zh")
    
    # 查找所有 YAML 文件
    yaml_files = []
    for module in ['user', 'group', 'messaging', 'room', 'conversation', 'call-invitation', 'bot', 'zim-audio']:
        module_path = base_path / module
        if module_path.exists():
            yaml_files.extend(module_path.glob('*.yaml'))
    
    fixed_count = 0
    for yaml_file in yaml_files:
        if yaml_file.name != 'shared-components.yaml':  # 跳过共享组件文件
            if fix_yaml_file(yaml_file):
                fixed_count += 1
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == "__main__":
    main()
