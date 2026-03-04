import os
import random
import time
from datetime import datetime

import zmq


def resolve_topic(publish_kind: str) -> str:
    kind = (publish_kind or "").strip().lower()
    if kind in {"p1", "time", "hora", "clock"}:
        return "TIME"
    if kind in {"p2", "dice", "dado", "random"}:
        return "DICE"
    raise ValueError("PUBLISH_KIND inválido. Use 'time' (P1) ou 'dice' (P2).")


NAME = os.getenv("NAME", "P1")
TOPIC = resolve_topic(os.getenv("PUBLISH_KIND", "time"))
INTERVAL = float(os.getenv("INTERVAL", "1"))

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

# Dá um tempo pro SUB registrar as inscrições via XPUB/XSUB.
time.sleep(0.5)

while True:
    if TOPIC == "TIME":
        payload = datetime.now().strftime("%H:%M:%S")
    else:  # TOPIC == "DICE"
        payload = str(random.randint(1, 6))

    # Mensagem com tópico (prefix) via multipart: [TOPIC][PAYLOAD]
    pub.send_multipart([TOPIC.encode("utf-8"), payload.encode("utf-8")])
    print(f"[{NAME}] {TOPIC} {payload}", flush=True)
    time.sleep(INTERVAL)

pub.close()
context.close()
