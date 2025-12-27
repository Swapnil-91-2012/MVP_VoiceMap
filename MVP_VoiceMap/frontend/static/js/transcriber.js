document.addEventListener("DOMContentLoaded", () => {
  const demoBtn = document.getElementById("demoBtn");
  const statusDiv = document.getElementById("status");
  const outputText = document.getElementById("outputText");

  if (!demoBtn || !statusDiv || !outputText) {
    console.error("Missing Transcriber DOM elements");
    return;
  }

  const API_BASE = "https://mvp-voicemap.onrender.com";

  demoBtn.addEventListener("click", async () => {
    statusDiv.textContent = "Running demo transcription...";
    outputText.textContent = "";

    try {
      const res = await fetch(`${API_BASE}/transcribe-demo`, {
        method: "POST"
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Server error");
      }

      const data = await res.json();
      statusDiv.textContent = "Transcription complete";
      outputText.textContent = data.text || "No text returned";

    } catch (err) {
      console.error(err);
      statusDiv.textContent = "Error: " + err.message;
    }
  });
});
