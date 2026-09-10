# Kunka Screenwriting Master

Chinese-first screenwriting skills for Codex and Claude Code. [中文说明](README.md)

Thirteen focused skills help develop premises, structure stories, write scenes and dialogue, revise drafts, check continuity, plan series, adapt material, prepare screenplay text, and write pitches. The package contains instructions and tools; your AI assistant performs the writing.

## Install in Codex

Requires Git and Python 3.9+. No third-party Python packages are needed for installation.

```bash
git clone https://github.com/geslie1/kunka-screenwriting-master.git
cd kunka-screenwriting-master
python3 scripts/install.py --dry-run
python3 scripts/install.py
```

The destination is `$CODEX_HOME/skills`, or `~/.codex/skills` by default. Use the skills on the next turn in clients with dynamic discovery; reopen the conversation if needed.

```text
Use $kunka-screenwriter to develop a ten-minute mystery with two actors and one main location.
Use $kunka-dialogue to revise this dialogue while preserving the final line.
Use $kunka-continuity to check who knows what in these scenes.
```

## Install in Claude Code

```text
/plugin marketplace add geslie1/kunka-screenwriting-master
/plugin install kunka-screenwriting@kunka-screenwriting-master
```

Start with `/kunka-screenwriting:kunka-screenwriter`, or describe the relevant writing task. Skill bodies are written in Chinese; descriptions include English routing terms.

## Design

The entrypoint routes only to relevant skills. Small edits do not require a full project workflow. Creative conventions remain choices rather than mandatory beat counts or page percentages. Ongoing work distinguishes confirmed facts from proposed changes in a compact project record.

Dedicated revision and continuity skills require text evidence and distinguish confirmed contradictions from missing context. Format guidance delivers actual source files and does not claim PDF or FDX export without a real converter.

See the [skill catalog](README.md), [original example](examples/dialogue-workshop.md), and [design review](docs/design-review.md). Reduced instruction size is an engineering result, not a measured improvement in writing quality.

## Updates and validation

```bash
git pull --ff-only
python3 scripts/install.py --update --dry-run
python3 scripts/install.py --update
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Identical installations are skipped. Differing files require `--update`, which saves originals in a timestamped sibling backup directory outside skill discovery. The installer prints its exact location. To restore, move the current selected skill outside the discovery directory, then move the saved directory back. To uninstall, remove only this package's installed `kunka-*` directories.

Normal installation exceptions trigger rollback. Power loss or forced termination may require manual recovery. Check any existing installer lock before removing it. Original `sw-*` installations are not modified.

CI validates packaging and isolated installation. [Behavioral cases](tests/behavioral-cases.md) are manual acceptance scenarios, not an automated model benchmark. No renderer, model runtime, or third-party corpus is bundled.

## Attribution and license

Inspired by [jtydhr88/screenwriting-skills](https://github.com/jtydhr88/screenwriting-skills). This is a newly authored implementation with a different task-oriented module layout, not a relicensing of that project's materials. It excludes its skill bodies, translated excerpts and work-specific analysis tables. See [NOTICE](NOTICE.md).

Newly written code, instructions, templates and examples are released under the [MIT License](LICENSE). Linked third-party works retain their own rights. Contributions should include a concrete use case and validation; do not submit third-party excerpts without redistribution rights.
