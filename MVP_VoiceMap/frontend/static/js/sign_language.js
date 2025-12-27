document.addEventListener("DOMContentLoaded", () => {
  const statusDiv = document.getElementById("statusSign");
  const videoContainer = document.getElementById("videoContainer");
  const demoBtn = document.getElementById("demoBtnSign");

  if (!statusDiv || !videoContainer || !demoBtn) {
    console.error("Missing Sign Language DOM elements");
    return;
  }

  if (!window.SIGN_MAP) {
    statusDiv.textContent = "Sign map failed to load.";
    return;
  }

  const API_BASE = "https://mvp-voicemap.onrender.com";

  demoBtn.addEventListener("click", async () => {
    statusDiv.textContent = "Generating sign language demo...";
    videoContainer.innerHTML = "";

    try {
      const res = await fetch(`${API_BASE}/sign-demo`, {
        method: "POST"
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Server error");
      }

      const data = await res.json();

      if (!data.gloss) {
        throw new Error("No gloss returned");
      }

      playSigns(data.gloss);

    } catch (err) {
      console.error(err);
      statusDiv.textContent = "Error: " + err.message;
    }
  });

  function playSigns(text) {
    videoContainer.innerHTML = "";

    const words = text.toUpperCase().split(/\s+/);
    let index = 0;

    const video = document.createElement("video");
    video.autoplay = true;
    video.muted = true;
    video.controls = false;
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
        next();
        return;
      }

      video.src = `static/signs/${file}`;
      video.onended = next;
      video.play();
    }

    statusDiv.textContent = "Playing demo...";
    next();
  }
});
