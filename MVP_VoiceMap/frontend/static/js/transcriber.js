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
      const res = await fetch("https://mvp-voicemap.onrender.com/transcribe-demo", {
  method: "POST"
})
;

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Demo failed");

      statusDiv.textContent = "Transcription complete";
      outputText.textContent = data.text;

    } catch (err) {
      statusDiv.textContent = err.message;
    }
  });

});
