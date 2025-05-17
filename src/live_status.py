from enum import Enum
import logging
from typing import Optional, Dict, Any

class LiveStatus(Enum):
    PREPARING = 0  # 未开播
    LIVE = 1      # 直播中
    ROUND = 2     # 轮播中
    OFFLINE = -1  # 已下播

class RoomStatusChecker:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def update_room_info(self, room_id: int, room_info: Optional[Dict[str, Any]]) -> LiveStatus:
        """Update room info and return live status
        
        Args:
            room_id: Room ID
            room_info: Room info dict from API response
            
        Returns:
            LiveStatus enum indicating current status
        """
        if room_info is None:
            self.logger.info(f"{room_id} - Room is not streaming (offline or not exist)")
            return LiveStatus.OFFLINE
            
        try:
            live_status = room_info.get("live_status", LiveStatus.OFFLINE.value)
            title = room_info.get("title", "")
            online = room_info.get("online", 0)
            
            status = LiveStatus(live_status)
            
            if status == LiveStatus.PREPARING:
                self.logger.info(f"{room_id} - Room is preparing to stream")
            elif status == LiveStatus.LIVE:
                self.logger.info(f"{room_id} - Room is streaming: {title} (viewers: {online})")
            elif status == LiveStatus.ROUND:
                self.logger.info(f"{room_id} - Room is playing round video")
            elif status == LiveStatus.OFFLINE:
                self.logger.info(f"{room_id} - Room is offline")
                
            return status
            
        except (KeyError, ValueError) as e:
            self.logger.warning(f"{room_id} - Failed to parse room info: {e}")
            return LiveStatus.OFFLINE 