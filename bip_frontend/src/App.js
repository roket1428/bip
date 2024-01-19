import './styles/styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap-reboot.min.css';
import 'bootstrap-icons/font/bootstrap-icons.min.css';
import { Container, Stack } from 'react-bootstrap';
import { Navbar } from 'react-bootstrap';
import PageContainer from './components/PageContainer';

function App({ queryClient }) {
    return (
        <Stack>
            <Navbar className="bg-navbar shadow-sm">
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
            <PageContainer queryClient={queryClient} />
            <div className='d-flex justify-content-center'>
                <h4 className='version-info'>BIP - Prototype version - KarneParser (Legacy)</h4>
            </div>
        </Stack>
    );
}

export default App;
