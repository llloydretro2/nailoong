import cv2
import os
import tqdm

DEFAULT_FRAME_RATE = 30  # 默认帧率


def loadVideo(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None
    return cap


def generateScreenshot(video_path):
    # 创建保存截图的目录
    save_path = os.path.join("screenshot",
                             os.path.basename(video_path).replace(".mp4", ""))
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 读取视频，若失败则返回
    cap = loadVideo(video_path)
    if cap is None:
        return None

    # 获取视频的帧率
    fps = DEFAULT_FRAME_RATE if cap.get(cv2.CAP_PROP_FPS) == 0 else cap.get(
        cv2.CAP_PROP_FPS)

    # 计算每0.1秒对应的帧数
    interval_frames = int(fps * 0.1)

    frame_number = 0
    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if not ret:
            break

        # 保存截图
        cv2.imwrite(f"{save_path}/{frame_number}.jpg", frame)
        frame_number += interval_frames

    cap.release()
    cv2.destroyAllWindows()

    return


def generateSymmetry(pic_path):
    img = cv2.imread(pic_path)
    if img is None:
        print(f"Error: Could not read image {pic_path}.")
        return

    # 获取图像的宽度和高度
    height, width = img.shape[:2]

    # 生成以左半部分为基准的镜像对称图片
    left_half = img[:, :width // 2]
    right_half_mirrored = cv2.flip(left_half, 1)
    left_based_mirrored_img = cv2.hconcat([left_half, right_half_mirrored])
    left_based_mirrored_img_path = pic_path.replace(
        ".jpg", "_left_based_mirrored.jpg")
    if not os.path.exists(os.path.dirname(left_based_mirrored_img_path)):
        cv2.imwrite(left_based_mirrored_img_path, left_based_mirrored_img)
        print(
            f"Saved left-based mirrored image as {left_based_mirrored_img_path}"
        )

    # 生成以右半部分为基准的镜像对称图片
    right_half = img[:, width // 2:]
    left_half_mirrored = cv2.flip(right_half, 1)
    right_based_mirrored_img = cv2.hconcat([left_half_mirrored, right_half])
    right_based_mirrored_img_path = pic_path.replace(
        ".jpg", "_right_based_mirrored.jpg")
    if not os.path.exists(os.path.dirname(right_based_mirrored_img_path)):
        cv2.imwrite(right_based_mirrored_img_path, right_based_mirrored_img)
        print(
            f"Saved right-based mirrored image as {right_based_mirrored_img_path}"
        )


def calculate_orb_similarity(img1, img2):
    # 初始化ORB检测器
    orb = cv2.ORB_create()

    # 检测并计算特征点和描述符
    keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

    # 创建BFMatcher对象
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # 匹配描述符
    matches = bf.match(descriptors1, descriptors2)

    # 按照距离排序
    matches = sorted(matches, key=lambda x: x.distance)

    # 计算相似度
    similarity = sum([1 - match.distance / 256
                      for match in matches]) / len(matches)
    return similarity


def listFiles(directory, suffix):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(suffix):
                files.append(os.path.join(root, filename))
    return files


if __name__ == "__main__":
    video_address = r'C:\Users\15532\OneDrive\Code\python\symmetry\video'
    mp4_files = listFiles(video_address, ".mp4")

    for file in tqdm.tqdm(mp4_files):
        generateScreenshot(file)

    png_files = listFiles("screenshot", ".png")
    for pic in tqdm.tqdm(png_files):
        generateSymmetry(pic)
