# Kunka Screenwriting Master

Chinese-first screenwriting skills for Codex and Claude Code.

[中文](README.md) · [Example](examples/dialogue-workshop.md) · [Installation guide](docs/installation.md) · [MIT License](LICENSE)

**From a story idea to a complete screenplay.**

Thirteen focused skills help develop premises, shape characters, write scenes and dialogue, revise drafts, and plan series. Describe your project in natural language and work with the model configured in your AI client.

## What you can create

| Starting point | Task | Output |
| --- | --- | --- |
| An idea, image, or character | Explore the central conflict | Story options and a logline |
| A chosen premise | Develop structure and relationships | Outline, characters, and a draft |
| A scene that needs work | Revise actions and dialogue | Replacement scene text |
| A complete draft | Check motivation, causality, and continuity | Located findings and revisions |
| An ongoing series | Connect episode stories and character changes | Episode outlines and project notes |

Develop your project in stages or ask for a complete draft directly. Specify the format, length, relationships, and ending you want to preserve.

## Install in Codex

Requires Git and Python 3.9+. Installation uses the Python standard library.

```bash
git clone https://github.com/geslie1/kunka-screenwriting-master.git
cd kunka-screenwriting-master
python3 scripts/install.py --dry-run
python3 scripts/install.py
```

The destination is `$CODEX_HOME/skills`, or `~/.codex/skills` by default. Use the skills on the next turn in clients with dynamic discovery; reopen the conversation if needed.

## Install in Claude Code

```text
/plugin marketplace add geslie1/kunka-screenwriting-master
/plugin install kunka-screenwriting@kunka-screenwriting-master
```

Start with `/kunka-screenwriting:kunka-screenwriter`, or describe a writing task. Skill bodies are written in Chinese; descriptions include English routing terms.

## Try these prompts

**Write a short film**

```text
Use $kunka-screenwriter to write a ten-minute mystery set in a late-night convenience store.
Use three main characters. Plant clues for the final twist. Deliver a complete first draft.
```

**Revise an existing draft**

```text
Use $kunka-revision to revise this screenplay.
Preserve the relationships and ending. Fix motivation and causality before polishing dialogue.
Provide the revised text and a short explanation of the changes.
```

**Resume a project**

```text
Use $kunka-screenwriter to read this project's story-bible.md and continue scene three.
Keep the confirmed setting and ending.
```

For a concrete example, read the [dialogue workshop](examples/dialogue-workshop.md).

## Skill catalog

| Skill | Focus |
| --- | --- |
| `kunka-screenwriter` | Start or resume a project and select the next task |
| `kunka-premise` | Premises, themes, and loglines |
| `kunka-structure` | Outlines, causality, and narrative order |
| `kunka-character` | Motivation, relationships, and character choices |
| `kunka-scene` | Scene writing, action, and pacing |
| `kunka-dialogue` | Dialogue, subtext, and distinct voices |
| `kunka-revision` | Evidence-based review and revision |
| `kunka-continuity` | Timelines, props, and character knowledge |
| `kunka-series` | Episode plans and continuing arcs |
| `kunka-adaptation` | Adaptation choices and changes of medium |
| `kunka-format` | Chinese screenplay text and Fountain |
| `kunka-pitch` | Loglines, synopses, and project pitches |
| `kunka-style-lab` | Compare narrative approaches using original scenes |

## How it works

- Load the skills relevant to the current task.
- Adapt the approach to the author's chosen form and constraints.
- Keep confirmed decisions separate from proposed changes.
- Locate revision findings in the actual text.
- Deliver editable screenplay text for continued writing and formatting.

For ongoing projects, the [story-bible template](plugins/kunka-screenwriting/skills/kunka-screenwriter/assets/story-bible.md) records decisions, draft locations, and the next step.

## Update

```bash
git pull --ff-only
python3 scripts/install.py --update --dry-run
python3 scripts/install.py --update
```

Identical files are skipped; updates back up differing installed skills. See the [installation guide](docs/installation.md) for custom destinations, selective installation, restoration, and removal.

## FAQ

**Does the package need an API key?** It uses your client's configured model service. The package requires no separate API key; usage costs and limits depend on the client.

**Can I revise just one passage?** Yes. Specify the passage and what must stay unchanged, or use `kunka-dialogue` directly.

**Can it export PDF?** The skills prepare screenplay text or Fountain source. PDF and FDX output require a real converter in your environment; no renderer is bundled.

**How does project memory work?** The assistant reads and updates a local `story-bible.md`. This editable record needs to stay consistent with the screenplay.

## Development

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

CI checks metadata, links, packaging, and installation behavior. See [design and maintenance](docs/design-review.md) and the [manual behavioral cases](tests/behavioral-cases.md). Writing quality should be evaluated against actual drafts.

## License and contributions

The skills, templates, examples, and code are available under the [MIT License](LICENSE).

Issues and pull requests are welcome. Include a concrete writing task, observed behavior, and expected result. Contribute examples you wrote or have permission to redistribute.
