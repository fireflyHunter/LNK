import cv2
vidcap = cv2.VideoCapture("https://mtc.cdn.vine.co/r/videos/0429DC760A1147631740152922112_368ee8b2941.0.1.12376952153331684897.mp4")
success,image = vidcap.read()
frame = 0;
count = 0

fps = vidcap.get(cv2.CAP_PROP_FPS)
print(fps)
while success:
    success,image = vidcap.read()
    if frame%(fps/2)==0:
        cv2.imwrite("frame%d.jpg" % count, image)
        count += 1
        # save frame as JPEG file
    frame += 1
print(frame)
vidcap.release()


