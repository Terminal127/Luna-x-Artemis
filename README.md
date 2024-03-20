<p align="center">
<img align=centre src="[https://github.com/Terminal127/Luna-x-Artemis/blob/main/src/lunavideo.mp4](https://github.com/Terminal127/Luna-x-Artemis/blob/main/src/lunavideo.mp4)" alt=bot width=700 height=400>
</p>


# Luna-x-Artemis

A virtual assistant written in python.


## Usage/Examples

```javascript
import Component from 'my-project'

function App() {
  return <Component />
}
```


## Running Tests

To run tests, run the following command

```bash
  npm run test
```


## Features

- Gesture Controlled
- Feature enriched
- Cross platform

### Luna: Virtual Assistant Project Analysis

#### Key Points:

1. **Modular Structure with Asynchronous Operations:**
   - The project showcases a modular structure with different functionalities encapsulated within separate classes and methods. This modular approach enhances code readability, maintainability, and scalability.
   - Asynchronous programming using `asyncio` is employed for handling various tasks such as continuous speech recognition, handling app openings and closures, handling voice typing, etc. Asynchronous operations help in achieving concurrency and non-blocking execution, thereby improving overall performance and responsiveness of the virtual assistant.

2. **Integration of Multiple APIs and Services:**
   - Luna integrates various APIs and services to extend its functionality, such as:
     - Azure Cognitive Services for speech recognition and synthesis.
     - Selenium WebDriver for web automation tasks.
     - Dark Mode API for enabling dark mode functionality.
     - Google Maps API for retrieving and displaying maps.
     - Spotify API for music playback.
     - RapidAPI for fetching data from the YouTube Music API.
   - This integration diversifies Luna's capabilities, allowing it to perform a wide range of tasks including sending WhatsApp messages, controlling applications, searching the web, playing music, and more.
## Optimizations

"Previously, the code utilized multithreading for concurrent execution. However, due to Python's limitations in true parallelism with multithreading, we opted for asyncio to enable asynchronous programming. This choice was made to leverage Python's asyncio library, which provides a more efficient and scalable approach to handling concurrent tasks. Asynchronous programming with asyncio allows for non-blocking execution, improving overall performance and responsiveness in our application."

