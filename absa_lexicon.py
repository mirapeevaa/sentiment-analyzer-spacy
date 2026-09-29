from dataclasses import dataclass
import spacy

nlp = spacy.load("en_core_web_sm")

@dataclass
class AspectSentiment:
    aspect: str
    aspect_span: tuple[int, int]
    sentiment: str
    sentiment_degree: float
    evidence: str
    evidence_span: tuple[int, int]


def analyze(text: str) -> list[AspectSentiment]:
    doc = nlp(text)
    results: list[AspectSentiment] = []

    return results


if __name__ == "__main__":
    sample = "The battery life is amazing but the screen is not great."
    for result in analyze(sample):
        print(result)