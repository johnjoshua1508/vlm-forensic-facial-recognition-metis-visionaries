# Search System Export

This folder contains all necessary components to run the image and text search system.

## Contents:
- faiss_index_final.bin: The FAISS index for similarity search.
- path_mapping.pkl: Mapping from index positions to subject IDs.
- metadata.csv: Complete metadata for all images.
- search_config.json: Configuration parameters for the system.
- sample_images/: A set of sample images for testing.

## Setup Instructions:
1. Install required packages: `pip install streamlit torch torchvision faiss-cpu clip-by-openai pandas pillow`
2. Place the app.py file (your Streamlit UI) in the same directory as this export.
3. Run: `streamlit run app.py`

Note: For full functionality, ensure that the complete image dataset is available.
