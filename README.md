# MCP Security Case Study

This project demonstrates common security vulnerabilities in a client-server application built with the MCP framework.

## Project Structure

-   `create_db.py`: A utility script to create and populate the `medical_records.db` SQLite database from `synthetic_medical_records.csv`.
-   `server.py`: The server code containing critical security vulnerabilities.
-   `client.py`: A client application designed to run tests against both servers, demonstrating the exploits of the vulnerabilities.
-   `synthetic_medical_records.csv`: A CSV file with sample data used to populate the database.

## How to Run the Demonstration

1. **Install Python3 and requirements.txt**

```bash
sudo apt install python3 python3-pip
pip install -r requirements.txt --break-system-packages
```

2. **Create database**

    Run `python create_db.py` to create `medical_records.db`

3. **Run local llm**
    Install `llama.cpp` and run a local llm, for example:
    
    ```bash
    ~/llama.cpp/build/bin/llama-server -m gemma-3-27b-it-Q4_0.gguf --host 0.0.0.0 --port 8000
    ```
4.  **Start the vulnerable server**:
    ```bash
    python server.py
    ```
    The server will start on `http://127.0.0.1:6278`.

5.  **Run the client against the server**
    ```bash
    python client.py
    ```