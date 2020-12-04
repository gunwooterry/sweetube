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

function getTimestamp(second) {
  let rounded = Math.round(second);
  return `${Math.floor(rounded / 60)}:${rounded % 60}`;
}

export default function Sweetube({ data, isOpen, onClose }) {
  return (
    <Modal
      onClose={onClose}
      closeable
      isOpen={isOpen}
      animate
      size={SIZE.auto}
      role={ROLE.dialog}
    >
      <ModalHeader>Hate Speech Detected</ModalHeader>
      <ModalBody>
        {data.map(s => <p>{s.text} (at {getTimestamp(s.start_time)})</p>)}
      </ModalBody>
      <ModalFooter>
        <ModalButton kind={ButtonKind.tertiary}>
          Skip
        </ModalButton>
        <ModalButton>Stop Watching</ModalButton>
      </ModalFooter>
    </Modal>
  )
}
