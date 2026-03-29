# AutoScript Public

[![CI](https://github.com/Nightaw/autoscript-public/actions/workflows/ci.yml/badge.svg)](https://github.com/Nightaw/autoscript-public/actions/workflows/ci.yml)

一个面向 GitHub 展示的公开版仓库，用来呈现“移动端音视频自动化测试框架”的工程化思路，以及其中最适合公开演示的核心分析能力。

## 这是什么

这个仓库不是把原始工作项目整包搬上来，而是把其中最有技术展示价值、且适合公开的部分重构成一个可运行 demo：

- 播放器输出状态卡顿识别
- 多信号超时事件聚类
- 分辨率变化时间线提取
- mock worker 服务与结构化报告输出

仓库中的代码、样例和文档都围绕一个目标展开：让面试官能在很短时间内看懂这个项目解决什么问题、你做了哪些事情、你的实现思路是否靠谱。

## 这个仓库解决什么问题

移动端音视频质量测试真正困难的地方，不是“写一个自动化脚本点点点”，而是把下面这些能力串成一条能复用的链路：

- 真机执行场景
- 录屏与日志采集
- 卡顿与分辨率等指标提取
- 结果结构化输出
- 新业务的快速接入

这个公开版仓库重点展示其中的“结果提取”和“工程化组织”。

## 架构视图

```mermaid
flowchart LR
    A["Scheduler / Client"] --> B["Worker Service"]
    B --> C["Device Discovery"]
    B --> D["Scenario Runner"]
    B --> E["Artifact Collection"]
    E --> F["Log Parsing"]
    E --> G["OCR / Video Post-process"]
    F --> H["Structured Metrics"]
    G --> H
```

## 为什么仓库内容没有原项目那么多

因为公开版的目标不是“文件数量尽量多”，而是“展示你真正的技术能力且不泄漏公司资产”。

原始项目里很多内容不适合直接公开：

- 内网地址和设备清单
- 数据库连接和账号密码
- 强依赖真实环境的业务脚本
- 内部 APK、接口和样本

所以这里保留的是最能证明能力的部分：架构、指标提取思路、可运行 demo、输入输出样例和面试讲法。

## 当前可运行的 Demo

### 1. Output-State Stall Demo

通过 `stopOutput()` / `startOutput()` 配对恢复卡顿区间。

运行：

```bash
python3 tools/parse_demo_log.py samples/logs/demo_player.log
```

结果样例见 [output_stalls.json](./samples/results/output_stalls.json)。

### 2. Timeout Cluster Demo

把视频超时、音频超时、显示 idle、渲染超时等弱信号按时间邻近性聚类，得到“疑似卡顿窗口”。

运行：

```bash
python3 tools/parse_timeout_log.py samples/logs/demo_timeout.log
```

结果样例见 [timeout_clusters.json](./samples/results/timeout_clusters.json)。

### 3. Resolution Timeline Demo

解析解码器日志中的 `raw.size.width/height` 变化，输出规范化分辨率时间线。

运行：

```bash
python3 tools/parse_resolution_log.py samples/logs/demo_resolution.log
```

结果样例见 [resolution_timeline.json](./samples/results/resolution_timeline.json)。

### 4. Run All Demos

```bash
python3 tools/run_demo_suite.py
```

### 5. Mock Worker API Demo

启动本地 worker：

```bash
python3 tools/run_worker_server.py
```

然后触发一次 mock job：

```bash
curl -X POST http://127.0.0.1:7777/demo/run \
  -H "Content-Type: application/json" \
  -d @samples/payloads/baseline_playback.json
```

返回结果样例见 [baseline_playback_report.json](./samples/results/baseline_playback_report.json)。

## 仓库结构

```text
autoscript-public/
├── common/
│   ├── stall_detector.py        # 卡顿识别与聚类
│   ├── resolution_detector.py   # 分辨率时间线提取
│   └── demo_job_runner.py       # mock 场景编排与报告汇总
├── app/
│   ├── __init__.py              # Flask app factory
│   └── server.py                # worker demo API
├── tools/
│   ├── parse_demo_log.py        # 输出状态卡顿解析 CLI
│   ├── parse_timeout_log.py     # 超时聚类解析 CLI
│   ├── parse_resolution_log.py  # 分辨率解析 CLI
│   ├── run_demo_suite.py        # 一次跑完全部样例
│   ├── run_mock_job.py          # 输出结构化 demo report
│   └── run_worker_server.py     # 启动 worker demo 服务
├── samples/
│   ├── logs/                    # 脱敏日志输入
│   ├── payloads/                # mock 请求体
│   └── results/                 # 预期结果输出
├── tests/                       # 单元测试 / API 测试
└── docs/                        # 架构、设计取舍、面试摘要
```

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 tools/run_demo_suite.py
python3 tools/run_mock_job.py
```

## 测试

```bash
python3 -m unittest discover -s tests -v
```

## 面试时可以怎么讲

一句话版本：

> 我做的是一类移动端音视频自动化测试框架。它不只是做真机控制，还会把采集到的日志和视频进一步解析成卡顿、分辨率等质量指标，形成结构化结果。

展开讲时可以重点说三件事：

1. 为什么要做统一 worker 和统一设备抽象
2. 为什么单靠一种信号不够，要做多信号指标融合
3. 为什么公开版仓库保留的是可运行 demo 和设计思路，而不是直接搬运内部脚本

更完整的话术见 [interview-notes.md](./docs/interview-notes.md)。

## 为什么没有上传 APK

APK 通常不是这个项目最有价值的展示物，而且往往涉及分发权限、版权和公司资产边界。对面试更有帮助的，是把你的架构抽象、后处理逻辑、输入输出样例和设计取舍讲清楚。

## 文档

- [项目架构](./docs/architecture.md)
- [设计取舍](./docs/design-decisions.md)
- [Worker API Demo](./docs/worker-api.md)
- [面试摘要](./docs/interview-notes.md)
- [公开范围说明](./docs/public-scope.md)

## 注意事项

- 这不是原始工作仓库。
- 仓库中的示例代码和样例数据均为公开展示用途。
- 如果继续扩展这个仓库，应坚持“脱敏重构优先”而不是“直接搬运原项目文件”。
