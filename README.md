### Forensic Facial Recognition System - Visual Search System Using Vision-Language Models (VLMs)

## Project Overview

This project implements a visual search engine that leverages Vision-Language Models (VLMs), specifically CLIP (Contrastive Language-Image Pre-training), to retrieve relevant images based on both textual queries and sample images. The system creates a shared embedding space for images and text, enabling powerful multi-modal search capabilities in a forensic context.

## Problem Statement

Traditional image search systems rely on manually tagged metadata or basic visual features, which are limited in their ability to understand semantic content. This project addresses this limitation by:

1. Creating a unified embedding space where both images and text can be represented
2. Enabling search across modalities (text-to-image and image-to-image)
3. Providing a scalable solution for large image databases
4. Applying these capabilities to forensic facial recognition


## Domain Application: Forensic Facial Recognition

While the underlying technology can be applied to various domains, this implementation focuses on forensic facial recognition, helping law enforcement agencies to:

- Search through mugshot databases efficiently
- Match suspect descriptions to potential images
- Find similar faces based on a reference image
- Scale to handle large datasets with minimal performance degradation


## Key Objectives

### 1. Shared Embedding Space

- Utilize CLIP, a state-of-the-art VLM, to generate embeddings for both images and text
- Ensure semantically similar images and textual descriptions occupy nearby regions in the embedding space
- Fine-tune the model to better handle facial recognition tasks


### 2. Indexing & Retrieval

- Implement an efficient indexing pipeline using FAISS to store and retrieve image embeddings at scale
- Support fast similarity search methods (k-nearest neighbors, approximate nearest neighbors) to handle large datasets
- Optimize for both accuracy and search speed


### 3. Multi-Modal Querying

- Support multiple query types:

- Text Query: "Find a person with a square face and brown hair"
- Image Query: Find visually similar faces to a given example
- Handle advanced or compositional queries when possible


### 4. Evaluation & Metrics

- Assess retrieval performance using common image retrieval metrics (precision@k, recall@k, mean average precision)
- Perform qualitative analysis of retrieval quality (do the returned images match the query context?)


## Technical Implementation

### Core Components

- **CLIP Model**: Provides the foundation for the shared embedding space between images and text
- **FAISS Index**: High-performance similarity search for fast retrieval at scale
- **Flask Web Interface**: User-friendly interface for uploading images and displaying results
- **Preprocessing Pipeline**: Handles image normalization and feature extraction


### Technologies Used

- Python for backend processing
- PyTorch for deep learning and CLIP implementation
- FAISS for efficient similarity search
- Flask for web interface
- OpenCV for image processing


## Challenges Addressed

### 1. Embedding Alignment

- Ensuring robust alignment between text embeddings and image embeddings
- Handling domain shifts between CLIP's training data and forensic images


### 2. Data Acquisition & Diversity

- Curating a sufficiently large and diverse image dataset for meaningful search results
- Balancing coverage with label accuracy and textual annotations


### 3. Scalability & Performance

- Managing large-scale image datasets (tens of thousands to millions of images)
- Optimizing latency for real-time or near real-time search experiences


### 4. Semantic Granularity

- Handling nuanced or complex descriptions of facial features
- Dealing with subtle visual differences between similar faces


### 5. User Experience

- Designing intuitive interfaces for multi-modal searches
- Providing clear feedback mechanisms when queries fail or return irrelevant results



## Expected Outcomes

### Functional Visual Search Engine

- Users can input textual queries or provide an image sample
- The system returns the most semantically similar images from the indexed dataset


### Quantitative Performance

- Demonstrable retrieval performance improvements over baseline or keyword-only systems
- Clear metrics to gauge effectiveness on test queries


### Scalable Deployment

- Ability to handle growth in dataset size without significant drops in retrieval speed or accuracy
- Potential integration into a cloud-based environment or containerized solution for easy scaling


### Extensibility

- Potential to incorporate user feedback to refine search results over time
- Easy adaptation to various domains beyond forensic applications


## Contributors

- Chandan N
- H John Joshua
- Jude Franklin
