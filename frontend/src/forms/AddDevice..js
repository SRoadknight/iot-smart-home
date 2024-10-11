import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';


const AddDevice = ({ onFormSubmit, roomId }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [type, setType] = useState('');
    const [name, setName] = useState('');
    const [model, setModel] = useState('');
    const [status, setStatus] = useState('');
    const [id, setId] = useState(roomId);


    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const handleFormSubmit = (event) => {
        event.preventDefault();
        const device = { type, name, model, status, room_id: id};
        onFormSubmit(device);
        setType('');
        setName('');
        setModel('');
        setStatus('');
        closeModal();
    }

    return (
        <>
            <Button onClick={openModal}>Add Device</Button>
            <Modal show={isModalOpen} onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Add Device</Modal.Title>
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
                        <Form.Group controlId="type" className="mb-3">
                            <Form.Label>Type</Form.Label>
                            <Form.Control
                                type="text"
                                value={type}
                                onChange={(event) => setType(event.target.value)}
                            />
                        </Form.Group>
                        <Form.Group controlId="model" className="mb-3">
                            <Form.Label>Model</Form.Label>
                            <Form.Control
                                type="text"
                                value={model}
                                onChange={(event) => setModel(event.target.value)}
                            />
                        </Form.Group>
                        <Form.Group controlId="status" className="mb-3">
                            <Form.Label>Status</Form.Label>
                            <Form.Control
                                type="text"
                                value={status}
                                onChange={(event) => setStatus(event.target.value)}
                            />
                        </Form.Group>
                        <Button type="submit">Add Device</Button>
                    </Form>
                </Modal.Body>
            </Modal>
        </>
    );
}


export default AddDevice;