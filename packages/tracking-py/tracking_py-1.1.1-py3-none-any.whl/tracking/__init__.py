import cv2

from typing import Union, Tuple, List

from . import exceptions

from .config import Config
from .enums import FingerEnum as finger
from .enums import SideEnum as side
from .enums import TypeEnum as type
from .enums import RunningModeEnum as running_mode
from .webcam import WebCam

CONFIG = Config()

def init(
        screen_size: Union[Tuple[int, int], List[int]],
        video_capture: Union[cv2.VideoCapture, int] = 0,
        flags: List[Union[int, type]] = 0
):
    CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT = screen_size
    CONFIG.VIDEO_CAPTURE = WebCam(video_capture)
    
    for flag in [flags] if isinstance(flags, (int, type)) else set(flags):
        value = flag.value if isinstance(flag, type) else flag
        
        if value == 0:
            raise NotImplementedError('Eye tracking not implemented')
        elif value == 1:
            from .face_tracking import Tracking as FaceTrackingClass
            
            global FaceTracking
            FaceTracking = FaceTrackingClass
        elif value == 2:
            from .hand_tracking import Tracking as HandTrackingClass
            
            global HandTracking
            HandTracking = HandTrackingClass
        else:
            raise exceptions.InvalidFlagException(f"Invalid Flag {flag}, use a tracking.type value")