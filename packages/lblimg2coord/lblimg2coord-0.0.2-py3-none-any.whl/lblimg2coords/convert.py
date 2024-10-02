# convert.py

import os
import cv2
import argparse
from tqdm import tqdm
import glob


def convert_contours_to_polygons(input_dir, output_dir, threshold_area):
    # Use glob to get files with jpg and png extensions

    image_files = glob.glob(os.path.join(input_dir, '*.jpg')) + glob.glob(os.path.join(input_dir, '*.png'))
    print(f"Found {len(image_files)} images in the input directory")

    for j in tqdm(image_files, desc="Processing images"):
        image_path = os.path.join(input_dir, j)

        # Load the binary mask and get its contours
        try:
            mask = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

            H, W = mask.shape
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Convert the contours to polygons
            polygons = []
            for cnt in contours:
                if cv2.contourArea(cnt) > threshold_area:
                    polygon = [(x / W, y / H) for point in cnt for x, y in point]
                    polygons.append(polygon)

            # Save the polygons to a file
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(j)[0]}.txt")
            with open(output_file_path, 'w') as f:
                for polygon in polygons:
                    f.write(' '.join(map(lambda p: f'{p[0]} {p[1]}', polygon)) + '\n')
        except Exception as e:
            print(f"Error processing image '{image_path}': {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert contours to polygons")
    parser.add_argument("--input_dir", required=True, help="Path to the input directory containing binary masks")
    parser.add_argument("--output_dir", required=True, help="Path to the output directory to save polygons")
    parser.add_argument("--threshold_area", type=float, default=0, help="Contour area threshold")

    args = parser.parse_args()

    # Validate input and output directories
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        exit(1)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)
        print("Folder created at: ", args.output_dir)
    # Call the function to convert contours to polygons
    print("Converting contours to polygons...")
    convert_contours_to_polygons(args.input_dir, args.output_dir, args.threshold_area)
    print("Done!")


if __name__ == "__main__":
    main()
