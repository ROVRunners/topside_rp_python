from typing import NamedTuple


class VideoConfig(NamedTuple):
    """Describe a UDP socket configuration for video"""
    ip_address: str
    port: int = 5600
    timeout: float = .25
    max_attempts: int = 40
    buffer_size: int = 65535
    chunk_size: int = 16384
    width: int = 640
    height: int = 480
