import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import Table from 'react-bootstrap/Table';

const RoomConsumption = () => {
    const { id: roomId } = useParams();
    const [room, setRoom] = useState(null);

    useEffect(() => {
        axiosClient.get(`/rooms/${roomId}/consumption`)
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
                        <th>Consumption</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {room.map(consumption => (
                        <tr key={consumption.consumption_id}>
                            <td>
                                <a href={`/devices/${consumption.device_id}`}>
                                    {consumption.device_name}
                                </a>
                            </td>
                            <td>{consumption.device_model}</td>
                            <td>{consumption.device_consumption}</td>
                            <td>{consumption.timestamp}</td>
                        </tr>
                    ))
                    }
                </tbody>
            </Table>
            )}
        </>
    );
}

export default RoomConsumption;
