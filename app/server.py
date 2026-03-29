from __future__ import annotations

from flask import Flask, jsonify, request

from common.demo_job_runner import list_scenarios, run_demo_scenario


def register_routes(app: Flask) -> None:
    @app.get("/health")
    def health() -> tuple[str, int]:
        return "ok", 200

    @app.get("/demo/scenarios")
    def scenarios():
        return jsonify({"scenarios": list_scenarios()})

    @app.post("/demo/run")
    def run_demo():
        payload = request.get_json(silent=True) or {}
        scenario = payload.get("scenario", "baseline_playback")
        report = run_demo_scenario(scenario)
        return jsonify(report)
