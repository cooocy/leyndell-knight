# Leyndell Knight

## Overview

This project includes two main tools: `oss_helper` and `disk_cleaner`, designed for managing OSS (Object Storage
Service) and cleaning local disk space, respectively.

- **oss_helper**: Provides common operations for OSS, such as listing, downloading, uploading, and deleting objects.
- **disk_cleaner**: Cleans temporary or unused files from the local disk to free up storage space.

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:

   N/A

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### oss_helper

`oss_helper` is a command-line tool for interacting with OSS. It supports the following commands:

#### 1. Help

Displays help information:

```bash
python leyndell_knight.py oss help
```

#### 2. List Objects

Lists objects in OSS:

```bash
python leyndell_knight.py oss list [--marker <key>] [--limit <limit>]
```

- `--marker`: (Optional) Start listing from the specified object.
- `--limit`: (Optional) Number of objects to return (default: 20).

#### 3. Download Object

Downloads an object from OSS to the local machine:

```bash
python leyndell_knight.py oss download <key> [path]
```

- `<key>`: Name of the object in OSS.
- `[path]`: (Optional) Local path to save the file (default: current directory).

#### 4. Upload File

Uploads a local file to OSS:

```bash
python leyndell_knight.py oss put <file>
```

- `<file>`: Path to the local file.

#### 5. Delete Object

Deletes an object from OSS:

```bash
python leyndell_knight.py oss delete <key>
```

- `<key>`: Name of the object in OSS.

#### 6. Clean Logs

Deletes the log file:

```bash
python leyndell_knight.py oss gc
```

### disk_cleaner

`disk_cleaner` is a tool for cleaning temporary or unused files from the local disk.

#### Usage

Run the following command to clean the specified dirs and files:

```bash
python leyndell_knight.py dc <level>
```

- `<level>`: ordinary or deep. You can define the garbage in the `config/app.yaml` file.

##### How to define the garbage

```yaml
disk_cleaner:
  ordinary:
    garbage:
      # Match one file.
      - '~/.python_history'

      # Match all dirs and files under Downloads dir.
      - '~/Downloads'

      # Match all files (no dirs) under Downloads dir.
      - '~/Downloads/*'

      # Match all files (no dirs) which the name starts with 'hello'.
      # e.g. hello1, hello2 ...
      - '~/Downloads/hello*'

      # Match all files (no dirs) which the name ends with '.png'.
      # e.g. a.png, b.png ...
      - '~/Downloads/*.png'

      # Must be an abs path.
      # '*' can only have one and must be the last part.
      # These are not valid.
      #      - 'a.png'
      #      - 'c/d/x.png'
      #      - '/a/*/x.png'
      #      - '/a/b/c/*xxx*'
```

## Configuration

See `config/app.yaml` for configuration options.

## Contribution

Feel free to submit issues or pull requests to improve this project.

## License

This project is licensed under the [Apache License](LICENSE).