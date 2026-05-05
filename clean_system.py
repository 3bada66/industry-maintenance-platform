#!/usr/bin/env python3
"""
Industry Maintenance Platform System Cleanup Script
================================

This script provides a clean way to completely reset the Industry Maintenance Platform system:
- Stop all containers
- Remove all volumes
- Remove all images (optional)
- Clean up any leftover files

Usage:
    python clean_system.py [--images] [--all]

Options:
    --images    Also remove Docker images
    --all       Remove everything including images and build cache
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def run_command(cmd, description, ignore_errors=False):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            print(f"⚠️  {description} failed (ignored): {e.stderr}")
            return True
        else:
            print(f"❌ {description} failed:")
            print(f"   Error: {e.stderr}")
            return False

def check_docker():
    """Check if Docker is running"""
    print("🔍 Checking Docker...")
    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        print("✅ Docker is running")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not running or not available")
        return False

def stop_containers():
    """Stop all Industry Maintenance Platform containers"""
    print("🛑 Stopping containers...")
    
    # Stop dev containers
    run_command("docker-compose -f docker-compose.dev.yml down", "Stopping dev containers", ignore_errors=True)
    
    # Stop prod containers
    run_command("docker-compose down", "Stopping prod containers", ignore_errors=True)
    
    # Stop any other containers that might be running
    run_command("docker ps -q --filter 'name=industry-maintenance-platform' | xargs -r docker stop", "Stopping any remaining Industry Maintenance Platform containers", ignore_errors=True)
    
    return True

def remove_volumes():
    """Remove all Industry Maintenance Platform volumes"""
    print("🗑️  Removing volumes...")
    
    # Remove specific volumes
    volumes = [
        "industry-maintenance-platform_industry-maintenance-platform_postgres_data",
        "industry-maintenance-platform_postgres_data"
    ]
    
    for volume in volumes:
        run_command(f"docker volume rm {volume}", f"Removing volume {volume}", ignore_errors=True)
    
    # Remove any other volumes with industry-maintenance-platform in the name
    run_command("docker volume ls -q --filter 'name=industry-maintenance-platform' | xargs -r docker volume rm", "Removing any remaining Industry Maintenance Platform volumes", ignore_errors=True)
    
    return True

def remove_networks():
    """Remove all Industry Maintenance Platform networks"""
    print("🌐 Removing networks...")
    
    # Remove specific networks
    networks = [
        "industry-maintenance-platform_industry-maintenance-platform-network",
        "industry-maintenance-platform-network"
    ]
    
    for network in networks:
        run_command(f"docker network rm {network}", f"Removing network {network}", ignore_errors=True)
    
    # Remove any other networks with industry-maintenance-platform in the name
    run_command("docker network ls -q --filter 'name=industry-maintenance-platform' | xargs -r docker network rm", "Removing any remaining Industry Maintenance Platform networks", ignore_errors=True)
    
    return True

def remove_images(remove_all=False):
    """Remove Industry Maintenance Platform Docker images"""
    print("🖼️  Removing images...")
    
    # Remove specific images
    images = [
        "industry-maintenance-platform-backend",
        "industry-maintenance-platform-frontend"
    ]
    
    for image in images:
        run_command(f"docker rmi {image}", f"Removing image {image}", ignore_errors=True)
    
    if remove_all:
        # Remove all images with industry-maintenance-platform in the name
        run_command("docker images -q --filter 'reference=*industry-maintenance-platform*' | xargs -r docker rmi -f", "Removing all Industry Maintenance Platform images", ignore_errors=True)
        
        # Clean up dangling images
        run_command("docker image prune -f", "Cleaning up dangling images", ignore_errors=True)
    
    return True

def clean_build_cache():
    """Clean Docker build cache"""
    print("🧹 Cleaning build cache...")
    
    run_command("docker builder prune -f", "Cleaning build cache", ignore_errors=True)
    run_command("docker system prune -f", "Cleaning system", ignore_errors=True)
    
    return True

def clean_local_files():
    """Clean local files that might be left over"""
    print("📁 Cleaning local files...")
    
    # Remove common temporary files
    temp_files = [
        "*.pyc",
        "__pycache__",
        ".pytest_cache",
        "*.log",
        "node_modules"
    ]
    
    for pattern in temp_files:
        run_command(f"find . -name '{pattern}' -type d -exec rm -rf {{}} + 2>/dev/null || true", f"Removing {pattern}", ignore_errors=True)
        run_command(f"find . -name '{pattern}' -type f -delete 2>/dev/null || true", f"Removing {pattern} files", ignore_errors=True)
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Clean Industry Maintenance Platform system completely")
    parser.add_argument("--images", action="store_true", help="Also remove Docker images")
    parser.add_argument("--all", action="store_true", help="Remove everything including images and build cache")
    
    args = parser.parse_args()
    
    print("🧹 Industry Maintenance Platform System Cleanup")
    print("="*40)
    
    # Check Docker
    if not check_docker():
        sys.exit(1)
    
    # Confirm action
    if args.all:
        print("\n⚠️  WARNING: This will remove ALL Industry Maintenance Platform Docker images and build cache!")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Cleanup cancelled.")
            return
    
    # Stop containers
    if not stop_containers():
        sys.exit(1)
    
    # Remove volumes
    if not remove_volumes():
        sys.exit(1)
    
    # Remove networks
    if not remove_networks():
        sys.exit(1)
    
    # Remove images if requested
    if args.images or args.all:
        if not remove_images(args.all):
            sys.exit(1)
    
    # Clean build cache if requested
    if args.all:
        if not clean_build_cache():
            sys.exit(1)
    
    # Clean local files
    clean_local_files()
    
    print("\n" + "="*50)
    print("🎉 CLEANUP COMPLETED!")
    print("="*50)
    print("\n✅ All Industry Maintenance Platform containers, volumes, and networks have been removed.")
    if args.images or args.all:
        print("✅ Docker images have been removed.")
    if args.all:
        print("✅ Build cache has been cleaned.")
    print("\n🚀 To start fresh, run: python init_system.py --clean")
    print("="*50)

if __name__ == "__main__":
    main() 