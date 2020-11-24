chrome.runtime.onMessage.addListener((request) => {
  if (request.type === 'show-modal') {
    showModal(request.data);
  }
})

const showModal = async (data) => {
  // TODO: Popup modal properly with given data
  console.log("SHOW MODAL CALLED");
  console.log(data)
}