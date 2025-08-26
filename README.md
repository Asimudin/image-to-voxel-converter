# Image to Voxel Converter

Convert 2D images into 3D voxel representations using multiple algorithms.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🎯 Features

- **Three Conversion Methods:**
  - **Height-Based**: Brightness → Height mapping
  - **Color-Layered**: Hue → Depth layers  
  - **Structure-Based**: Edge detection → Internal structure

- **Multiple Output Formats:**
  - NumPy compressed arrays (`.npz`)
  - Binary format (`.bin`)
  - 3D visualizations

- **Interactive Visualizations:**
  - 3D scatter plots
  - Cross-sectional slice views
  - Processing step visualization

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/image-to-voxel-converter.git
cd image-to-voxel-converter

# Install dependencies
pip install -r requirements.txt

# Run the converter
python src/image_to_voxel.py --input your_image.jpg --method all
```

## 📊 Results

Your image: **1822 x 2000 pixels** → Three voxel representations:

| Method | Voxels Created | File Size | Description |
|--------|----------------|-----------|-------------|
| Height-Based | 34,354 | 515 KB | Terrain-like height map |
| Color-Layered | 2,078 | 31 KB | Colors separated by depth |
| Structure-Based | 12,204 | 183 KB | Complex internal structure |

## 🛠️ Installation

```bash
pip install opencv-python numpy matplotlib pillow
```

Or using the requirements file:
```bash
pip install -r requirements.txt
```

## 💡 Usage Examples

### Basic Usage
```python
from src.image_to_voxel import ImageToVoxelConverter

converter = ImageToVoxelConverter()
voxels = converter.convert_image("path/to/image.jpg", method="height")
```

### Advanced Usage
```python
# Custom parameters
voxels = converter.convert_image(
    image_path="image.jpg",
    method="structure", 
    voxel_resolution=64,
    max_height=32
)

# Save results
converter.save_voxels(voxels, "output/my_voxels.npz")
```

## 📁 Project Structure

```
image-to-voxel-converter/
├── src/
│   ├── image_to_voxel.py      # Main converter class
│   ├── voxel_methods.py       # Conversion algorithms
│   └── visualization.py       # 3D plotting functions
├── examples/
│   ├── basic_usage.py         # Simple examples
│   └── advanced_demo.py       # Advanced features
├── docs/
│   └── API.md                 # API documentation
├── tests/
│   └── test_converter.py      # Unit tests
├── requirements.txt
├── setup.py
└── README.md
```

## 🎨 Conversion Methods Explained

### 1. Height-Based Voxels
Converts image brightness to height, creating a terrain-like 3D representation.
- **Use case**: Topographical maps, height fields
- **Best for**: High contrast images

### 2. Color-Layered Voxels  
Separates colors into different depth layers based on hue values.
- **Use case**: Artistic visualizations, color analysis
- **Best for**: Colorful, vibrant images

### 3. Structure-Based Voxels
Uses edge detection and distance transforms to create complex internal structures.
- **Use case**: Detailed 3D models, structural analysis
- **Best for**: Images with clear edges and shapes

## 🔧 API Reference

### `ImageToVoxelConverter`

#### Methods
- `convert_image(image_path, method, **kwargs)` - Convert image to voxels
- `save_voxels(voxels, filepath)` - Save voxel data
- `load_voxels(filepath)` - Load saved voxel data
- `visualize_3d(voxels)` - Create 3D visualization

#### Parameters
- `voxel_resolution` (int): Grid resolution (default: 64)
- `max_height` (int): Maximum height for height-based method (default: 32)
- `layers` (int): Number of layers for color-based method (default: 16)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenCV for image processing
- Matplotlib for 3D visualization
- NumPy for numerical computations

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/image-to-voxel-converter](https://github.com/yourusername/image-to-voxel-converter)
