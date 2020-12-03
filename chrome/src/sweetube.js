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

export default function Sweetube() {
  const [isOpen, setIsOpen] = useState(true);
  return (
    <Modal
      onClose={() => setIsOpen(false)}
      closeable
      isOpen={isOpen}
      animate
      autoFocus
      size={SIZE.default}
      role={ROLE.dialog}
    >
      <ModalHeader>Hate Speech Detected</ModalHeader>
      <ModalBody>
        Do you want to continue?
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