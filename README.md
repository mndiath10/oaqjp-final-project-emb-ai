# Final project

## Emotion Detection Web Application

This is the **Final project** for the IBM course *Developing AI Applications with Python and Flask*.

The application analyzes text using the Watson NLP EmotionPredict service and returns scores for anger, disgust, fear, joy, and sadness, plus the dominant emotion. It is packaged as `EmotionDetection` and deployed with Flask.

### Features
- Emotion detection with Watson NLP
- Formatted dictionary output with `dominant_emotion`
- Packaged Python module (`EmotionDetection`)
- Unit tests for five emotion statements
- Flask web UI at `/emotionDetector`
- Error handling for blank / invalid input
- Static code analysis with pylint (target score: 10.00/10)

### How to run
```bash
pip install flask requests pylint
python3 server.py
```
Then open `http://localhost:5000`

### Unit tests
```bash
python3 test_emotion_detection.py
```

### Static analysis
```bash
pylint server.py
```
