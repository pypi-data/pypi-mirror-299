# Constants
LANGUAGE_CONSTANTS = {
    "python": {
        "file_extension": ".py",
        "ignore_files": [".python-version"],
        "ignore_folders": [".git", ".vscode", "venv", ".github", "__pycache__", "logs"],
        "file_size_limit": 10 * 1024 * 1024,  # 10 MB
    },
    "csharp": {
        "file_extension": ".cs",
        "ignore_files": ["*.dll", "*.exe"],
        "ignore_folders": [".git", ".vs", "bin", "obj", ".vscode", ".github"],
        "file_size_limit": 20 * 1024 * 1024,  # 20 MB
    },
    "javascript": {
        "file_extension": ".js",
        "ignore_files": [],
        "ignore_folders": [],
        "file_size_limit": 5 * 1024 * 1024,  # 5 MB
    },
    "typescript": {
        "file_extension": ".ts",
        "ignore_files": [],
        "ignore_folders": [],
        "file_size_limit": 10 * 1024 * 1024,  # 10 MB
    },
}

DEFAULT_LANGUAGE = "python"
