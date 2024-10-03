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
from ak_transcribe import Transcribe
from ak_transcribe import Transcriber
from pathlib import Path
Transcriber.process(filepath=Path("path/to/media/file"))

# Return Srt file
Transcriber.srt

# Return Transcript text
Transcriber.txt
```

<!-- License -->
## License

See [LICENSE](/LICENSE) for more information.

<!-- Contact -->
## Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/ak_transcribe](https://github.com/rpakishore/ak_transcribe)
