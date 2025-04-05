import faiss
import numpy as np
import os
import pickle
from config import Config
from models import Subject

class FaissIndex:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FaissIndex, cls).__new__(cls)
            cls._instance._load_index()
        
        return cls._instance
    
    def _load_index(self):
        """Load the FAISS index and path mapping"""
        try:
            # Load the FAISS index
            self.index = faiss.read_index(os.path.join(Config.SEARCH_SYSTEM_DIR, "faiss_index_final.bin"))
            
            # Load the path mapping
            with open(os.path.join(Config.SEARCH_SYSTEM_DIR, "path_mapping.pkl"), "rb") as f:
                self.path_mapping = pickle.load(f)
            
            print(f"Loaded FAISS index with {self.index.ntotal} vectors")
            print(f"Loaded path mapping with {len(self.path_mapping)} entries")
            
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            # Initialize empty index and mapping
            self.index = faiss.IndexFlatL2(512)  # CLIP embeddings are 512-dimensional
            self.path_mapping = {}
    
    def save_index(self):
        """Save the FAISS index and path mapping to disk"""
        try:
            # Save the FAISS index
            faiss.write_index(self.index, os.path.join(Config.SEARCH_SYSTEM_DIR, "faiss_index_final.bin"))
            
            # Save the path mapping
            with open(os.path.join(Config.SEARCH_SYSTEM_DIR, "path_mapping.pkl"), "wb") as f:
                pickle.dump(self.path_mapping, f)
            
            return True
        except Exception as e:
            print(f"Error saving FAISS index: {e}")
            return False
    
    def add_embedding(self, subject_id, embedding):
        """
        Add a new embedding to the index
        
        Args:
            subject_id: ID of the subject
            embedding: Numpy array embedding
            
        Returns:
            bool: Success status
        """
        try:
            # Reshape embedding for FAISS
            embedding = embedding.astype(np.float32).reshape(1, -1)
            
            # Add to FAISS index
            self.index.add(embedding)
            
            # Update path mapping
            new_idx = len(self.path_mapping)
            self.path_mapping[new_idx] = subject_id
            
            # Save the updated index
            self.save_index()
            
            return True
        except Exception as e:
            print(f"Error adding embedding: {e}")
            return False
    
    def search(self, embedding, top_k=5, threshold=None):
        """
        Search for similar embeddings
        
        Args:
            embedding: Numpy array query embedding
            top_k: Number of results to return
            threshold: Optional distance threshold
            
        Returns:
            list: List of (subject_id, distance) tuples
        """
        try:
            # Reshape embedding for FAISS
            embedding = embedding.astype(np.float32).reshape(1, -1)
            
            # Search the index
            distances, indices = self.index.search(embedding, top_k)
            
            # Apply threshold if provided
            if threshold is not None and distances[0][0] > threshold:
                return []
            
            # Map indices to subject IDs
            results = [(self.path_mapping[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
            
            return results
        except Exception as e:
            print(f"Error searching index: {e}")
            return []
    
    def get_index_size(self):
        """Get the number of vectors in the index"""
        return self.index.ntotal

