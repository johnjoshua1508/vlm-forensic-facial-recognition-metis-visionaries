import os
import time
import json
import tempfile
import traceback
import shutil
import numpy as np
import pandas as pd
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.utils import secure_filename
from datetime import datetime

from config import Config
from database import db
from models import Subject, User
from utils import ClipModel, FaissIndex, is_human_face
from utils.evaluation import precision_at_k, recall_at_k, average_precision

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize CLIP model and FAISS index
clip_model = ClipModel()
faiss_index = FaissIndex()

@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Helper function to get correct file path with different extensions
def get_correct_file_path(base_dir, file_id):
    # Try with .jpg extension first
    path_jpg = os.path.join(base_dir, file_id + ".jpg")
    if os.path.exists(path_jpg):
        return path_jpg
    
    # Try without extension
    path = os.path.join(base_dir, file_id)
    if os.path.exists(path):
        return path
    
    # Try with other common extensions
    for ext in [".jpeg", ".png", ".gif"]:
        path_ext = os.path.join(base_dir, file_id + ext)
        if os.path.exists(path_ext):
            return path_ext
    
    # Return the jpg path as default even if it doesn't exist
    return path_jpg

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.find_by_username(username)
        
        if user and user.check_password(password):
            login_user(user)
            user.update_last_login()
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get system stats
    try:
        total_subjects = 0
        try:
            metadata_df = pd.read_csv(Config.METADATA_CSV_PATH)
            total_subjects = len(metadata_df)
        except Exception as e:
            flash(f'Error reading metadata CSV: {str(e)}', 'warning')
            total_subjects = "Unknown (CSV error)"
            
        stats = {
            'total_subjects': total_subjects,
            'index_size': faiss_index.get_index_size(),
            'device': clip_model.get_device().upper()
        }
        
        return render_template('dashboard.html', stats=stats)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        print(traceback.format_exc())
        return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        search_type = request.form.get('search_type')
        top_k = int(request.form.get('top_k', 5))
        results = []
        search_time = 0
        text_query = None
        image_path = None
        
        try:
            start_time = time.time()
            
            if search_type == 'text':
                text_query = request.form.get('text_query')
                if not text_query:
                    flash('Please enter a text query', 'danger')
                    return redirect(url_for('search'))
                
                # Get threshold from form or use session/default
                threshold = float(request.form.get('threshold_text', session.get('threshold_text', Config.THRESHOLD_TEXT)))
                
                # Encode text and search
                text_embedding = clip_model.encode_text(text_query)
                distances, indices = faiss_index.index.search(np.array([text_embedding]).astype(np.float32), top_k)
                
                # Apply threshold
                if distances[0][0] > threshold:
                    flash(f'No matching results found (best distance {distances[0][0]:.2f} exceeds threshold {threshold})', 'warning')
                    return redirect(url_for('search'))
                
                # Get results
                for i, idx in enumerate(indices[0]):
                    subject_id = faiss_index.path_mapping[idx]
                    distance = distances[0][i]
                    similarity = 1.0 / (1.0 + distance)
                    
                    # Get metadata
                    try:
                        metadata = Subject.get_metadata_for_id(subject_id)
                    except Exception as e:
                        print(f"Error getting metadata for {subject_id}: {e}")
                        metadata = {"Error": "Failed to load metadata"}
                    
                    results.append({
                        'subject_id': subject_id,
                        'distance': distance,
                        'metadata': metadata
                    })
            
            elif search_type == 'image':
                # Check if image was uploaded
                if 'image' not in request.files:
                    flash('No image file provided', 'danger')
                    return redirect(url_for('search'))
                
                image_file = request.files['image']
                
                if image_file.filename == '':
                    flash('No image selected', 'danger')
                    return redirect(url_for('search'))
                
                if image_file and allowed_file(image_file.filename):
                    # Save the uploaded image
                    filename = secure_filename(image_file.filename)
                    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image_file.save(temp_path)
                    image_path = url_for('static', filename=f'uploads/{filename}')
                    
                    # Check if image contains a face
                    if not is_human_face(temp_path):
                        flash('No human face detected in the uploaded image', 'danger')
                        return redirect(url_for('search'))
                    
                    # Get threshold from form or use session/default
                    threshold = float(request.form.get('threshold_image', session.get('threshold_image', Config.THRESHOLD_IMAGE)))
                    
                    # Encode image and search
                    image_embedding = clip_model.encode_image(temp_path)
                    distances, indices = faiss_index.index.search(np.array([image_embedding]).astype(np.float32), top_k)
                    
                    # Apply threshold
                    if distances[0][0] > threshold:
                        flash(f'No matching results found (best distance {distances[0][0]:.2f} exceeds threshold {threshold})', 'warning')
                        return redirect(url_for('search'))
                    
                    # Get results
                    for i, idx in enumerate(indices[0]):
                        subject_id = faiss_index.path_mapping[idx]
                        distance = distances[0][i]
                        similarity = 1.0 / (1.0 + distance)
                        
                        # Get metadata
                        try:
                            metadata = Subject.get_metadata_for_id(subject_id)
                        except Exception as e:
                            print(f"Error getting metadata for {subject_id}: {e}")
                            metadata = {"Error": "Failed to load metadata"}
                        
                        results.append({
                            'subject_id': subject_id,
                            'distance': distance,
                            'metadata': metadata
                        })
            
            elif search_type == 'combined':
                text_query = request.form.get('text_query')
                embeddings = []
                
                # Check if image was uploaded
                if 'image' in request.files and request.files['image'].filename != '':
                    image_file = request.files['image']
                    
                    if allowed_file(image_file.filename):
                        # Save the uploaded image
                        filename = secure_filename(image_file.filename)
                        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        image_file.save(temp_path)
                        image_path = url_for('static', filename=f'uploads/{filename}')
                        
                        # Check if image contains a face
                        if not is_human_face(temp_path):
                            flash('No human face detected in the uploaded image', 'danger')
                            return redirect(url_for('search'))
                        
                        # Encode image
                        image_embedding = clip_model.encode_image(temp_path)
                        embeddings.append(image_embedding)
                
                # Encode text if provided
                if text_query:
                    text_embedding = clip_model.encode_text(text_query)
                    embeddings.append(text_embedding)
                
                if not embeddings:
                    flash('Please provide at least one of: text query or image', 'danger')
                    return redirect(url_for('search'))
                
                # Get threshold from form or use session/default
                threshold = float(request.form.get('threshold_combined', session.get('threshold_combined', Config.THRESHOLD_COMBINED)))
                
                # Combine embeddings
                combined_embedding = np.mean(np.vstack(embeddings), axis=0).reshape(1, -1).astype(np.float32)
                
                # Search with combined embedding
                distances, indices = faiss_index.index.search(combined_embedding, top_k)
                
                # Apply threshold
                if distances[0][0] > threshold:
                    flash(f'No matching results found (best distance {distances[0][0]:.2f} exceeds threshold {threshold})', 'warning')
                    return redirect(url_for('search'))
                
                # Get results
                for i, idx in enumerate(indices[0]):
                    subject_id = faiss_index.path_mapping[idx]
                    distance = distances[0][i]
                    similarity = 1.0 / (1.0 + distance)
                    
                    # Get metadata
                    try:
                        metadata = Subject.get_metadata_for_id(subject_id)
                    except Exception as e:
                        print(f"Error getting metadata for {subject_id}: {e}")
                        metadata = {"Error": "Failed to load metadata"}
                    
                    results.append({
                        'subject_id': subject_id,
                        'distance': distance,
                        'metadata': metadata
                    })
            
            search_time = time.time() - start_time
            
            # Save images to static folder for display
            for result in results:
                subject_id = result['subject_id']
                front_image_path = get_correct_file_path(Config.IMAGE_BASE_DIR, subject_id)
                
                if os.path.exists(front_image_path):
                    dest_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{subject_id}.jpg")
                    shutil.copy2(front_image_path, dest_path)
            
            return render_template('results.html', 
                                  results=results, 
                                  query_type=search_type, 
                                  text_query=text_query, 
                                  image_path=image_path,
                                  search_time=search_time)
        
        except Exception as e:
            flash(f'Error during search: {str(e)}', 'danger')
            print(traceback.format_exc())
            return redirect(url_for('search'))
    
    return render_template('search.html')

@app.route('/add_subject', methods=['GET', 'POST'])
@login_required
def add_subject():
    if request.method == 'POST':
        try:
            # Get form data
            sex = request.form.get('sex')
            
            # Get height from combined fields or use the combined value if provided
            if 'height' in request.form:
                height = request.form.get('height')
            else:
                height_feet = request.form.get('height_feet', '0')
                height_inches = request.form.get('height_inches', '0')
                height = f"{height_feet} ft. {height_inches.zfill(2)} in."
            
            weight = request.form.get('weight') + " lbs."
            hair = request.form.get('hair')
            eyes = request.form.get('eyes')
            race = request.form.get('race')
            sex_offender = request.form.get('sex_offender')
            offense = request.form.get('offense')
            
            # Check if images were uploaded
            if 'front_image' not in request.files or 'side_image' not in request.files:
                flash('Please upload both front and side images', 'danger')
                return redirect(url_for('add_subject'))
            
            front_image = request.files['front_image']
            side_image = request.files['side_image']
            
            if front_image.filename == '' or side_image.filename == '':
                flash('Please select both front and side images', 'danger')
                return redirect(url_for('add_subject'))
            
            if not (allowed_file(front_image.filename) and allowed_file(side_image.filename)):
                flash('Invalid file type. Please upload JPG, JPEG, or PNG images', 'danger')
                return redirect(url_for('add_subject'))
            
            # Generate a new unique ID
            new_subject_id = Subject.get_next_id()
            
            # Save uploaded images to temporary files
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_front:
                front_image.save(temp_front)
                front_path = temp_front.name
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_side:
                side_image.save(temp_side)
                side_path = temp_side.name
            
            # Prepare metadata
            metadata = {
                "Sex": sex,
                "Height": height,
                "Weight": weight,
                "Hair": hair,
                "Eyes": eyes,
                "Race": race,
                "Sex Offender": sex_offender,
                "Offense": offense
            }
            
            # Extract fused embedding
            front_embedding = clip_model.encode_image(front_path)
            side_embedding = clip_model.encode_image(side_path)
            
            # Fuse by averaging
            fused_embedding = (front_embedding + side_embedding) / 2.0
            
            # Create and save the subject
            subject = Subject(
                subject_id=new_subject_id,
                metadata=metadata,
                front_image_path=os.path.join(Config.IMAGE_BASE_DIR, new_subject_id + ".jpg"),
                side_image_path=os.path.join(Config.SIDE_IMAGE_DIR, new_subject_id + ".jpg"),
                embedding=fused_embedding
            )
            subject.save()
            
            # Add embedding to FAISS index
            faiss_index.add_embedding(new_subject_id, fused_embedding)
            
            # Save the front and side images to the appropriate directories
            dest_front_path = os.path.join(Config.IMAGE_BASE_DIR, new_subject_id + ".jpg")
            dest_side_path = os.path.join(Config.SIDE_IMAGE_DIR, new_subject_id + ".jpg")
            
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(dest_front_path), exist_ok=True)
            os.makedirs(os.path.dirname(dest_side_path), exist_ok=True)
            
            # Copy images
            shutil.copy2(front_path, dest_front_path)
            shutil.copy2(side_path, dest_side_path)
            
            # Clean up temporary files
            os.unlink(front_path)
            os.unlink(side_path)
            
            # Also save to uploads for display
            front_image.seek(0)
            front_image.save(os.path.join(app.config['UPLOAD_FOLDER'], new_subject_id + ".jpg"))
            
            # Update the CSV file with the new subject
            try:
                # Check if CSV exists and has headers
                csv_exists = os.path.exists(Config.METADATA_CSV_PATH) and os.path.getsize(Config.METADATA_CSV_PATH) > 0
                
                new_row = {'ID': new_subject_id}
                new_row.update(metadata)
                new_row_df = pd.DataFrame([new_row])
                
                if csv_exists:
                    # Read existing CSV to get column order
                    try:
                        existing_df = pd.read_csv(Config.METADATA_CSV_PATH)
                        # Ensure new row has same columns as existing CSV
                        for col in existing_df.columns:
                            if col not in new_row:
                                new_row[col] = None
                        # Reorder columns to match existing CSV
                        new_row_df = pd.DataFrame([new_row], columns=existing_df.columns)
                    except Exception as e:
                        print(f"Error reading existing CSV: {e}")
                        # Continue with default column order
                
                    # Append to existing CSV
                    with open(Config.METADATA_CSV_PATH, 'a', newline='') as f:
                        new_row_df.to_csv(f, header=False, index=False)
                else:
                    # Create new CSV with headers
                    new_row_df.to_csv(Config.METADATA_CSV_PATH, index=False)
                
                flash(f'Subject {new_subject_id} successfully added to the database!', 'success')
            except Exception as e:
                flash(f'Error updating metadata CSV: {str(e)}. Subject was added to the database but metadata CSV was not updated.', 'warning')
                print(traceback.format_exc())
            
            return redirect(url_for('add_subject'))
        
        except Exception as e:
            flash(f'Error adding subject: {str(e)}', 'danger')
            print(traceback.format_exc())
            return redirect(url_for('add_subject'))
    
    return render_template('add_subject.html')

@app.route('/remove_subject', methods=['GET', 'POST'])
@login_required
def remove_subject():
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        confirm = request.form.get('confirm')
        
        if not subject_id:
            flash('Please provide a subject ID to remove', 'danger')
            return redirect(url_for('remove_subject'))
        
        if not confirm:
            flash('Please confirm that you want to remove this subject', 'danger')
            return redirect(url_for('remove_subject'))
        
        try:
            # Check if the subject exists
            subject_exists = False
            try:
                metadata_df = pd.read_csv(Config.METADATA_CSV_PATH)
                subject_exists = subject_id in metadata_df['ID'].astype(str).values
            except Exception as e:
                flash(f'Error reading metadata CSV: {str(e)}', 'warning')
                # Continue with removal process even if CSV read fails
            
            if not subject_exists:
                flash(f'Subject {subject_id} not found in the metadata CSV. Continuing with removal process.', 'warning')
            
            # Remove from database
            deleted_count = Subject.delete_by_id(subject_id)
            if deleted_count == 0:
                flash(f'Subject {subject_id} not found in the database', 'warning')
            
            # Remove from CSV file if it exists
            try:
                if subject_exists:
                    metadata_df = metadata_df[metadata_df['ID'].astype(str) != subject_id]
                    metadata_df.to_csv(Config.METADATA_CSV_PATH, index=False)
                    flash(f'Subject {subject_id} removed from metadata CSV', 'success')
            except Exception as e:
                flash(f'Error updating metadata CSV: {str(e)}', 'warning')
            
            # Remove images from file system
            front_image_path = os.path.join(Config.IMAGE_BASE_DIR, subject_id + ".jpg")
            side_image_path = os.path.join(Config.SIDE_IMAGE_DIR, subject_id + ".jpg")
            
            # Also try without extension
            front_image_path_no_ext = os.path.join(Config.IMAGE_BASE_DIR, subject_id)
            side_image_path_no_ext = os.path.join(Config.SIDE_IMAGE_DIR, subject_id)
            
            files_removed = False
            
            # Remove front image if it exists
            if os.path.exists(front_image_path):
                os.remove(front_image_path)
                files_removed = True
            elif os.path.exists(front_image_path_no_ext):
                os.remove(front_image_path_no_ext)
                files_removed = True
            
            # Remove side image if it exists
            if os.path.exists(side_image_path):
                os.remove(side_image_path)
                files_removed = True
            elif os.path.exists(side_image_path_no_ext):
                os.remove(side_image_path_no_ext)
                files_removed = True
            
            if files_removed:
                flash(f'Subject {subject_id} images removed from file system', 'success')
            else:
                flash('Warning: Subject images were not found in the file system', 'warning')
            
            flash('Note: The subject embedding may still exist in the FAISS index. To completely remove it, you would need to rebuild the index.', 'info')
            
            return redirect(url_for('remove_subject'))
        
        except Exception as e:
            flash(f'Error removing subject: {str(e)}', 'danger')
            print(traceback.format_exc())
            return redirect(url_for('remove_subject'))
    
    return render_template('remove_subject.html')

@app.route('/evaluation', methods=['GET', 'POST'])
@login_required
def evaluation():
    if request.method == 'POST':
        eval_type = request.form.get('eval_type')
        ground_truth = request.form.get('ground_truth')
        top_k = int(request.form.get('top_k', 5))
        
        if not ground_truth:
            flash('Please provide ground truth IDs', 'danger')
            return redirect(url_for('evaluation'))
        
        ground_truth_ids = [id.strip() for id in ground_truth.split(",")]
        ground_truth_set = set(ground_truth_ids)
        
        try:
            retrieved_ids = []
            
            if eval_type == 'text':
                text_query = request.form.get('text_query')
                
                if not text_query:
                    flash('Please provide a text query', 'danger')
                    return redirect(url_for('evaluation'))
                
                # Encode text and search
                text_embedding = clip_model.encode_text(text_query)
                distances, indices = faiss_index.index.search(np.array([text_embedding]).astype(np.float32), top_k)
                
                # Get retrieved IDs
                for idx in indices[0]:
                    subject_id = faiss_index.path_mapping[idx]
                    retrieved_ids.append(subject_id)
            
            elif eval_type == 'image':
                # Check if image was uploaded
                if 'eval_image' not in request.files:
                    flash('No image file provided', 'danger')
                    return redirect(url_for('evaluation'))
                
                image_file = request.files['eval_image']
                
                if image_file.filename == '':
                    flash('No image selected', 'danger')
                    return redirect(url_for('evaluation'))
                
                if image_file and allowed_file(image_file.filename):
                    # Save the uploaded image
                    filename = secure_filename(image_file.filename)
                    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image_file.save(temp_path)
                    image_path = url_for('static', filename=f'uploads/{filename}')
                    
                    # Encode image and search
                    image_embedding = clip_model.encode_image(temp_path)
                    distances, indices = faiss_index.index.search(np.array([image_embedding]).astype(np.float32), top_k)
                    
                    # Get retrieved IDs
                    for idx in indices[0]:
                        subject_id = faiss_index.path_mapping[idx]
                        retrieved_ids.append(subject_id)
            
            elif eval_type == 'combined':
                text_query = request.form.get('text_query')
                embeddings = []
                
                # Check if image was uploaded
                if 'eval_image' in request.files and request.files['eval_image'].filename != '':
                    image_file = request.files['eval_image']
                    
                    if allowed_file(image_file.filename):
                        # Save the uploaded image
                        filename = secure_filename(image_file.filename)
                        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        image_file.save(temp_path)
                        image_path = url_for('static', filename=f'uploads/{filename}')
                        
                        # Encode image
                        image_embedding = clip_model.encode_image(temp_path)
                        embeddings.append(image_embedding)
                
                # Encode text if provided
                if text_query:
                    text_embedding = clip_model.encode_text(text_query)
                    embeddings.append(text_embedding)
                
                if not embeddings:
                    flash('Please provide at least one of: text query or image', 'danger')
                    return redirect(url_for('evaluation'))
                
                # Combine embeddings
                combined_embedding = np.mean(np.vstack(embeddings), axis=0).reshape(1, -1).astype(np.float32)
                
                # Search with combined embedding
                distances, indices = faiss_index.index.search(combined_embedding, top_k)
                
                # Get retrieved IDs
                for idx in indices[0]:
                    subject_id = faiss_index.path_mapping[idx]
                    retrieved_ids.append(subject_id)
            
            # Calculate metrics
            precision = precision_at_k(retrieved_ids, ground_truth_set, top_k)
            recall = recall_at_k(retrieved_ids, ground_truth_set, top_k)
            ap = average_precision(retrieved_ids, ground_truth_set)
            
            return render_template('evaluation.html', 
                                  eval_type=eval_type,
                                  text_query=request.form.get('text_query', ''),
                                  ground_truth=ground_truth,
                                  retrieved=", ".join(retrieved_ids),
                                  precision=precision,
                                  recall=recall,
                                  ap=ap,
                                  top_k=top_k,
                                  image_path=locals().get('image_path'))
        
        except Exception as e:
            flash(f'Error during evaluation: {str(e)}', 'danger')
            print(traceback.format_exc())
            return redirect(url_for('evaluation'))
    
    return render_template('evaluation.html')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        try:
            # Get threshold values from form
            threshold_text = float(request.form.get('threshold_text', Config.THRESHOLD_TEXT))
            threshold_image = float(request.form.get('threshold_image', Config.THRESHOLD_IMAGE))
            threshold_combined = float(request.form.get('threshold_combined', Config.THRESHOLD_COMBINED))
            
            # Store in session
            session['threshold_text'] = threshold_text
            session['threshold_image'] = threshold_image
            session['threshold_combined'] = threshold_combined
            
            flash('Settings updated successfully!', 'success')
            return redirect(url_for('settings'))
        except Exception as e:
            flash(f'Error updating settings: {str(e)}', 'danger')
            print(traceback.format_exc())
            return redirect(url_for('settings'))
    
    # Get current threshold values
    threshold_text = session.get('threshold_text', Config.THRESHOLD_TEXT)
    threshold_image = session.get('threshold_image', Config.THRESHOLD_IMAGE)
    threshold_combined = session.get('threshold_combined', Config.THRESHOLD_COMBINED)
    
    return render_template('settings.html', 
                          threshold_text=threshold_text,
                          threshold_image=threshold_image,
                          threshold_combined=threshold_combined)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# Add this route to your main.py file

@app.route('/subject/<subject_id>/details', methods=['GET'])
@login_required
def get_subject_details(subject_id):
    """API endpoint to get subject details"""
    try:
        # Get metadata for the subject
        metadata = Subject.get_metadata_for_id(subject_id)
        
        if not metadata:
            return jsonify({"error": "Subject not found"}), 404
            
        # Return the metadata as JSON
        return jsonify(metadata)
    except Exception as e:
        print(f"Error getting subject details: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Create initial admin user if it doesn't exist
def create_admin_user():
    admin = User.find_by_username('admin')
    if not admin:
        admin = User(username='admin', password='admin123', role='admin')
        admin.save()
        print("Admin user created")

if __name__ == '__main__':
    create_admin_user()
    app.run(debug=True)

