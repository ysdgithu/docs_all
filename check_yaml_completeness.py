#!/usr/bin/env python3
"""
检查 YAML 文件的完整性
"""

import os
from pathlib import Path

def check_module(module_path):
    """检查单个模块的 YAML 文件完整性"""
    module_name = module_path.name
    print(f"\n=== {module_name.upper()} 模块 ===")
    
    mdx_files = []
    yaml_files = []
    
    for file in module_path.iterdir():
        if file.is_file():
            if file.suffix == '.mdx' and file.name != 'open-api-desc.mdx' and not file.name.startswith('messagebody'):
                mdx_files.append(file.stem)
            elif file.suffix == '.yaml':
                yaml_files.append(file.stem)
    
    mdx_files.sort()
    yaml_files.sort()
    
    print(f"MDX 文件数量: {len(mdx_files)}")
    print(f"YAML 文件数量: {len(yaml_files)}")
    
    # 检查缺失的 YAML 文件
    missing_yaml = set(mdx_files) - set(yaml_files)
    if missing_yaml:
        print(f"❌ 缺失的 YAML 文件: {sorted(missing_yaml)}")
    else:
        print("✅ 所有 MDX 文件都有对应的 YAML 文件")
    
    # 检查多余的 YAML 文件
    extra_yaml = set(yaml_files) - set(mdx_files)
    if extra_yaml:
        print(f"ℹ️  额外的 YAML 文件: {sorted(extra_yaml)}")
    
    return len(missing_yaml) == 0

def main():
    """主函数"""
    base_path = Path("core_products/zim/zh/docs_zim_server_zh")
    
    modules = ['user', 'group', 'messaging', 'room', 'conversation', 'call-invitation', 'bot', 'zim-audio']
    
    all_complete = True
    total_mdx = 0
    total_yaml = 0
    
    for module in modules:
        module_path = base_path / module
        if module_path.exists():
            is_complete = check_module(module_path)
            all_complete = all_complete and is_complete
            
            # 统计文件数量
            mdx_count = len([f for f in module_path.iterdir() 
                           if f.suffix == '.mdx' and f.name != 'open-api-desc.mdx' and not f.name.startswith('messagebody')])
            yaml_count = len([f for f in module_path.iterdir() if f.suffix == '.yaml'])
            
            total_mdx += mdx_count
            total_yaml += yaml_count
        else:
            print(f"\n=== {module.upper()} 模块 ===")
            print("❌ 模块目录不存在")
            all_complete = False
    
    print(f"\n{'='*50}")
    print(f"总结:")
    print(f"总 MDX 文件数: {total_mdx}")
    print(f"总 YAML 文件数: {total_yaml}")
    
    if all_complete:
        print("🎉 所有模块的 YAML 文件都已完整!")
    else:
        print("⚠️  还有模块缺少 YAML 文件")

if __name__ == "__main__":
    main()
