# 项目架构

## 1. 目标

这个公开版仓库重点展示一类自动化测试框架的工程结构，而不是复刻原有生产项目。

这类项目通常要解决四件事：

1. 任务如何进入执行节点
2. 设备如何被统一控制
3. 场景脚本如何复用和扩展
4. 结果如何从日志/视频中提取出来

## 2. 参考架构

```text
Scheduler / Client
        |
        v
Worker Service
        |
        +--> Device Discovery
        +--> Health Check
        +--> Scenario Runner
        +--> Screen Recording
        +--> Log Collection
        +--> Post Processing
        +--> Structured Result Output
```

## 3. 典型模块划分

### Worker Service

负责接收任务、启动场景、维护执行状态，并暴露健康检查和结果回传接口。

### Device Abstraction

屏蔽 Android / iOS 差异，把设备连接、应用启动、录屏、手势操作等能力收敛到公共层。

### Scenario Scripts

按业务形态拆分脚本，例如：

- video
- short_video
- live
- meeting_video

这样新场景接入时只需要在统一约定下补充适配逻辑。

### Post Processing

质量指标提取通常有两条链路：

- 日志解析：速度快，适合提取播放器状态变化
- OCR / 视频抽帧：适合补充日志盲区

## 4. 为什么这种结构适合放在简历里

因为它体现的不是“我写过几个自动化脚本”，而是：

- 我把执行入口、设备控制、场景组织和结果分析做成了框架
- 我考虑了扩展性，而不是只满足单一场景
- 我关注真实执行环境中的工程问题，比如设备状态、时间同步、结果回传
