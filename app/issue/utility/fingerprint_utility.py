from __future__ import annotations

import hashlib


class FingerprintUtil:
    @staticmethod
    def compute(
        service: str,
        exception_type: str,
        traceback: str,
    ) -> str:
        top_frame = FingerprintUtil._extract_top_frame(traceback)
        raw = f"{service}:{exception_type}:{top_frame}"
        return hashlib.sha256(raw.encode()).hexdigest()

    @staticmethod
    def _extract_top_frame(traceback: str) -> str:
        lines = [
            line.strip() for line in traceback.strip().splitlines() if line.strip()
        ]
        return lines[-1] if lines else "unknown"
