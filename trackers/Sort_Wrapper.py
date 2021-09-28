from sort import Sort

class Sort_Wrapper():    
    def __init__(self, max_age = 1, min_hits = 3, iou_threshold = 0.3):
        self.sort = Sort(max_age = max_age, min_hits = min_hits, iou_threshold = iou_threshold)
        self.target_id = 0 
        
    def update(self, boxes):
        if len(boxes) > 0:
            boxes = self.sort.update(boxes)
        else:
            boxes = self.sort.update()
        pass

if __name__ == "__main__":
    sort_tracker = Sort_Wrapper()