// scanner.js
// Scans a QR code from the device camera using the jsQR library,
// then /items/ the decoded text to the FastAPI backend at /items/.

// Grab the page elements that the JS needs to interact with.
// These IDs must match the elements in templates/index.html.
const video = document.getElementById("video");
const button = document.getElementById("button");
const resultPlaceholder = document.getElementById("resultPlaceholder");
const resultLink = document.getElementById("resultLink");
const resultText = document.getElementById("resultText");
const errorDisplay = document.getElementById("status");

// Camera stream and a flag that controls the scan loop.
let stream = null;
let scanning = false;

// We draw video frames into an offscreen canvas so jsQR can read pixel data.
// "willReadFrequently" is a hint to the browser that we'll call getImageData a lot.
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d", { willReadFrequently: true });

// Show a message in the status box, then hide it after 5 seconds.
function showError(message) {
  if (!errorDisplay) return;
  errorDisplay.textContent = message;
  errorDisplay.style.display = "block";
  setTimeout(() => (errorDisplay.style.display = "none"), 5000);
}

// If the jsQR library failed to load (e.g. /static/js/jsQR.js is missing),
// the browser will not have a global `jsQR` function, so warn the user early.
if (typeof jsQR === "undefined") {
  showError("Error: jsQR library failed to load. Check /static/js/jsQR.js exists.");
}

function setVisible(el, visible) {
  if (!el) return;
  el.hidden = !visible;
}

/** Shows a clickable link for http/https URLs; plain text otherwise. */
function renderDecoded(decodedText) {
  const text = decodedText.trim();
  setVisible(resultPlaceholder, false);

  if (text.startsWith("http://") || text.startsWith("https://")) {
    resultLink.href = text;
    resultLink.textContent = text;
    setVisible(resultLink, true);
    setVisible(resultText, false);
    return;
  }

  resultText.textContent = text;
  setVisible(resultText, true);
  setVisible(resultLink, false);
}

// Save scan event, item, and linking token (three API calls in order).
async function postResult(decodedText) {
  const headers = { "Content-Type": "application/json" };

  try {
    // 1) Scan — record that the camera read this QR
    const scanRes = await fetch("/scans/", {
      method: "POST",
      headers,
      body: JSON.stringify({ text: decodedText, source: "camera" }),
    });
    if (!scanRes.ok) {
      const errorData = await scanRes.json().catch(() => ({}));
      showError("Scan error: " + (errorData.detail || scanRes.status));
      return;
    }
    const scan = await scanRes.json();

    // 2) Item — save decoded text (same as before)
    const itemRes = await fetch("/items/", {
      method: "POST",
      headers,
      body: JSON.stringify({ name: decodedText }),
    });
    if (!itemRes.ok) {
      const errorData = await itemRes.json().catch(() => ({}));
      showError("Item error: " + (errorData.detail || itemRes.status));
      return;
    }
    const item = await itemRes.json();

    // 3) Token — link this scan to this item
    const tokenRes = await fetch("/tokens/", {
      method: "POST",
      headers,
      body: JSON.stringify({
        text: decodedText,
        source: "scanner",
        date: new Date().toISOString().slice(0, 19),
        item_id: item.id,
        scan_id: scan.id,
      }),
    });
    if (!tokenRes.ok) {
      const errorData = await tokenRes.json().catch(() => ({}));
      showError("Token error: " + (errorData.detail || tokenRes.status));
      return;
    }
  } catch (err) {
    showError("Failed to connect to server: " + err);
  }
}


// Called repeatedly via requestAnimationFrame while `scanning` is true.
// Each call grabs the latest video frame and asks jsQR if it sees a QR code.
function scanFrame() {
  if (!scanning) return;

  // Wait until the video has at least one full frame ready to read.
  if (video.readyState === video.HAVE_ENOUGH_DATA) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

    // jsQR returns either null (no code found) or an object whose `data`
    // property contains the decoded string.
    const code = jsQR(imageData.data, imageData.width, imageData.height);
    if (code && code.data) {
      // Stop the loop so we don't scan the same code many times in a row.
      scanning = false;

      const decodedText = code.data;
      renderDecoded(decodedText);

      // Release the camera so the indicator light/preview turns off.
      if (stream) stream.getTracks().forEach((t) => t.stop());

      // Send the decoded text to the backend (fire-and-forget; errors are
      // handled inside postResult via showError).
      postResult(decodedText);
      return;
    }
  }

  // Schedule the next frame check on the browser's render loop.
  requestAnimationFrame(scanFrame);
}

// Wire up the "Request camera" button. Browsers only allow getUserMedia
// after a user gesture, which is why this lives inside a click handler.
button.addEventListener("click", async () => {
  try {
    // Ask for the back-facing camera ("environment") and no microphone.
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
      audio: false,
    });

    video.srcObject = stream;
    await video.play();
    video.style.display = "block";

    scanning = true;
    requestAnimationFrame(scanFrame);
  } catch (err) {
    // Most common causes: user denied permission, no camera available,
    // or the page is not on a secure origin (must be localhost or HTTPS).
    console.error(err);
    showError("Camera permission denied or not available.");
  }
});
