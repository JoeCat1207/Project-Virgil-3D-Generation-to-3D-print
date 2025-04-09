import os
import subprocess
import sys
import shutil
from pathlib import Path
import trimesh

def obj_to_stl(obj_file_path):
    """Convert OBJ file to STL if needed"""
    stl_file_path = obj_file_path.replace('.obj', '.stl')
    
    # Load the mesh
    mesh = trimesh.load(obj_file_path)
    
    # Export as STL
    mesh.export(stl_file_path)
    print(f"Converted OBJ to STL: {stl_file_path}")
    
    return stl_file_path

def process_with_superslicer(model_path, config_path=None):
    """Process 3D model with SuperSlicer"""
    # Create directories if they don't exist
    config_dir = "SuperSlicer_configs"
    gcode_dir = "Gcode_output"
    
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(gcode_dir, exist_ok=True)
    
    # Convert to STL if the file is OBJ
    if model_path.lower().endswith('.obj'):
        model_path = obj_to_stl(model_path)
    
    # Use default config or user-provided config
    if config_path is None:
        # Use a default config file path - this should be created by the user
        config_path = os.path.join(config_dir, "default_config.ini")
        
        # Create a simple default config file if it doesn't exist
        if not os.path.exists(config_path):
            print(f"WARNING: Default config file not found at {config_path}")
            print("Please create a SuperSlicer config file before running this script")
            return None
    
    # Get model filename without extension
    model_name = os.path.basename(model_path)
    name_without_ext = os.path.splitext(model_name)[0]
    
    # Output gcode path
    gcode_path = os.path.join(gcode_dir, f"{name_without_ext}.gcode")
    
    # Determine SuperSlicer executable based on OS
    superslicer_path = None
    if sys.platform == "darwin":  # macOS
        # Common installation paths for macOS
        possible_paths = [
            "/Applications/SuperSlicer.app/Contents/MacOS/superslicer",
            "/Applications/SuperSlicer.app/Contents/MacOS/SuperSlicer"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                superslicer_path = path
                break
    elif sys.platform == "win32":  # Windows
        # Common installation paths for Windows
        possible_paths = [
            "C:/Program Files/SuperSlicer/superslicer_console.exe",
            "C:/Program Files (x86)/SuperSlicer/superslicer_console.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                superslicer_path = path
                break
    elif sys.platform == "linux":  # Linux
        # Try to find superslicer in PATH
        try:
            superslicer_path = subprocess.check_output(["which", "superslicer"]).strip().decode()
        except:
            superslicer_path = None
    
    if not superslicer_path:
        print("SuperSlicer executable not found. Please install SuperSlicer or specify the correct path.")
        return None
    
    # Command to run SuperSlicer from command line
    cmd = [
        superslicer_path,
        "--load", config_path,
        "--output", gcode_path,
        "--export-gcode",
        model_path
    ]
    
    try:
        print(f"Running SuperSlicer with command: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"SuperSlicer successfully processed the model.")
        print(f"G-code file saved to: {gcode_path}")
        return gcode_path
    except subprocess.CalledProcessError as e:
        print(f"Error running SuperSlicer: {e}")
        print(f"Error output: {e.stderr}")
        return None

if __name__ == "__main__":
    # Import the shape generation function
    from hunyuan3dgen import generate_3d_shape
    
    # Generate 3D shape
    obj_file_path = generate_3d_shape()
    
    # Process with SuperSlicer
    if obj_file_path and os.path.exists(obj_file_path):
        gcode_path = process_with_superslicer(obj_file_path)
        if gcode_path:
            print(f"Full processing pipeline completed successfully.")
            print(f"Generated 3D model: {obj_file_path}")
            print(f"Sliced G-code file: {gcode_path}")
    else:
        print("Failed to generate 3D shape from image.")