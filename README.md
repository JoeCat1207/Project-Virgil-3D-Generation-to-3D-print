# Project Virgil

This project uses Tencent's Hunyuan3D shape generation model to create 3D models from images, then processes them with SuperSlicer for 3D printing.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install SuperSlicer:
   - Download from: https://github.com/supermerill/SuperSlicer/releases
   - Install according to your operating system instructions

3. Place SuperSlicer config files in the `SuperSlicer_configs` folder

## Usage

1. Run the full pipeline (generate 3D model and slice):
   ```
   python superslicer_processor.py
   ```

2. To specify a custom image:
   ```python
   # Edit hunyuan3dgen.py and modify the image path, then run:
   python superslicer_processor.py
   ```

## Output

- 3D models (.obj files) are saved to: `3D generated Shapes`
- G-code files are saved to: `Gcode_output`

## Configuration

- Place SuperSlicer configuration files in `SuperSlicer_configs`
- Default config path: `SuperSlicer_configs/default_config.ini`