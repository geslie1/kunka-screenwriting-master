# 昆卡编剧大师

**Kunka Screenwriting Master** — 面向 Codex 与 Claude Code 的中文编剧技能包。

[English](README_EN.md) · [优化说明](docs/design-review.md) · [使用示例](examples/dialogue-workshop.md) · [MIT License](LICENSE)

把一个点子推进成故事，把已有剧本改得更准确。13 个按需加载的技能覆盖构思、人物、结构、场景、对白、改稿和交付。这里提供的是 AI 工作指令、模板和安装工具；实际创作由你使用的 AI 助手完成。

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

安装后可直接描述编剧任务，或调用 `/kunka-screenwriting:kunka-screenwriter`。插件打包结构遵循 [Claude Code 插件文档](https://code.claude.com/docs/en/plugins-reference)。

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

## 与原项目的关系

本项目受 [jtydhr88/screenwriting-skills](https://github.com/jtydhr88/screenwriting-skills) 启发，在审视其工作方式后重新编写技能指令、示例和工程工具。原项目以编剧书籍与作品研究为主；昆卡版聚焦可执行的创作和改稿任务。

原仓库未提供标准开源许可证，并注明个人学习用途。本仓库不收录它的书籍摘录、译文、逐场案例表或原技能正文，也不为那些材料重新授权。原项目与作者的贡献在 [来源说明](NOTICE.md) 中保留。

主要改进：简短触发描述、按需路由、尊重创作形式、独立改稿与连续性检查、可恢复升级、自动校验。详细取舍及验证边界见 [优化说明](docs/design-review.md)。压缩文件大小不等同于已经证明创作质量提升。

## 安装管理

```bash
# 只安装总入口；完整配套能力建议使用默认的全量安装
python3 scripts/install.py --skill kunka-screenwriter

# 指定技能目录
python3 scripts/install.py --dest /path/to/skills

# 获取新版，然后备份并更新不同的文件
git pull --ff-only
python3 scripts/install.py --update --dry-run
python3 scripts/install.py --update
```

重复安装相同内容会跳过；不同内容默认报错，避免覆盖自己的修改。`--update` 会将原技能目录保存到目标技能目录旁的 `skills-kunka-backups/<时间-随机标识>/`（实际前缀随 `--dest` 目录名变化），路径会打印出来。升级时只替换选中的 `kunka-*` 技能，不删除原有 `sw-*` 技能。

恢复旧版：停止安装程序，将要替换的当前技能目录先移到技能发现目录之外，再将输出备份中的同名目录移回目标位置。卸载时只移走本项目对应的 `kunka-*` 目录。备份、稿件和原项目技能可独立保留。

安装器在正常异常处理中回滚本次已移动文件；突然断电或强制终止不保证自动恢复。遇到安装锁时先确认没有安装进程，再处理遗留锁和备份，避免并发改写。

## 开发与验证

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

校验覆盖技能名称、精简前言格式、UI 元数据、内部链接与插件路径。安装测试覆盖重复安装、冲突、备份、失败回滚、符号链接与安装锁。GitHub Actions 执行同样检查及隔离安装。

[行为验收案例](tests/behavioral-cases.md) 用于在目标 AI 客户端复测；自动检查无法证明所有模型都遵守技能，也不替代对剧本质量的人工判断。PDF/FDX 需要用户环境中真实可用的转换工具，本包不内置渲染器。

## 许可与贡献

新编写的技能、模板、示例与代码采用 [MIT](LICENSE) 许可，可使用、修改和再分发。第三方名称与被链接材料不因本许可证改变权利归属。

欢迎提交带具体输入、实际表现和期望结果的 Issue。改动请附适用场景与验证结果；不接受没有再分发依据的书籍摘录或第三方剧本大段文本。
