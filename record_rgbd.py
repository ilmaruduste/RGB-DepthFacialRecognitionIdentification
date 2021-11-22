import imageio
import numpy as np
import pyrealsense2 as rs
import os
import shutil
import argparse
import keyboard
from time import localtime, strftime

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-f', '--folder', action='store', help = 'The name of the folder you want to store the data in.')
args = my_parser.parse_args()
data_folder_name = args.folder

def make_clean_folder(path_folder):
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
    else:
        user_input = input("%s not empty. Overwrite? (y/n) : " % path_folder)
        if user_input.lower() == "y":
            shutil.rmtree(path_folder)
            os.makedirs(path_folder)
        else:
            exit()



def record_rgbd(data_folder_name):
    folder_path = os.path.join("data", data_folder_name)
    make_clean_folder(folder_path)

    pipeline = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_sensor.set_option(
        rs.option.visual_preset, 3
    )  # Set high accuracy for depth sensor
    depth_scale = depth_sensor.get_depth_scale()

    clipping_distance_in_meters = 1
    clipping_distance = clipping_distance_in_meters / depth_scale

    align_to = rs.stream.color
    align = rs.align(align_to)

    while True:

        user_input = input("Press C (and Enter) to capture a foto or Q (and Enter) to shut down the program!")

        if user_input.lower() == "c":
            try:
                frames = pipeline.wait_for_frames()
                aligned_frames = align.process(frames)
                aligned_depth_frame = aligned_frames.get_depth_frame()
                color_frame = aligned_frames.get_color_frame()

                if not aligned_depth_frame or not color_frame:
                    raise RuntimeError("Could not acquire depth or color frames.")

                depth_image = np.asanyarray(aligned_depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                grey_color = 153
                depth_image_3d = np.dstack(
                    (depth_image, depth_image, depth_image)
                )  # Depth image is 1 channel, color is 3 channels
                bg_removed = np.where(
                    (depth_image_3d > clipping_distance) | (depth_image_3d <= 0),
                    grey_color,
                    color_image,
                )

                color_image = color_image[..., ::-1]

                current_time = strftime("%Y%m%d_%H%M%S", localtime())
                depth_filename = current_time + "_depth.png"
                rgb_filename = current_time + "_rgb.png"

                imageio.imwrite(os.path.join(folder_path, depth_filename), depth_image)
                imageio.imwrite(os.path.join(folder_path, rgb_filename), color_image)

            finally:
                print(f"RGB image written to {os.path.join(folder_path, rgb_filename)}!")
                print(f"Depth image written to {os.path.join(folder_path, depth_filename)}!")

        elif user_input.lower() == "q":
            print("Stopping program!")
            pipeline.stop()

        else: 
            print("Input not recognised, try again!")

    return color_image, depth_image


if __name__ == "__main__":
    record_rgbd(data_folder_name)