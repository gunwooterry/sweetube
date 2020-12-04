/* eslint-disable no-undef */
import { analyzeTranscript } from './sweetube/fetch.js'

var lastId = "";

async function onVideoUpdated(details) {
  let videoId = getVideoId(details.url);
  // 여러 번 불리는 문제가 있어 중복으로 요청하는 경우를 filter out 한다.
  if (lastId === videoId) {
    return;
  }
  lastId = videoId;
  let sentences = (await analyzeTranscript(videoId)).data;
  let topThree = chooseTopThree(sentences);
  if (topThree.length > 0) {
    chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
      chrome.tabs.sendMessage(tabs[0].id, { type: "show-modal", data: topThree });
    });
  }
}

function chooseTopThree(sentences) {
  return sentences
    .filter(s => s.confidence > 0.7)
    .sort((s1, s2) => s2.confidence - s1.confidence)
    .slice(0, 3);
}

function getVideoId(url) {
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url.match(regExp);
    return (match && match[7].length === 11)? match[7] : false;
}

chrome.webNavigation.onHistoryStateUpdated.addListener(onVideoUpdated, {
  url: [
    { urlContains: 'youtube.com/watch' },
  ],
});
