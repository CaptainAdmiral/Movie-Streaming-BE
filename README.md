# Movie Streaming Backend

A FastAPI backend server for a movie streaming site.

## Running the Application

### Running with Python
```bash
pip install -r requirements.txt
python backend.py
```
Requires Python 3.12.

### Running with Windows Executable
```bash
./backend.exe
```

### Running with Docker
```bash
docker build -t movie-streaming .
docker run -p 8000:8000 movie-streaming
```

The API will be available at `http://localhost:8000`