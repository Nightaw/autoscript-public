from __future__ import annotations

from flask import Flask, jsonify, request

from common.demo_job_runner import (
    build_markdown_report,
    describe_architecture,
    list_available_devices,
    list_scenarios,
    run_demo_scenario,
)
from common.job_queue import enqueue_job, get_job, list_jobs, process_next_job


def register_routes(app: Flask) -> None:
    @app.get("/health")
    def health() -> tuple[str, int]:
        return "ok", 200

    @app.get("/demo/devices")
    def devices():
        platform = request.args.get("platform")
        role = request.args.get("role")
        return jsonify({"devices": list_available_devices(platform=platform, role=role)})

    @app.get("/demo/scenarios")
    def scenarios():
        return jsonify({"scenarios": list_scenarios()})

    @app.get("/demo/architecture")
    def architecture():
        return jsonify(describe_architecture())

    @app.get("/demo/jobs")
    def jobs():
        return jsonify({"jobs": list_jobs()})

    @app.get("/demo/jobs/<job_id>")
    def job_detail(job_id: str):
        job = get_job(job_id)
        if not job:
            return jsonify({"error": "job not found"}), 404
        return jsonify(job)

    @app.post("/demo/jobs")
    def create_job():
        payload = request.get_json(silent=True) or {}
        scenario = payload.get("scenario", "baseline_playback")
        return jsonify(enqueue_job(scenario)), 201

    @app.post("/demo/jobs/process")
    def process_job():
        job = process_next_job()
        if job is None:
            return jsonify({"error": "no queued jobs"}), 404
        return jsonify(job)

    @app.post("/demo/run")
    def run_demo():
        payload = request.get_json(silent=True) or {}
        scenario = payload.get("scenario", "baseline_playback")
        report = run_demo_scenario(scenario)
        return jsonify(report)

    @app.get("/demo/report.md")
    def markdown_report():
        scenario = request.args.get("scenario", "baseline_playback")
        return build_markdown_report(scenario), 200, {"Content-Type": "text/markdown; charset=utf-8"}
