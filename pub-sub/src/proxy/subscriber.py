import os

import zmq


NAME = os.getenv("NAME", "S")
# Ex.: "TIME" | "DICE" | "TIME,DICE" | "*" (tudo)
SUB_TOPICS = os.getenv("SUB_TOPICS", "*")

context = zmq.Context()
sub = context.socket(zmq.SUB)
sub.connect("tcp://proxy:5556")

topics_raw = (SUB_TOPICS or "").strip()
if topics_raw in {"", "*", "ALL", "all"}:
    # vazio = recebe tudo
    sub.setsockopt_string(zmq.SUBSCRIBE, "")
else:
    for topic in topics_raw.split(","):
        topic = topic.strip()
        if topic:
            sub.setsockopt_string(zmq.SUBSCRIBE, topic)

while True:
    topic_b, payload_b = sub.recv_multipart()
    topic = topic_b.decode("utf-8", errors="replace")
    payload = payload_b.decode("utf-8", errors="replace")
    print(f"[{NAME}] {topic} -> {payload}", flush=True)

sub.close()
context.close()
