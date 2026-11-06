# Corsa Life Dialer

A dialer for following up with old leads, connected to Dialpad.

- Click **Call** to dial through Dialpad (direct API, embedded mini dialer, or the desktop app).
- Log each call as **Didn't Answer**, **Can't Talk Now / Call Back Later** (pick a callback time), or **Left Voicemail**. You can also mark **Closed / Sold**, **Not Interested** or **Wrong #**.
- The call queue puts callbacks that are due first, then leads you haven't called, then retries.
- Filter by call source. Each lead keeps its notes and call history. **Export** results to a CSV for PolicyTech.

## Use it
1. Open **Start Dialer (Windows).bat** or **Start Dialer (Mac).command**. You need Python from python.org. You can also open `index.html` in Chrome.
2. Click **Import leads** and choose your call list CSV.
3. Click ⚙ to add your Dialpad API key so calls go straight out of Dialpad.

Client lists and API keys are never stored in this repo. They stay in your browser on your computer.
