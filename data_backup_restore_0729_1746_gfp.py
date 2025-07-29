# 代码生成时间: 2025-07-29 17:46:01
# data_backup_restore.py - A simple data backup and restore service using Starlette framework

from pathlib import Path
from datetime import datetime
import shutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


# Constants for backup location and backup file extension
BACKUP_DIR = Path('/path/to/backups')
BACKUP_EXT = '.backup'


# Backup function to save data
def backup_data(data_path: Path) -> str:
    """
    Create a backup of the specified data directory.
    :param data_path: Path to the data directory to backup
    :return: The path to the backup file on success, otherwise None
    """
    try:
        # Ensure backup directory exists
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

        # Create a timestamped backup file path
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        backup_file_name = f'{data_path.name}_{timestamp}{BACKUP_EXT}'
        backup_file_path = BACKUP_DIR / backup_file_name

        # Copy the data directory to the backup location
        shutil.copytree(str(data_path), str(backup_file_path))
        return str(backup_file_path)
    except Exception as e:
        print(f'Error creating backup: {e}')
        return ''


# Restore function to restore data from a backup
def restore_data(backup_path: Path, target_path: Path) -> bool:
    """
    Restore data from the specified backup directory.
    :param backup_path: Path to the backup directory to restore from
    :param target_path: Path to the data directory to restore to
    :return: True on success, False otherwise
    """
    try:
        # Ensure backup and target directories exist
        if not backup_path.exists() or not backup_path.is_dir():
            print('Backup directory does not exist or is not a directory.')
            return False

        if not target_path.exists() or not target_path.is_dir():
            print('Target directory does not exist.')
            return False

        # Restore the data from backup directory to target directory
        shutil.copytree(str(backup_path), str(target_path), dirs_exist_ok=True)
        return True
    except Exception as e:
        print(f'Error restoring data: {e}')
        return False


# Create the Starlette app
app = Starlette(debug=True)

# Define a route for creating a backup
@app.route('/backup', methods=['POST'])
async def backup(request):
    data_path_str = request.json.get('data_path')
    if not data_path_str:
        return JSONResponse({'error': 'Missing data_path parameter'}, status_code=400)

    data_path = Path(data_path_str)
    backup_path = backup_data(data_path)
    if backup_path:
        return JSONResponse({'message': 'Backup created successfully', 'backup_path': backup_path}, status_code=200)
    else:
        return JSONResponse({'error': 'Failed to create backup'}, status_code=500)

# Define a route for restoring data
@app.route('/restore', methods=['POST'])
async def restore(request):
    backup_path_str = request.json.get('backup_path')
    target_path_str = request.json.get('target_path')
    if not backup_path_str or not target_path_str:
        return JSONResponse({'error': 'Missing backup_path or target_path parameter'}, status_code=400)

    backup_path = Path(backup_path_str)
    target_path = Path(target_path_str)
    success = restore_data(backup_path, target_path)
    if success:
        return JSONResponse({'message': 'Data restored successfully'}, status_code=200)
    else:
        return JSONResponse({'error': 'Failed to restore data'}, status_code=500)


# Mount the routes to the app
app.add_route('/backup', backup)
app.add_route('/restore', restore)
