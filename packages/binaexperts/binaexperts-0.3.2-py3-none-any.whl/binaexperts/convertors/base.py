import io
import yaml
import json
import os
import zipfile
import cv2
import numpy as np
import datetime

from struct import unpack
from abc import ABC, abstractmethod
from typing import Union, IO, Any, Dict, Tuple
from binaexperts.convertors.const import *
from jsonschema import validate, ValidationError




# Function to get image dimensions from bytes
def get_image_dimensions(image_bytes: bytes) -> Tuple[int, int]:
    """
    Get the dimensions (width, height) of an image from its byte content.

    :param image_bytes: Byte content of the image.
    :return: A tuple containing (width, height).
    """
    # Minimum length check to prevent processing invalid or mock content
    if len(image_bytes) < 10:
        print("Warning: Image content too short to determine dimensions. Returning default dimensions.")
        return 640, 480  # Return default dimensions for mock or invalid content

    # Read the first few bytes of the image to determine the format and size
    with io.BytesIO(image_bytes) as img_file:
        # Check if it's a JPEG file
        img_file.seek(0)
        img_file.read(2)
        b = img_file.read(1)
        try:
            # Counter to avoid infinite loops
            max_iterations = 100  # Set an appropriate limit for iterations
            iteration_count = 0

            while b and b != b'\xDA':  # Search for the start of the image data (SOS marker)
                # Increment iteration counter
                iteration_count += 1
                if iteration_count > max_iterations:
                    print("Warning: Exceeded maximum iterations. Returning default dimensions.")
                    return 640, 480  # Return default dimensions to avoid infinite loop

                while b != b'\xFF':  # Find marker
                    b = img_file.read(1)
                while b == b'\xFF':  # Skip padding
                    b = img_file.read(1)
                if b >= b'\xC0' and b <= b'\xC3':  # Start of Frame markers for JPEG
                    img_file.read(3)  # Skip segment length and precision
                    h, w = unpack('>HH', img_file.read(4))  # Read height and width
                    return w, h
                else:
                    segment_length = unpack('>H', img_file.read(2))[0]
                    if segment_length <= 2:  # Prevent zero or negative length reads
                        print("Warning: Invalid segment length. Returning default dimensions.")
                        return 640, 480
                    img_file.read(segment_length - 2)  # Skip other segments
                b = img_file.read(1)
        except Exception as e:
            print(f"Error reading image dimensions: {e}. Returning default dimensions.")
        return 640, 480  # Fallback if dimensions couldn't be read


class BaseConvertor(ABC):
    """
    Base class for data format converters. This class provides a framework
    for converting datasets between different formats, such as COCO, YOLO,
    and others, using a normalized intermediate format.
    """

    def __init__(self):
        """
        Initialize the base converter class. This base class is intended to be
        inherited by specific format converters (e.g., COCO, YOLO).
        """
        pass

    @abstractmethod
    def load(
            self,
            source: Union[str, IO[bytes]]
    ) -> Any:
        """
        Load the data from the source format.

        :param source: File-like object or path representing the source dataset.
        :return: Loaded data in the source format.
        """
        raise NotImplementedError("The 'load' method must be overridden by subclasses.")

    @abstractmethod
    def normalize(
            self,
            data: Any
    ) -> Dict:
        """
        Convert the source format data to the normalized format.

        :param data: Loaded data in the source format.
        :return: Data converted to the normalized format as a dictionary.
        """
        raise NotImplementedError("The 'normalize' method must be overridden by subclasses.")

    @abstractmethod
    def convert(
            self,
            normalized_data: Dict,
            destination: Union[str, IO[bytes]]
    ) -> Any:
        """
        Convert the normalized format data to the target format.

        :param normalized_data: Data in the normalized format as a dictionary.
        :param destination: File-like object or path representing the target dataset.
        :return: Converted data in the target format.
        """
        raise NotImplementedError("The 'convert' method must be overridden by subclasses.")

    @abstractmethod
    def save(
            self,
            data: Any,
            destination: Union[str, IO[bytes]]
    ) -> None:
        """
        Save the data in the target format.

        :param data: Data in the target format.
        :param destination: File-like object to save the target dataset.
        """
        raise NotImplementedError("The 'save' method must be overridden by subclasses.")


class COCOConvertor(BaseConvertor):

    def __init__(self):
        super().__init__()

        # Load the JSON schema using a relative path from the current file
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'coco.json')
        with open(schema_path, 'r') as schema_file:
            self.coco_schema = json.load(schema_file)

        # Load the normalizer JSON schema
        normalizer_schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'normalizer.json')
        with open(normalizer_schema_path, 'r') as schema_file:
            self.normalizer_schema = json.load(schema_file)

    def _loadhelper_coco_data(self, coco_data, dataset, subdir, source_zip=None):
        """
        Helper method to load categories, images, and annotations from COCO data.
        """
        # Load categories if not already present
        if not dataset['categories']:
            for cat in coco_data.get('categories', []):
                category = {
                    'id': cat['id'],
                    'name': cat['name'],
                    'supercategory': cat.get('supercategory', 'none')
                }
                dataset['categories'].append(category)

        # Load images
        for img in coco_data.get('images', []):
            unique_image_id = f"{subdir}_{img['id']}"  # Prefix with split
            image_file_name = img['file_name']
            image_path = f"{subdir}/{image_file_name}"

            image_content = None
            # Read image content if available in the source zip
            if source_zip and image_path in source_zip.namelist():
                with source_zip.open(image_path) as img_file:
                    image_content = img_file.read()
            elif source_zip:
                print(f"Warning: Image file {image_path} not found in zip archive.")

            image = {
                'id': unique_image_id,
                'file_name': image_file_name,
                'width': img.get('width', 0),
                'height': img.get('height', 0),
                'split': subdir,
                'source_zip': source_zip,
                'image_content': image_content
            }
            dataset['images'].append(image)

        # Load annotations
        for ann in coco_data.get('annotations', []):
            unique_image_id = f"{subdir}_{ann['image_id']}"  # Ensure mapping to unique image ID
            annotation = {
                'id': ann['id'],
                'image_id': unique_image_id,
                'category_id': ann['category_id'],
                'bbox': ann['bbox'],
                'segmentation': ann.get('segmentation', []),  # Include segmentation data
                'area': ann.get('area', 0.0),
                'iscrowd': ann.get('iscrowd', 0)
            }
            # Ensure segmentation is correctly formatted (a list of lists of coordinates)
            if not isinstance(annotation['segmentation'], list):
                print(f"Warning: Invalid segmentation format for annotation ID {ann['id']}.")

            dataset['annotations'].append(annotation)

    def load(self, source: Union[str, IO[bytes]]) -> Dict:
        """
        Load COCO dataset from a zip file, directory, or an in-memory object.

        :param source: A Path, a File-like object (e.g., a BytesIO object), or an opened ZipFile containing the COCO data.
        :return: A dictionary representing the COCO dataset.
        """
        subdirs = ['train', 'test', 'valid']
        dataset = {
            'info': {},
            'images': [],
            'annotations': [],
            'categories': [],
            'licenses': []
        }

        if isinstance(source, str):
            # If the source is a file path (zip file)
            if zipfile.is_zipfile(source):
                with zipfile.ZipFile(source, 'r') as zip_file:
                    for subdir in subdirs:
                        annotation_path = f"{subdir}/_annotations.coco.json"

                        # Skip subdir if the annotation file does not exist
                        if annotation_path not in zip_file.namelist():
                            print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                            continue

                        with zip_file.open(annotation_path) as file:
                            coco_data = json.load(file)

                            # Validate coco_data against the loaded schema to ensure its structure is correct
                            try:
                                validate(instance=coco_data, schema=self.coco_schema)
                            except ValidationError as e:
                                print(f"Validation error in {subdir}: {e.message}")
                                continue  # Skip processing this subdir if validation fails

                        # Use the helper method to load data
                        self._loadhelper_coco_data(coco_data, dataset, subdir, source_zip=zip_file)

            else:
                # If the source is a directory path
                for subdir in subdirs:
                    annotation_file = os.path.join(source, subdir, '_annotations.coco.json')

                    # Skip subdir if the annotation file does not exist
                    if not os.path.isfile(annotation_file):
                        print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                        continue

                    with open(annotation_file, 'r') as file:
                        coco_data = json.load(file)

                        # Validate coco_data against the loaded schema to ensure its structure is correct
                        try:
                            validate(instance=coco_data, schema=self.coco_schema)
                        except ValidationError as e:
                            print(f"Validation error in {subdir}: {e.message}")
                            continue  # Skip processing this subdir if validation fails

                    # Use the helper method to load data
                    self._loadhelper_coco_data(coco_data, dataset, subdir)

        elif isinstance(source, zipfile.ZipFile):
            # Handle opened zip file case
            for subdir in subdirs:
                annotation_path = f"{subdir}/_annotations.coco.json"

                # Skip subdir if the annotation file does not exist
                if annotation_path not in source.namelist():
                    print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                    continue

                with source.open(annotation_path) as file:
                    coco_data = json.load(file)

                    # Validate coco_data against the loaded schema to ensure its structure is correct
                    try:
                        validate(instance=coco_data, schema=self.coco_schema)
                    except ValidationError as e:
                        print(f"Validation error in {subdir}: {e.message}")
                        continue  # Skip processing this subdir if validation fails

                # Use the helper method to load data
                self._loadhelper_coco_data(coco_data, dataset, subdir, source_zip=source)

        elif hasattr(source, 'read'):
            # If the source is a file-like object (e.g., BytesIO), open it as a zip file
            with zipfile.ZipFile(source, 'r') as zip_file:
                for subdir in subdirs:
                    annotation_path = f"{subdir}/_annotations.coco.json"

                    # Skip subdir if the annotation file does not exist
                    if annotation_path not in zip_file.namelist():
                        print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                        continue

                    with zip_file.open(annotation_path) as file:
                        coco_data = json.load(file)

                        # Validate coco_data against the loaded schema to ensure its structure is correct
                        try:
                            validate(instance=coco_data, schema=self.coco_schema)
                        except ValidationError as e:
                            print(f"Validation error in {subdir}: {e.message}")
                            continue  # Skip processing this subdir if validation fails

                    # Use the helper method to load data
                    self._loadhelper_coco_data(coco_data, dataset, subdir, source_zip=zip_file)

        else:
            raise ValueError("Source must be either a directory path, a file-like object, or an opened zip file.")

        return dataset

    def normalize(self, data: dict) -> dict:
        """
        Convert COCO dataset dictionary to a normalized dataset dictionary, supporting both object detection and segmentation.

        :param data: A dictionary representing the COCO dataset.
        :return: A dictionary representing the normalized dataset.
        """
        normalized_dataset = {
            "info": {
                "description": "Converted from COCO",
                "dataset_name": "COCO Dataset",
                "dataset_type": "Object Detection and Segmentation",
                "splits": {}  # Add split information if necessary
            },
            "images": [],
            "annotations": [],
            "categories": [],
            "licenses": data.get("licenses", []),
            "nc": len(data['categories']),
            "names": [cat['name'] for cat in data['categories']]
        }

        # Create category ID mapping
        category_id_map = {cat['id']: idx for idx, cat in enumerate(data['categories'])}

        # Map image IDs to normalized IDs
        image_id_map = {image['id']: idx for idx, image in enumerate(data['images'])}

        annotation_id = 1  # Initialize annotation ID

        # Convert and add images
        for image in data['images']:
            # Ensure 'width' and 'height' are present
            if 'width' not in image or 'height' not in image:
                print(f"Warning: Image {image['file_name']} is missing 'width' or 'height'. Skipping...")
                continue  # Skip images without width or height

            normalized_image = {
                "id": image_id_map[image['id']],
                "file_name": image['file_name'],
                "width": image['width'],  # Ensure width is present
                "height": image['height'],  # Ensure height is present
                "split": image.get('split', 'train'),  # Default to 'train' if split not specified
                "source_zip": image.get('source_zip'),
                "image_content": image.get('image_content')
            }
            normalized_dataset["images"].append(normalized_image)
            print(
                f"Normalized Image: {normalized_image['file_name']}, ID: {normalized_image['id']}, Width: {normalized_image['width']}, Height: {normalized_image['height']}")

        # Convert and add annotations
        for ann in data['annotations']:
            if ann['category_id'] not in category_id_map:
                print(f"Warning: Unknown category_id {ann['category_id']} for annotation ID {ann['id']}. Skipping...")
                continue  # Skip unknown categories

            if 'image_id' not in ann:
                print(f"Warning: Annotation ID {ann['id']} is missing 'image_id'. Skipping...")
                continue  # Skip annotations without image_id

            if ann['image_id'] not in image_id_map:
                print(f"Warning: Image ID {ann['image_id']} for annotation ID {ann['id']} does not exist. Skipping...")
                continue  # Skip annotations with invalid image_id

            normalized_annotation = {
                "id": annotation_id,
                "image_id": image_id_map[ann['image_id']],
                "category_id": category_id_map[ann['category_id']],
                "bbox": ann.get('bbox', []),
                "segmentation": ann.get('segmentation', []),
                "area": ann.get('area', 0.0),
                "iscrowd": ann.get('iscrowd', 0),
                "bbox_format": 'xywh'  # COCO uses xywh format
            }
            normalized_dataset["annotations"].append(normalized_annotation)
            print(
                f"Normalized Annotation ID: {normalized_annotation['id']}, Image ID: {normalized_annotation['image_id']}, Class ID: {normalized_annotation['category_id']}, BBox: {normalized_annotation['bbox']}, Segmentation: {normalized_annotation['segmentation']}")
            annotation_id += 1

        # Convert and add categories
        for cat in data['categories']:
            normalized_category = {
                "id": category_id_map[cat['id']],
                "name": cat['name'],
                "supercategory": cat.get('supercategory', 'none')
            }
            normalized_dataset["categories"].append(normalized_category)
            print(f"Normalized Category: {normalized_category['name']}, ID: {normalized_category['id']}")

        return normalized_dataset

    def convert(self, normalized_data: dict, destination: Union[str, IO[bytes]]) -> dict:
        """
        Convert the normalized dataset format back to COCO format and write it to the destination.

        :param normalized_data: A dictionary representing the normalized data.
        :param destination: File-like object (e.g., zip file) to save the COCO dataset.
        :return: A dictionary representing the COCO dataset.
        """
        # Create a COCO dataset object with the required metadata
        coco_dataset = {
            "info": {
                "description": normalized_data.get("description", "Converted YOLO Dataset"),  # Default description
                "dataset_name": normalized_data.get("dataset_name", "YOLO to COCO Conversion"),  # Default dataset name
                "dataset_type": normalized_data.get("dataset_type", "Object Detection"),  # Default dataset type
                "date_created": normalized_data.get("date_created",
                                                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            },
            "images": [],
            "annotations": [],
            "categories": [],
            "licenses": normalized_data.get("licenses", [{"id": 1, "name": "Unknown License", "url": ""}])
            # Default license
        }

        # Add images to the COCO dataset
        for normalized_image in normalized_data.get("images", []):
            coco_image = {
                "id": normalized_image.get("id"),
                "file_name": normalized_image.get("file_name"),
                "width": normalized_image.get("width", 0),
                "height": normalized_image.get("height", 0),
                "split": normalized_image.get("split", ""),
                "source_zip": normalized_image.get("source_zip", None),
                "image_content": normalized_image.get("image_content", None)
            }
            coco_dataset["images"].append(coco_image)

        annotation_id = 1
        # Add annotations to the COCO dataset
        for normalized_annotation in normalized_data.get("annotations", []):
            # Extract segmentation data, ensuring it's correctly formatted for COCO
            segmentation = normalized_annotation.get("segmentation", [])
            if segmentation:
                # Ensure segmentation is a list of lists for polygons or RLE for masks
                if not isinstance(segmentation, list) or not all(isinstance(seg, list) for seg in segmentation):
                    print(f"Warning: Invalid segmentation format for annotation ID {annotation_id}.")

            coco_annotation = {
                "id": annotation_id,
                "image_id": normalized_annotation.get("image_id"),
                "category_id": normalized_annotation.get("category_id"),
                "bbox": normalized_annotation.get("bbox", []),
                "segmentation": segmentation,  # Include segmentation data as is
                "area": normalized_annotation.get("area", 0.0),
                "iscrowd": normalized_annotation.get("iscrowd", 0)
            }
            coco_dataset["annotations"].append(coco_annotation)
            annotation_id += 1

        # Add categories to the COCO dataset
        for normalized_category in normalized_data.get("categories", []):
            coco_category = {
                "id": normalized_category.get("id"),
                "name": normalized_category.get("name"),
                "supercategory": normalized_category.get("supercategory", "none")
            }
            coco_dataset["categories"].append(coco_category)

        # Validate the COCO dataset against the loaded COCO schema
        try:
            validate(instance=coco_dataset, schema=self.coco_schema)
            print("COCO dataset successfully validated against the COCO schema.")
        except ValidationError as e:
            print(f"Validation error in COCO dataset: {e.message}")
            raise

        # Write the COCO format dataset to the destination
        self.save(coco_dataset, destination)

        return coco_dataset

    def save(self, data: dict, destination: Union[str, IO[bytes], None] = None):
        """
        Save the COCO dataset to a zip file or an in-memory buffer if the destination is None.

        :param data: A dictionary representing the COCO dataset.
        :param destination: Path, file-like object, or None where the zip archive will be written.
        """
        # Handle the case when destination is None by using BytesIO
        if destination is None:
            print("No destination provided, using in-memory buffer.")
            destination = io.BytesIO()

        is_file_like = not isinstance(destination, str)

        # Validate the COCO dataset against the loaded COCO schema before saving
        try:
            validate(instance=data, schema=self.coco_schema)
            print("COCO dataset successfully validated against the COCO schema.")
        except ValidationError as e:
            print(f"Validation error in COCO dataset: {e.message}")
            raise

        # Prepare the zip file
        if is_file_like:
            zip_file = zipfile.ZipFile(destination, 'w')
        else:
            if not destination.lower().endswith('.zip'):
                destination += '.zip'
            zip_file = zipfile.ZipFile(destination, 'w')

        with zip_file as zip_file:
            for split in [TRAIN_DIR, VALID_DIR, TEST_DIR]:
                # Filter images and annotations for the current split
                split_images = [img for img in data.get('images', []) if img.get('split') == split]
                split_annotations = [ann for ann in data.get('annotations', []) if
                                     ann.get('image_id') in {img.get('id') for img in split_images}]

                # Ensure that the 'info' section is populated
                split_coco_info = {
                    "description": data.get('info', {}).get("description", "YOLO to COCO conversion"),
                    "dataset_name": data.get('info', {}).get("dataset_name", "Converted YOLO Dataset"),
                    "dataset_type": data.get('info', {}).get("dataset_type", "Object Detection"),
                    "date_created": data.get('info', {}).get("date_created",
                                                             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                }

                # Prepare the split COCO format dictionary
                split_coco = {
                    "info": split_coco_info,
                    "licenses": data.get('licenses', []),
                    "images": [
                        {
                            "id": img.get('id'),
                            "file_name": img.get('file_name'),
                            "width": img.get('width', 0),
                            "height": img.get('height', 0),
                            "split": img.get('split', '')
                        }
                        for img in split_images
                    ],
                    "annotations": [
                        {
                            "id": ann.get('id'),
                            "image_id": ann.get('image_id'),
                            "category_id": ann.get('category_id'),
                            "bbox": ann.get('bbox', []),
                            "segmentation": ann.get('segmentation', []),
                            "area": ann.get('area', 0.0),
                            "iscrowd": ann.get('iscrowd', 0)
                        }
                        for ann in split_annotations
                    ],
                    "categories": [
                        {
                            "id": cat.get('id'),
                            "name": cat.get('name'),
                            "supercategory": cat.get('supercategory', 'none')
                        }
                        for cat in data.get('categories', [])
                    ]
                }

                # Skip if no images are found for this split
                if not split_images:
                    print(WARNING_NO_IMAGES_FOUND.format(split))
                    continue

                # Log segmentation data for validation
                for ann in split_annotations:
                    if 'segmentation' in ann and ann['segmentation']:
                        if not isinstance(ann['segmentation'], list) or not all(
                                isinstance(seg, list) for seg in ann['segmentation']):
                            print(
                                f"Warning: Segmentation data is not in the correct format for annotation ID {ann['id']}.")

                # Create the filename for the annotations JSON file
                json_filename = ANNOTATION_JSON_PATH_TEMPLATE.format(split)

                # Convert the COCO dictionary to JSON and write it to the zip file
                coco_json_content = json.dumps(split_coco, indent=4)
                zip_file.writestr(json_filename, coco_json_content)
                print(f"Saved annotations for '{split}' split with {len(split_annotations)} annotations.")

                # Save images directly in the split directory inside the zip file
                for image in split_images:
                    image_path = os.path.join(split, image.get('file_name'))

                    if image.get('image_content'):
                        zip_file.writestr(image_path, image.get('image_content'))
                        print(f"Saved image: {image_path}")
                    else:
                        print(f"Warning: No image content found for {image.get('file_name')}")

        if isinstance(destination, io.BytesIO):
            print("COCO dataset successfully saved to the in-memory zip file.")
        else:
            print(f"COCO dataset successfully saved to '{destination}'.")


class YOLOConvertor(BaseConvertor):

    def __init__(self):
        super().__init__()
        # Load the JSON schema for YOLO and Normalizer using relative paths from the current file
        yolo_schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'yolo.json')
        normalizer_schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'normalizer.json')

        # Load YOLO schema
        with open(yolo_schema_path, 'r') as schema_file:
            self.yolo_schema = json.load(schema_file)

        # Load Normalizer schema
        with open(normalizer_schema_path, 'r') as schema_file:
            self.normalizer_schema = json.load(schema_file)

    def load(self, source: Union[str, IO[bytes]]) -> dict:
        """
        Load YOLO dataset from a zip file, directory, or in-memory object.

        :param source: File-like object (e.g., a BytesIO object) or directory containing the zip archive with YOLO data.
        :return: A dictionary representing the YOLO dataset populated with the data.
        """
        subdirs = [TRAIN_DIR, VALID_DIR, TEST_DIR]
        dataset = {
            "images": [],
            "class_names": [],
            "licenses": []
        }

        if isinstance(source, str):
            # Case 1: If the source is a file path (zip file)
            if zipfile.is_zipfile(source):
                with zipfile.ZipFile(source, 'r') as zip_file:
                    # Load class names from data.yaml if available
                    self._loadhelper_yolo_from_zip(zip_file, dataset, subdirs)
            else:
                # Case 2: If the source is a directory path
                self._loadhelper_yolo_from_directory(source, dataset, subdirs)

        elif isinstance(source, zipfile.ZipFile):
            # Handle opened zip file case
            self._loadhelper_yolo_from_zip(source, dataset, subdirs)

        elif hasattr(source, 'read'):
            # Handle in-memory file-like object (e.g., BytesIO)
            with zipfile.ZipFile(source) as zip_file:
                self._loadhelper_yolo_from_zip(zip_file, dataset, subdirs)

        else:
            raise ValueError(INVALID_SOURCE_ERROR)

        # Validate the loaded dataset against the yolo.json schema
        try:
            validate(instance=dataset, schema=self.yolo_schema)
            print("YOLO dataset successfully validated against the YOLO schema.")
        except ValidationError as e:
            print(f"Validation error: {e.message}")

        return dataset

    def _loadhelper_yolo_from_zip(self, zip_file: zipfile.ZipFile, dataset: dict, subdirs: list):
        if YOLO_YAML_FILENAME in zip_file.namelist():
            with zip_file.open(YOLO_YAML_FILENAME) as file:
                data_yaml = yaml.safe_load(file)
                dataset["class_names"] = data_yaml.get('names', [])
                dataset["licenses"] = [{"id": 1, "name": data_yaml.get('license', 'Unknown License'),
                                        "url": data_yaml.get('license_url', '')}]

        for subdir in subdirs:
            image_dir = YOLO_IMAGE_DIR_PATH_TEMPLATE.format(subdir)
            label_dir = YOLO_LABEL_DIR_PATH_TEMPLATE.format(subdir)

            if not any(path.startswith(image_dir) for path in zip_file.namelist()):
                continue

            for img_path in zip_file.namelist():
                if img_path.startswith(image_dir) and (img_path.endswith('.jpg') or img_path.endswith('.png')):
                    image_file_name = os.path.basename(img_path)
                    image_path = f"{subdir}/images/{image_file_name}"
                    label_file_name = image_file_name.replace('.jpg', '.txt').replace('.png', '.txt')
                    label_path = f"{subdir}/labels/{label_file_name}"

                    if image_path in zip_file.namelist():
                        with zip_file.open(image_path) as img_file:
                            image_content = img_file.read()

                        yolo_image = {
                            "file_name": image_file_name,
                            "annotations": [],
                            "split": subdir,
                            "source_zip": zip_file,
                            "image_content": image_content
                        }

                        if label_path in zip_file.namelist():
                            with zip_file.open(label_path) as label_file:
                                for line in io.TextIOWrapper(label_file, encoding='utf-8'):
                                    values = list(map(float, line.strip().split()))
                                    if len(values) == 5:
                                        # Handle bounding box annotations
                                        class_id, cx, cy, w, h = values
                                        yolo_annotation = {
                                            "class_id": int(class_id),
                                            "cx": cx,
                                            "cy": cy,
                                            "width": w,
                                            "height": h
                                        }
                                        yolo_image["annotations"].append(yolo_annotation)
                                    elif len(values) > 5:
                                        # Handle segmentation data
                                        class_id = int(values[0])
                                        segmentation = values[
                                                       1:]  # All remaining values are segmentation points (x1, y1, x2, y2, ...)
                                        yolo_annotation = {
                                            "class_id": class_id,
                                            "segmentation": segmentation
                                        }
                                        yolo_image["annotations"].append(yolo_annotation)

                        dataset["images"].append(yolo_image)

    def _loadhelper_yolo_from_directory(self, source: str, dataset: dict, subdirs: list):
        """
        Helper method to load YOLO data from a directory.
        """
        for subdir in subdirs:
            image_dir = os.path.join(source, subdir, YOLO_IMAGES_SUBDIR)
            label_dir = os.path.join(source, subdir, YOLO_LABELS_SUBDIR)

            # Skip subdir if images or labels folders do not exist
            if not os.path.isdir(image_dir) or not os.path.isdir(label_dir):
                print(WARNING_MISSING_DIR.format(subdir))
                continue

            # Load images and annotations from the directory
            for image_file_name in os.listdir(image_dir):
                if image_file_name.endswith('.jpg') or image_file_name.endswith('.png'):
                    image_path = os.path.join(image_dir, image_file_name)
                    label_file_name = image_file_name.replace('.jpg', '.txt').replace('.png', '.txt')
                    label_path = os.path.join(label_dir, label_file_name)

                    # Read image content
                    with open(image_path, 'rb') as img_file:
                        image_content = img_file.read()

                    yolo_image = {
                        "file_name": image_file_name,
                        "annotations": [],
                        "split": subdir,
                        "image_content": image_content
                    }

                    # Load annotations if the corresponding label file exists
                    if os.path.isfile(label_path):
                        with open(label_path, 'r') as label_file:
                            for line in label_file:
                                values = list(map(float, line.strip().split()))
                                if len(values) == 5:
                                    # Handle bounding box annotations
                                    class_id, cx, cy, w, h = values
                                    yolo_annotation = {
                                        "class_id": int(class_id),
                                        "cx": cx,
                                        "cy": cy,
                                        "width": w,
                                        "height": h
                                    }
                                    yolo_image["annotations"].append(yolo_annotation)
                                elif len(values) > 5:
                                    # Handle segmentation data
                                    class_id = int(values[0])
                                    segmentation = values[
                                                   1:]  # All remaining values are segmentation points (x1, y1, x2, y2, ...)
                                    yolo_annotation = {
                                        "class_id": class_id,
                                        "segmentation": segmentation
                                    }
                                    yolo_image["annotations"].append(yolo_annotation)

                    dataset["images"].append(yolo_image)

    def normalize(self, data: dict) -> dict:
        """
        Normalize the YOLO dataset into a standard format, handling both object detection and segmentation datasets.

        :param data: A dictionary representing the YOLO dataset.
        :return: A dictionary representing the normalized dataset.
        """
        # Determine the dataset type (Object Detection or Segmentation)
        dataset_type = "Object Detection"
        for image in data.get('images', []):
            for ann in image.get('annotations', []):
                if 'segmentation' in ann and ann['segmentation']:
                    dataset_type = "Segmentation"
                    break  # Stop checking further once segmentation is detected

        # Create the normalized dataset structure with metadata
        normalized_dataset = {
            "info": {
                "description": f"Converted from YOLO Dataset ({dataset_type})",
                "dataset_name": "YOLO Dataset",
                "dataset_type": dataset_type,  # Use the detected dataset type
                "date_created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "splits": {},
            },
            "images": [],
            "annotations": [],
            "categories": [],
            "licenses": data.get("licenses", []),
            "nc": len(data.get("class_names", [])),
            "names": data.get("class_names", []),
        }

        image_id_map = {}
        annotation_id = 1

        # Convert images
        for idx, yolo_image in enumerate(data.get('images', [])):
            image_content = yolo_image.get('image_content')
            file_name = yolo_image['file_name']
            split = yolo_image['split']

            if image_content:
                width, height = get_image_dimensions(image_content)

            if width == 0 or height == 0:
                continue

            normalized_image = {
                "id": idx,
                "file_name": file_name,
                "width": width,
                "height": height,
                "split": split,
                "source_zip": yolo_image.get('source_zip'),
                "image_content": image_content
            }
            image_id_map[file_name] = idx
            normalized_dataset["images"].append(normalized_image)

        # Convert annotations
        for yolo_image in data.get('images', []):
            image_id = image_id_map.get(yolo_image['file_name'])
            if image_id is None:
                continue

            width = normalized_dataset["images"][image_id]["width"]
            height = normalized_dataset["images"][image_id]["height"]

            for ann in yolo_image.get('annotations', []):
                if 'segmentation' in ann and ann['segmentation']:
                    # Handle segmentation data
                    segmentation = [[coord * width if i % 2 == 0 else coord * height for i, coord in
                                     enumerate(ann['segmentation'])]]
                    area = cv2.contourArea(np.array(segmentation).reshape(-1, 2).astype(np.float32))
                    bbox = cv2.boundingRect(np.array(segmentation).reshape(-1, 2).astype(np.float32))
                    x, y, w, h = bbox
                else:
                    # Convert bbox from YOLO format (cx, cy, w, h) to COCO format (x, y, w, h)
                    cx, cy, w, h = ann['cx'], ann['cy'], ann['width'], ann['height']
                    x = (cx - w / 2) * width
                    y = (cy - h / 2) * height
                    bbox = [x, y, w * width, h * height]
                    segmentation = []  # No segmentation data in this case
                    area = w * h * width * height

                normalized_annotation = {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": ann['class_id'],
                    "bbox": bbox,
                    "segmentation": segmentation,
                    "area": area,
                    "iscrowd": 0,
                    "bbox_format": "xywh"
                }
                normalized_dataset["annotations"].append(normalized_annotation)
                annotation_id += 1

        # Convert categories
        for idx, class_name in enumerate(data.get("class_names", [])):
            normalized_category = {
                "id": idx,
                "name": class_name,
                "supercategory": "none"
            }
            normalized_dataset["categories"].append(normalized_category)

        # Validate the normalized dataset
        try:
            validate(instance=normalized_dataset, schema=self.normalizer_schema)
            print("Normalized dataset successfully validated against the Normalizer schema.")
        except ValidationError as e:
            print(f"Validation error in normalized dataset: {e.message}")

        return normalized_dataset

    def convert(
            self,
            normalized_data: dict,
            destination: Union[str, IO[bytes]]
    ) -> dict:
        """
        Convert NormalizedDataset to YOLO format and save to destination.

        :param normalized_data: Normalized dataset as a dictionary.
        :param destination: Path or BytesIO object where the zip archive will be written.
        :return: YOLODataset object.
        """
        # Initialize a list to store YOLO-format images
        yolo_images = []

        # Create a mapping from image ID to annotations
        image_to_annotations = {}
        for annotation in normalized_data.get('annotations', []):
            if annotation['image_id'] not in image_to_annotations:
                image_to_annotations[annotation['image_id']] = []
            image_to_annotations[annotation['image_id']].append(annotation)

        print(f"Total Images to Convert: {len(normalized_data.get('images', []))}")
        print(f"Total Annotations: {len(normalized_data.get('annotations', []))}\n")

        # Process each image and its corresponding annotations
        for normalized_image in normalized_data.get('images', []):
            annotations = image_to_annotations.get(normalized_image['id'], [])

            print(f"Processing Image: {normalized_image['file_name']}, Annotations Count: {len(annotations)}")

            # List of YOLO-format annotations for this image
            yolo_annotations = []

            for normalized_annotation in annotations:
                # Ensure 'width' and 'height' are present
                if 'width' not in normalized_image or 'height' not in normalized_image:
                    print(
                        f"Error: Missing 'width' or 'height' for image {normalized_image['file_name']}. Skipping this image.")
                    break  # Skip to next image

                img_width = normalized_image['width']
                img_height = normalized_image['height']

                # Check if 'bbox' exists or 'segmentation' exists
                has_bbox = 'bbox' in normalized_annotation and normalized_annotation['bbox']
                has_segmentation = 'segmentation' in normalized_annotation and normalized_annotation['segmentation']

                if not has_bbox and not has_segmentation:
                    print(
                        f"Warning: No bbox or segmentation found for annotation in image {normalized_image['file_name']}.")
                    continue  # Skip annotations without bbox or segmentation

                # Process bounding box if present
                if has_bbox:
                    if normalized_annotation.get('bbox_format') == 'xywh':  # COCO format
                        x, y, w, h = normalized_annotation['bbox']
                        # Convert COCO bbox (xywh) to YOLO bbox (cxcywh)
                        cx = (x + w / 2) / img_width
                        cy = (y + h / 2) / img_height
                        width = w / img_width
                        height = h / img_height
                    else:
                        print(f"Warning: Unsupported bbox format: {normalized_annotation.get('bbox_format')}")
                        continue

                    # Ensure values are between 0 and 1 (for YOLO format)
                    cx = min(max(cx, 0.0), 1.0)
                    cy = min(max(cy, 0.0), 1.0)
                    width = min(max(width, 0.0), 1.0)
                    height = min(max(height, 0.0), 1.0)

                    # Round values to six decimal places
                    cx = round(cx, 6)
                    cy = round(cy, 6)
                    width = round(width, 6)
                    height = round(height, 6)

                    print(
                        f"  Annotation Class ID: {normalized_annotation['category_id']}, BBox: ({cx}, {cy}, {width}, {height})")

                    # Create a YOLO annotation dictionary entry
                    yolo_annotation = {
                        'class_id': normalized_annotation['category_id'],
                        'bbox': [cx, cy, width, height],
                        'segmentation': normalized_annotation.get('segmentation', [])
                    }
                    yolo_annotations.append(yolo_annotation)

                # Process segmentation if present
                if has_segmentation and normalized_annotation['segmentation']:
                    # Handle segmentation annotations
                    # Assuming segmentation is a list of polygons (list of lists)
                    for seg in normalized_annotation['segmentation']:
                        if not isinstance(seg, list):
                            print(
                                f"Warning: Segmentation data is not a list of lists for image {normalized_image['file_name']}. Skipping this segmentation.")
                            continue
                        try:
                            normalized_segmentation = [
                                coord / img_width if i % 2 == 0 else coord / img_height
                                for i, coord in enumerate(seg)
                                if isinstance(coord, (int, float))
                            ]
                            print(
                                f"  Processing Segmentation for Class ID: {normalized_annotation['category_id']}, Segmentation: {normalized_segmentation}")

                            # Prepare the line to include class_id followed by segmentation points
                            seg_str = " ".join(f"{coord:.6f}" for coord in normalized_segmentation)
                            seg_annotation = {
                                'class_id': normalized_annotation['category_id'],
                                'segmentation': [normalized_segmentation],  # Wrap in list
                                'bbox': []  # No bbox for segmentation-only annotations
                            }
                            yolo_annotations.append(seg_annotation)
                        except Exception as e:
                            print(f"Error processing segmentation for image {normalized_image['file_name']}: {e}")

            if len(yolo_annotations) == 0:
                print(f"Warning: No annotations found for image {normalized_image['file_name']}")

            # Create the image entry, including 'width' and 'height'
            yolo_image = {
                "file_name": normalized_image['file_name'],
                "annotations": yolo_annotations,
                "split": normalized_image['split'],  # Include split attribute
                "source_zip": normalized_image.get('source_zip'),
                "image_content": normalized_image.get('image_content'),
                "width": normalized_image['width'],
                "height": normalized_image['height']
            }

            yolo_images.append(yolo_image)

        # Prepare YOLO dataset
        yolo_dataset = {
            "images": yolo_images,
            "class_names": normalized_data.get('names', [])
        }

        # Save the YOLO dataset to destination
        self.save(yolo_dataset, destination)

        return yolo_dataset

    def save(self, data: dict, destination: Union[str, io.BytesIO, None] = None):
        """
        Save YOLO dataset to a zip file.

        :param data: A dictionary representing the YOLO dataset.
        :param destination: Path, BytesIO object, or None where the zip archive will be written.
        """
        # Validate the data against the YOLO schema before saving
        try:
            validate(instance=data, schema=self.yolo_schema)
            print("YOLO dataset successfully validated against the YOLO schema.")
        except ValidationError as e:
            print(f"Validation error in YOLO dataset: {e.message}")
            raise

        # If destination is None, create an in-memory BytesIO zip file
        if destination is None:
            destination = io.BytesIO()

        with zipfile.ZipFile(destination, 'w') as zip_file:
            # Create the YAML structure with correct paths and names formatting
            dataset_yaml = {
                'train': '../train/images',
                'val': '../valid/images',
                'test': '../test/images',
                'nc': len(data['class_names']),
                'names': data['class_names']
            }

            # Use yaml.safe_dump to generate the YAML content
            yaml_content = yaml.safe_dump(
                dataset_yaml,
                default_flow_style=False,
                sort_keys=False
            )

            # Manually adjust the 'names' field to be formatted with single quotes inside brackets
            yaml_lines = yaml_content.splitlines()
            formatted_lines = []
            for line in yaml_lines:
                if line.startswith('names:'):
                    # Correctly format the names list with single quotes
                    names_str = ', '.join([f"'{name}'" for name in data['class_names']])
                    formatted_lines.append(f"names: [{names_str}]")
                elif not line.startswith('- '):  # Avoid adding extra list items
                    formatted_lines.append(line)
            yaml_content = '\n'.join(formatted_lines)

            # Write the corrected YAML content to the zip file
            zip_file.writestr("data.yaml", yaml_content)
            print("Saved data.yaml")

            # Save images and labels into respective directories within the zip file
            for image in data['images']:
                split_dir = f"{image['split']}/images"
                labels_dir = f"{image['split']}/labels"

                # Save image content if available
                if image.get('image_content'):
                    zip_file.writestr(os.path.join(split_dir, image['file_name']), image['image_content'])
                    print(f"Saved image: {os.path.join(split_dir, image['file_name'])}")
                else:
                    print(f"Warning: No image content available for {image['file_name']}")

                # Create and add the label file to the zip archive
                label_file_name = os.path.splitext(image['file_name'])[0] + '.txt'
                label_zip_path = os.path.join(labels_dir, label_file_name)  # Save to the labels folder
                label_content = ""

                # Ensure 'width' and 'height' are present
                if 'width' not in image or 'height' not in image:
                    print(
                        f"Error: Missing 'width' or 'height' for image {image['file_name']}. Skipping label creation.")
                    continue

                width = image['width']
                height = image['height']

                # Generate label content
                for annotation in image.get('annotations', []):
                    if isinstance(annotation, dict):
                        if 'segmentation' in annotation and annotation['segmentation']:
                            # Handle segmentation annotations
                            try:
                                # Check if segmentation is a list of lists
                                if not all(isinstance(seg, list) for seg in annotation['segmentation']):
                                    print(
                                        f"Warning: Segmentation data is not a list of lists for image {image['file_name']}. Skipping this segmentation.")
                                    continue

                                # Normalize and flatten all polygons
                                normalized_segmentation = [
                                    coord / width if i % 2 == 0 else coord / height
                                    for seg in annotation['segmentation']
                                    for i, coord in enumerate(seg)
                                    if isinstance(coord, (int, float))
                                ]

                                # Prepare the line to include class_id followed by segmentation points
                                seg_str = " ".join(f"{coord:.6f}" for coord in normalized_segmentation)
                                line = f"{annotation['class_id']} {seg_str}"
                                label_content += line + "\n"
                            except Exception as e:
                                print(f"Error processing segmentation for image {image['file_name']}: {e}")
                        elif 'bbox' in annotation and annotation['bbox']:
                            # Handle bounding box annotations
                            bbox = annotation['bbox']
                            if isinstance(bbox, list) and len(bbox) == 4:
                                cx, cy, width_norm, height_norm = bbox
                                # Prepare the line to include class_id and normalized bbox coordinates
                                line = f"{annotation['class_id']} {cx:.6f} {cy:.6f} {width_norm:.6f} {height_norm:.6f}"
                                label_content += line + "\n"
                            else:
                                print(f"Warning: Invalid bbox format for annotation in image {image['file_name']}.")
                        else:
                            print(
                                f"Warning: Missing bbox or segmentation data for annotation in image {image['file_name']}.")
                    else:
                        print(f"Warning: Annotation for image {image['file_name']} is not a dictionary. Skipping...")

                # Ensure the label content is not empty before writing to file
                if label_content.strip():
                    zip_file.writestr(label_zip_path, label_content)
                    print(f"Saved label file: {label_zip_path} with {len(image.get('annotations', []))} annotations")
                else:
                    print(f"Warning: Empty label file for {image['file_name']}")

        # Final success message
        if isinstance(destination, io.BytesIO):
            print("YOLO dataset successfully written to the in-memory zip file.")
        else:
            print(f"YOLO dataset successfully saved to '{destination}'.")

        # Return the in-memory zip file if destination was None
        if isinstance(destination, io.BytesIO):
            destination.seek(0)
            return destination

