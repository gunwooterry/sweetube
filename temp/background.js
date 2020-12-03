import { getHateSpeech } from './fetch.js'

async function onVideoUpdated(details) {
  // TODO: Called multiple times when video changed
  let hateSpeechData = await getHateSpeech(getYoutubeId(details.url))
  if (includesHateSpeech(hateSpeechData)) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, { type: "show-modal", data: hateSpeechData });
    });
  }
}

function includesHateSpeech(data) {
  // TODO: Do we need to modify the rule to check data is hateful?
  if (data) {
    return true
  }
  return false
}

function getYoutubeId(url) {
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url.match(regExp);
    return (match&&match[7].length==11)? match[7] : false;
}

chrome.webNavigation.onHistoryStateUpdated.addListener(onVideoUpdated, {
  url: [
    { urlContains: 'youtube.com/watch' },
  ],
});