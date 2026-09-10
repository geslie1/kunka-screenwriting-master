# 安装管理

[返回首页](../README.md)

以下命令适用于从仓库安装到 Codex 的本地 Python 安装器。Claude Code 插件安装方式见首页。

## 安装位置

默认目标为 `$CODEX_HOME/skills`；未设置 `CODEX_HOME` 时使用 `~/.codex/skills`。需要 Python 3.9+，不依赖第三方 Python 包。

```bash
# 先查看计划，不写入文件
python3 scripts/install.py --dry-run

# 安装全部 13 个技能
python3 scripts/install.py

# 指定目标技能目录
python3 scripts/install.py --dest /path/to/skills

# 仅安装所需技能，--skill 可以重复指定
python3 scripts/install.py --skill kunka-screenwriter --skill kunka-dialogue
```

完整配套能力建议全量安装。相同内容重复安装会跳过；发现不同内容时默认报错，防止覆盖本地修改。安装器只处理选中的 `kunka-*` 技能。

## 更新与备份

```bash
git pull --ff-only
python3 scripts/install.py --update --dry-run
python3 scripts/install.py --update
```

`--update` 会先备份有差异的已安装目录，再替换对应技能。备份保存在目标技能目录旁：

```text
skills/
skills-kunka-backups/
  <时间-随机标识>/
    kunka-dialogue/
```

目录前缀随 `--dest` 的末级目录名变化，安装器会打印实际路径。备份放在技能发现目录之外，避免客户端同时加载旧版。使用自定义目标时，更新命令也要带上相同的 `--dest`。

## 恢复与卸载

恢复前停止安装程序，将需要替换的当前技能目录移到技能发现目录之外，再将备份中的同名目录移回原安装位置。保留当前版本副本，便于必要时撤销恢复。

卸载时只移走本项目安装的对应 `kunka-*` 目录。创作项目的剧本和 `story-bible.md` 独立保存在用户项目中。

## 常见安装问题

| 提示 | 处理方式 |
| --- | --- |
| Existing files differ | 先查看本地修改；需要升级时使用 `--update` 保留备份 |
| Another install may be active | 先确认是否有正在运行的安装程序；仅在确认退出后处理遗留锁 |
| Unknown skill | 对照首页技能目录检查名称 |
| Symbolic links are not supported | 使用常规目录作为技能源与对应安装目标 |

安装器在一般异常处理中恢复本次已经移动的文件。突然断电或强制终止可能留下安装锁、临时目录或备份，需要根据打印的路径核对后恢复。
