import io
import os
import zipfile
from io import BytesIO

from typing import Any, Union, IO
from binaexperts.convertors import const
from binaexperts.convertors.base import YOLOConvertor, COCOConvertor


class Convertor:

    def __init__(self):
        pass

    @staticmethod
    def get_convertor(format_type: str):
        if format_type.lower() == const.CONVERTOR_FORMAT_YOLO:
            return YOLOConvertor()
        elif format_type.lower() == const.CONVERTOR_FORMAT_COCO:
            return COCOConvertor()
        else:
            raise ValueError(f"Unsupported format type: {format_type}")

    def convert(
            self,
            source_format: str,
            target_format: str,
            source: Union[str, IO[bytes]],
            destination: Union[str, IO[bytes]] = None
    ) -> Union[None, IO[bytes]]:
        # Get the correct convertors based on the formats passed
        source_convertor = self.get_convertor(source_format)
        target_convertor = self.get_convertor(target_format)

        # Handle source as either a path or file-like object
        if isinstance(source, str):
            if zipfile.is_zipfile(source):  # Handle zip file case
                with zipfile.ZipFile(source, 'r') as zip_ref:
                    source_data = source_convertor.load(zip_ref)
            else:
                with open(source, 'rb') as source_file:
                    source_data = source_convertor.load(source_file)
        else:
            source_data = source_convertor.load(source)

        # Convert to the normalized format
        normalized_data = source_convertor.normalize(source_data)

        # If destination is specified, save the output to it
        if destination:
            # Handle destination as directory or file-like object
            if isinstance(destination, str) and os.path.isdir(destination):
                destination_file_path = os.path.join(destination, 'converted_dataset.zip')
                with open(destination_file_path, 'wb') as destination_file:
                    target_data = target_convertor.convert(normalized_data, destination_file)
            else:
                target_data = target_convertor.convert(normalized_data, destination)

            # Save the target format dataset
            target_convertor.save(target_data, destination)
            return None  # No need to return anything when saved to disk

        else:
            # No destination provided, output the result as an in-memory IO object
            in_memory_output = BytesIO()
            target_data = target_convertor.convert(normalized_data, in_memory_output)
            in_memory_output.seek(0)  # Reset pointer to the beginning of the BytesIO object
            # Return the in-memory output for further use
            return in_memory_output