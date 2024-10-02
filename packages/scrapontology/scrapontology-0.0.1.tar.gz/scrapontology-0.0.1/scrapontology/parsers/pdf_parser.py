from typing import List, Dict, Any, Optional, TypedDict
from .base_parser import BaseParser
from ..primitives import Entity, Relation
import base64
import os
import tempfile
import json
from .prompts import DIGRAPH_EXAMPLE_PROMPT, JSON_SCHEMA_PROMPT, RELATIONS_PROMPT, UPDATE_ENTITIES_PROMPT, EXTRACT_ENTITIES_CODE_PROMPT, FIX_CODE_PROMPT
from PIL import Image
import inspect
import subprocess
import logging
import re
from ..llm_client import LLMClient
from requests.exceptions import ReadTimeout
from langgraph.graph import StateGraph, START, END

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def encode_image(image_path: str) -> str:
    """
    Encodes an image to a base64 string.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def is_poppler_installed() -> bool:
    """Check if pdftoppm is available in the system's PATH."""
    try:
        subprocess.run(['pdftoppm', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def list_directory(path: str):
    """List contents of a directory."""
    try:
        files = os.listdir(path)
        for f in files:
            logging.info(f"File in directory: {os.path.join(path, f)}")
    except Exception as e:
        logging.error(f"Error listing directory {path}: {e}")

def load_pdf_as_images(pdf_path: str) -> Optional[List[Image.Image]]:
    """
    Converts a PDF file to a list of images, one per page, using pdftoppm.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        Optional[List[Image.Image]]: A list of images if successful, None otherwise.
    """
    logging.info(f"Processing PDF: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        logging.error(f"PDF file not found: {pdf_path}")
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not is_poppler_installed():
        logging.error("Poppler is not installed.")
        raise EnvironmentError("Poppler is not installed. Please install it to use this functionality.")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_prefix = os.path.join(temp_dir, 'pdf_page')
        logging.info(f"Output prefix: {output_prefix}")

        command = ['pdftoppm', pdf_path, output_prefix, '-png']
        logging.info(f"Running command: {' '.join(command)}")

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            logging.info("PDF conversion completed successfully")

            logging.info("Listing directory contents after conversion:")
            list_directory(temp_dir)

            images = []
            page_num = 1
            while True:
                image_path = f"{output_prefix}-{page_num}.png"
                if not os.path.exists(image_path):
                    break
                logging.info(f"Loading image: {image_path}")
                
                # Using context manager to ensure the file is closed properly after use
                with Image.open(image_path) as img:
                    # Append a copy of the image to the list, closing the original image
                    images.append(img.copy())
                page_num += 1

            return images

        except subprocess.CalledProcessError as e:
            logging.error(f"Error converting PDF: {e}")
            logging.error(f"Command output: {e.output}")
            logging.error(f"Command error: {e.stderr}")
            return None

def save_image_to_temp(image: Image.Image) -> str:
    """
    Saves an image to a temporary file.

    Args:
        image (Image.Image): The image to save.

    Returns:
        str: The path to the temporary file.
    """
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        image.save(temp_file.name, 'JPEG')
        return temp_file.name

def process_pdf(pdf_path: str) -> Optional[List[str]]:
    """
    Processes a PDF file and converts each page to a base64 encoded image.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        List[str] or None: A list of base64 encoded images if successful, None otherwise.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Load PDF as images
    images = load_pdf_as_images(pdf_path)
    if not images:
        return None

    base64_images = []

    for page_num, image in enumerate(images, start=1):
        temp_image_path = None
        try:
            # Save image to temporary file
            temp_image_path = save_image_to_temp(image)
            
            # Convert image to base64
            base64_image = encode_image(temp_image_path)
            base64_images.append(base64_image)

        except Exception as e:
            logging.error(f"Error processing page {page_num}: {e}")
        finally:
            # Ensure temp file is deleted even in case of an error
            if temp_image_path and os.path.exists(temp_image_path):
                os.unlink(temp_image_path)

    return base64_images

class PDFState(TypedDict):
    file_path: str
    base64_images: List[str]
    entities: List[Entity]
    relations: List[Relation]
    json_schema: Dict[str, Any]

class PDFParser(BaseParser):
    def __init__(self, llm_client: LLMClient):
        super().__init__(llm_client)
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(PDFState)
        
        builder.add_node("process_pdf", self._process_pdf)
        builder.add_node("extract_entities", self._extract_entities)
        builder.add_node("extract_relations", self._extract_relations)
        builder.add_node("update_entities", self._update_entities)
        
        builder.add_edge(START, "process_pdf")
        builder.add_edge("process_pdf", "extract_entities")
        builder.add_edge("extract_entities", "extract_relations")
        builder.add_edge("extract_relations", "update_entities")
        builder.add_edge("update_entities", END)
        
        return builder.compile()

    def _process_pdf(self, state: PDFState) -> PDFState:
        file_path = state['file_path']
        base64_images = process_pdf(file_path)
        return {"base64_images": base64_images, **state}

    def _extract_entities(self, state: PDFState) -> PDFState:
        base64_images = state['base64_images']
        entities_json_schema = self._generate_json_schema(base64_images)
        entities = self._extract_entities_from_schema(entities_json_schema)
        return {"entities": entities, "json_schema": entities_json_schema, **state}

    def _extract_relations(self, state: PDFState) -> PDFState:
        entities = state['entities']
        relations = self._extract_relations_from_entities(entities)
        return {"relations": relations, **state}

    def _update_entities(self, state: PDFState) -> PDFState:
        existing_entities = state.get('entities', [])
        new_entities = self._update_entities_list(existing_entities)
        return {"entities": new_entities, **state}

    def parse(self, file_path: str) -> Dict[str, Any]:
        initial_state = PDFState(file_path=file_path, base64_images=[], entities=[], relations=[], json_schema={})
        final_state = self.graph.invoke(initial_state)
        return {
            "entities": final_state['entities'],
            "relations": final_state['relations'],
            "json_schema": final_state['json_schema']
        }

    # Implement the helper methods (_generate_json_schema, _extract_entities_from_schema, etc.) here
    # ...