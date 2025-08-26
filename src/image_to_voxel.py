# Image to Voxel Converter - Main Module
# Converts 2D images into 3D voxel representations using multiple algorithms

import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from PIL import Image
import argparse

class ImageToVoxelConverter:
    """Main class for converting images to voxel representations"""
    
    def __init__(self):
        self.supported_methods = ['height', 'color', 'structure', 'all']
    
    def convert_image(self, image_path, method='height', **kwargs):
        """
        Convert image to voxels using specified method
        
        Args:
            image_path (str): Path to input image
            method (str): Conversion method ('height', 'color', 'structure', 'all')
            **kwargs: Method-specific parameters
        
        Returns:
            dict: Voxel data and metadata
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Load image
        img_bgr = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        print(f"📏 Processing image: {img_rgb.shape[1]} x {img_rgb.shape[0]}")
        
        results = {}
        
        if method == 'all':
            methods_to_run = ['height', 'color', 'structure']
        else:
            methods_to_run = [method]
        
        for m in methods_to_run:
            print(f"\n🔄 Running {m} method...")
            
            if m == 'height':
                voxels, colors = self._height_based_voxels(
                    img_rgb, 
                    kwargs.get('voxel_resolution', 64),
                    kwargs.get('max_height', 32)
                )
            elif m == 'color':
                voxels, colors = self._color_layered_voxels(
                    img_rgb,
                    kwargs.get('voxel_resolution', 48),
                    kwargs.get('layers', 16)
                )
            elif m == 'structure':
                voxels, colors = self._structure_based_voxels(
                    img_rgb,
                    kwargs.get('voxel_resolution', 56),
                    kwargs.get('depth_levels', 24)
                )
            
            occupied_count = np.sum(voxels)
            print(f"✅ Created {occupied_count} voxels using {m} method")
            
            results[m] = {
                'voxels': voxels,
                'colors': colors,
                'count': occupied_count,
                'method': m
            }
        
        return results
    
    def _height_based_voxels(self, image, voxel_resolution=64, max_height=32):
        """Convert image to voxels using brightness as height"""
        resized = cv2.resize(image, (voxel_resolution, voxel_resolution))
        gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
        heights = ((gray / 255.0) * max_height).astype(int)
        
        voxel_grid = np.zeros((voxel_resolution, voxel_resolution, max_height), dtype=bool)
        colors = np.zeros((voxel_resolution, voxel_resolution, max_height, 3), dtype=np.uint8)
        
        for x in range(voxel_resolution):
            for y in range(voxel_resolution):
                height = heights[y, x]
                if height > 0:
                    for z in range(height):
                        voxel_grid[x, y, z] = True
                        colors[x, y, z] = resized[y, x]
        
        return voxel_grid, colors
    
    def _color_layered_voxels(self, image, voxel_resolution=48, layers=16):
        """Create voxels with different colors at different heights"""
        resized = cv2.resize(image, (voxel_resolution, voxel_resolution))
        hsv = cv2.cvtColor(resized, cv2.COLOR_RGB2HSV)
        
        voxel_grid = np.zeros((voxel_resolution, voxel_resolution, layers), dtype=bool)
        colors = np.zeros((voxel_resolution, voxel_resolution, layers, 3), dtype=np.uint8)
        
        for x in range(voxel_resolution):
            for y in range(voxel_resolution):
                pixel_rgb = resized[y, x]
                pixel_hsv = hsv[y, x]
                
                hue_layer = int((pixel_hsv[0] / 180.0) * layers)
                hue_layer = min(hue_layer, layers - 1)
                
                if pixel_hsv[1] > 30 and pixel_hsv[2] > 30:
                    voxel_grid[x, y, hue_layer] = True
                    colors[x, y, hue_layer] = pixel_rgb
        
        return voxel_grid, colors
    
    def _structure_based_voxels(self, image, voxel_resolution=56, depth_levels=24):
        """Create voxels based on image structure and edges"""
        resized = cv2.resize(image, (voxel_resolution, voxel_resolution))
        gray_resized = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
        
        edges = cv2.Canny(gray_resized, 50, 150)
        dist_transform = cv2.distanceTransform(255 - edges, cv2.DIST_L2, 5)
        
        max_dist = np.max(dist_transform)
        if max_dist > 0:
            depth_map = (dist_transform / max_dist * (depth_levels - 1)).astype(int)
        else:
            depth_map = np.zeros_like(dist_transform, dtype=int)
        
        voxel_grid = np.zeros((voxel_resolution, voxel_resolution, depth_levels), dtype=bool)
        colors = np.zeros((voxel_resolution, voxel_resolution, depth_levels, 3), dtype=np.uint8)
        
        for x in range(voxel_resolution):
            for y in range(voxel_resolution):
                max_depth = depth_map[y, x]
                pixel_color = resized[y, x]
                
                for z in range(max_depth + 1):
                    voxel_grid[x, y, z] = True
                    color_intensity = 1.0 - (z / max(depth_levels, 1)) * 0.5
                    colors[x, y, z] = (pixel_color * color_intensity).astype(np.uint8)
        
        return voxel_grid, colors
    
    def save_voxels(self, voxel_data, output_path):
        """Save voxel data to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if output_path.endswith('.npz'):
            occupied = np.where(voxel_data['voxels'])
            np.savez_compressed(
                output_path,
                positions=np.column_stack(occupied),
                colors=voxel_data['colors'][occupied],
                grid_shape=voxel_data['voxels'].shape,
                method=voxel_data['method']
            )
        elif output_path.endswith('.bin'):
            self._save_binary_format(voxel_data, output_path)
        
        print(f"✅ Saved voxel data: {output_path}")
    
    def visualize_3d(self, voxel_data, max_voxels=8000):
        """Create 3D visualization of voxels"""
        voxel_grid = voxel_data['voxels']
        colors = voxel_data['colors']
        
        occupied = np.where(voxel_grid)
        
        if len(occupied[0]) == 0:
            print("❌ No voxels to display")
            return
        
        if len(occupied[0]) > max_voxels:
            indices = np.random.choice(len(occupied[0]), max_voxels, replace=False)
            occupied = (occupied[0][indices], occupied[1][indices], occupied[2][indices])
        
        voxel_colors = colors[occupied] / 255.0
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        ax.scatter(occupied[0], occupied[1], occupied[2], 
                  c=voxel_colors, s=20, alpha=0.8)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'3D Voxels - {voxel_data["method"].title()} Method')
        
        plt.tight_layout()
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Convert image to voxel representation')
    parser.add_argument('--input', '-i', required=True, help='Input image path')
    parser.add_argument('--output', '-o', default='output/', help='Output directory')
    parser.add_argument('--method', '-m', default='all', choices=['height', 'color', 'structure', 'all'],
                       help='Conversion method')
    parser.add_argument('--resolution', '-r', type=int, default=64, help='Voxel grid resolution')
    parser.add_argument('--visualize', '-v', action='store_true', help='Show 3D visualization')
    
    args = parser.parse_args()
    
    converter = ImageToVoxelConverter()
    
    try:
        results = converter.convert_image(
            args.input, 
            method=args.method,
            voxel_resolution=args.resolution
        )
        
        # Save results
        os.makedirs(args.output, exist_ok=True)
        for method_name, voxel_data in results.items():
            output_file = os.path.join(args.output, f'{method_name}_voxels.npz')
            converter.save_voxels(voxel_data, output_file)
            
            if args.visualize:
                converter.visualize_3d(voxel_data)
        
        print(f"\n✅ Conversion complete! Results saved to {args.output}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
