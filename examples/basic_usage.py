#!/usr/bin/env python3
"""
Basic usage examples for Image to Voxel Converter
"""

from src.image_to_voxel import ImageToVoxelConverter
import os

def basic_example():
    """Basic usage example"""
    print("=== BASIC USAGE EXAMPLE ===")
    
    # Initialize converter
    converter = ImageToVoxelConverter()
    
    # Example image path (replace with your image)
    image_path = "path/to/your/image.jpg"
    
    if not os.path.exists(image_path):
        print(f"Please provide a valid image path. Current: {image_path}")
        return
    
    # Convert using height method
    results = converter.convert_image(image_path, method='height')
    
    # Save results
    os.makedirs('output', exist_ok=True)
    converter.save_voxels(results['height'], 'output/my_voxels.npz')
    
    # Visualize
    converter.visualize_3d(results['height'])

def advanced_example():
    """Advanced usage with custom parameters"""
    print("=== ADVANCED USAGE EXAMPLE ===")
    
    converter = ImageToVoxelConverter()
    
    # Custom parameters
    results = converter.convert_image(
        "path/to/your/image.jpg",
        method='all',
        voxel_resolution=128,  # Higher resolution
        max_height=64,        # Taller structures
        layers=32            # More color layers
    )
    
    # Process each method result
    for method_name, voxel_data in results.items():
        print(f"Method: {method_name}")
        print(f"Voxels created: {voxel_data['count']}")
        
        # Save with custom name
        output_file = f"output/advanced_{method_name}.npz"
        converter.save_voxels(voxel_data, output_file)

if __name__ == '__main__':
    basic_example()
    # advanced_example()
