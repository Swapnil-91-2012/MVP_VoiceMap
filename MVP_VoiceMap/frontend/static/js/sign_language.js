document.addEventListener("DOMContentLoaded", () => {

  const recordButton = document.getElementById("recordButtonSign");
  const uploadBtn = document.getElementById("uploadBtnSign");
  const uploadInput = document.getElementById("uploadSign");
  const statusDiv = document.getElementById("statusSign");
  const videoContainer = document.getElementById("videoContainer");
  const demoBtn = document.getElementById("demoBtnSign");

  if (!statusDiv || !videoContainer || !demoBtn) {
    console.error("Missing essential DOM elements for Sign Language Mode");
    return;
  }

  if (!window.SIGN_MAP) {
    statusDiv.textContent = "Sign map failed to load.";
    console.error("SIGN_MAP not found");
    return;
  }

  const API_BASE = "https://mvp-voicemap.onrender.com";

  // --- Demo Button ---
  demoBtn.addEventListener("click", async () => {
    statusDiv.textContent = "Generating sign language demo...";
    videoContainer.innerHTML = "";

    try {
      const res = await fetch(`${API_BASE}/sign-demo`, {
        method: "POST"
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || "Demo failed");
      }

      const data = await res.json();

      if (!data.gloss || typeof data.gloss !== "string") {
        throw new Error("Invalid gloss received from server");
      }

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
      const res = await fetch(`${API_BASE}/sign-language`, {
        method: "POST",
        body: formData
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || "Processing failed");
      }

      const data = await res.json();

      if (!data.transcription || typeof data.transcription !== "string") {
        throw new Error("Invalid transcription from server");
      }

      playSigns(data.transcription);

    } catch (err) {
      console.error(err);
      statusDiv.textContent = `Error: ${err.message}`;
    }
  }

  // --- Play signs from text ---
  function playSigns(text) {
    videoContainer.innerHTML = "";

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
        console.warn(`Missing sign for: ${word}`);
        next();
        return;
      }

      video.src = `/static/signs/${file}`;
      video.onended = next;
      video.play().catch(console.error);
    }

    statusDiv.textContent = "Playing demo...";
    next();
  }

});
