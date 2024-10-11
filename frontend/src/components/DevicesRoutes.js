import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { NavLink, Outlet } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { useParams } from 'react-router-dom';


const DevicesRoutes = () => {
    const { id: deviceId } = useParams();
    const [device, setDevice] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axiosClient.get(`/devices/${deviceId}`)
            .then(response => {
                setDevice(response.data);
                setLoading(false);
                console.log('Device fetched: ', response.data);
            })
            .catch(error => {
                console.error('Error fetching device: ', error);
            });
    }, [deviceId]);
    
    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <Navbar>
                <Navbar.Brand>
                    <Nav.Link as={NavLink} to="summary">{device.name}</Nav.Link>
                </Navbar.Brand>
                <Nav className="mr-auto">
                    <Nav.Link as={NavLink} to="activity">Activity Log</Nav.Link>
                    <Nav.Link as={NavLink} to="consumption">Consumption Log</Nav.Link>
                </Nav>
            </Navbar>
            <Outlet />
        </div>
    );
}

export default DevicesRoutes;