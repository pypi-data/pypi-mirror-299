<!--- Heading --->
<div align="center">
  <h1>ak_transcribe</h1>
</div>
<br />

<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

<!-- Getting Started -->
## Getting Started

<!-- Prerequisites -->
### Prerequisites

Python 3.11 or above

**Note for Ubuntu/Debian:**
This project uses `python-magic` to identify file types. So the libmagic C library needs to be installed need to be installed. See [python-magic](https://pypi.org/project/python-magic/) for more information.

For Debian/Ubuntu systems:

- `sudo apt-get install libmagic1`

For OSX:

- When using Homebrew: `brew install libmagic`
- When using macports: `port install file`

For Windows:

- _No additional requirements_

<!-- Installation -->
### Installation

```bash
  pip install ak_transcribe
```

Check configs

```python
  import ak_transcribe
  ak_transcribe.test_configs()
```
<!-- Usage -->
## Usage


```python
from ak_transcribe import Transcriber
from pathlib import Path
Transcriber.process(filepath=Path("path/to/media/file"))

# Return Srt file
Transcriber.srt

# Embed subtitle file into the video
Transcriber.embed_srt(filepath=Path("path/to/media/file"))

# Return Transcript text
Transcriber.txt

# Return the json text string
Transcriber.json

# Extract txt from srt file
from ak_transcribe import converter
converter.srt_to_txt("path/to/srt/file")
```

<!-- License -->
## License

See [LICENSE](/LICENSE) for more information.

<!-- Contact -->
## Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/ak_transcribe](https://github.com/rpakishore/ak_transcribe)
