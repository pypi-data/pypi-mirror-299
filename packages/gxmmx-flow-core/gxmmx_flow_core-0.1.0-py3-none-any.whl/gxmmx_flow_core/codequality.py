import os
import json
import hashlib
import random
from enum import Enum

from .core import Flow
from .log import FlowLog
from .errors import FlowError, FlowCodeQualityError


class CodeQualitySeverity(Enum):
    INFO = 1
    MINOR = 2
    MAJOR = 3
    CRITICAL = 4
    BLOCKER = 5


class CodeQualityObject:
    def __init__(self, **kwargs):

        self.name = kwargs.get("name") or kwargs.get("check_name")
        if self.name is None:
            raise FlowCodeQualityError(
                "Code quality object is missing 'check_name' field"
            )
        if not isinstance(self.name, str):
            raise FlowCodeQualityError(
                "Code quality object has invalid 'check_name' field"
            )

        self.desc = kwargs.get("desc") or kwargs.get("description")
        if self.desc is None:
            raise FlowCodeQualityError(
                f"Code quality object '{self.name}' is missing 'description' field"
            )
        if not isinstance(self.desc, str):
            raise FlowCodeQualityError(
                "Code quality object has invalid 'description' field"
            )

        self.severity = kwargs.get("severity")
        if self.severity is None:
            self.severity = "blocker"
        if not isinstance(self.severity, str):
            raise FlowCodeQualityError(
                "Code quality object has invalid 'severity' field"
            )
        if self.severity.lower() not in [
            sev.lower() for sev in CodeQualitySeverity.__members__
        ]:
            raise FlowCodeQualityError(
                f"Code quality object '{self.name}' has invalid severity declaration.\
                    Must be one of: {[name.lower() for name in CodeQualitySeverity.__members__]}"
            )

        if (_loc := kwargs.get("location")) is not None:
            if isinstance(_loc, dict):
                if (_path := _loc.get("path")) is not None:
                    self.path = _path
                if (_lines := _loc.get("lines")) is not None:
                    if isinstance(_lines, dict):
                        self.begin = _lines.get("begin")
                        self.end = _lines.get("end")

        self.path = kwargs.get("path") or kwargs.get("file")
        if self.path is None:
            self.path = "unspecified"
        if not isinstance(self.path, str):
            raise FlowCodeQualityError("Code quality object has invalid 'path' field")

        self.fingerprint = kwargs.get("fingerprint") or kwargs.get("hash")
        if self.fingerprint is None:
            self.fingerprint = self._gen_hash(self.path)

        self.begin = kwargs.get("begin")
        if self.begin is None:
            self.begin = 0

        self.end = kwargs.get("end")
        if self.end is None:
            self.end = self.begin

    def _gen_hash(self, path: str) -> str:
        if os.path.exists(path):
            file_path = path
        elif os.path.exists(f"{Flow._root_dir}/{path}"):
            file_path = f"{Flow._root_dir}/{path}"
        else:
            return f"{random.getrandbits(128):032x}"

        buffer_size = 65536
        hash = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                while True:
                    data = f.read(buffer_size)
                    if not data:
                        break
                    hash.update(data)
            return hash.hexdigest()
        except Exception:
            return f"{random.getrandbits(128):032x}"

    def to_dict(self) -> dict:
        return {
            "check_name": self.name,
            "description": self.desc,
            "severity": self.severity,
            "fingerprint": self.fingerprint,
            "location": {
                "path": self.path,
                "lines": {"begin": self.begin, "end": self.end},
            },
        }


class FlowCodeQuality:
    def __init__(self, name: str) -> None:
        self.objects: list[CodeQualityObject] = []
        self.name = "_".join(name.lower().split())
        cq_path = "gxmmx_flow/codequality"
        Flow.ensure_directory(cq_path)
        self.file = f"{cq_path}/{self.name}.json"

    def message(
        self,
        name: str,
        desc: str,
        severity: str,
        path: str | None = None,
        begin: int | None = None,
        end: int | None = None,
        fingerprint: str | None = None,
    ) -> None:
        self.objects.append(
            CodeQualityObject(
                name=name,
                desc=desc,
                severity=severity,
                path=path,
                begin=begin,
                end=end,
                fingerprint=fingerprint,
            )
        )

    def info(
        self,
        name: str,
        desc: str,
        path: str | None = None,
        begin: int | None = None,
        end: int | None = None,
        fingerprint: str | None = None,
    ) -> None:
        self.objects.append(
            CodeQualityObject(
                name=name,
                desc=desc,
                severity="info",
                path=path,
                begin=begin,
                end=end,
                fingerprint=fingerprint,
            )
        )

    def minor(
        self,
        name: str,
        desc: str,
        path: str | None = None,
        begin: int | None = None,
        end: int | None = None,
        fingerprint: str | None = None,
    ) -> None:
        self.objects.append(
            CodeQualityObject(
                name=name,
                desc=desc,
                severity="minor",
                path=path,
                begin=begin,
                end=end,
                fingerprint=fingerprint,
            )
        )

    def major(
        self,
        name: str,
        desc: str,
        path: str | None = None,
        begin: int | None = None,
        end: int | None = None,
        fingerprint: str | None = None,
    ) -> None:
        self.objects.append(
            CodeQualityObject(
                name=name,
                desc=desc,
                severity="major",
                path=path,
                begin=begin,
                end=end,
                fingerprint=fingerprint,
            )
        )

    def critical(
        self,
        name: str,
        desc: str,
        path: str | None = None,
        begin: int | None = None,
        end: int | None = None,
        fingerprint: str | None = None,
    ) -> None:
        self.objects.append(
            CodeQualityObject(
                name=name,
                desc=desc,
                severity="critical",
                path=path,
                begin=begin,
                end=end,
                fingerprint=fingerprint,
            )
        )

    def blocker(
        self,
        name: str,
        desc: str,
        path: str | None = None,
        begin: int | None = None,
        end: int | None = None,
        fingerprint: str | None = None,
    ) -> None:
        self.objects.append(
            CodeQualityObject(
                name=name,
                desc=desc,
                severity="blocker",
                path=path,
                begin=begin,
                end=end,
                fingerprint=fingerprint,
            )
        )

    def from_json(self, report: str) -> None:
        report_list = json.loads(report)
        if not isinstance(report_list, list):
            raise FlowCodeQualityError("Invalid code quality report, must be list")
        for object in report_list:
            if not isinstance(object, dict):
                raise FlowCodeQualityError(
                    "Invalid code quality report, each object must be a dictionary"
                )
            self.objects.append(CodeQualityObject(**object))

    def write(self) -> None:
        object_dicts = [obj.to_dict() for obj in self.objects]
        try:
            with open(self.file, "w") as file:
                json.dump(
                    object_dicts,
                    file,
                )
        except Exception:
            raise FlowError(f"Could not write report to: '{self.file}'")

        obj_info_count = 0
        obj_warn_count = 0
        obj_crit_count = 0

        if len(self.objects) > 0:
            FlowLog.msg("----------------------------------------")
            FlowLog.msg(f"Code Quality [{self.name}]:")
            for obj in self.objects:
                end = f":{obj.end}" if obj.end != obj.begin else ""
                if CodeQualitySeverity[obj.severity.upper()].value >= 4:
                    obj_crit_count += 1
                    FlowLog.err(
                        f"{obj.name} - {obj.desc} ({obj.path}:{obj.begin}{end})", False
                    )
                elif CodeQualitySeverity[obj.severity.upper()].value >= 2:
                    obj_warn_count += 1
                    FlowLog.wrn(
                        f"{obj.name} - {obj.desc} ({obj.path}:{obj.begin}{end})"
                    )
                else:
                    obj_info_count += 1
                    FlowLog.msg(
                        f"{obj.name} - {obj.desc} ({obj.path}:{obj.begin}{end})"
                    )
        FlowLog.msg("----------------------------------------")
        FlowLog.msg(f"Code Quality Report Summary [{self.name}]:")
        if len(self.objects) == 0:
            FlowLog.ok("Total: 0 (100%)")
            FlowLog.msg("----------------------------------------")
        else:
            FlowLog.err(f"Critical: {obj_crit_count}", False)
            FlowLog.wrn(f"Warning:  {obj_warn_count}")
            FlowLog.msg(f"Info:     {obj_crit_count}")
            FlowLog.msg("----------------------------------------")
            FlowLog.msg(f"Total:    {len(self.objects)}")
            FlowLog.msg("----------------------------------------")

        if obj_crit_count > 0:
            exit(1)
