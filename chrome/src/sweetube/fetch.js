const serverUrl = "http://localhost:5000" //TBD

async function getData(url = serverUrl) {
  const response = await fetch(url, {
    method: 'GET',
  })
  return response.json();
}

async function postData(url = serverUrl, data) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  return response.json();
}

export async function analyzeTranscript(videoUrl) {
  return await getData(serverUrl + '/videos/' + videoUrl)
}

export async function feedback(data) {
  return await postData(serverUrl + '/feedback', data)
}
