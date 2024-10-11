import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import AddRoom from '../forms/AddRoom';

const ViewRooms = () => {
    const [rooms, setRooms] = useState([]);

    useEffect(() => {
        let params = { include_devices: true };
        axiosClient.get('/rooms', { params })
            .then(response => {
                setRooms(response.data);
                console.log('Rooms fetched: ', response.data);
            })
            .catch(error => {
                console.error('Error fetching rooms: ', error);
            });
    }, []);

    const handleFormSubmit = (room) => {
        axiosClient.post('/rooms', room)
            .then(response => {
                setRooms([...rooms, response.data]);
                console.log('Room added: ', response.data);
            })
            .catch(error => {
                console.error('Error adding room: ', error);
            });
    }


    return (
        <>
            <Card className="mb-3">
                    <Card.Header>
                        <Card.Title>Rooms</Card.Title>
                        <AddRoom onFormSubmit={handleFormSubmit} />
                    </Card.Header>
                <Card.Body>
                    <Row>
                        {rooms.map(room => (
                            <Col key={room._id} md={4} className="mb-3">
                                <Card>
                                    <Card.Header>
                                        <Card.Title>{room.name}</Card.Title>
                                    </Card.Header>
                                    <Card.Body>
                                        {room.devices  && (
                                            <Card.Text>
                                                <strong>Devices</strong>: {room.devices.length}
                                            </Card.Text>
                                        )}
                                        {room.temperature && (
                                            <Card.Text>
                                                <strong>Temperature</strong>: {room.temperature}°C
                                            </Card.Text>
                                        )}
                                        <Button variant="primary" href={`/rooms/${room._id}`}>View Room</Button>
                                    </Card.Body>
                                </Card>
                            </Col>
                        ))}
                    </Row>
                </Card.Body>
            </Card>
        </>
    );
}

export default ViewRooms;