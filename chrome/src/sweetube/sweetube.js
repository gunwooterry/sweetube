import React from 'react';
import {
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalButton,
  SIZE,
  ROLE
} from 'baseui/modal';
import { KIND as ButtonKind } from 'baseui/button';
import { feedback } from './fetch.js'

function getTimestamp(second) {
  let rounded = Math.round(second);
  let min = Math.floor(rounded / 60)
  let sec = rounded % 60
  min = 10 > min ? '0' + min : min;
  sec = 10 > sec ? '0' + sec : sec;
  return `${min}:${sec}`;
}

export default function Sweetube({ videoId, topThree, rateSentence, isOpen, onClose }) {
  function backToPreviousPage() {
    window.history.back();
    onClose();
  }
  function sendRate(isValid) {
    // fire and forget
    feedback(
      {
        video_id: videoId,
        phrase: rateSentence.text,
        is_valid: isValid,
      }
    )
  }
  return (
    <Modal
      onClose={onClose}
      closeable
      isOpen={isOpen}
      animate
      size={SIZE.auto}
      role={ROLE.dialog}
      overrides={{
        Root: {
          style: () => ({
            zIndex: '9999',
          })
        }
      }}
    >
      <ModalHeader>Hate Speech Detected</ModalHeader>
      <ModalBody>
        <p>{topThree.map(s => <p>{s.text} (at {getTimestamp(s.start_time)})</p>)}</p>
        <br/>
        <h3>Please rate text to improve our model</h3>
        <p>{rateSentence.text}</p>
        <ModalButton onClick={() => sendRate(true)}>
          It's harmful
        </ModalButton>
        <ModalButton kind={ButtonKind.tertiary} onClick={() => sendRate(false)}>Harmless</ModalButton>
      </ModalBody>
      <ModalFooter>
        <ModalButton kind={ButtonKind.tertiary} onClick={onClose}>
          Skip
        </ModalButton>
        <ModalButton onClick={backToPreviousPage}>Stop Watching</ModalButton>
      </ModalFooter>
    </Modal>
  )
}
