
import faiss
import pickle
import pandas as pd
import json
import os

try:
    index = faiss.read_index("faiss_index_final.bin")
    print("✓ FAISS index loaded successfully")
    
    with open("path_mapping.pkl", "rb") as f:
        path_mapping = pickle.load(f)
    print(f"✓ Path mapping loaded successfully ({len(path_mapping)} items)")
    
    metadata_df = pd.read_csv("metadata.csv")
    print(f"✓ Metadata loaded successfully ({len(metadata_df)} rows)")
    
    with open("search_config.json", "r") as f:
        config = json.load(f)
    print("✓ Config loaded successfully")
    
    print("\nAll components loaded successfully! System is ready to use.")
except Exception as e:
    print(f"Error: {e}")
