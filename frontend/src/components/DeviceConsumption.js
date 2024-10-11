import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import Table from 'react-bootstrap/Table';
import Card from 'react-bootstrap/Card';

const DeviceConsumption = () => {
    const { id } = useParams();
    const [device, setDevice] = useState(null);

    useEffect(() => {
        axiosClient.get(`/devices/${id}/consumption`)
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
                        <Card.Title>Recent Consumption</Card.Title>
                    </Card.Header>
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Consumption (kWh)</th>
                            <th>Time (Minute intervals)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {device.map(consumption => (
                            <tr key={consumption.consumption_id}>
                                <td>{consumption.value}</td>
                                <td>{consumption.timestamp}</td>
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

export default DeviceConsumption;