# Worker API Demo

这个公开版仓库额外提供了一层 mock worker 服务，用来展示“分析能力如何挂到服务接口上”，而不是只停留在离线脚本层。

## 启动

```bash
python3 tools/run_worker_server.py
```

默认监听：

- `http://127.0.0.1:7777`

## 接口

### `GET /health`

用于健康检查。

返回：

```text
ok
```

### `GET /demo/scenarios`

返回当前可运行的 demo 场景列表。

### `POST /demo/run`

触发一次 mock job，返回结构化质量报告。

示例请求体：

```json
{
  "scenario": "baseline_playback"
}
```

示例返回见 [baseline_playback_report.json](../samples/results/baseline_playback_report.json)。

## 为什么这层有价值

因为真实项目通常不是“人工执行一个脚本然后看 stdout”，而是：

- 上层调度系统下发任务
- worker 节点执行场景
- worker 节点返回结构化结果

即使公开版不能带出真实调度系统，也应该把这种接口形态展示出来。
