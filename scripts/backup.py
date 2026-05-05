#!/usr/bin/env python3
"""
Industry Maintenance Platform Backup Script
Creates a complete backup of the Industry Maintenance Platform system including:
- Database dump
- Uploaded files
- Configuration files
- Logs (optional)
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
import tarfile
import gzip
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Industry Maintenance PlatformBackup:
    def __init__(self, backup_dir="backups", include_logs=False):
        self.backup_dir = Path(backup_dir)
        self.include_logs = include_logs
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_name = f"industry-maintenance-platform_backup_{self.timestamp}"
        self.backup_path = self.backup_dir / self.backup_name
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self):
        """Create a complete backup of Industry Maintenance Platform"""
        logger.info(f"Starting Industry Maintenance Platform backup: {self.backup_name}")
        
        try:
            # Create backup directory
            self.backup_path.mkdir(exist_ok=True)
            
            # 1. Database backup
            self.backup_database()
            
            # 2. Uploads backup
            self.backup_uploads()
            
            # 3. Configuration backup
            self.backup_config()
            
            # 4. Logs backup (optional)
            if self.include_logs:
                self.backup_logs()
            
            # 5. Create metadata
            self.create_metadata()
            
            # 6. Create compressed archive
            self.create_archive()
            
            # 7. Cleanup temporary files
            self.cleanup()
            
            logger.info(f"Backup completed successfully: {self.backup_path}.tar.gz")
            return str(self.backup_path) + ".tar.gz"
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            self.cleanup()
            raise
    
    def backup_database(self):
        """Backup PostgreSQL database"""
        logger.info("Backing up database...")
        
        try:
            # Get database connection details from environment
            db_host = os.getenv("DB_HOST", "localhost")
            db_port = os.getenv("DB_PORT", "5432")
            db_name = os.getenv("DB_NAME", "industry-maintenance-platform")
            db_user = os.getenv("DB_USER", "industry-maintenance-platform_user")
            db_password = os.getenv("DB_PASSWORD", "secure_password_123")
            
            # Create database dump
            dump_file = self.backup_path / "database.sql"
            
            # Set PGPASSWORD environment variable
            env = os.environ.copy()
            env["PGPASSWORD"] = db_password
            
            # Run pg_dump
            cmd = [
                "pg_dump",
                "-h", db_host,
                "-p", db_port,
                "-U", db_user,
                "-d", db_name,
                "--no-password",
                "--verbose",
                "--clean",
                "--if-exists",
                "--create",
                "-f", str(dump_file)
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Database backup failed: {result.stderr}")
            
            logger.info("Database backup completed")
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            raise
    
    def backup_uploads(self):
        """Backup uploaded files"""
        logger.info("Backing up uploads...")
        
        uploads_dir = Path("uploads")
        if uploads_dir.exists():
            backup_uploads_dir = self.backup_path / "uploads"
            shutil.copytree(uploads_dir, backup_uploads_dir)
            logger.info("Uploads backup completed")
        else:
            logger.warning("Uploads directory not found, skipping")
    
    def backup_config(self):
        """Backup configuration files"""
        logger.info("Backing up configuration...")
        
        config_files = [
            "backend/.env",
            "docker-compose.yml",
            "docker-compose.prod.yml",
            "production.env.example"
        ]
        
        config_dir = self.backup_path / "config"
        config_dir.mkdir(exist_ok=True)
        
        for config_file in config_files:
            if Path(config_file).exists():
                shutil.copy2(config_file, config_dir)
                logger.info(f"Backed up: {config_file}")
            else:
                logger.warning(f"Config file not found: {config_file}")
    
    def backup_logs(self):
        """Backup log files"""
        logger.info("Backing up logs...")
        
        logs_dir = Path("logs")
        if logs_dir.exists():
            backup_logs_dir = self.backup_path / "logs"
            shutil.copytree(logs_dir, backup_logs_dir)
            logger.info("Logs backup completed")
        else:
            logger.warning("Logs directory not found, skipping")
    
    def create_metadata(self):
        """Create backup metadata"""
        logger.info("Creating backup metadata...")
        
        metadata = {
            "backup_name": self.backup_name,
            "timestamp": self.timestamp,
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "includes_logs": self.include_logs,
            "files": []
        }
        
        # List all files in backup
        for file_path in self.backup_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.backup_path)
                metadata["files"].append({
                    "path": str(relative_path),
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
        
        # Write metadata
        metadata_file = self.backup_path / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info("Backup metadata created")
    
    def create_archive(self):
        """Create compressed archive"""
        logger.info("Creating compressed archive...")
        
        archive_path = str(self.backup_path) + ".tar.gz"
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(self.backup_path, arcname=self.backup_name)
        
        # Get archive size
        archive_size = Path(archive_path).stat().st_size
        logger.info(f"Archive created: {archive_path} ({archive_size / (1024*1024):.2f} MB)")
    
    def cleanup(self):
        """Clean up temporary backup directory"""
        if self.backup_path.exists():
            shutil.rmtree(self.backup_path)
            logger.info("Temporary files cleaned up")

def main():
    parser = argparse.ArgumentParser(description="Industry Maintenance Platform Backup Script")
    parser.add_argument(
        "--backup-dir", 
        default="backups", 
        help="Backup directory (default: backups)"
    )
    parser.add_argument(
        "--include-logs", 
        action="store_true", 
        help="Include log files in backup"
    )
    parser.add_argument(
        "--list", 
        action="store_true", 
        help="List existing backups"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_backups(args.backup_dir)
        return
    
    try:
        backup = Industry Maintenance PlatformBackup(args.backup_dir, args.include_logs)
        backup_file = backup.create_backup()
        print(f"✅ Backup completed: {backup_file}")
        
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        sys.exit(1)

def list_backups(backup_dir):
    """List existing backups"""
    backup_path = Path(backup_dir)
    
    if not backup_path.exists():
        print("No backup directory found")
        return
    
    backups = []
    for file_path in backup_path.glob("industry-maintenance-platform_backup_*.tar.gz"):
        stat = file_path.stat()
        backups.append({
            "name": file_path.name,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime)
        })
    
    if not backups:
        print("No backups found")
        return
    
    print(f"Found {len(backups)} backup(s):")
    print("-" * 80)
    
    for backup in sorted(backups, key=lambda x: x["modified"], reverse=True):
        size_mb = backup["size"] / (1024 * 1024)
        print(f"{backup['name']:<50} {size_mb:>8.2f} MB  {backup['modified'].strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 