import time, gc
from cli import getcliargs
from lexer import tokenize
from parser import parse
from runtime import evaluate

# --- prep program once ---
USERCODE = getcliargs()
src = []
for raw_line in USERCODE.splitlines():
    code = raw_line.split(";", 1)[0]
    if code.strip():
        src.append(code)

tokens = tokenize("\n".join(src))
wholetoken = []
while tokens:
    wholetoken.append(parse(tokens))

# --- benchmark ---
ROUNDS = 10
times = []

gc.disable()  # avoid GC noise during timing
prev = time.perf_counter()  # start lap clock

for _ in range(ROUNDS):
    # run one round
    for action in wholetoken:
        evaluate(action)

    now = time.perf_counter()
    lap = now - prev          # time for THIS round only
    times.append(lap)
    prev = now                # reset lap start
    print("first 5 laps (s):", [round(t, 6) for t in times[:5]])
    print("last 5 laps  (s):", [round(t, 6) for t in times[-5:]])
    print("avg:", sum(times)/len(times), "sec/round")

gc.enable()

# print a few laps + summary


# write once at the end (avoid I/O in the hot loop)
with open(r"C:\\Coding\\etc\\cpython.log", "a") as f:
    for t in times:
        f.write(f"{t}\n")
