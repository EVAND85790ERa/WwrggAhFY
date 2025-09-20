# 代码生成时间: 2025-09-20 08:13:15
import os
import quart
from pathlib import Path


def rename_files(directory: str, prefix: str) -> None:
    """
    Renames files in the specified directory with a given prefix.
    """
    path = Path(directory)
    if not path.exists() or not path.is_dir():
# 改进用户体验
        raise FileNotFoundError(f'The directory {directory} does not exist.')

    for index, file in enumerate(path.iterdir()):
        if file.is_file():
            # Generate new file name with prefix and index
            new_name = f"{prefix}{index}_{file.name}"
            new_file_path = file.with_name(new_name)
            try:
                file.rename(new_file_path)
                print(f'Renamed {file.name} to {new_name}')
            except OSError as e:
                print(f'Error renaming {file.name} to {new_name}: {e}')


@app.route('(rename_route)', methods=['POST'])
def rename_route():
    """
    Quart route to trigger file renaming.
    """
    try:
        directory = request.form.get('directory')
        prefix = request.form.get('prefix')
        if not directory or not prefix:
            return jsonify({'error': 'Missing directory or prefix parameter'}), 400

        rename_files(directory, prefix)
        return jsonify({'message': 'Files renamed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)