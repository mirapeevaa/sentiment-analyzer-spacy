TEST_DATA = [
    {
        "text": "The battery life is amazing but the screen is not great.",
        "source": "mandatory",
        "expected": [
            {"aspect": "battery life", "sentiment": "positive"},
            {"aspect": "screen", "sentiment": "negative"},
        ],
    },
    {
        "text": "Food was okay, service was terrible.",
        "source": "mandatory",
        "expected": [
            {"aspect": "food", "sentiment": "neutral"},
            {"aspect": "service", "sentiment": "negative"},
        ],
    },
    {
        "text": "The camera is a bit disappointing for the price.",
        "source": "mandatory",
        "expected": [
            {"aspect": "camera", "sentiment": "negative"},
        ],
    },
    {
        "text": "I really loved the design, though the price is far from reasonable.",
        "source": "mandatory",
        "expected": [
            {"aspect": "design", "sentiment": "positive"},
            {"aspect": "price", "sentiment": "negative"},
        ],
    },
    {
        "text": "Staff were not very friendly and the room was not clean.",
        "source": "mandatory",
        "expected": [
            {"aspect": "staff", "sentiment": "negative"},
            {"aspect": "room", "sentiment": "negative"},
        ],
    },
    {
        "text": "The plot was great, the acting was even better.",
        "source": "mandatory",
        "expected": [
            {"aspect": "plot", "sentiment": "positive"},
            {"aspect": "acting", "sentiment": "positive"},
        ],
    },
    {
        "text": "It's not the worst laptop I've used, but it's not good either.",
        "source": "mandatory",
        "expected": [
            {"aspect": "laptop", "sentiment": "neutral"},
        ],
    },
    {
        "text": "The hotel room was spacious and the view was stunning.",
        "source": "mandatory",
        "expected": [
            {"aspect": "room", "sentiment": "positive"},
            {"aspect": "view", "sentiment": "positive"},
        ],
    },
    {
        "text": "Customer support was unhelpful and rude.",
        "source": "mandatory",
        "expected": [
            {"aspect": "customer support", "sentiment": "negative"},
        ],
    },
    {
        "text": "The soundtrack was forgettable, but the visuals were stunning.",
        "source": "mandatory",
        "expected": [
            {"aspect": "soundtrack", "sentiment": "negative"},
            {"aspect": "visuals", "sentiment": "positive"},
        ],
    },
]