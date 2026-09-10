# 昆卡编剧大师

**Kunka Screenwriting Master** — 面向 Codex 与 Claude Code 的中文编剧技能包。

[English](README_EN.md) · [使用示例](examples/dialogue-workshop.md) · [安装管理](docs/installation.md) · [MIT License](LICENSE)

**从一个点子，到一份完整剧本。**

昆卡编剧大师通过 13 个专用技能，帮助你构思故事、塑造人物、编写场景、润色对白和修改初稿。适用于短片、短剧、长片与连续剧，在 Codex 或 Claude Code 中直接用自然语言开始创作。

## 你可以用它做什么

| 你手里的材料 | 可以交给昆卡的任务 | 得到什么 |
| --- | --- | --- |
| 一句话、一个画面、一个人物 | 发展核心冲突，探索故事方向 | 一句话故事与创作方案 |
| 已经选定的故事方向 | 设计结构、人物关系和场景 | 大纲、人物表与剧本初稿 |
| 一段不满意的戏 | 调整动作、对白和潜台词 | 可直接替换的场景 |
| 一份完整初稿 | 检查动机、因果、时间线和信息冲突 | 有具体位置的改稿意见与修订 |
| 一部准备继续开发的剧集 | 安排本集故事与跨集变化 | 分集大纲与项目记录 |

可以按阶段开发，也可以直接要求写正文。你的题材、人物设定、结局和篇幅要求会作为本次创作的依据。

## 开始使用

### Codex

需要 Git 和 Python 3.9+，运行安装不需要第三方 Python 包：

```bash
git clone https://github.com/geslie1/kunka-screenwriting-master.git
cd kunka-screenwriting-master
python3 scripts/install.py --dry-run
python3 scripts/install.py
```

默认安装到 `$CODEX_HOME/skills`；未设置 `CODEX_HOME` 时使用 `~/.codex/skills`。安装后在支持技能动态发现的 Codex 中从下一轮对话使用；若客户端尚未刷新，重新打开会话。

```text
使用 $kunka-screenwriter，帮我开发一个十分钟悬疑短片。
要求两个演员、一个主要场景，先给两个故事方向。
```

单个任务可直接指定专用技能：

```text
使用 $kunka-dialogue，润色下面的对白，保留最后一句和人物关系。
使用 $kunka-continuity，检查这份剧本的时间线和人物知情是否冲突。
使用 $kunka-revision，直接修改这份初稿中最影响因果的三处问题。
```

### Claude Code

在 Claude Code 内执行：

```text
/plugin marketplace add geslie1/kunka-screenwriting-master
/plugin install kunka-screenwriting@kunka-screenwriting-master
```

安装后可直接描述编剧任务，或调用 `/kunka-screenwriting:kunka-screenwriter`。

## 试着这样说

**从零写短片**

```text
使用昆卡编剧大师，写一个约十分钟的现实悬疑短片。
三个主要人物，故事发生在一间深夜营业的便利店。
结尾要有反转，但前面要留下能回看的线索。直接给完整初稿。
```

**修改已有剧本**

```text
使用 $kunka-revision，检查下面的初稿。
保留人物关系与结局，优先修复动机和因果问题，再调整对白。
请给出修改后的正文，并简要说明改动。
```

**继续上次的项目**

```text
使用 $kunka-screenwriter，读取这个项目的 story-bible.md。
沿用已确认设定，继续写第三场，不重新讨论结局。
```

想先看具体效果，可以阅读 [对白修改示例：搬琴](examples/dialogue-workshop.md)。

## 13 个技能

| 技能 | 使用时机 | 典型结果 |
| --- | --- | --- |
| `kunka-screenwriter` | 新项目、续写、不知道下一步 | 当前阶段的成果与项目状态 |
| `kunka-premise` | 点子与主题开发 | 故事方向、一句话故事 |
| `kunka-structure` | 大纲、转折与节奏 | 因果链与结构修订 |
| `kunka-character` | 人物动机和关系 | 可表演的选择与人物差异 |
| `kunka-scene` | 写或改一场戏 | 场景正文 |
| `kunka-dialogue` | 台词与潜台词 | 可直接替换的对白 |
| `kunka-revision` | 综合审读与改稿 | 有证据的问题及修改 |
| `kunka-continuity` | 时间、道具、知情核对 | 确定冲突与待核实事项 |
| `kunka-series` | 短剧、连续剧与单元剧 | 分集表、季线与角色变化 |
| `kunka-adaptation` | 小说、舞台文本或事件改编 | 视角与媒介转换方案 |
| `kunka-format` | 中文剧本或 Fountain | 源文件及格式检查 |
| `kunka-pitch` | 项目介绍与提案 | 简介、梗概、推介稿 |
| `kunka-style-lab` | 探索不同叙事方式 | 同一情境的原创版本比较 |

持续项目可使用 [story-bible 模板](plugins/kunka-screenwriting/skills/kunka-screenwriter/assets/story-bible.md) 保存已确认设定、暂定方案和下一步。单次润色不要求建立项目档案。

## 创作方式

- **按任务使用技能**：构思、大纲、对白、改稿各有入口，也可由总入口选择当前需要的方法。
- **适配作品形式**：短片、群像、观察式叙事和开放结局都可按你的意图展开。
- **保留创作决定**：将已确认设定与暂定方案分开记录，方便后续接着写。
- **用文本证据改稿**：指出问题的位置和影响，区分明确矛盾、缺少前情与风格建议。
- **交付可编辑文本**：支持中文场号剧本与 Fountain 源文件，方便继续修改或排版。

## 更新

```bash
git pull --ff-only
python3 scripts/install.py --update --dry-run
python3 scripts/install.py --update
```

相同内容会跳过，更新前会备份已有文件。指定目录、单项安装、恢复和卸载方式见 [安装管理](docs/installation.md)。

## 常见问题

**需要单独配置 API Key 吗？**

技能包本身不需要。它使用 Codex 或 Claude Code 已配置的模型服务，使用费用与额度遵循对应客户端。

**可以只改一段对白吗？**

可以。直接说明要改的段落和需要保留的内容，或调用 `kunka-dialogue`。

**能导出 PDF 吗？**

可以先生成中文剧本或 Fountain 源文件。PDF、FDX 导出需要当前环境另有可用的转换工具；本包不内置渲染器。

**能自动记住长篇设定吗？**

持续项目通过 `story-bible.md` 保存设定和进度，下次读取后继续。它是可编辑的项目记录，仍需随正文变化维护。

## 开发与验证

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

GitHub Actions 检查技能元数据、内部链接、插件路径与安装行为。维护约定见 [设计与维护](docs/design-review.md)。

[行为验收案例](tests/behavioral-cases.md) 供实际客户端复测。自动校验检查工程完整性；剧本效果需要结合具体稿件评估。

## 许可与贡献

本仓库的技能、模板、示例与代码采用 [MIT](LICENSE) 许可，可使用、修改和再分发。

欢迎通过 Issue 或 Pull Request 分享具体创作场景、问题和改进建议。提交示例请使用原创或具有再分发授权的材料。
