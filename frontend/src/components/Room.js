import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { statusMap } from '../utils//Utils';
import Table from 'react-bootstrap/Table';
import AddDevice from '../forms/AddDevice.';

const Room = () => {
    const { id: roomId } = useParams();
    const [room, setRoom] = useState(null);

    useEffect(() => {
        axiosClient.get(`/rooms/${roomId}?include_devices=true`)
            .then(response => {
                setRoom(response.data);
                console.log('Room fetched: ', response.data);
            })
            .catch(error => {
                console.error('Error fetching room: ', error);
            });
    }, [roomId]);

    const handleFormSubmit = (device) => {
        axiosClient.post(`/devices`, device)
            .then(response => {
                setRoom({ ...room, devices: [...room.devices, response.data] });
                console.log('Device added: ', response.data);
            })
            .catch(error => {
                console.error('Error adding device: ', error);
            });
    }

    return (
        <>
            {room && (
                <Card className="mb-3">
                    <Card.Header>
                        <Card.Title>{room.name}</Card.Title>
                        <AddDevice onFormSubmit={handleFormSubmit} roomId={room._id} />
                    </Card.Header>
                    <Card.Body>
                        <Row>
                            {room.devices.map(device => (
                                <Col key={device._id} md={4} className="mb-3">
                                    <Card>
                                        <Card.Header>
                                            <Card.Title>
                                                <a href={`/devices/${device._id}`}>
                                                    {device.name}
                                                </a>
                                            </Card.Title>
                                        </Card.Header>
                                        <Card.Body>
                                            <Card.Text>
                                                {device.type}
                                            </Card.Text>
                                            <Card.Text>
                                                {device.model}
                                            </Card.Text>
                                            <Card.Text>
                                                {statusMap(device.status)}
                                            </Card.Text>
                                        </Card.Body>
                                    </Card>
                                </Col>
                            ))}
                        </Row>
                    </Card.Body>
                </Card>
            )}
        </>
    );
}

export default Room;