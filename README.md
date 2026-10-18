# ma3-osc

A tiny, dependency-free CLI to send [grandMA3](https://www.malighting.com/) command-line commands over **OSC** — no Python packages required, just the standard library.

It sends an OSC message to the desk's `/cmd` address with a single string argument, which grandMA3 executes in its command line.

## Requirements

- Python 3 (standard library only)
- A grandMA3 console (or onPC) reachable over the network with OSC input enabled

## grandMA3 setup

On the desk: **Menu → In & Out → OSC**, on the active config line:

| Setting | Value |
|---|---|
| Enable Input | `Yes` |
| **Receive Command** | **`Yes`** ← critical; defaults to `No`, independent of general Receive |
| Prefix | *(blank)* |
| Input Port | e.g. `53000` |

Without **Receive Command = Yes**, packets are accepted on the port but nothing executes.

> Tip: a command-line *error* on the desk (e.g. "cannot create object") actually confirms OSC is received and parsed end-to-end — it's just a syntax issue in the command string.

## Usage

```bash
# Default host/port (edit defaults in the script or pass flags)
./ma3-osc.py "Go+ Exec 202"

./ma3-osc.py "Fixture 1 At 75"
./ma3-osc.py "FaderMaster Page 1.201 At 100"

# Explicit host/port
./ma3-osc.py --host 192.168.10.163 --port 53000 "Off Exec 202"
```

### Options

| Flag | Default | Description |
|---|---|---|
| `--host` | `192.168.10.163` | grandMA3 IP address |
| `--port` | `53000` | OSC input (UDP) port |
| `--address` | `/cmd` | OSC address (blank prefix → `/cmd`) |

Any valid grandMA3 command-line string works as the argument.

## How it works

OSC messages are plain UDP. This tool builds a minimal OSC packet by hand:

```
/cmd  ,s  "<your command>"
```

- OSC address `/cmd` (null-terminated, 4-byte padded)
- type-tag string `,s` (one string argument)
- the command string (null-terminated, 4-byte padded)

That's it — no libraries, no framework.

## References

- [grandMA3 OSC remote inputs (MA Lighting)](https://help.malighting.com/grandMA3/2.0/HTML/remote_inputs_osc.html)
- [Open Sound Control spec](https://opensoundcontrol.stanford.edu/spec-1_0.html)

## License

MIT — see [LICENSE](LICENSE).
