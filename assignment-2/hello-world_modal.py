import sys
from modal import App

app = App("eg: hello-world")

@app.function()
def f(i):
    if i%2 == 0:
        print("hello", i)
    else:
        print("world", i, file=sys.stderr)

    return i*i

@app.local_entrypoint()
def main():
    print(f.local(1000))

    print(f.remote(1000))

    total =0
    for ret in f.map(range(200)):
        total += ret

    print(total)
