import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { statusMap } from '../utils/Utils';

const ViewDevices = () => {
    const [devices, setDevices] = useState([]);

    useEffect(() => {
        axiosClient.get('/devices')
            .then(response => {
                setDevices(response.data);
                console.log('Devices fetched: ', response.data);
            })
            .catch(error => {
                console.error('Error fetching devices: ', error);
            });
    }, []);

    return (
        <>
            <Card className="mb-3">
                    <Card.Header>
                        <Card.Title>Devices</Card.Title>
                    </Card.Header>
                <Card.Body>
                    <Row>
                        {devices.map(device => (
                            <Col key={device._id} md={4} className="mb-3">
                                <Card>
                                    <Card.Header>
                                        <Card.Title>{device.name}</Card.Title>
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
                                        <Card.Text>
                                            <a href={`/rooms/${device.room_id}`}>
                                                {device.room.name}
                                            </a>
                                        </Card.Text>
                                  
                                        <Button variant="primary" href={`/devices/${device._id}`}>View</Button>
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

export default ViewDevices;