/* eslint-disable no-undef */
import React, { useState } from 'react';
import { Client as Styletron } from 'styletron-engine-atomic';
import { Provider as StyletronProvider } from 'styletron-react';
import { LightTheme, BaseProvider, styled } from 'baseui';
import Sweetube from './sweetube/sweetube';

const engine = new Styletron();
const Centered = styled('div', {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  height: '100%',
});

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [topThree, setTopThree] = useState([]);
  const [rateSentence, setRateSentence] = useState('');
  const [videoId, setVideoId] = useState('');
  chrome.runtime.onMessage.addListener(request => {
    if (request.type === 'show-modal') {
      document.querySelector('.video-stream').pause();
      setTopThree(request.topThree);
      setRateSentence(request.rateSentence);
      setVideoId(request.videoId);
      setIsOpen(true);
    }
  });
  return (
    <StyletronProvider value={engine}>
      <BaseProvider theme={LightTheme}>
        <Centered>
          <Sweetube
            topThree={topThree}
            rateSentence={rateSentence}
            videoId={videoId}
            isOpen={isOpen}
            onClose={() => setIsOpen(false)}
          />
        </Centered>
      </BaseProvider>
    </StyletronProvider>
  );
}

export default App;
