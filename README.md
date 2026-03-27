# AutoScript Public Demo

一个面向 GitHub 展示的公开版仓库，用来呈现“移动端音视频自动化测试框架”的工程化思路，而不是原始内部项目的完整拷贝。

## 项目简介

这个仓库展示了一套典型的移动端音视频自动化测试框架会如何组织：

- 统一的 worker 服务入口
- Android / iOS 设备控制抽象
- 场景化脚本组织方式
- 日志解析与质量指标提取
- OCR / 视频后处理补充链路

公开版保留架构思路、目录设计和 demo 代码，移除了内网地址、账号密码、真实业务脚本和生产环境配置。

## 适合怎么讲

可以把它描述为：

> 一个用于移动端音视频质量验证的自动化测试框架。系统通过 worker 接口接收任务，驱动 Android/iOS 真机执行播放类场景，采集录屏和日志，并在后处理阶段提取卡顿、分辨率等质量指标。

## 亮点

- 把零散自动化脚本沉淀成统一框架
- 跨 Android / iOS 的设备控制抽象
- 日志解析与视觉识别双通路
- 面向多业务形态的脚本组织方式
- 适合扩展到长视频、短视频、直播等多类场景

## 仓库结构

```text
autoscript-public/
├── docs/                    # 架构说明、公开范围、面试摘要
├── common/                  # 通用 demo 代码
├── tools/                   # 本地演示工具
├── samples/                 # 脱敏后的示例数据
├── requirements.txt         # Python 依赖
└── .gitignore
```

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tools/parse_demo_log.py samples/logs/demo_player.log
```

## Demo 能力

当前 demo 提供一个从零实现的日志卡顿解析示例：

- 输入：播放器日志
- 规则：匹配 `stopOutput()` 与 `startOutput()` 成对事件
- 输出：卡顿区间列表与统计结果

这部分代码是为公开展示重新编写的通用示例，不依赖内部服务。

## 文档

- [项目架构](./docs/architecture.md)
- [面试摘要](./docs/interview-notes.md)
- [公开范围说明](./docs/public-scope.md)

## 注意事项

- 这不是原始工作仓库。
- 仓库中的示例数据和代码均为公开展示用途。
- 如果要进一步对外发布，应继续保持脱敏与重构原则，避免带入任何公司资产。
