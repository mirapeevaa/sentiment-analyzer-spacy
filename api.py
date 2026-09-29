from datetime import datetime
from collections import Counter

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from absa_lexicon import analyze
from test_data import TEST_DATA

app = FastAPI(title="Lexicon ABSA")


class TextInput(BaseModel):
    text: str


class AspectSentimentOut(BaseModel):
    aspect: str
    aspect_span: tuple[int, int]
    sentiment: str
    sentiment_degree: float
    evidence: str
    evidence_span: tuple[int, int]


@app.post("/analyze", response_model=list[AspectSentimentOut])
def analyze_endpoint(payload: TextInput):
    return analyze(payload.text)


# ---------------------------------------------------------------------------
# Evaluation runner
# ---------------------------------------------------------------------------

def match_aspect(predicted_aspect: str, gold_aspect: str) -> bool:
    predicted_aspect = predicted_aspect.lower()
    gold_aspect = gold_aspect.lower()
    return predicted_aspect in gold_aspect or gold_aspect in predicted_aspect


def run_evaluation(output_path: str = "evaluation_results.md") -> None:
    client = TestClient(app)

    labels = ["positive", "negative", "neutral"]
    confusion = Counter()
    misses = 0
    extras = 0
    lines = []

    for item in TEST_DATA:
        text = item["text"]
        expected = item["expected"]
        source = item.get("source", "unknown")

        response = client.post("/analyze", json={"text": text})
        predicted = response.json()

        lines.append(f"### {text}  _(source: {source})_\n")

        matched_gold_idxs = set()
        for pred in predicted:
            match_found = False
            for i, gold in enumerate(expected):
                if i in matched_gold_idxs:
                    continue
                if match_aspect(pred["aspect"], gold["aspect"]):
                    matched_gold_idxs.add(i)
                    match_found = True
                    confusion[(gold["sentiment"], pred["sentiment"])] += 1
                    lines.append(
                        f"- aspect `{pred['aspect']}` -> predicted "
                        f"**{pred['sentiment']}** ({pred['sentiment_degree']:+.2f}), "
                        f"gold **{gold['sentiment']}**"
                    )
                    break
            if not match_found:
                extras += 1
                lines.append(f"- aspect `{pred['aspect']}` -> EXTRA (no gold match)")

        for i, gold in enumerate(expected):
            if i not in matched_gold_idxs:
                misses += 1
                lines.append(f"- gold aspect `{gold['aspect']}` -> MISSED (no prediction)")

        lines.append("")

    # --- confusion matrix ---
    total_matched = sum(confusion.values())
    correct = sum(confusion[(l, l)] for l in labels)
    accuracy = (correct / total_matched * 100) if total_matched else 0.0

    matrix_lines = ["| gold \\ predicted | " + " | ".join(labels) + " |",
                     "|---|" + "---|" * len(labels)]
    for gold_label in labels:
        row = [str(confusion[(gold_label, pred_label)]) for pred_label in labels]
        matrix_lines.append(f"| **{gold_label}** | " + " | ".join(row) + " |")

    # --- write output file ---
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Evaluation Results\n\n")
        f.write(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n")
        f.write(f"Total sentences: {len(TEST_DATA)}\n\n")
        f.write(f"Matched pairs: {total_matched}, Misses: {misses}, Extras: {extras}\n\n")
        f.write(f"**Accuracy (matched pairs): {accuracy:.1f}%**\n\n")
        f.write("## Confusion Matrix\n\n")
        f.write("\n".join(matrix_lines))
        f.write("\n\n## Per-Sentence Results\n\n")
        f.write("\n".join(lines))

    print(f"Accuracy: {accuracy:.1f}%  (matched={total_matched}, "
          f"misses={misses}, extras={extras})")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    run_evaluation()