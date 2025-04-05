from database import db
from bson import ObjectId
import datetime
import pandas as pd
from config import Config

class Subject:
    def __init__(self, subject_id, metadata, front_image_path, side_image_path, embedding=None):
        self.subject_id = subject_id
        self.metadata = metadata
        self.front_image_path = front_image_path
        self.side_image_path = side_image_path
        self.embedding = embedding
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
    
    def save(self):
        subject_data = {
            "subject_id": self.subject_id,
            "metadata": self.metadata,
            "front_image_path": self.front_image_path,
            "side_image_path": self.side_image_path,
            "embedding": self.embedding.tolist() if self.embedding is not None else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
        result = db.subjects.update_one(
            {"subject_id": self.subject_id},
            {"$set": subject_data},
            upsert=True
        )
        
        return result.upserted_id or result.modified_count
    
    @classmethod
    def find_by_id(cls, subject_id):
        subject_data = db.subjects.find_one({"subject_id": subject_id})
        if not subject_data:
            return None
        
        return cls(
            subject_id=subject_data["subject_id"],
            metadata=subject_data["metadata"],
            front_image_path=subject_data["front_image_path"],
            side_image_path=subject_data["side_image_path"],
            embedding=subject_data.get("embedding")
        )
    
    @classmethod
    def find_all(cls):
        subjects = []
        for subject_data in db.subjects.find():
            subjects.append(cls(
                subject_id=subject_data["subject_id"],
                metadata=subject_data["metadata"],
                front_image_path=subject_data["front_image_path"],
                side_image_path=subject_data["side_image_path"],
                embedding=subject_data.get("embedding")
            ))
        return subjects
    
    @classmethod
    def delete_by_id(cls, subject_id):
        result = db.subjects.delete_one({"subject_id": subject_id})
        return result.deleted_count
    
    @classmethod
    def get_next_id(cls):
        """
        Generate a new unique ID by finding the last ID in the dataset and incrementing it by 1.
        Reads the CSV file directly to get the latest IDs.
        """
        try:
            # Read the CSV file to get all IDs
            metadata_path = Config.METADATA_CSV_PATH
            all_ids = []
            
            # Read the CSV in chunks to avoid loading the entire file
            for chunk in pd.read_csv(metadata_path, chunksize=1000):
                all_ids.extend(chunk['ID'].astype(str).tolist())
            
            if not all_ids:
                return "A00001"  # Default if no IDs exist
            
            # Sort the IDs to find the last one
            # This assumes IDs are in a format where alphabetical sorting works
            sorted_ids = sorted(all_ids)
            last_id = sorted_ids[-1]
            
            # Extract the letter prefix and numeric part
            prefix = ''.join(c for c in last_id if c.isalpha())
            numeric_part = ''.join(c for c in last_id if c.isdigit())
            
            if not prefix or not numeric_part:
                # Fallback if the ID format is unexpected
                return f"Y{int(datetime.datetime.now().timestamp())}"
            
            # Increment the numeric part
            next_num = int(numeric_part) + 1
            # Format with the same number of leading zeros
            next_id = f"{prefix}{next_num:0{len(numeric_part)}d}"
            
            return next_id
        except Exception as e:
            print(f"Error generating unique ID: {e}")
            # Fallback to a timestamp-based ID
            return f"Y{int(datetime.datetime.now().timestamp())}"

    @classmethod
    def get_metadata_for_id(cls, subject_id):
        """
        Get metadata for a specific subject ID from the CSV file
        
        Args:
            subject_id: ID of the subject
            
        Returns:
            dict: Metadata for the subject or None if not found
        """
        try:
            # Use pandas to read just the row with the matching ID
            metadata_path = Config.METADATA_CSV_PATH
            # Read the CSV in chunks to avoid loading the entire file
            for chunk in pd.read_csv(metadata_path, chunksize=1000):
                # Find rows matching the ID
                meta = chunk[chunk['ID'].astype(str) == subject_id]
                if not meta.empty:
                    # Convert to dictionary
                    return meta.iloc[0].to_dict()
            # If we get here, no matching ID was found
            return None
        except Exception as e:
            print(f"Error accessing metadata for ID {subject_id}: {e}")
            return None

