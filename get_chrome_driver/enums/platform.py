from enum import Enum


class Platform(Enum):
    win32 = "win32"
    win64 = "win64"
    linux32 = "linux32"
    linux64 = "linux64"
    mac32 = "mac32"
    mac64 = "mac64"
    mac_arm64 = "mac-arm64"
    mac_x64 = "mac-x64"
