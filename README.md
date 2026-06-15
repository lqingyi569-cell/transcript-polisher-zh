# transcript-polisher-zh

一个用于整理中文录音转写稿、逐字稿、课堂实录、会议记录和访谈稿的 Codex Skill。

它采用“扩展完整通顺版”标准：修复语序、重复、断句和明显识别错误，同时尽量保留原稿中的案例事实、连续追问、观点分歧、反例和论证过程，避免把完整逐字稿压缩成摘要。

## 特点

- 默认保留原稿主体信息量，而非生成课程提要
- 保留 `【老师】`、`【同学】`、`【主持人】` 等发言标记
- 保留不同观点、反驳过程和开放问题
- 对无法可靠恢复的专名和数字采取保守处理
- 支持 DOCX、Markdown 和纯文本稿件
- 提供篇幅保留率、标题和角色标记审计脚本
- 要求 DOCX 成品渲染后逐页检查

## 安装

将仓库克隆到 Codex Skills 目录：

```bash
git clone https://github.com/lqingyi569-cell/transcript-polisher-zh.git \
  ~/.codex/skills/transcript-polisher-zh
```

安装审计脚本依赖：

```bash
python3 -m pip install -r requirements.txt
```

重新启动 Codex，或开始一个新会话，使 Skill 被发现。

## 使用

直接提出类似请求：

```text
请把桌面的课堂转文字稿整理得通顺一些，保留完整问答和案例细节。
```

也可以明确调用：

```text
使用 $transcript-polisher-zh 将这份逐字稿整理成扩展完整通顺版。
```

## 审计

```bash
python3 scripts/audit_transcript.py 原始稿.docx 修订稿.docx
```

脚本会报告：

- 中文字符保留率
- 段落数
- 标题数量及缺失标题
- 发言角色数量
- 常见重复词和 `【转写存疑】` 标记

字符保留率只用于预警，不能替代人工语义检查。

## 目录

```text
.
├── SKILL.md
├── agents/openai.yaml
├── references/quality-standard.md
└── scripts/audit_transcript.py
```

## License

[MIT](LICENSE)
