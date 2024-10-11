import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { useParams } from 'react-router-dom';
import { Card, Nav } from 'react-bootstrap';
import { statusMap } from '../utils/Utils';
import DeviceActivities from './DeviceActivities';
import DeviceConsumption from './DeviceConsumption';

const Device = () => {
    const { id } = useParams();
    const [device, setDevice] = useState(null);

    useEffect(() => {
        axiosClient.get(`/devices/${id}`)
            .then(response => {
                setDevice(response.data);
            })
            .catch(error => {
                console.error(error);
            });
    }, [id]);

    return (
        <div>
            {device && (
                <>
                <Card className="mb-3">
                    <Card.Header>
                        <Card.Title>{device.name} - Info </Card.Title>
                    </Card.Header>
                    <Card.Body>
                        <Card.Text>
                            <a href={`/rooms/${device.room_id}`}>{device.room.name}
                            </a>
                        </Card.Text>
                        <Card.Text>Type: {device.type}</Card.Text>
                        <Card.Text>Model: {device.model}</Card.Text>
                        <Card.Text>Status: {statusMap(device.status)}</Card.Text>
                    </Card.Body>
                </Card>
                { <DeviceActivities /> }
                { <DeviceConsumption />}

                </>
            )}
        </div>
    );
}

export default Device;


