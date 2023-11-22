# Django
from django.forms import (
    DateField,
    ModelForm,
    widgets,
)

# wger
from wger.gallery.models import Image
from wger.utils.constants import DATE_FORMATS
from wger.utils.widgets import Html5DateInput

# Image sanitization
from PIL import Image as PillowImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import piexif
import sys

class ImageForm(ModelForm):
    date = DateField(input_formats=DATE_FORMATS, widget=Html5DateInput())

    class Meta:
        model = Image
        exclude = []
        widgets = {
            "user": widgets.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        print("Cleaned data: ", cleaned_data)

        # Access the image data and remove metadata
        image_data = cleaned_data.get("image")
        print("Type of data: ", type(cleaned_data))

        # Read the content of the uploaded file
        file_content = image_data.read()
        content_type = image_data.content_type

        # Remove metadata from the image
        img = PillowImage.open(BytesIO(file_content))
        # print("image: ", img.info)
        if "exif" in img.info:
            exif_dict = piexif.load(img.info["exif"])
            print("Exif keys: ", list(exif_dict.keys()))
            exif_dict["0th"].pop(piexif.ImageIFD.Make)
            exif_dict["0th"].pop(piexif.ImageIFD.Model)
            exif_dict["0th"].pop(piexif.ImageIFD.Software)
            print("exif_dict[Exif] = ", list(exif_dict["Exif"].keys()))
            keys_to_remove = exif_dict["GPS"].keys()
            for key in list(keys_to_remove):
                exif_dict["GPS"].pop(key, None)
            exif_bytes = piexif.dump(exif_dict)
            img_without_metadata = PillowImage.open(BytesIO(file_content))
            img_without_metadata.info["exif"] = exif_bytes

            print("Cleaned image out of metadata")
            # Save the modified image to an in-memory buffer
            output = BytesIO()
            img_without_metadata.save(output, format='JPEG')
            output.seek(0)

            # Create a new InMemoryUploadedFile object with the modified content
            modified_img = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image_data.name.split('.'), 'image/jpeg', sys.getsizeof(output), None)
            cleaned_data['image'] = modified_img  # Replace the original image with the modified one

            """ # Create a new InMemoryUploadedFile object with the modified content and name
            file_name = image_data.name
            new_file_name = file_name.split(".")[0] + "_1." + file_name.split(".")[1]
            modified_file = InMemoryUploadedFile(
                file=BytesIO(img_without_metadata.tobytes()),
                field_name=None,  # Set the field_name to None as it's not relevant for re-uploading
                name=new_file_name,  # Set the new file name
                content_type=content_type,
                size=len(img_without_metadata.tobytes()),
                charset=None,  # Set the charset if applicable
            )"""

            #cleaned_data["image"] = modified_file

        return cleaned_data
