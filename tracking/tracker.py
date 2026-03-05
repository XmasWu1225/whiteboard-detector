import numpy as np
from typing import List, Optional, Dict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from tracking.sort import Sort
from config import Config


class WhiteboardTracker:
    def __init__(self, max_age: int = None, min_hits: int = None, iou_threshold: float = None):
        self.max_age = max_age if max_age else Config.SORT_MAX_AGE
        self.min_hits = min_hits if min_hits else Config.SORT_MIN_HITS
        self.iou_threshold = iou_threshold if iou_threshold else Config.SORT_IOU_THRESHOLD
        
        self.sort_tracker = Sort(max_age=self.max_age, 
                                  min_hits=self.min_hits, 
                                  iou_threshold=self.iou_threshold)
        
        self.active_trackers: Dict[int, dict] = {}
        self.frame_count = 0
    
    def update(self, detections: List[dict]) -> List[dict]:
        self.frame_count += 1
        
        if not detections:
            return []
        
        dets = np.array([[d['bbox'][0], d['bbox'][1], d['bbox'][2], d['bbox'][3]] 
                        for d in detections])
        
        trackers = self.sort_tracker.update(dets)
        
        tracked_objects = []
        for tracker in trackers:
            track_id = int(tracker[4])
            bbox = [int(tracker[0]), int(tracker[1]), int(tracker[2]), int(tracker[3])]
            
            if track_id not in self.active_trackers:
                self.active_trackers[track_id] = {
                    'id': track_id,
                    'bbox': bbox,
                    'first_seen': self.frame_count,
                    'last_seen': self.frame_count,
                    'frame_count': 0
                }
            else:
                self.active_trackers[track_id]['bbox'] = bbox
                self.active_trackers[track_id]['last_seen'] = self.frame_count
                self.active_trackers[track_id]['frame_count'] += 1
            
            tracked_objects.append({
                'id': track_id,
                'bbox': bbox,
                'age': self.active_trackers[track_id]['frame_count']
            })
        
        self._cleanup_inactive_trackers()
        
        return tracked_objects
    
    def _cleanup_inactive_trackers(self):
        to_remove = []
        for track_id, tracker in self.active_trackers.items():
            if self.frame_count - tracker['last_seen'] > self.max_age:
                to_remove.append(track_id)
        
        for track_id in to_remove:
            del self.active_trackers[track_id]
    
    def get_most_stable_tracker(self) -> Optional[dict]:
        if not self.active_trackers:
            return None
        
        stable_tracker = max(self.active_trackers.items(), 
                           key=lambda x: x[1]['frame_count'])
        
        return stable_tracker[1]
    
    def get_tracker_by_id(self, track_id: int) -> Optional[dict]:
        return self.active_trackers.get(track_id)
    
    def reset(self):
        self.sort_tracker = Sort(max_age=self.max_age, 
                                  min_hits=self.min_hits, 
                                  iou_threshold=self.iou_threshold)
        self.active_trackers = {}
        self.frame_count = 0
