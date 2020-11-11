async function onVideoUpdated(details) {
  // TODO: Called multiple times when video changed
  if (await includesHateSpeech(details.url)) {
    alert("Hate speech detected!");
  }
}

async function includesHateSpeech(url) {
  // TODO
  return Promise.resolve(Math.random() < 0.2);
}

chrome.webNavigation.onHistoryStateUpdated.addListener(onVideoUpdated, {
  url: [
    { urlContains: 'youtube.com/watch' },
  ],
});
