import Button from 'react-bootstrap/Button';

const Home = () => {
    return (
        <div>
            <h1>Home</h1>
            <p>Welcome to the IoThings Home Page - Under construction</p>
            <Button variant="primary" className="m-2" href="/rooms">View Rooms</Button>
            <Button variant="primary" className="m-2" href="/devices">View Devices</Button>
        </div>
    );
}

export default Home;