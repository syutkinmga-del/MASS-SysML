#!/usr/bin/env python3
"""Check SysML sources by sending them to isolated Jupyter kernel sessions."""

from __future__ import annotations

import argparse
import hashlib
import json
import queue
import re
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

try:
    from jupyter_client import KernelManager
except ImportError as exc:
    print(
        "ERROR: jupyter_client is required. Install it in the selected Python "
        "environment before running this check.",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODELS = (
    REPOSITORY_ROOT / "MASSKernel_v1.0.sysml",
    REPOSITORY_ROOT / "MASSKernel_v1.0_candidate.sysml",
)
DIAGNOSTIC_PATTERNS = (
    re.compile(r"\bERROR:\s*no viable alternative\b", re.IGNORECASE),
    re.compile(r"\bsyntax\s+error\b", re.IGNORECASE),
    re.compile(r"\bparse\s+error\b", re.IGNORECASE),
    re.compile(r"\b(?:could not|cannot|can't|failed to)\s+resolve\b", re.IGNORECASE),
    re.compile(r"\bunresolved\s+(?:reference|symbol|name|feature)\b", re.IGNORECASE),
    re.compile(r"\b(?:unknown|undefined|unrecognized)\s+(?:symbol|name|feature|element|input)\b", re.IGNORECASE),
    re.compile(r"\bunexpected\s+(?:token|input|character|end|eof)\b", re.IGNORECASE),
    re.compile(r"\b(?:missing|required)\s+(?:reference|element|feature|argument)\b", re.IGNORECASE),
    re.compile(r"\b(?:linking|resolution)\s+error\b", re.IGNORECASE),
    re.compile(r"\b(?:error|exception|fatal)\s*:", re.IGNORECASE),
)
PACKAGE_RESULT = re.compile(r"^Package\s+([^\s(]+)\s+\([^)]+\)\s*$")
LOG4J_WARNING = re.compile(r"log4j:WARN\b")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run a smoke probe and validate each SysML file in a fresh Jupyter "
            "kernel session."
        )
    )
    parser.add_argument(
        "--kernel",
        default="sysml",
        help="Jupyter kernelspec name (default: sysml)",
    )
    parser.add_argument(
        "--startup-timeout",
        type=float,
        default=120,
        help="Maximum seconds to wait for each kernel to become ready (default: 120)",
    )
    parser.add_argument(
        "--execution-timeout",
        type=float,
        default=300,
        help="Maximum seconds to wait for IOPub idle (default: 300)",
    )
    parser.add_argument(
        "--reply-timeout",
        type=float,
        default=30,
        help="Maximum seconds to wait for execute_reply after idle (default: 30)",
    )
    parser.add_argument(
        "models",
        nargs="*",
        type=Path,
        help=(
            "SysML source files to check; by default checks "
            "MASSKernel_v1.0.sysml and MASSKernel_v1.0_candidate.sysml"
        ),
    )
    args = parser.parse_args()
    if min(args.startup_timeout, args.execution_timeout, args.reply_timeout) <= 0:
        parser.error("timeouts must be greater than zero")
    args.models = args.models or list(DEFAULT_MODELS)
    return args


def message_text(content: dict[str, Any]) -> str:
    pieces: list[str] = []
    text = content.get("text")
    if isinstance(text, str):
        pieces.append(text)
    data = content.get("data")
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, str):
                pieces.append(value)
    if content.get("ename") or content.get("evalue"):
        pieces.append(f"{content.get('ename', '')}: {content.get('evalue', '')}")
    traceback = content.get("traceback")
    if isinstance(traceback, list):
        pieces.extend(str(line) for line in traceback)
    return "\n".join(pieces)


def classify_output(
    expected_package: str,
    reply: dict[str, Any] | None,
    idle_seen: bool,
    messages: list[dict[str, Any]],
) -> tuple[str, str]:
    if not idle_seen:
        return "INDETERMINATE", "IOPub idle was not received before the timeout"
    if reply is None:
        return "INDETERMINATE", "execute_reply was not received before the timeout"
    if reply.get("status") != "ok":
        return "FAIL", f"execute_reply status is {reply.get('status')!r}"

    errors = [message for message in messages if message["msg_type"] == "error"]
    if errors:
        return "FAIL", "one or more IOPub error messages were received"

    output = "\n".join(message["text"] for message in messages)
    for pattern in DIAGNOSTIC_PATTERNS:
        match = pattern.search(output)
        if match:
            classification = (
                "FAIL"
                if match.group(0).lower().startswith("error:")
                else "INDETERMINATE"
            )
            return (
                classification,
                f"diagnostic-like text was emitted: {match.group(0)!r}",
            )

    package_results: list[str] = []
    for message in messages:
        if message["msg_type"] not in ("execute_result", "display_data"):
            continue
        for line in message["text"].splitlines():
            match = PACKAGE_RESULT.fullmatch(line.strip())
            if match:
                package_results.append(match.group(1))

    if expected_package not in package_results:
        return (
            "INDETERMINATE",
            "expected package result "
            f"'Package {expected_package} (<UUID>)' was not received",
        )
    return (
        "PASS",
        "execute_reply status=ok, IOPub idle received, no IOPub errors or "
        "diagnostic text, expected Package result received",
    )


def read_log(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def run_probe(
    label: str,
    source: str,
    expected_package: str,
    kernel_name: str,
    startup_timeout: float,
    execution_timeout: float,
    reply_timeout: float,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "label": label,
        "kernel": kernel_name,
        "started": False,
        "idle": False,
        "reply": None,
        "messages": [],
        "classification": "INDETERMINATE",
        "detail": "probe did not complete",
        "exception": None,
        "shutdown": False,
        "log4j_warnings": [],
    }
    manager = KernelManager(kernel_name=kernel_name)
    client = None

    with tempfile.TemporaryDirectory(prefix="sysml-pilot-") as temp_dir:
        stdout_path = Path(temp_dir) / "kernel.stdout.log"
        stderr_path = Path(temp_dir) / "kernel.stderr.log"
        try:
            with stdout_path.open("w", encoding="utf-8") as stdout_log, stderr_path.open(
                "w", encoding="utf-8"
            ) as stderr_log:
                manager.start_kernel(
                    cwd=str(REPOSITORY_ROOT),
                    stdout=stdout_log,
                    stderr=stderr_log,
                )
                result["started"] = True
                client = manager.client()
                client.start_channels()
                client.wait_for_ready(timeout=startup_timeout)

                request_id = client.execute(
                    source,
                    store_history=False,
                    stop_on_error=True,
                )
                execution_deadline = time.monotonic() + execution_timeout
                while time.monotonic() < execution_deadline:
                    remaining = execution_deadline - time.monotonic()
                    try:
                        message = client.get_iopub_msg(timeout=min(1.0, remaining))
                    except (queue.Empty, TimeoutError):
                        continue

                    if message.get("parent_header", {}).get("msg_id") != request_id:
                        continue

                    message_type = message.get("msg_type", "")
                    content = message.get("content", {})
                    if message_type in {
                        "stream",
                        "display_data",
                        "execute_result",
                        "error",
                    }:
                        result["messages"].append(
                            {
                                "msg_type": message_type,
                                "text": message_text(content),
                            }
                        )
                    elif (
                        message_type == "status"
                        and content.get("execution_state") == "idle"
                    ):
                        result["idle"] = True
                        break

                if result["idle"]:
                    reply_deadline = time.monotonic() + reply_timeout
                    while time.monotonic() < reply_deadline:
                        remaining = reply_deadline - time.monotonic()
                        try:
                            message = client.get_shell_msg(
                                timeout=min(1.0, remaining)
                            )
                        except (queue.Empty, TimeoutError):
                            continue
                        if (
                            message.get("parent_header", {}).get("msg_id")
                            == request_id
                        ):
                            result["reply"] = message.get("content", {})
                            break
        except Exception as exc:
            result["exception"] = f"{type(exc).__name__}: {exc}"
        finally:
            if client is not None:
                try:
                    client.stop_channels()
                except Exception as exc:
                    result["exception"] = (
                        f"{result['exception']}; " if result["exception"] else ""
                    ) + f"stopping channels failed: {type(exc).__name__}: {exc}"
            try:
                manager.shutdown_kernel(now=True)
                result["shutdown"] = not manager.is_alive()
            except Exception as exc:
                result["exception"] = (
                    f"{result['exception']}; " if result["exception"] else ""
                ) + f"kernel shutdown failed: {type(exc).__name__}: {exc}"

        process_logs = "\n".join(
            part for part in (read_log(stdout_path), read_log(stderr_path)) if part
        )
        result["log4j_warnings"] = [
            line for line in process_logs.splitlines() if LOG4J_WARNING.search(line)
        ]

    classification, detail = classify_output(
        expected_package,
        result["reply"],
        result["idle"],
        result["messages"],
    )
    result["classification"] = classification
    result["detail"] = detail
    if result["exception"]:
        result["classification"] = "FAIL"
        result["detail"] = result["exception"]
    elif not result["shutdown"]:
        result["classification"] = "FAIL"
        result["detail"] = "kernel shutdown could not be confirmed"
    return result


def print_probe(result: dict[str, Any]) -> None:
    print(f"\n=== {result['label']} ===")
    print(f"kernel: {result['kernel']}")
    print(f"kernel_started: {result['started']}")
    print(f"iopub_idle_received: {result['idle']}")
    print(f"execute_reply: {json.dumps(result['reply'], ensure_ascii=False)}")
    print(f"kernel_shutdown_confirmed: {result['shutdown']}")
    print(f"result: {result['classification']}")
    print(f"diagnostics: {result['detail']}")

    counts = {
        message_type: sum(
            message["msg_type"] == message_type for message in result["messages"]
        )
        for message_type in ("stream", "display_data", "execute_result", "error")
    }
    print(
        "iopub_counts: "
        + ", ".join(f"{message_type}={count}" for message_type, count in counts.items())
    )
    for message in result["messages"]:
        text = message["text"].rstrip()
        if text:
            print(f"iopub_{message['msg_type']}: {text}")

    if result["log4j_warnings"]:
        print("kernel_startup_warnings (separate from model diagnostics):")
        for warning in result["log4j_warnings"]:
            print(f"  {warning}")


def main() -> int:
    args = parse_args()
    failed = False

    smoke = run_probe(
        label="smoke",
        source="package PilotSmokeTest { part def Vessel; }",
        expected_package="PilotSmokeTest",
        kernel_name=args.kernel,
        startup_timeout=args.startup_timeout,
        execution_timeout=args.execution_timeout,
        reply_timeout=args.reply_timeout,
    )
    print_probe(smoke)
    if smoke["classification"] != "PASS":
        print("\nModel checks skipped because the smoke probe did not pass.")
        return 1

    for model_path in args.models:
        path = model_path.expanduser()
        if not path.is_absolute():
            path = Path.cwd() / path
        try:
            data = path.read_bytes()
        except OSError as exc:
            print(f"\nERROR: cannot read {path}: {exc}", file=sys.stderr)
            failed = True
            continue

        digest = hashlib.sha256(data).hexdigest()
        try:
            source = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            print(f"\nERROR: {path} is not valid UTF-8: {exc}", file=sys.stderr)
            failed = True
            continue

        package_match = re.search(
            r"(?m)^\s*package\s+([A-Za-z_][A-Za-z0-9_:]*)\b",
            source,
        )
        if package_match is None:
            print(
                f"\nERROR: cannot determine the top-level package in {path}",
                file=sys.stderr,
            )
            failed = True
            continue

        result = run_probe(
            label=str(path),
            source=source,
            expected_package=package_match.group(1).split("::")[-1],
            kernel_name=args.kernel,
            startup_timeout=args.startup_timeout,
            execution_timeout=args.execution_timeout,
            reply_timeout=args.reply_timeout,
        )
        print(f"\nfile: {path}")
        print(f"sha256: {digest}")
        print_probe(result)
        if result["classification"] != "PASS":
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
