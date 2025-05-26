const MEET_URL_PATTERN =
  /^https:\/\/meet\.google\.com\/[a-z]{3}-[a-z]{4}-[a-z]{3}$/;
const BOT_SERVER = "http://localhost:8000/new-meeting"; // Your bot server endpoint

let detectedMeetings = new Set();

/**
 * Notifies the bot server about a new Google Meet URL.
 *
 * @param {string} url - The Google Meet URL to notify the server about.
 *
 * @return {void}
 */
function notifyServer(url) {
  // Avoid duplicate notifications for the same URL
  if (detectedMeetings.has(url)) return;

  detectedMeetings.add(url);

  // Send the Google Meet URL to the backend server
  fetch(BOT_SERVER, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      meetUrl: url,
      timestamp: new Date().toISOString(),
    }),
  })
    .then((response) => {
      if (!response.ok) {
        console.error("Failed to notify bot server");
      }
    })
    .catch((error) => {
      console.error("Error notifying bot server:", error);
    });

  // Clear old meetings after 24 hours to prevent memory buildup
  setTimeout(() => detectedMeetings.delete(url), 24 * 60 * 60 * 1000);
}

// Listen for URL changes or page loads in Google Meet
chrome.webNavigation.onCompleted.addListener((details) => {
  if (MEET_URL_PATTERN.test(details.url)) {
    notifyServer(details.url);
  }
});

chrome.webNavigation.onHistoryStateUpdated.addListener((details) => {
  if (MEET_URL_PATTERN.test(details.url)) {
    notifyServer(details.url);
  }
});

// Optional: Add a listener for when the extension is installed or updated
chrome.runtime.onInstalled.addListener(() => {
  console.log("Meet Detector extension installed and running");
});
