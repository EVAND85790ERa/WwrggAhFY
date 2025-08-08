# 代码生成时间: 2025-08-08 15:47:10
import quart
import shutil
import os
import json
from datetime import datetime

"""
A Quart application to handle data backup and restore.
"""

app = quart.Quart(__name__)

# Configurations
BACKUP_DIR = 'backup'
DATA_FILE = 'data.json'

# Create backup directory if it does not exist
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

@app.route('/backup', methods=['POST'])
async def create_backup():
    """
    Endpoint to create a backup of the data file.
    """
    try:
        # Create a timestamped backup filename
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        backup_filename = f'{DATA_FILE}_{timestamp}.json'
        backup_path = os.path.join(BACKUP_DIR, backup_filename)

        # Copy the data file to the backup directory
        shutil.copy(DATA_FILE, backup_path)

        return quart.jsonify({'message': 'Backup created successfully', 'filename': backup_filename}), 200
    except Exception as e:
        return quart.jsonify({'error': str(e)}), 500

@app.route('/restore', methods=['POST'])
async def restore_backup():
    """
    Endpoint to restore the data file from a backup.
    """
    try:
        # Get the backup filename from the request data
        backup_filename = quart.request.json['filename']

        # Check if the backup file exists
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        if not os.path.isfile(backup_path):
            return quart.jsonify({'error': 'Backup file not found'}), 404

        # Restore the data file from the backup
        shutil.copy(backup_path, DATA_FILE)

        return quart.jsonify({'message': 'Data restored successfully'}), 200
    except Exception as e:
        return quart.jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Quart application
    app.run(debug=True)
