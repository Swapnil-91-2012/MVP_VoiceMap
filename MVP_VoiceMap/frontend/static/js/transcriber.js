document.addEventListener("DOMContentLoaded", () => {

  const demoBtn = document.getElementById("demoBtn");
  const statusDiv = document.getElementById("status");
  const outputText = document.getElementById("outputText");

  if (!demoBtn || !statusDiv || !outputText) {
    console.error("Transcriber MVP: Missing DOM elements");
    return;
  }

  demoBtn.addEventListener("click", async () => {
    statusDiv.textContent = "Running demo transcription...";
    outputText.textContent = "";

    try {
      const res = await fetch(
        "https://mvp-voicemap.onrender.com/transcribe-demo",
        { method: "POST" }
      );

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || "Demo transcription failed");
      }

      const data = await res.json();

      statusDiv.textContent = "Transcription complete";
      outputText.textContent = data.text || "(No text returned)";

    } catch (err) {
      console.error(err);
      statusDiv.textContent = `Error: ${err.message}`;
    }
  });

});
