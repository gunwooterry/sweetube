let serverUrl = "http://localhost:5000" //TBD

async function getData(url = serverUrl) {
  const response = await fetch(url, {
    method: 'get',
  })
  return response.json();
}

export async function getHateSpeech(videoUrl) {
  return await getData(serverUrl + '/videos/' + videoUrl)
}