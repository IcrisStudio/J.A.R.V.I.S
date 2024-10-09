document.addEventListener("DOMContentLoaded", () => {
    startSpeechRecognition();
});

const recognition = new webkitSpeechRecognition();
const visualizerDiv = document.getElementById("visualizer");

// Create 20 bars for the visualizer
for (let i = 0; i < 20; i++) {
    var newBar = document.createElement("div");
    newBar.classList.add("bar");
    visualizerDiv.appendChild(newBar);
}

recognition.continuous = false; // Set to false to trigger 'onend' after each recognition
recognition.lang = 'en-US';

const visualizerBars = document.querySelectorAll('.bar');
let audioContext, analyser, microphone;

recognition.onresult = (event) => {
    const query = event.results[0][0].transcript;

    // Animate the query text
    animateText(query);

    // Send query to backend to fetch the AI response
    fetch("/generate-ai-response", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const aiResponse = data.Response;

        // Animate the AI response text
        animateText(aiResponse);

        // Send the AI response to the backend (if needed)
        return fetch("/speech-to-text", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ response: aiResponse })
        });
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Restart speech recognition after the response is processed
        startSpeechRecognition();
    })
    .catch(error => {
        console.error("Error", error);
        startSpeechRecognition(); // Restart even if there's an error
    });
};

recognition.onend = () => {
    stopAudioVisualizer();
    // Automatically restart speech recognition
    startSpeechRecognition();
};

function startSpeechRecognition() {
    startAudioVisualizer();
    recognition.start();
}

function startAudioVisualizer() {
    if (!navigator.mediaDevices.getUserMedia) {
        console.log("Your browser does not support audio input.");
        return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        microphone = audioContext.createMediaStreamSource(stream);
        microphone.connect(analyser);
        analyser.fftSize = 64;

        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        function draw() {
            analyser.getByteFrequencyData(dataArray);

            visualizerBars.forEach((bar, index) => {
                const value = dataArray[index] || 1; // Ensure a minimum height
                bar.style.height = `${Math.max(value / 2, 5)}px`; // Scale height, minimum 2px
            });

            requestAnimationFrame(draw);
        }
        draw();
    })
    .catch(error => console.error("Error accessing microphone: ", error));
}

function stopAudioVisualizer() {
    if (audioContext) {
        audioContext.close();
        audioContext = null;
    }
}

function animateText(text) {
    const resultElement = document.getElementById("result");

    // Clear any existing content
    resultElement.textContent = '';

    // Wrap each letter and space in a span
    resultElement.innerHTML = text.split('').map(letter => {
        // Preserve spaces by wrapping them in a span with a specific class
        if (letter === ' ') {
            return `<span class='letter space'> </span>`;
        }
        return `<span class='letter'>${letter}</span>`;
    }).join('');

    // Animation for letters and spaces
    anime.timeline({ loop: false })
    .add({
        targets: '.letter',
        opacity: [0, 1],
        translateY: [25, 0],
        easing: 'easeOutExpo',
        duration: 600,
        delay: (el, i) => 20 * i
    });
}
