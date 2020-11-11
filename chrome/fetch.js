let serverUrl = "" //TBD

async function postData(url = serverUrl, data = {}) {
  const response = await fetch(url, {
    method: 'post',
    body: JSON.stringify(data)
  })
  return response.json();
}

export async function postUrl(url) {
  return await postData(serverUrl, {video_url: url})
}