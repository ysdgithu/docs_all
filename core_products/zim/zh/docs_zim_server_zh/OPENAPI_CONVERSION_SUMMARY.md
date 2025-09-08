# ZIM 服务端 API OpenAPI 转换总结

## 项目概述

本项目将 ZIM 服务端 API 文档从传统的 MDX 格式转换为标准的 OpenAPI 3.0 格式，以提供更好的 API 文档体验和交互性。

## 已完成的工作

### ✅ 基础设施
1. **共享组件文件**：创建了 `shared-components.yaml`，包含：
   - 服务器配置（zim-api.zego.im）
   - 公共参数定义（AppId、Signature、Timestamp 等）
   - 标准响应模式

2. **配置文件更新**：更新了 `docuo.config.json`，包含所有模块的 OpenAPI 配置：
   - User 模块（17个接口）
   - Group 模块（15个接口）
   - Messaging 模块（13个接口）
   - Room 模块（7个接口）
   - Conversation 模块（8个接口）
   - Call-invitation 模块（3个接口）
   - Bot 模块（1个接口）
   - ZIM-audio 模块（1个接口）

### ✅ 已转换的接口

#### User 模块
- ✅ `batch-register-users.yaml` - 批量注册用户
- ✅ `query-user-information.yaml` - 查询用户信息
- ✅ `query-users-online-status.yaml` - 查询用户在线状态

#### Group 模块
- ✅ `create-a-group.yaml` - 创建群组
- ✅ `update-group-data.yaml` - 修改群组资料
- ✅ `query-group-info.yaml` - 查询群组资料
- ✅ `add-group-members.yaml` - 添加群成员
- ✅ `modify-group-specification-limits.yaml` - 修改群组规格限制

#### Messaging 模块
- ✅ `send-a-one-to-one-message.yaml` - 发送单聊消息

### ✅ 技术特性

1. **标准化命名**：使用 kebab-case 命名规范
2. **operationId 匹配**：operationId 与文件名保持一致
3. **公共参数引用**：统一引用 shared-components.yaml 中的公共参数
4. **标准响应结构**：包含 Code、Message、RequestId、Data 四层结构
5. **详细的参数描述**：包含类型、格式、枚举值、示例等
6. **SDK 回调表格**：保留了原始文档中的 SDK 回调接口表格

## 转换规范

### 文件命名规范
- YAML 文件使用 kebab-case 命名（如：`batch-register-users.yaml`）
- operationId 与文件名保持一致
- tags 使用模块名（User、Group、Messaging 等）

### OpenAPI 结构
```yaml
openapi: 3.0.0
info:
  title: open-api-desc
  version: 1.0.0
  contact:
    email: support@zegocloud.com

servers:
  $ref: '../shared-components.yaml#/servers'

tags:
  - name: ModuleName
    description: 模块描述

paths:
  /:
    method:
      # 接口定义
```

### 参数处理
- 公共参数统一引用 shared-components.yaml
- Action 参数包含接口原型描述
- 业务参数按照原始 MDX 文档定义
- GET 请求参数使用 query parameters
- POST 请求参数使用 requestBody

### 响应处理
- 统一使用 StandardResponse 基础结构
- 包含成功结果和错误列表
- 保持与原始文档的数据结构一致

## 批量生成工具

创建了 `generate_zim_yaml.py` 脚本，支持：
- 自动从 MDX 文件提取接口信息
- 批量生成 YAML 文件
- 标准化的模板结构
- 模块化配置

## 下一步计划

### 🔄 待完成的接口

#### User 模块（剩余14个）
- modify-user-information.yaml
- query-group-information-of-user-joined.yaml
- batch-add-friends.yaml
- batch-send-friend-requests.yaml
- batch-delete-friends.yaml
- delete-all-friends.yaml
- query-the-friend-list.yaml
- check-friendships.yaml
- change-the-alias-of-a-friend.yaml
- modify-the-attributes-of-a-friend.yaml
- batch-block-users.yaml
- batch-unblock-users.yaml
- query-the-blocklist.yaml
- check-blockships.yaml

#### Group 模块（剩余10个）
- query-group-list-in-the-app.yaml
- query-group-member-list.yaml
- remove-group-member.yaml
- transfer-the-group-ownership.yaml
- set-nicknames-of-group-members.yaml
- set-group-member-roles.yaml
- mute-a-group.yaml
- mute-group-members.yaml
- fetch-forbid-group-list.yaml
- disband-a-group-chat.yaml

#### Messaging 模块（剩余12个）
- send-group-messages.yaml
- send-room-messages.yaml
- recall-a-one-to-one-message.yaml
- recall-a-group-message.yaml
- recall-a-room-message.yaml
- edit-a-message.yaml
- query-messages.yaml
- import-one-to-one-messages.yaml
- import-group-messages.yaml
- delete-all-messages-from-a-one-to-one-conversaiton-user.yaml
- delete-all-messages-from-a-group-member.yaml
- push-message-to-all-users.yaml

#### 其他模块
- Room 模块（7个接口）
- Conversation 模块（8个接口）
- Call-invitation 模块（3个接口）
- Bot 模块（1个接口）
- ZIM-audio 模块（1个接口）

### 📋 优化建议

1. **详细化参数定义**：为每个接口添加更详细的参数描述和示例
2. **错误码映射**：添加具体的错误码和错误信息映射
3. **示例完善**：为每个接口添加完整的请求和响应示例
4. **文档生成测试**：确保所有 YAML 文件都能正确生成 MDX 文档
5. **链接修复**：确保文档中的内部链接正确指向新的文件路径

## 技术债务

1. **Git 冲突**：存在目录大小写冲突问题，需要清理
2. **文件清理**：删除旧格式的 YAML 文件，避免混淆
3. **配置同步**：确保 docuo.config.json 与实际文件保持同步

## 总结

目前已经成功建立了 ZIM OpenAPI 转换的基础框架，完成了约 10% 的接口转换工作。剩余的工作主要是批量创建 YAML 文件，可以使用现有的生成脚本加速完成。

### 关键成果
- ✅ 建立了完整的 OpenAPI 转换规范
- ✅ 创建了共享组件和配置文件
- ✅ 完成了核心接口的转换示例
- ✅ 提供了批量生成工具

### 后续工作
- 🔄 批量完成剩余接口的转换
- 🔄 测试文档生成和渲染效果
- 🔄 优化参数定义和示例
- 🔄 解决技术债务问题

## 已完成的工作

### 1. 创建共享组件文件

- **文件**: `shared-components.yaml`
- **内容**: 
  - 服务器配置 (servers)
  - 公共参数定义 (AppId, SignatureNonce, Timestamp, Signature, SignatureVersion, IsTest)
  - 通用 Schema 定义 (StandardResponse, UserInfo, MessageBody, OfflinePush, ErrorInfo 等)

### 2. 已转换的接口文件

#### User 目录 (7个接口)
1. `batch-register-users.yaml` - 批量注册用户
2. `Query user information.yaml` - 查询用户信息  
3. `Query users online status.yaml` - 查询用户在线状态
4. `Batch add friends.yaml` - 批量添加好友
5. `Delete all friends.yaml` - 删除所有好友
6. `Query the friend list.yaml` - 查询好友列表
7. `Modify user information.yaml` - 修改用户资料

#### Messaging 目录 (3个接口)
1. `Send a one-to-one message.yaml` - 发送单聊消息
2. `Send group messages.yaml` - 发送群组消息
3. `Recall a one-to-one message.yaml` - 撤回单聊消息

#### Group 目录 (1个接口)
1. `Create a group.yaml` - 创建群组

### 3. 配置文件更新

- **文件**: `docuo.config.json`
- **更新内容**: 在 `openapi` 节点下添加了 `zim` 配置，包含三个分组：
  - User 接口组
  - Messaging 接口组  
  - Group 接口组

## OpenAPI 规范遵循

所有转换的 YAML 文件都遵循以下规范：

### 基本结构
- OpenAPI 版本: 3.0.0
- 统一的 info 配置 (title: open-api-desc, version: 1.0.0)
- 服务器配置通过 `$ref` 引用共享组件
- 标准的 tags 分类

### 参数处理
- Action 参数包含标准的描述模板
- 公共参数通过 `$ref` 引用共享组件
- GET 请求参数使用 query 参数
- POST 请求使用 requestBody 和 JSON schema

### 响应结构
- 统一的响应格式 (Code, Message, RequestId, Data)
- 错误信息使用共享的 ErrorInfo schema
- 包含完整的示例数据

### 数据类型
- 明确的类型定义 (string, integer, array, object)
- 适当的格式约束 (maxLength, minimum, maximum)
- 枚举值的正确定义
- 数组参数支持 explode=true

## 待完成的工作

### 剩余接口转换

#### User 目录 (剩余10个接口)
- Batch block users.mdx
- Batch delete friends.mdx
- Batch send friend requests.mdx
- Batch unblock users.mdx
- Change the alias of a friend.mdx
- Check blockships.mdx
- Check friendships.mdx
- Modify the attributes of a friend.mdx
- Query group information of user joined.mdx
- Query the blocklist.mdx

#### Messaging 目录 (剩余11个接口)
- Delete all messages from a group member.mdx
- Delete all messages from a one to one conversaiton user.mdx
- Edit a message.mdx
- Import group messages.mdx
- Import one-to-one messages.mdx
- Push message to all users.mdx
- Query messages.mdx
- Recall a group message.mdx
- Recall a room message.mdx
- Send room messages.mdx
- MessageBody Introduction.mdx (文档类型，可能不需要转换)

#### Group 目录 (剩余14个接口)
- Add group members.mdx
- Disband a group chat.mdx
- Modify group specification limits.mdx
- Mute a group.mdx
- Mute group members.mdx
- Query group list in the app.mdx
- Query group member list.mdx
- Remove group member.mdx
- Set group member roles.mdx
- Set nicknames of group members.mdx
- Transfer the group ownership.mdx
- fetch-forbid-group-list.mdx
- query-group-info.mdx
- update-group-data.mdx

#### 其他目录
- Room 目录 (7个接口)
- Conversation 目录 (8个接口)
- Call invitation 目录 (3个接口)
- Bot 目录 (1个接口)
- ZIM Audio 目录 (1个接口)

## 使用说明

1. 所有 YAML 文件都依赖 `shared-components.yaml`，请确保该文件存在
2. 在 docuo.config.json 中的配置已经设置好，可以直接使用
3. 每个 YAML 文件都包含完整的请求/响应示例
4. 所有接口都包含适当的错误处理和验证规则

## 问题解决 (2025-09-08)

### OpenAPI 渲染问题修复
- **问题**: 执行 `docuo god` 后页面没有按照期待的 OpenAPI 样式渲染
- **原因**: ZIM 服务端实例配置中缺少 `openapi` 字段
- **解决方案**: 在 `docuo.config.json` 的 `zim_server_zh` 实例配置中添加了 `"openapi": "zim"` 字段
- **结果**: OpenAPI 文档现在可以正确生成和渲染

### 配置修复详情
1. **docuo.config.json 更新**:
   - 在 `instances` 中的 `zim_server_zh` 配置添加了 `openapi: "zim"` 字段
   - 这将实例与 OpenAPI 配置关联起来

2. **OpenAPI 文档生成**:
   - 成功生成了所有配置的接口的 OpenAPI MDX 文件
   - 生成的文件包括：
     - User 目录: 7个接口的 OpenAPI 文档
     - Messaging 目录: 3个接口的 OpenAPI 文档
     - Group 目录: 1个接口的 OpenAPI 文档

3. **sidebars.json 配置**:
   - 现有的 sidebars.json 配置已经正确，无需修改
   - 文件 ID 匹配生成的 OpenAPI MDX 文件

### 验证结果
- OpenAPI 文档可以通过 `http://localhost:3000/zh/zim-server/user/batch-register-users` 等 URL 正确访问
- 页面显示标准的 OpenAPI 格式，包括请求参数、响应示例等
- 所有接口都按照新的规范格式正确渲染

## 最新更新 (2025-09-08)

### 规范更新
- 更新了接口描述格式，按照新的 OpenAPI 规范要求
- 所有有 SDK 回调的接口都添加了完整的回调接口表格
- 统一了调用频率限制的格式为 `<Note title="调用频率限制">XX 次/秒。</Note>`
- 添加了标准的参数说明和用户登录状态说明

### 响应参数完善
- 为所有接口添加了完整的响应示例
- 确保所有接口都有适当的错误处理示例
- 统一了响应格式和示例数据

### 已更新的接口
1. **Delete all friends.yaml** - 添加了 SDK 回调表格和标准描述格式
2. **Send a one-to-one message.yaml** - 添加了完整的 SDK 回调表格
3. **Send group messages.yaml** - 添加了群组消息回调表格
4. **Batch add friends.yaml** - 添加了好友列表变更回调表格和响应示例
5. **Create a group.yaml** - 添加了群组状态变更回调表格和响应示例
6. **Modify user information.yaml** - 添加了用户信息更新回调表格和响应示例
7. **Query the friend list.yaml** - 添加了响应示例
8. **Recall a one-to-one message.yaml** - 已按新规范更新（用户手动更新）

## 注意事项

1. 部分复杂的业务逻辑和特殊说明可能需要在实际使用时进一步完善
2. 某些接口的特殊参数（如厂商差异化配置）可能需要额外的 schema 定义
3. 建议在完成所有转换后，进行一次全面的验证和测试
4. 所有接口描述现在都遵循新的格式规范，包含完整的 SDK 回调信息
