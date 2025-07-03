import os
import zipfile
import tempfile
import ffmpeg


def get_opcion_armado():
    print("How do you want to configure the video?")
    print("1. By frames per second (FPS)")
    print("2. By total duration")

    while True:
        choice = input("Enter your choice (1 or 2): \n")
        if choice == "1":
            fps = int(input("Enter the number of frames per second: \n"))
            return {"type": "fps", "value": fps}
        elif choice == "2":
            duration = float(input("Enter the total duration in seconds: \n"))
            return {"type": "duration", "value": duration}
        else:
            print("Invalid option. Please enter 1 or 2.")


def get_images_path():
    print("Images must be in a folder or zip file inside the current directory.")
    print("How do you want to provide the images?")
    print("1. From a ZIP file")
    print("2. From a folder")
    while True:
        choice = input("Enter your choice (1 or 2): \n")
        if choice == "1":
            print("Enter the path to the ZIP file relative to the current directory:")
            print("Example: './MyImages/Resonance.zip'")
            zip_path = input("ZIP file path: \n")
            if not zip_path.endswith(".zip"):
                print("Please make sure the file has a .zip extension.")
                continue
            if not os.path.exists(zip_path):
                print("The ZIP file does not exist. Please check the path.")
                continue
            return {"type": "zip", "path": zip_path}

        elif choice == "2":
            print("Enter the folder path relative to the current directory:")
            print("Example: './MyImages/'")
            folder_path = input("Folder path: \n")
            if not folder_path.endswith("/"):
                print("Please make sure the folder path ends with '/'.")
                continue
            if not os.path.exists(folder_path):
                print("The folder does not exist. Please check the pdath.")
                continue
            return {"type": "folder", "path": folder_path}
        else:
            print("Invalid option. Please enter 1 or 2.")


def calcular_config_video(video_config, img_count):
    if video_config["type"] == "fps":
        fps = video_config["value"]
        duration = img_count / fps
    elif video_config["type"] == "duration":
        duration = video_config["value"]
        fps = img_count / duration

    return {"fps": fps, "duration": duration}


def extract_images_from_zip(zip_path, temp_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    image_files = []
    for root, _, files in os.walk(temp_dir):
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
                image_files.append(os.path.join(root, f))
    image_files.sort()
    return image_files


def get_images_list(path_img):
    if path_img["type"] == "zip":
        temp_dir = tempfile.mkdtemp()
        images = extract_images_from_zip(path_img["path"], temp_dir)
    else:
        folder = path_img["path"]
        images = [os.path.join(folder, f) for f in os.listdir(folder)
                  if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff"))]
        images.sort()
    return images

def make_video(images, fps, output_path="output.mp4"):
    if not images:
        print("No images found to create the video.")
        return
    (
        ffmpeg
        .input('pipe:', format='image2pipe', framerate=fps)
        .output(output_path, vcodec='libx264', pix_fmt='yuv420p')
        .overwrite_output()
        .run(input=b''.join([open(img, 'rb').read() for img in images]))
    )
    print(f"Video created successfully!: {output_path}")


if __name__ == "__main__":
    video_config = get_opcion_armado()
    path_img = get_images_path()
    images = get_images_list(path_img)
    config = calcular_config_video(video_config, len(images))
    print(f"Number of images: {len(images)}")
    print(f"FPS: {config['fps']}, Duration: {config['duration']} seconds")
    make_video(images, config['fps'])
    input("\nPress Enter to exit...")
