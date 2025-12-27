document.addEventListener("DOMContentLoaded", () => {
  const recordButton = document.getElementById("recordButtonSign");
  const uploadBtn = document.getElementById("uploadBtnSign");
  const uploadInput = document.getElementById("uploadSign");
  const statusDiv = document.getElementById("statusSign");
  const videoContainer = document.getElementById("videoContainer");
  const demoBtn = document.getElementById("demoBtnSign");

  // Check required DOM elements
  if (!statusDiv || !videoContainer || !demoBtn) {
    console.error("Missing essential DOM elements for Sign Language Mode");
    return;
  }

  // Check SIGN_MAP
  if (!window.SIGN_MAP) {
    statusDiv.textContent = "Sign map failed to load.";
    console.error("SIGN_MAP not found");
    return;
  }

  // --- Demo Button ---
  demoBtn.addEventListener("click", async () => {
    console.log("Demo button clicked");
    statusDiv.textContent = "Generating sign language demo...";
    videoContainer.innerHTML = "";

    try {
      const res = await fetch("https://mvp-voicemap.onrender.com/sign-demo", {
  method: "POST"
})
);
      console.log("Fetch response:", res);

      const data = await res.json();
      console.log("Data received:", data);

      if (!res.ok) throw new Error(data.error || "Demo failed");
      if (!data.gloss || typeof data.gloss !== "string") throw new Error("Invalid gloss text from server");

      playSigns(data.gloss);

    } catch (err) {
      console.error(err);
      statusDiv.textContent = `Error: ${err.message}`;
    }
  });

  // --- Audio Recording & Upload (optional) ---
  if (recordButton && uploadBtn && uploadInput) {
    const recorder = new AudioRecorder();
    let isRecording = false;

    recordButton.addEventListener("click", async () => {
      if (!isRecording) {
        try {
          await recorder.start();
          isRecording = true;
          recordButton.textContent = "STOP RECORDING";
          statusDiv.textContent = "Recording...";
        } catch (err) {
          statusDiv.textContent = err.message;
        }
      } else {
        const audioBlob = await recorder.stop();
        isRecording = false;
        recordButton.textContent = "START RECORDING 🎤";

        if (!audioBlob) return;
        statusDiv.textContent = "Processing audio...";
        sendAudio(audioBlob);
      }
    });

    uploadBtn.addEventListener("click", () => uploadInput.click());

    uploadInput.addEventListener("change", () => {
      const file = uploadInput.files[0];
      if (!file) return;
      statusDiv.textContent = "Uploading audio...";
      sendAudio(file);
    });
  }

  async function sendAudio(audioData) {
    const formData = new FormData();
    formData.append("audio", audioData);

    try {
      const res = await fetch("/sign-language", { method: "POST", body: formData });
      const data = await res.json();

      if (!res.ok) throw new Error(data.error || "Processing failed");
      if (!data.transcription || typeof data.transcription !== "string") throw new Error("Invalid transcription from server");

      playSigns(data.transcription);

    } catch (err) {
      console.error(err);
      statusDiv.textContent = `Error: ${err.message}`;
    }
  }

  // --- Play signs from text ---
  function playSigns(text) {
    if (!text || typeof text !== "string") {
      statusDiv.textContent = "Invalid text for sign playback";
      return;
    }

    videoContainer.innerHTML = ""; // Clear previous content
    const words = text.toUpperCase().split(/\s+/);
    let index = 0;

    const video = document.createElement("video");
    video.autoplay = true;
    video.muted = true;
    video.style.width = "100%";
    videoContainer.appendChild(video);

    function next() {
      if (index >= words.length) {
        statusDiv.textContent = "Playback finished";
        return;
      }

      const word = words[index++];
      const file = window.SIGN_MAP[word];

      if (!file) {
        console.warn(`Missing video for word: "${word}"`);
        next(); // skip missing word
        return;
      }

      video.src = `/static/signs/${file}`;
      video.play().catch(err => console.error("Video playback error:", err));
      video.onended = next;
    }

    statusDiv.textContent = "Playing demo...";
    next();
  }
});
