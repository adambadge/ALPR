import main_functions as mf
import time

print('Quick 3 seconds! Line up the photo to test')
mf.camera.start_preview()
mf.time.sleep(5)
mf.camera.stop_preview()


print('Taking photo')
image_file = mf.take_photo()
print('Sending to the cloud to process')
rego       = mf.image_to_plate(image_file)



print('cloud rego result = '+rego)


print('Checking with VicRoads...Just a moment')
reg_status  = mf.get_registration_details(rego)
print(reg_status)





