import logging
from typing import Optional, Dict, Any
from live_status import RoomStatusChecker, LiveStatus

class LiveMonitor:
    def __init__(self, room_id: int, logger=None):
        self.room_id = room_id
        self.logger = logger or logging.getLogger(__name__)
        self.status_checker = RoomStatusChecker(logger)
        self._current_status = LiveStatus.OFFLINE
        
    async def update_room_info(self, room_info: Optional[Dict[str, Any]]) -> None:
        """Update room info and handle status changes
        
        Args:
            room_info: Room info dict from API response
        """
        try:
            new_status = self.status_checker.update_room_info(self.room_id, room_info)
            await self.handle_status_change(self._current_status, new_status)
            self._current_status = new_status
        except Exception as e:
            # Log as warning instead of error for expected states like room not streaming
            self.logger.warning(f"{self.room_id} - Room info update: {e}")
            
    async def handle_status_change(self, old_status: LiveStatus, new_status: LiveStatus) -> None:
        """Handle room status changes
        
        Args:
            old_status: Previous live status
            new_status: New live status
        """
        if old_status == new_status:
            return
            
        if new_status == LiveStatus.PREPARING:
            self.logger.info(f"{self.room_id} - Room is preparing to stream")
        elif new_status == LiveStatus.LIVE:
            self.logger.info(f"{self.room_id} - Room started streaming")
        elif new_status == LiveStatus.ROUND:
            self.logger.info(f"{self.room_id} - Room started round video")
        elif new_status == LiveStatus.OFFLINE:
            self.logger.info(f"{self.room_id} - Room went offline") 