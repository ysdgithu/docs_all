---
type: "manual"
---

---
type: "manual"---

# OpenAPI 文档生成与维护规范（ZEGO 服务端 API 通用）

以下规则总结自本轮改造工作，适用于 ZEGO 所有服务端 API 文档（各产品线/语言/区域）对应的 OpenAPI YAML 的生成与后续维护。

## 目录与命名
- 每个 mdx 对应一个同名 yaml，目录结构与 mdx 所在目录一致。
- operationId 使用 mdx 文件名（不带扩展名），如 start-cdn-recrod.mdx → operationId: start-cdn-recrod。
- tags 取 mdx 所在目录名，例如：cdn、room、media-service、stream-mixing、moderation、scene。

## OpenAPI 基本骨架
- openapi 版本统一为 3.0.0，info 中保持 title=open-api-desc、version=1.0.0、contact 为 ZEGO 支持邮箱。
- 每个 YAML 必须显式包含 servers，且使用共享文件统一维护：
  - 在 paths 节点前加入：
    servers:
      $ref: '../shared-components.yaml#/servers'
  - 特例（如 scene/set-scene-template 走 metaworld 域名）如需差异化，先与维护者确认；缺省仍引 shared-components.yaml。

## 公共参数与 Action
- 公共参数统一从 shared-components.yaml 引用：
  - AppId、SignatureNonce、Timestamp、Signature、SignatureVersion、IsTest。
- GET/POST 的参数顺序：
  1) Action
  2) 公共参数（如上）
  3) 业务参数（按 mdx 定义）
- Action 字段要求：
  - 必填，in=query，schema.enum 为具体 Action 值（例如 MergeMedia）。
  - description 使用固定 MD 块，格式如下：
    > 接口原型参数
    >
    > https://rtc-api.zego.im?Action=YourAction

## paths 与方法
- paths 下仅保留根路径 /。
- 请求方法遵循 mdx：GET 或 POST。POST 场景使用 requestBody.application/json，Schema 从组件中引用。

## 类型与格式
- 明确的数值类型补充 format：
  - int32、int64、uint32、float 等；时间戳统一 int64 秒（按 mdx）。
- 枚举使用 enum 指定合法值；必要时 default 与 enum 同步约束。
- array 参数采用 style=form + explode=true 以支持多值形态。

## 响应结构
- 统一包含 Code、Message、RequestId、Data 四层结构（除非 mdx 特别说明返回为空）。
- Data 内的厂商差异（如 Tencent、Huawei、Ws）要按照 mdx 列表精确还原结构与字段。

## 生成流程（操作步骤）
1) 读取对应 mdx，确定：请求方法、Action、业务参数、响应结构与示例、频率限制与注意事项。
2) 新建同名 yaml，填充固定骨架：openapi、info、tags、servers（$ref）、paths:/、方法、Action 描述块、公共参数 $ref。
3) 按 mdx 定义补充业务参数，保持顺序与约束（required、enum、format、样例）。
4) 依据 mdx 的“响应参数/示例” 定义 components.schemas，注意多厂商差异结构与字段。
5) 保存并在 TASKS.md 勾选条目。

## 其他约定
- 禁止在 YAML 内手写 servers 列表，统一引用 shared-components.yaml。
- 如需新增服务器域或特殊域名，先在 shared-components.yaml 维护后再通过 $ref 引用。
- 不要在 YAML 内定义或复制公共参数实体，统一从 shared-components.yaml 引用，避免漂移。
- 对于 POST 接口，Headers 信息在文档说明即可，不在 OpenAPI 中强制定义。
- 如 mdx 中存在“厂商限定生效”的参数/字段，需在 description 中明确。

## 示例片段
- 引用 servers：
  servers:
    $ref: '../shared-components.yaml#/servers'
- 引用公共参数：
  - $ref: '../shared-components.yaml#/components/parameters/AppId'
  - $ref: '../shared-components.yaml#/components/parameters/IsTest'
- Action 描述模板：
  description: |
    > 接口原型参数
    >
    > https://rtc-api.zego.im?Action=MergeMedia'

## 接口描述
- 当前生成
  description: |
        调用此接口，您可以撤回 2 分钟内的单聊会话消息。如需撤回更早之前的消息，请联系 ZEGO 技术支持，最多可撤回 24 小时内发出的消息。
        
        消息撤回后，消息接收用户将通过 ZIM SDK 的回调接口，接收消息已被撤回的通知。
        
        调用频率限制：20 次/秒。
- 应该生成
  description: |
        调用此接口，您可以撤回 2 分钟内的单聊会话消息。如需撤回更早之前的消息，请联系 ZEGO 技术支持，最多可撤回 24 小时内发出的消息。

        消息撤回后，消息接收用户将通过以下 ZIM SDK 的回调接口，接收消息已被撤回的通知。
        
        | iOS-25% | Android-25% | macOS-25% | Windows-25% |
        |-----|---------|-------|---------|
        | [messageRevokeReceived](https://doc-zh.zego.im/article/api?doc=zim_API~objective-c_ios~protocol~ZIMEventHandler#zim-message-revoke-received) | [onMessageRevokeReceived](https://doc-zh.zego.im/article/api?doc=zim_API~java_android~class~ZIMEventHandler#on-message-revoke-received) | [messageRevokeReceived](https://doc-zh.zego.im/article/api?doc=zim_API~objective-c_macos~protocol~ZIMEventHandler#zim-message-revoke-received) | [onMessageRevokeReceived](https://doc-zh.zego.im/article/api?doc=zim_API~cpp_windows~class~ZIMEventHandler#on-message-revoke-received) |
        
        | Web-25% | 小程序-25% | Flutter-25% | React Native-25% |
        |---------|-----|--------|--------------|
        | [messageRevokeReceived](https://doc-zh.zego.im/article/api?doc=zim_API~javascript_web~interface~ZIMEventHandler#message-revoke-received) | [messageRevokeReceived](https://doc-zh.zego.im/article/api?doc=zim_API~javascript_wxxcx~interface~ZIMEventHandler#message-revoke-received) | [onMessageRevokeReceived](https://pub.dev/documentation/zego_zim/latest/zego_zim/ZIMEventHandler/onMessageRevokeReceived.html) | [messageRevokeReceived](https://doc-zh.zego.im/article/api?doc=zim_API~javascript_react-native~interface~ZIMEventHandler#message-revoke-received) |
        
        | Unity3D-25% | uni-app \| uni-app x-25% | HarmonyOS-25% |
        |---------|---------|---------|
        | [OnMessageRevokeReceived](https://doc-zh.zego.im/article/api?doc=zim_API~cs_unity3d~class~ZIMEventHandler#on-message-revoke-received) | [messageRevokeReceived](https://doc-zh.zego.im/article/api?doc=zim_API~javascript_uni-app~interface~ZIMEventHandler#message-revoke-received) | [messageRevokeReceived](https://doc-zh.zego.im/article/api?doc=zim_API~javascript_harmony~interface~ZIMEventHandler#message-revoke-received) |

        <Note title="调用频率限制">20 次/秒。</Note>

        以下请求参数列表仅列出了接口请求参数和部分公共参数，完整公共参数列表请参考 [调用方式 - 公共请求参数](../Accessing%20Server%20APIs.mdx#2-公共参数)。

        <Note title="说明">
        以下 `FromUserId` 和 `ToUserId` 对应的用户已在客户端调用 `login` 方法登录 ZIM 服务，或开发者已调用 [服务端 API](./../User/Batch%20register%20users.mdx) 注册相关的 userID。
        </Note>



