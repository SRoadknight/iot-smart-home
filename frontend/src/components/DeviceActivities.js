import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import Table from 'react-bootstrap/Table';
import Card from 'react-bootstrap/Card';

const DeviceActivities = () => {
    const { id } = useParams();
    const [device, setDevice] = useState(null);

    useEffect(() => {
        axiosClient.get(`/devices/${id}/activities`)
            .then(response => {
                setDevice(response.data);
                console.log('Device fetched: ', response.data);
            })
            .catch(error => {
                console.error('Error fetching device: ', error);
            });
    }, [id]);

    return (
        <>
            {device && (
                <Card className="mb-3">
                    <Card.Header>
                        <Card.Title>Recent Activities</Card.Title>
                    </Card.Header>
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Activity</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {device.map(activity => (
                            <tr key={activity.activity_id}>
                                <td>{activity.activity}</td>
                                <td>{activity.timestamp}</td>
                            </tr>
                        ))
                        }
                    </tbody>
                </Table>
                </Card>
            )}
        </>
    );
}

export default DeviceActivities;

