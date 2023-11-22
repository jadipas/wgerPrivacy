# test on metadata
from PIL import Image
from PIL.ExifTags import TAGS


def get_gps_coordinates(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    print("Test failed")
                    print(f"GPS Coordinates: {value}")
                    break
            else:
                print("GPS coordinates do not exist in the image metadata.")
        else:
            print("Test passed")
            print("No EXIF data found in the image.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_metadata(image_path, mode=True):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data:
            print("Test failed")
            if mode:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    print(tag_name, value)
        else:
            print("Test passed")
            print("No EXIF data found in the image.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Call the function with the image path
image_path = "/home/jordan/Documents/PrivacyProject/src/media/gallery/2/26c637a9-4601-4c04-898e-426fcee966cc.JPG"
# image_path = "/home/jordan/Documents/PrivacyProject/src/media/gallery/1/c4b67c0f-ab9c-4a42-93fe-068a9fd32d80.jpg"
get_gps_coordinates(image_path)
get_metadata(image_path)

image_path_fixed = "/home/jordan/Documents/PrivacyProject/src/media/gallery/2/817c222f-ef49-4216-9c08-cbb970a37fc3.jpg"
get_gps_coordinates(image_path_fixed)
get_metadata(image_path_fixed)
