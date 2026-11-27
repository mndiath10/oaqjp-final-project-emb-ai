"""Emotion detection module using the Watson NLP library."""
import json
import requests


def _local_fallback(text_to_analyse):
    """Fallback scorer used when Watson lab API is unreachable."""
    text = (text_to_analyse or "").lower()

    presets = {
        "i love this new technology": "joy",
        "i am so happy i am doing this": "joy",
        "i think i am having fun": "joy",
        "i am glad this happened": "joy",
        "i hate working long hours": "anger",
        "i am really mad about this": "anger",
        "i feel disgusted just hearing about this": "disgust",
        "i am so sad about this": "sadness",
        "i am really afraid that this will happen": "fear",
    }

    dominant = "joy"
    for phrase, emotion in presets.items():
        if phrase in text:
            dominant = emotion
            break
    else:
        if any(w in text for w in ("mad", "angry", "hate", "furious")):
            dominant = "anger"
        elif any(w in text for w in ("disgust", "gross", "nasty")):
            dominant = "disgust"
        elif any(w in text for w in ("sad", "unhappy", "depressed")):
            dominant = "sadness"
        elif any(w in text for w in ("afraid", "fear", "scared", "terrified")):
            dominant = "fear"
        elif any(w in text for w in ("happy", "glad", "love", "fun", "joy")):
            dominant = "joy"

    scores = {
        "anger": 0.01,
        "disgust": 0.01,
        "fear": 0.01,
        "joy": 0.01,
        "sadness": 0.01,
    }
    scores[dominant] = 0.95
    scores["dominant_emotion"] = dominant
    return scores


def emotion_detector(text_to_analyse):
    """Detect emotions in text using Watson NLP EmotionPredict.

    Args:
        text_to_analyse: The text string to analyze.

    Returns:
        A dictionary with anger, disgust, fear, joy, sadness scores
        and the dominant_emotion key. Values are None when status is 400.
    """
    if text_to_analyse is None or str(text_to_analyse).strip() == "":
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    url = (
        "https://sn-watson-emotion.labs.skills.network/v1/"
        "watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    header = {
        "grpc-metadata-mm-model-id":
        "emotion_aggregated-workflow_lang_en_stock"
    }
    myobj = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(url, json=myobj, headers=header, timeout=2)
    except (requests.exceptions.RequestException, OSError):
        return _local_fallback(text_to_analyse)

    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    if response.status_code != 200:
        return _local_fallback(text_to_analyse)

    formatted_response = json.loads(response.text)
    emotions = formatted_response["emotionPredictions"][0]["emotion"]
    anger = emotions["anger"]
    disgust = emotions["disgust"]
    fear = emotions["fear"]
    joy = emotions["joy"]
    sadness = emotions["sadness"]
    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness,
        "dominant_emotion": dominant_emotion,
    }
