from sort import Sort
from watergun import WaterGun
from TFLite_Wrapper import TFLite_Wrapper
#create instance of MobileNet, SORT, and Water Gun
model = TFLite_Wrapper()
mot_tracker = Sort() 
water_gun = WaterGun()
water_gun.start()

# get detections
detections = model.update(frame)

# update SORT
track_bbs_ids = mot_tracker.update(detections)

# track_bbs_ids is a np array where each row contains a valid bounding box and track_id (last column)
...