import cv2
import os
import argparse
import time
from multiprocessing import Process

def work(cap, cam, frame_interval):
    start = time.time()
    img_idx = 1
    # Read until video is completed
    while cap.isOpened():
        curr_time = time.time()
        elapsed = curr_time - start
        ret, frame = cap.read()
        if elapsed >= frame_interval:
            # Capture frame-by-frame
            if ret:
                # Save the resulting frame
                cv2.imwrite(f’{cam}/{img_idx}_{time.time()}.jpg’, frame)
                img_idx += 1
                print(f’{cam} time {time.time() - start}‘)
                start = time.time()
            else:
                break
    cap.release()

# get arguments from command line
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(‘--frame_interval’, type=float, default=30)
    args = parser.parse_args()
    # Open the video from http server
    stream_address = {
        “front_left”: “http://192.168.168.105:8080/stream?topic=/argus/ar0234_front_left/image_raw”,
        “front_right”: “http://192.168.168.105:8080/stream?topic=/argus/ar0234_front_right/image_raw”,
        “side_left”: “http://192.168.168.105:8080/stream?topic=/argus/ar0234_side_left/image_raw”,
        “side_right”: “http://192.168.168.105:8080/stream?topic=/argus/ar0234_side_right/image_raw”,
        “rear”: “http://192.168.168.105:8080/stream?topic=/argus/ar0234_rear/image_raw”
    }
    cap_front_left = cv2.VideoCapture(stream_address[“front_left”])
    cap_front_right = cv2.VideoCapture(stream_address[“front_right”])
    cap_side_left = cv2.VideoCapture(stream_address[“side_left”])
    cap_side_right = cv2.VideoCapture(stream_address[“side_right”])
    cap_rear = cv2.VideoCapture(stream_address[“rear”])
    cam_list = [“front_left”, “front_right”, “side_left”, “side_right”, “rear”]
    for i in range(len(cam_list)):
        if not os.path.exists(cam_list[i]):
            os.mkdir(cam_list[i])
    cap_list = [cap_front_left, cap_front_right, cap_side_left, cap_side_right, cap_rear]
    process_list = []
    for i in range(len(cap_list)):
        process = Process(target=work, args=(cap_list[i], cam_list[i], args.frame_interval))
        process_list.append(process)
    for i in range(len(cap_list)):
        process_list[i].start()
    for i in range(len(cap_list)):
        process_list[i].join()
if __name__ == ‘__main__‘:
    main()