import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/NavBar';
import Container from 'react-bootstrap/Container';
import NavDropdown from 'react-bootstrap/NavDropdown';

const AppNav = () => {



    return (
        <Navbar expand="lg">
            <Container>
                <Navbar.Brand href="/">IoThings</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <NavDropdown title="Rooms" id="basic-nav-dropdown">
                            <NavDropdown.Item href="/rooms">View Rooms</NavDropdown.Item>
                        </NavDropdown>
                        <NavDropdown title="Devices" id="basic-nav-dropdown">
                            <NavDropdown.Item href="/devices">View Devices</NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );

};

export default AppNav;