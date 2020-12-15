import React, { useState } from 'react';
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
import { Notification } from "baseui/notification";
import { EmoticonRating } from 'baseui/rating';
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
  const [rating, setRating] = useState(0);
  feedback(
    {
      video_id: videoId,
      phrase: rateSentence.text,
      is_valid: rating < 3,
    }
  )
  function backToPreviousPage() {
    window.history.back();
    onClose();
  }
  return (
    <Modal
      onClose={onClose}
      closeable
      isOpen={isOpen}
      animate
      size={SIZE.default}
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
        {topThree.map(s => 
          <Notification
            overrides={{
              Body: {style: {width: 'auto'}},
            }}
          >
            <b>{getTimestamp(s.start_time)}</b> {s.text}
          </Notification>
        )}
      </ModalBody>
      <ModalHeader>How do you feel about this sentence?</ModalHeader>
      <ModalBody>
        <Notification
          overrides={{
            Body: {style: {width: 'auto'}},
          }}  
        >
          {rateSentence.text}
        </Notification>
        <EmoticonRating value={rating} onChange={({value}) => setRating(value)}/>
      </ModalBody>
      <ModalFooter>
        <ModalButton kind={ButtonKind.tertiary} onClick={onClose}>
          Keep Watching
        </ModalButton>
        <ModalButton onClick={backToPreviousPage}>Stop Watching</ModalButton>
      </ModalFooter>
    </Modal>
  )
}
