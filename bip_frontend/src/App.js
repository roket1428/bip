import './styles/styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap-reboot.min.css';
import 'bootstrap-icons/font/bootstrap-icons.min.css';
import { Container, Stack } from 'react-bootstrap';
import { Navbar } from 'react-bootstrap';
import PageContent from './components/PageContent';

function App() {
    return (
        <Stack>
            <Navbar className="bg-navbar rounded-4 rounded-bottom-0 m-1 mb-0 shadow-sm">
                <Container className='justify-content-center'>
                    <Navbar.Brand>
                        <img
                            alt="BIP logo"
                            src="/img/favicon-32x32.png"
                            width="32"
                            height="32"
                            className="d-inline-block align-top"
                        />{' '}
                        Bilgi İşleme Projesi
                    </Navbar.Brand>
                </Container>
            </Navbar>
            <PageContent />
        </Stack>
    );
}

export default App;
