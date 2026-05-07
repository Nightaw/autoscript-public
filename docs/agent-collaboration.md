# Agent Collaboration

最近一轮重构把项目从“单仓库脚本集合”进一步拆成了更适合 agent 开发的协作方式。公开版用一个可运行 trace 展示这条链路：

```text
manualscript -> clawscript -> autoscript -> autoscript-public
```

这不是把内部仓库原样搬出来，而是保留协作边界、任务契约、运行时抽象和结果样例。

## 三个仓库各自负责什么

| Repo | 角色 | 对下游交付 |
| --- | --- | --- |
| `manualscript` | 配置驱动的场景源头，沉淀 app profile、设备约束、场景参数和质量预期 | 任务参数、场景名、时长、滑动间隔、指标口径 |
| `clawscript` | agent/SOP 层，把自然语言任务转成可执行步骤和安全护栏 | SOP、agent task spec、debug artifact 约定 |
| `autoscript` | worker、parser、metric、report 层，负责执行和结构化输出 | JSON result、Markdown report、parser summary |

`autoscript-public` 负责把这条链路做成脱敏后的展示版本，方便直接运行和阅读。

## Agent 化以后解决了什么

旧的自动化脚本更像“固定动作序列”。agent 化以后，核心变化是把运行过程拆成可替换策略：

- `AgentContext` 保存设备、应用、任务、调试产物和运行状态。
- `PopupHandler` 处理弹窗和权限类干扰。
- `PlayEntryHandler` 负责从 App 首页进入播放状态。
- `PlayValidator` 判断是否真的进入有效播放。
- `ContentClassifier` 判断内容类型和当前页面状态。
- `Swiper` 执行滑动节奏。
- `StallDetector` 收集卡顿证据。

这样不同 App 的差异主要落在策略层，worker、parser 和 report 层不需要跟着重写。

## 一条公开 trace

示例任务 `8088` 的自然语言输入可以概括为：

> 打开一个短视频 App，进入播放状态，每 5 秒滑动一次，观看 60 秒，检测卡顿并输出结构化结果。

公开版把它转成下面这个任务契约：

```json
{
  "task_id": "8088",
  "device_id": "demo-android-01",
  "app": "ShortVideoDemo",
  "scenario": "short_video.agent_stall.basic",
  "watch_duration_sec": 60,
  "swipe_interval_sec": 5,
  "output_path": "samples/results/agent_short_video_report.json"
}
```

## 怎么运行

```bash
python3 tools/show_agent_collaboration.py --format json
python3 tools/show_agent_collaboration.py --format markdown
```

启动 Flask demo 后也可以访问：

```bash
curl http://127.0.0.1:7777/demo/agent-collaboration
curl http://127.0.0.1:7777/demo/agent-collaboration.md
```

## 公开版保留和移除的边界

保留：

- 仓库职责分工
- agent 任务契约
- runner/strategy/parser/report 的分层边界
- 可运行 CLI 和 API
- JSON / Markdown 样例产物

移除：

- 内部 App 标识
- 真实设备清单
- 私有 SOP 内容
- 二进制产物
- 公司内部接口和路径

这也是后续把 `clawscript` 单独公开时的衔接点：`clawscript` 负责展示 agent/SOP 生成和执行方式，`autoscript-public` 负责展示结果如何进入 worker、parser 和报告链路。
