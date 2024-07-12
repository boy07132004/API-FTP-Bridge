# API-FTP-Bridge

API-FTP-Bridge is a tool that receives requests through Flask server and writes them as files to a specified FTP server.


## Usage

1. Clone this repository and install the required dependencies:
    ```bash
    git clone https://github.com/boy07132004/API-FTP-Bridge.git
    cd API-FTP-Bridge
    
    pip install -r requirements.txt
    ```

2. Configure the `core/config.ini` file:

    First, copy the `core/config.template` to `core/config.ini`:
    ```bash
    cp core/config.template core/config.ini
    ```
    Then fill config settings in config.ini

3. Run the flask server


## Configuration

- **FTP Settings**
  - `FTP_SERVER`: IP address of the FTP server
  - `FTP_USER`: Username for the FTP server
  - `FTP_PASSWD`: Password for the FTP server
* The FTP user needs to have permissions to create folders/files, and the root path must be the recipe folder.


## API Endpoints
| HTTP Verbs | Endpoints | Request | Response |
| --- | --- | --- | --- |
| GET | /list_recipe | 
| GET | /list_recipe_backup |
| POST | /get_recipes_content | {"recipes": ["a", "b"]} | {"a": {"a.proc": "aproc", "a.proc1": "aproc1", "a.hdr": "ahdr"}} |
| POST | /get_backup_recipes_content | {"recipes": ["a", "b"]} | {"a": {"a.proc": "aproc", "a.proc1": "aproc1", "a.hdr": "ahdr"}} |
| POST | /create_recipes | {"a": {"a.proc": "", "a.proc1": "", "a.hdr": ""}} | ["a.proc OK", "a.proc1 OK", "a.hdr OK"] |
| POST | /restore | {"recipes": ["a", "b"]} | ["a.proc OK", "a.proc1 OK", "a.hdr OK"] |

- If you create a recipe that already exists, the original recipe will first be backed up to the backup folder before proceeding with the creation.
- If the /restore api receives a recipe that does not exist in the backup folder, it will return $recipe_name not found
