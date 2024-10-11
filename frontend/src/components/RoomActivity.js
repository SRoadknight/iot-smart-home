import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Table from 'react-bootstrap/Table';
import { statusMap } from '../utils/Utils';


const RoomActivity = () => {
    const { id: roomId } = useParams();
    const [room, setRoom] = useState(null);

    useEffect(() => {
        axiosClient.get(`/rooms/${roomId}/activities`)
            .then(response => {
                setRoom(response.data);
                console.log('Room fetched: ', response.data);
            })
            .catch(error => {
                console.error('Error fetching room: ', error);
            });
    }, [roomId]);

    return (
        <>
            {room && (
                <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Model</th>
                        <th>Status</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {room.map(activity => (
                        <tr key={activity.activity_id}>
                            <td>
                                <a href={`/devices/${activity.device_id}`}>
                                    {activity.device_name}
                                </a>
                            </td>
                            <td>{activity.device_model}</td>
                            <td>{statusMap(activity.activity)}</td>
                            <td>{activity.timestamp}</td>
                        </tr>
                    ))
                    }
                </tbody>
            </Table>
            )}
        </>
    );
}

export default RoomActivity;