import './styles/styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap-reboot.min.css';
import 'bootstrap-icons/font/bootstrap-icons.min.css';
import { Container, Stack } from 'react-bootstrap';
import { Navbar } from 'react-bootstrap';
import { Button } from 'react-bootstrap';
import FileUpload from './components/FileUpload';

function App() {
  return (
    <Stack>
      <Navbar className="bg-navbar rounded-4 rounded-bottom-0 m-1 mb-0 shadow-sm">
        <Container className='justify-content-center'>
          <Navbar.Brand>
            <img
              alt=""
              src="/img/favicon-32x32.png"
              width="32"
              height="32"
              className="d-inline-block align-top"
            />{' '}
            Bilgi İşleme Projesi
          </Navbar.Brand>
        </Container>
      </Navbar>

      <Navbar className="bg-navbar rounded-4 rounded-top-0 m-1 mt-0 shadow-sm">
        <Container fluid>
          <Button size='lg' className='btn-menu rounded-pill'>
            <i class="bi bi-caret-left-fill"></i>
          </Button>
          <h1 className='text-center'>2022-2023 Yılı Mezun Adayları Listesi</h1>
          <Button size='lg' className='btn-menu rounded-pill'>
            <i class="bi bi-caret-right-fill"></i>
          </Button>
        </Container>
      </Navbar>
      <Container className='d-flex fileupload-container'>
        <FileUpload />
      </Container>
    </Stack>
  );
}

export default App;
