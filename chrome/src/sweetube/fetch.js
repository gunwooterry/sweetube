const serverUrl = "http://localhost:5000" //TBD

async function getData(url = serverUrl) {
  const response = await fetch(url, {
    method: 'get',
  })
  return response.json();
}

async function postData(url = serverUrl, data) {
  const response = await fetch(url, {
    method: 'post',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    },
  })
  return response.json();
}

export async function analyzeTranscript(videoUrl) {
  return await getData(serverUrl + '/videos/' + videoUrl)
}

export async function feedback(data) {
  return await postData(serverUrl + '/feedback', data)
}
