# YouTube Comment Sentiment Analysis Dashboard

Uses a Fine-tuned BERT natural language model to analyze the top 100 liked comments on a given YouTube video URL, and outputs a dashboard made in Plotly. 

---

## Requirements

- Python 3.8+
- A YouTube Data API key (free from Google)
- Internet connection 

---

## Installation & Running the App

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Set up virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate   # On macOS/Linux
```

### 3. Install Libraries

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
YOUTUBE_API_KEY=your_api_key_here
```

### 5. Run app

```bash
python src/main.py
```

Then open browser and head to: http://127.0.0.1:8050/

---

## Example 

### Youtube Video:
<img width="1327" height="964" alt="Screenshot (113)" src="https://github.com/user-attachments/assets/e3c2e460-9e6c-487b-80d3-348fe90cf09d" />

### Output:
<img width="1912" height="974" alt="Screenshot (114)" src="https://github.com/user-attachments/assets/9fb944df-d4bd-43e2-929a-93a42ce79a92" />



