"""Start a child process so that its whole process tree can be killed later (Windows job object / POSIX session)."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    import ctypes
    from ctypes import wintypes

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    class _IO_COUNTERS(ctypes.Structure):
        _fields_ = [(n, ctypes.c_ulonglong) for n in (
            "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
            "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

    class _BASIC_LIMIT(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_longlong),
            ("PerJobUserTimeLimit", ctypes.c_longlong),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class _EXTENDED_LIMIT(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", _BASIC_LIMIT),
            ("IoInfo", _IO_COUNTERS),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    _JobObjectExtendedLimitInformation = 9
    _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000
    _kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    _kernel32.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
    _kernel32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
    _kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    _kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]


class ProcessTree:
    """A Popen plus the means to kill everything it spawned."""

    def __init__(self, cmd: list[str], *, cwd, env, stderr, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL):
        self._job = None
        if IS_WINDOWS:
            flags = subprocess.CREATE_NEW_PROCESS_GROUP
            self.proc = subprocess.Popen(
                cmd, cwd=cwd, env=env, stdin=stdin, stdout=stdout,
                stderr=stderr, creationflags=flags,
            )
            self._job = self._make_job()
        else:
            self.proc = subprocess.Popen(
                cmd, cwd=cwd, env=env, stdin=stdin, stdout=stdout,
                stderr=stderr, start_new_session=True,
            )

    def _make_job(self):
        try:
            job = _kernel32.CreateJobObjectW(None, None)
            if not job:
                return None
            info = _EXTENDED_LIMIT()
            info.BasicLimitInformation.LimitFlags = _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            if not _kernel32.SetInformationJobObject(job, _JobObjectExtendedLimitInformation, ctypes.byref(info), ctypes.sizeof(info)):
                _kernel32.CloseHandle(job)
                return None
            if not _kernel32.AssignProcessToJobObject(job, int(self.proc._handle)):
                _kernel32.CloseHandle(job)
                return None
            return job
        except Exception:
            return None

    @property
    def pid(self) -> int:
        return self.proc.pid

    def poll(self):
        return self.proc.poll()

    def wait(self, timeout: float) -> bool:
        try:
            self.proc.wait(timeout=max(0.0, timeout))
            return True
        except subprocess.TimeoutExpired:
            return False

    def kill_tree(self) -> None:
        """Kill the process and everything it spawned. Idempotent."""
        if IS_WINDOWS:
            if self._job is not None:
                try:
                    _kernel32.TerminateJobObject(self._job, 1)
                    _kernel32.CloseHandle(self._job)
                except Exception:
                    pass
                self._job = None
            if self.proc.poll() is None:
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(self.proc.pid)],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                if self.proc.poll() is None:
                    self.proc.kill()
        else:
            for sig in (signal.SIGTERM, signal.SIGKILL):
                try:
                    os.killpg(self.proc.pid, sig)
                except (ProcessLookupError, PermissionError):
                    break
                if sig == signal.SIGTERM:
                    deadline = time.monotonic() + 0.5
                    while time.monotonic() < deadline and self.proc.poll() is None:
                        time.sleep(0.02)
            if self.proc.poll() is None:
                self.proc.kill()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass
