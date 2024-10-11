import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { NavLink, Outlet } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { useParams } from 'react-router-dom';

const RoomRoutes = () => {

    const { id: roomId } = useParams();
    const [room, setRoom] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axiosClient.get(`/rooms/${roomId}`)
            .then(response => {
                setRoom(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching room: ', error);
            });
    }, [roomId]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <Navbar>
            <Navbar.Brand><Nav.Link as={NavLink} to="devices">{room.name}</Nav.Link></Navbar.Brand>
                <Nav className="mr-auto">
                    <Nav.Link as={NavLink} to="devices">Devices</Nav.Link>
                    <Nav.Link as={NavLink} to="activity">Activity Log</Nav.Link>
                    <Nav.Link as={NavLink} to="consumption">Consumption Log</Nav.Link>
                </Nav>
            </Navbar>
            <Outlet />
        </div>
    );
}

export default RoomRoutes;