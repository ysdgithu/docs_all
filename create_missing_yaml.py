#!/usr/bin/env python3
"""
创建缺失的 YAML 文件
"""

import os
import re
from pathlib import Path

# 基础 YAML 模板
YAML_TEMPLATE = """openapi: 3.0.0
info:
  title: open-api-desc
  version: 1.0.0
  contact:
    email: support@zegocloud.com

servers:
  - url: https://zim-api.zego.im
    description: ZIM 服务端 API 地址

tags:
  - name: {tag}
    description: {tag_description}

paths:
  /:
    {method}:
      tags:
        - {tag}
      summary: {summary}
      description: |
        {description}

        <Note title="调用频率限制">{rate_limit}</Note>

        以下请求参数列表仅列出了接口请求参数和部分公共参数，完整公共参数列表请参考 [调用方式 - 公共请求参数](../accessing-server-apis.mdx#2-公共参数)。
      operationId: {operation_id}
      parameters:
        - name: Action
          in: query
          required: true
          description: |
            > 接口原型参数
            >
            > https://zim-api.zego.im?Action={action}
          schema:
            type: string
            enum: ["{action}"]
        - $ref: '../shared-components.yaml#/components/parameters/AppId'
        - $ref: '../shared-components.yaml#/components/parameters/SignatureNonce'
        - $ref: '../shared-components.yaml#/components/parameters/Timestamp'
        - $ref: '../shared-components.yaml#/components/parameters/Signature'
        - $ref: '../shared-components.yaml#/components/parameters/SignatureVersion'
        - $ref: '../shared-components.yaml#/components/parameters/IsTest'
{request_body}
      responses:
        '200':
          description: 成功响应
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/{response_schema}'

components:
  schemas:
{schemas}
"""

def extract_mdx_info(mdx_path):
    """从 MDX 文件中提取信息"""
    try:
        with open(mdx_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "API"
        
        # 提取描述
        desc_match = re.search(r'## 描述\n\n(.+?)(?=\n##)', content, re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()
            # 简化描述，移除复杂的表格
            description = re.sub(r'\|[^|]*\|.*?\n', '', description, flags=re.MULTILINE)
            description = re.sub(r'\n\n+', '\n\n', description)
        else:
            description = title
        
        # 提取请求方法
        method_match = re.search(r'请求方法：(GET|POST)', content)
        method = method_match.group(1).lower() if method_match else "post"
        
        # 提取 Action
        action_match = re.search(r'Action=(\w+)', content)
        action = action_match.group(1) if action_match else "DefaultAction"
        
        # 提取频率限制
        rate_match = re.search(r'调用频率限制：(.+?)次/秒', content)
        rate_limit = rate_match.group(1) + " 次/秒。" if rate_match else "20 次/秒。"
        
        return {
            'title': title,
            'description': description,
            'method': method,
            'action': action,
            'rate_limit': rate_limit
        }
    except Exception as e:
        print(f"Error reading {mdx_path}: {e}")
        return None

def create_yaml_file(module, file_name, base_path):
    """创建单个 YAML 文件"""
    mdx_path = base_path / module / f"{file_name}.mdx"
    yaml_path = base_path / module / f"{file_name}.yaml"
    
    # 如果 YAML 文件已存在，跳过
    if yaml_path.exists():
        print(f"Skipping {yaml_path} (already exists)")
        return
    
    # 检查 MDX 文件是否存在
    if not mdx_path.exists():
        print(f"MDX file not found: {mdx_path}")
        return
    
    # 提取 MDX 信息
    mdx_info = extract_mdx_info(mdx_path)
    if not mdx_info:
        print(f"Failed to extract info from {mdx_path}")
        return
    
    # 模块配置
    module_configs = {
        'user': {'tag': 'User', 'tag_description': '用户管理相关接口'},
        'group': {'tag': 'Group', 'tag_description': '群组管理相关接口'},
        'messaging': {'tag': 'Messaging', 'tag_description': '消息管理相关接口'},
        'room': {'tag': 'Room', 'tag_description': '房间管理相关接口'},
        'conversation': {'tag': 'Conversation', 'tag_description': '会话管理相关接口'},
        'call-invitation': {'tag': 'CallInvitation', 'tag_description': '呼叫邀请相关接口'},
        'bot': {'tag': 'Bot', 'tag_description': '机器人相关接口'},
        'zim-audio': {'tag': 'ZimAudio', 'tag_description': 'ZIM 音频相关接口'}
    }
    
    module_config = module_configs.get(module, {'tag': 'API', 'tag_description': 'API 接口'})
    
    # 生成请求体和响应模式
    request_body = ""
    if mdx_info['method'] == 'post':
        schema_name = ''.join(word.capitalize() for word in file_name.split('-'))
        request_body = f"""      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/{schema_name}Request'"""
    
    response_schema = ''.join(word.capitalize() for word in file_name.split('-')) + 'Response'
    
    # 简单的 schema 定义
    schema_name = ''.join(word.capitalize() for word in file_name.split('-'))
    if mdx_info['method'] == 'post':
        schemas = f"""    {schema_name}Request:
      type: object
      properties:
        # TODO: 根据具体接口定义请求参数
        placeholder:
          type: string
          description: 占位符，需要根据实际接口定义

    {response_schema}:
      allOf:
        - $ref: '../shared-components.yaml#/components/schemas/StandardResponse'
        - type: object
          properties:
            # TODO: 根据具体接口定义响应数据
            Data:
              type: object
              description: 响应数据，需要根据实际接口定义"""
    else:
        schemas = f"""    {response_schema}:
      allOf:
        - $ref: '../shared-components.yaml#/components/schemas/StandardResponse'"""
    
    yaml_content = YAML_TEMPLATE.format(
        tag=module_config['tag'],
        tag_description=module_config['tag_description'],
        method=mdx_info['method'],
        summary=mdx_info['title'],
        description=mdx_info['description'],
        rate_limit=mdx_info['rate_limit'],
        operation_id=file_name,
        action=mdx_info['action'],
        request_body=request_body,
        response_schema=response_schema,
        schemas=schemas
    )
    
    # 写入文件
    try:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        print(f"Generated {yaml_path}")
    except Exception as e:
        print(f"Error writing {yaml_path}: {e}")

def main():
    """主函数"""
    base_path = Path("core_products/zim/zh/docs_zim_server_zh")
    
    # 缺失的文件列表
    missing_files = [
        # Group 模块
        ('group', 'disband-a-group-chat'),
        ('group', 'fetch-forbid-group-list'),
        ('group', 'mute-a-group'),
        ('group', 'mute-group-members'),
        ('group', 'query-group-list-in-the-app'),
        ('group', 'query-group-member-list'),
        ('group', 'remove-group-member'),
        ('group', 'set-group-member-roles'),
        ('group', 'set-nicknames-of-group-members'),
        ('group', 'transfer-the-group-ownership'),
    ]
    
    for module, file_name in missing_files:
        print(f"Processing {module}/{file_name}...")
        create_yaml_file(module, file_name, base_path)

if __name__ == "__main__":
    main()
