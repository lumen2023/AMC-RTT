# Non-Destructive Guard

This folder is an isolated theory, interface, transfer, and evidence artifact.
It does not modify, import, or override existing Drive-JEPA / AC-JEPA code.

本目录是独立的理论、接口、迁移与证据 artifact，不修改、不导入、不覆盖现有
Drive-JEPA / AC-JEPA 代码。

## Write Boundary

Allowed write boundary for this extraction and its follow-up optimization:

本次整理与后续优化允许的写入边界：

```text
AMC-RTT_v1.0/**
```

Disallowed write targets:

禁止写入：

```text
docs/**
navsim_v1/**
navsim_v2/**
scripts/**
tests/**
AMC-Drive/**
existing project configuration files
```

## Runtime Boundary

This toolkit does not:

本 toolkit 不会：

- launch planner training;
- load model checkpoints;
- run optimizer steps;
- alter AC-JEPA or Drive-JEPA parameters;
- register itself as a package;
- modify Python import paths;
- edit `.gitignore`, configs, or existing docs.

## Evidence Boundary / 证据边界

Old positive diagnostics are retained as evidence, but newer audits supersede
their over-broad interpretations. In particular:

旧的正向诊断仍保留为证据，但较新的 audit 会 supersede 其过宽解释：

- A14 rich-support interpretation is superseded by A15-A17.
- Teacher-side target variables cannot be counted as frozen AC-JEPA support.
- A18-A20 authorize objective design and read-only preflight only, not full
  planner training.
- The new theory files must label conditional results and hypotheses explicitly;
  no theorem may be upgraded into an empirical or universal claim silently.
- 新增理论文件必须明确标记 conditional result 与 hypothesis；任何定理都不能
  被静默升级成经验结论或 universal claim。

## Verification Checklist / 验证清单

After any edit to this folder, verify:

每次编辑本目录后执行：

```text
find AMC-RTT_v1.0 -type f | sort
git status --short -- AMC-RTT_v1.0
python - <<'PY'
import ast
from pathlib import Path
for path in Path("AMC-RTT_v1.0").rglob("*.py"):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
print("AST_OK")
PY
find AMC-RTT_v1.0 -type f \( -name '*.pyc' -o -path '*/__pycache__/*' \)
```

The expected project impact is only new or modified files under
`AMC-RTT_v1.0/`; no other path may appear in the task's diff.

预期影响只能是 `AMC-RTT_v1.0/` 下的新文件或修改；任务 diff 中不应出现其他
路径。
