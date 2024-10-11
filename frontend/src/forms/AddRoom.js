import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

const AddRoom = ({ onFormSubmit }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [name, setName] = useState('');

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const handleFormSubmit = (event) => {
        event.preventDefault();
        onFormSubmit({ name });
        setName('');
        closeModal();
    }

    return (
        <>
            <Button onClick={openModal}>Add Room</Button>
            <Modal show={isModalOpen} onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Add Room</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleFormSubmit}>
                        <Form.Group controlId="name" className="mb-3">
                            <Form.Label>Name</Form.Label>
                            <Form.Control
                                type="text"
                                value={name}
                                onChange={(event) => setName(event.target.value)}
                            />
                        </Form.Group>
                        <Button type="submit">Add Room</Button>
                    </Form>
                </Modal.Body>
            </Modal>
        </>
    );
}

export default AddRoom;
