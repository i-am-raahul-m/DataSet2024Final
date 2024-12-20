let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const sendBtn = document.getElementById("sendBtn");
const status = document.getElementById("status");
const audioPlayback = document.getElementById("audioPlayback");

recordBtn.addEventListener("click", async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
  mediaRecorder.onstop = () => {
    const blob = new Blob(audioChunks, { type: "audio/mp3" });
    audioChunks = [];
    const audioURL = URL.createObjectURL(blob);
    audioPlayback.src = audioURL;
    audioPlayback.style.display = "block";
    sendBtn.disabled = false;

    // Send audio blob to server
    sendBtn.onclick = () => sendAudio(blob);
  };

  mediaRecorder.start();
  status.textContent = "Status: Recording...";
  recordBtn.disabled = true;
  stopBtn.disabled = false;
});

stopBtn.addEventListener("click", () => {
  mediaRecorder.stop();
  status.textContent = "Status: Recording stopped.";
  recordBtn.disabled = false;
  stopBtn.disabled = true;
});

async function sendAudio(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob);

  const response = await fetch("/submit", {
    method: "POST",
    body: formData,
  });

  const result = await response.json();
  document.getElementById("result").textContent = `Complaint Text: ${result.transcription}`;
}
