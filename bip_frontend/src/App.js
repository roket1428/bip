import './styles/styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap-reboot.min.css';
import 'bootstrap-icons/font/bootstrap-icons.min.css';
import { Container, Stack } from 'react-bootstrap';
import { Navbar } from 'react-bootstrap';
import PageContent from './components/PageContent';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ThemeSwitcher from './components/ThemeSwitcher';

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: Infinity,
        },
    },
})

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <Stack>
                <Navbar className="bg-navbar shadow-sm">
                    <Container className='justify-content-center custom-container'>
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
                    <ThemeSwitcher />
                </Navbar>
                <PageContent />
            </Stack>
        </QueryClientProvider>
    );
}

export default App;
