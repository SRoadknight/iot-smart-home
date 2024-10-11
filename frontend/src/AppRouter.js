import { Route, Routes, Navigate} from 'react-router-dom';
import Home from './components/Home';
import RoomRoutes from './components/RoomRoutes';
import RoomActiveDevices from './components/RoomActiveDevices';
import DevicesRoutes from './components/DevicesRoutes';
import DeviceConsumption from './components/DeviceConsumption';
import ViewRooms from './components/ViewRooms';
import Room from './components/Room';
import RoomActivity from './components/RoomActivity';
import ViewDevices from './components/ViewDevices';
import RoomConsumption from './components/RoomConsumption';
import Device from './components/Device';
import DeviceActivities from './components/DeviceActivities';


const AppRouter = () => {


    return (
        <Routes>
            <Route path="/" element={<Navigate to="/home" replace />} />


            <Route path="/rooms/:id/*" element={<RoomRoutes />}>
                <Route index element={<Navigate to="devices" replace />} />
                <Route path="devices" element={<Room />} />
                <Route path="activity" element={<RoomActivity />} />
                <Route path="consumption" element={<RoomConsumption />} />
            </Route>


            <Route path="/devices/:id/*" element={<DevicesRoutes />}>
            <Route index element={<Navigate to="summary" replace />} />
                <Route path="summary" element={<Device />} />
                <Route path="activity" element={<DeviceActivities />} />
                <Route path="consumption" element={<DeviceConsumption />} />
            </Route>

            <Route path="/home" element={<Home />} />

            <Route path="/rooms" element={<ViewRooms />} />
            <Route path="/devices" element={<ViewDevices />} />
            
        </Routes>
    );
};

export default AppRouter;