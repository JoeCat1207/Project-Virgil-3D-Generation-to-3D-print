import os
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

def generate_3d_shape(image_path=None):
    # Initialize the pipeline from local path
    local_model_path = "INSERT_PATH"
    if os.path.exists(local_model_path):
        pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(local_model_path)
    else:
        pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('tencent/Hunyuan3D-2')
    
    # If no image path is provided, use a default image from Documents
    if image_path is None:
        # This path will need to be specified by the user later
        image_path = os.path.expanduser("~/'documents' but really put your OWN PATH/sample_image.jpeg")
    
    # Create output directory if it doesn't exist
    output_dir = "3D generated Shapes"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate 3D shape
    mesh = pipeline(image=image_path)[0]
    
    # Create output filename based on input image name
    base_filename = os.path.basename(image_path)
    name_without_ext = os.path.splitext(base_filename)[0]
    output_path = os.path.join(output_dir, f"{name_without_ext}.obj")
    
    # Export as OBJ file
    mesh.export(output_path)
    print(f"3D shape generated and saved to {output_path}")
    return output_path

if __name__ == "__main__":
    # Call the function without parameters to use default image
    # Or specify an image path like:
    # generate_3d_shape("/path/to/your/image.jpg")
    generate_3d_shape()
