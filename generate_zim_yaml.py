#!/usr/bin/env python3
"""
ZIM OpenAPI YAML 文件批量生成脚本
根据现有的 MDX 文件生成对应的 OpenAPI YAML 文件
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
  $ref: '../shared-components.yaml#/servers'

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
        
        # 提取描述 - 查找 ## 描述 部分
        desc_match = re.search(r'## 描述\n\n(.+?)(?=\n##)', content, re.DOTALL)
        if not desc_match:
            # 如果没有找到 ## 描述，尝试查找第一段内容
            desc_match = re.search(r'# .+?\n\n(.+?)(?=\n##)', content, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else title
        
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

def generate_yaml_file(module, file_name, base_path):
    """生成单个 YAML 文件"""
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
    
    # 需要处理的文件列表（从配置文件中提取）
    files_to_generate = [
        # User 模块
        ('user', 'modify-user-information'),
        ('user', 'query-group-information-of-user-joined'),
        ('user', 'batch-add-friends'),
        ('user', 'batch-send-friend-requests'),
        ('user', 'batch-delete-friends'),
        ('user', 'delete-all-friends'),
        ('user', 'query-the-friend-list'),
        ('user', 'check-friendships'),
        ('user', 'change-the-alias-of-a-friend'),
        ('user', 'modify-the-attributes-of-a-friend'),
        ('user', 'batch-block-users'),
        ('user', 'batch-unblock-users'),
        ('user', 'query-the-blocklist'),
        ('user', 'check-blockships'),
        
        # Messaging 模块
        ('messaging', 'send-group-messages'),
        ('messaging', 'send-room-messages'),
        ('messaging', 'recall-a-one-to-one-message'),
        ('messaging', 'recall-a-group-message'),
        ('messaging', 'recall-a-room-message'),
        ('messaging', 'edit-a-message'),
        ('messaging', 'query-messages'),
        ('messaging', 'import-one-to-one-messages'),
        ('messaging', 'import-group-messages'),
        ('messaging', 'delete-all-messages-from-a-one-to-one-conversaiton-user'),
        ('messaging', 'delete-all-messages-from-a-group-member'),
        ('messaging', 'push-message-to-all-users'),
        
        # Room 模块
        ('room', 'create-a-room'),
        ('room', 'query-room-attributes'),
        ('room', 'update-room-attributes'),
        ('room', 'obtain-information-about-users-in-a-room'),
        ('room', 'remove-user-from-the-room'),
        ('room', 'destroy-the-room'),
        ('room', 'query-whether-a-user-is-in-a-room'),
        
        # Conversation 模块
        ('conversation', 'query-conversation-list'),
        ('conversation', 'delete-a-conversation'),
        ('conversation', 'clear-the-unread-message-count-of-a-conversation'),
        ('conversation', 'mute-notifications-for-conversations'),
        ('conversation', 'pin-conversations-to-the-top'),
        ('conversation', 'set-conversation-marks'),
        ('conversation', 'query-the-message-list-of-one-on-one-chats'),
        ('conversation', 'query-the-message-list-of-group-chats'),
        
        # Call-invitation 模块
        ('call-invitation', 'send-a-call-invitation'),
        ('call-invitation', 'accept-a-call-invitation'),
        ('call-invitation', 'reject-a-call-invitation'),
        
        # Bot 模块
        ('bot', 'register-bots'),
        
        # ZIM-audio 模块
        ('zim-audio', 'obtain-a-license'),
    ]
    
    for module, file_name in files_to_generate:
        print(f"Processing {module}/{file_name}...")
        generate_yaml_file(module, file_name, base_path)

if __name__ == "__main__":
    main()
