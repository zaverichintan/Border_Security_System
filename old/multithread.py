import os
import threading

import cv2

my_opencv_path = '/home/zaverichintan/Study/final_year_project/file-video-stream/OpenCV/opencv-2.4.10'
video_path_1 = os.path.join(my_opencv_path, "samples", "cpp", "tutorial_code",
                            "HighGUI", "video-input-psnr-ssim", "video",
                            "Megamind.avi")
video_path_2 = os.path.join(my_opencv_path, "samples", "cpp", "tutorial_code",
                            "HighGUI", "video-input-psnr-ssim", "video",
                            "Megamind.avi")

assert os.path.isfile(video_path_1)
assert os.path.isfile(video_path_2)


class MyThread (threading.Thread):
    maxRetries = 2

    def __init__(self, thread_id, name, video_url, thread_lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.video_url = video_url
        self.thread_lock = thread_lock

    def run(self):
        print ("Starting " + self.name)
        window_name = self.name
        

        cv2.namedWindow(window_name)
        video = cv2.VideoCapture(self.video_url)


        while True:
            # self.thread_lock.acquire()  # These didn't seem necessary
            got_a_frame, image = video.read()
            # self.thread_lock.release()
            if not got_a_frame:  # error on video source or last frame finished
                break
            cv2.imshow(window_name, image)
            key = cv2.waitKey(50)
            if key == 27:
                break
        cv2.destroyWindow(window_name)

        print (self.name + " Exiting")


def main():
    thread_lock = threading.Lock()
    thread1 = MyThread(1, "Thread 1", video_path_1, thread_lock)
    thread2 = MyThread(2, "Thread 2", video_path_2, thread_lock)
    thread1.start()
    thread2.start()
    print ("Exiting Main Thread")

if __name__ == '__main__':
    main()