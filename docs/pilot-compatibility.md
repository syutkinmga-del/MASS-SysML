# SysML v2 Pilot Jupyter Compatibility Check

## Purpose and command

This check sends SysML source text directly to the configured Jupyter kernel. It does not use
`%load` or a local-path magic. Each smoke probe and each source file runs in a fresh kernel session.
The check requires Python, `jupyter_client` (including its `pyzmq` runtime dependency), the selected
Jupyter kernelspec, and the Java runtime required by that kernel. The environment used for the
recorded check had Python 3.12.6, `jupyter_client` 8.10.0, and `pyzmq` 27.2.0. No dependencies or
JAR files are bundled with this repository.

From the repository root, run:

```sh
python3 scripts/check_pilot.py
```

The kernel can be selected explicitly, and paths can be supplied for custom checks:

```sh
python3 scripts/check_pilot.py --kernel sysml
python3 scripts/check_pilot.py --kernel sysml path/to/model.sysml
```

The script has bounded defaults of 120 seconds for startup, 300 seconds for IOPub execution through
`idle`, and 30 seconds for `execute_reply` after `idle`. Each request's IOPub and shell messages are
matched by `parent_header.msg_id`. A pass requires `execute_reply` status `ok`, IOPub `idle`, no
IOPub error or diagnostic text, and the kernel's confirmed `execute_result` protocol:
`Package <package-name> (<UUID>)`. An explicit parser diagnostic such as
`ERROR:no viable alternative` is classified as `FAIL`; other missing or ambiguous evidence is
classified as `INDETERMINATE`. Both outcomes, errors, timeouts, or an unconfirmed kernel shutdown
result in a nonzero process exit. Every started kernel is shut down in a `finally` path.

## Confirmed local SNAPSHOT check (2026-11-19)

- Jupyter kernelspec: `sysml` (`display_name`: `SysML`, language: `sysml`).
- Java runtime: Temurin **21.0.12.1**.
- Installed kernel artifact: `jupyter-sysml-kernel-0.61.0-SNAPSHOT-all.jar`.
- JAR SHA-256: `4ee53832781b7733ff1428dde15998cd57b7ef58887ba68ccb1940afedbd0d5b`.
- Embedded Maven version: `0.61.0-SNAPSHOT`.
- The Pilot release version and source commit/build identifier are not available in the installed
  kernel metadata; the exact Pilot release/commit therefore remains unknown.

The checks below used the locally installed `0.61.0-SNAPSHOT` JAR. This is not the fixed upstream
release used by the CI workflow, and its result does not establish that release's compatibility.

## Confirmed local SNAPSHOT results (2026-11-19)

The installed kernel successfully processed the smoke source:

```sysml
package PilotSmokeTest { part def Vessel; }
```

The kernel returned an `execute_result` containing `Package PilotSmokeTest (<UUID>)`, followed by
IOPub `idle` and `execute_reply` status `ok`; there were no IOPub error messages or model diagnostic
text.

Each model was sent in a separate fresh `sysml` kernel session:

| File | SHA-256 | Result |
|---|---|---|
| `MASSKernel_v1.0.sysml` | `55d9100b977502286630a832a6fd6da5598ff732cec30ffe8d6d6e693db0d9a2` | `Package MASSKernel (<UUID>)`; `execute_reply` status `ok`; IOPub `idle`; no IOPub errors or model diagnostic text |
| `MASSKernel_v1.0_candidate.sysml` | `db3f214f1a6989fe705077f9f7bd19cfbea5ab6e7eb1f4a56824bf16da7d7fee` | `Package MASSKernel (<UUID>)`; `execute_reply` status `ok`; IOPub `idle`; no IOPub errors or model diagnostic text |

Kernel startup emitted log4j configuration warnings (`No appenders could be found for logger`,
`Please initialize the log4j system properly`, and the log4j FAQ notice). These are kernel process
startup warnings, separate from the model's IOPub output; they are not reported as model diagnostics.

## Fixed official release CI result (2026-11-19)

The separate workflow `.github/workflows/pilot-validation.yml` is configured to check the official
**2026-07 / Jupyter kernel 0.61.0** release from the
[official SysML v2 Pilot Implementation release](https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation/releases/tag/2026-07).
The release tag resolves to commit
[`c7fc737d56da9e2d78f9d7df6d38efbec2e7e965`](https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation/commit/c7fc737d56da9e2d78f9d7df6d38efbec2e7e965).

- Official archive: [`jupyter-sysml-kernel-0.61.0.zip`](https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation/releases/download/2026-07/jupyter-sysml-kernel-0.61.0.zip).
- ZIP SHA-256: `3d310efb8a5332b11ec2441697d40ae10e7e04cfb8c8d121c198ffba38229ada`.
- JAR path in the verified ZIP: `sysml/jupyter-sysml-kernel-0.61.0-all.jar`.
- Extracted JAR SHA-256: `602b53fa64d5af84480aa00e06e590a140d7d5c3651d4d76ac0e0055f89f0079`.
- The archive contains `install.py` at its root and a `sysml/` kernel-spec directory. Its installer
  supports `--sys-prefix`; the workflow uses that option so the kernel is installed in the
  GitHub-hosted CI Python prefix, not on a developer machine.
- CI is configured for Ubuntu 24.04, Temurin Java 21, and Python 3.12. Python dependencies are pinned
  in the workflow: `jupyter_client==8.10.0`, `jupyter_core==5.9.1`, `pyzmq==27.2.0`,
  `traitlets==5.16.1`, `tornado==6.5.8`, `platformdirs==4.11.7`,
  `python-dateutil==2.9.0.post0`, and `six==1.17.0`.

The [first pull-request workflow run](https://github.com/syutkinmga-del/MASS-SysML/actions/runs/44572418724)
completed successfully on 2026-11-19. It verified the ZIP and extracted JAR SHA-256 values above,
installed the kernel in the CI Python prefix, and ran
`python scripts/check_pilot.py --kernel sysml`.

The smoke probe, baseline, and candidate each returned the expected `Package ... (<UUID>)` result,
`execute_reply` status `ok`, IOPub `idle`, zero IOPub errors, and confirmed kernel shutdown. The
checker classified all three as `PASS`; it found no model diagnostic text. The validation-log
artifact was uploaded successfully.

The Jupyter kernel emitted log4j startup warnings (`No appenders could be found for logger`,
`Please initialize the logging system properly`, and the log4j FAQ notice). These were captured as
kernel startup warnings and were separate from model diagnostics.

The stable `0.61.0` release JAR is not byte-identical to the local `0.61.0-SNAPSHOT` JAR: their
SHA-256 values differ. Passing the local check therefore does not predict the result of the fixed
release CI check.

## Scope and limitations

This check establishes that this installed kernel accepted the supplied source and returned its
package result without reported parse/link diagnostics. It does **not** establish semantic
invariant or requirement regression, scenario behavior, nor integration compatibility with other
Pilot distributions or Hypha.

SK1–SK16 regression, CQ1–CQ12 regression, and operational behavior were not checked by this
Jupyter compatibility probe. The Pilot release version and commit/build identifier are unknown.
The successful result must not be presented as a substitute for those checks.

The checker negative-test contract is intentionally strict: a temporary malformed source producing
`ERROR:no viable alternative` must return `FAIL` and a nonzero process exit. An indeterminate result
is also non-success and returns nonzero.
