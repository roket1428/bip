import axios from 'axios';
import { useState, useEffect, useRef } from 'react';
import { keepPreviousData, useQuery } from '@tanstack/react-query';

import { Container } from 'react-bootstrap';
import { Navbar } from 'react-bootstrap';
import { Button } from 'react-bootstrap';
import { Accordion } from 'react-bootstrap';
import LoadingBar from 'react-top-loading-bar';

import FileUpload from './FileUpload';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';

function PageContent() {
    const loadingBar = useRef(null);

    // FileUpload component will update this state to recall fetchIndexes and trigger a re-render
    const [isFileUploaded, setFileUploaded] = useState(false);

    // indexes == list of unique graduation years
    // used for when to query the student list
    const [indexes, setIndexes] = useState([]);
    const [isFetchingIndexes, setFetchingIndexes] = useState(true);
    useEffect(() => {
        const fetchIndexes = async () => {
            const indexList = [];
            await axios.get('indexes')
                .then((request) => {
                    request.data.forEach(item => {
                        indexList.push(item['year']);
                    });
                    setIndexes(indexList);
                })
                .catch(() => {
                    console.log("No index found at the server!");
                })
                .finally(() => {
                    setFetchingIndexes(false);
                })
        }
        loadingBar.current.continuousStart();
        fetchIndexes();
        return () => {
            setFileUploaded(false);
        }
    }, [isFileUploaded, setFileUploaded]);

    let gradYear;
    const date = new Date();
    if (date.getMonth() >= 7) {
        gradYear = date.getFullYear() + 1;
    } else {
        gradYear = date.getFullYear();
    }

    // current page index will start at the current graduation year
    const [currentPage, setCurrentPage] = useState(gradYear);
    const goToNextPage = () => {
        setCurrentPage((prevPage) => prevPage + 1);
    };
    const goToPrevPage = () => {
        setCurrentPage((prevPage) => prevPage - 1);
    };

    const fetchPageContent = async (currentPage) => {
        const { data } = await axios.get('query', {
            params: {
                year: currentPage
            }
        })
        return data;
    }

    const { isPending, isError, isFetching, error, data, refetch } =
        useQuery({
            queryKey: ['student_list', currentPage],
            queryFn: () => fetchPageContent(currentPage),
            placeholderData: keepPreviousData,
            enabled: indexes.includes(currentPage),
        })

    useEffect(() => {
        loadingBar.current.complete();
    }, [isFetching]);

    return (
        <>
            <LoadingBar color='#2C56D1' ref={loadingBar} />
            <Navbar className="bg-navbar rounded-4 rounded-top-0 shadow-sm z-3">
                <Container>
                    <Button size='lg' className='btn-menu rounded-pill' onClick={goToPrevPage}>
                        <i className="bi bi-caret-left-fill"></i>
                    </Button>
                    <h1 className='text-center'>{currentPage - 1 + '-' + currentPage} Yılı Mezun Adayları Listesi</h1>
                    <Button size='lg' className='btn-menu rounded-pill' onClick={goToNextPage}>
                        <i className="bi bi-caret-right-fill"></i>
                    </Button>
                </Container>
            </Navbar>
            <Container className='d-flex fileupload-container'>
                {isFetchingIndexes
                    ? <p>Fetching indexes...</p>
                    : (indexes.includes(currentPage)
                        ? (isPending
                            ? (<p>Loading the student list...</p>)
                            : (isError
                                ? (<p>Error: {error.message}</p>)
                                : (<Accordion className='w-100' flush>
                                    {Object.keys(data).map((_v, i) => (
                                        <Accordion.Item eventKey={data[i].id} key={data[i].id}>
                                            <Accordion.Header>
                                                <div className='d-flex w-100 justify-content-between'>
                                                    <p title='Öğrenci Numarası' className='p-data'>{data[i].student_id}</p>
                                                    <p className='p-data p-name'>{data[i].name} {data[i].surname}</p>
                                                    <p title='Genel Not Ortalaması' className='p-data'>GNO: {data[i].gno}</p>
                                                    <p title='Toplam Kredi' className='p-data'>Kredi: {data[i].credits_sum}</p>
                                                    <p title='Toplam Puan' className='p-data'>Puan: {data[i].points_sum}</p>
                                                </div>
                                            </Accordion.Header>
                                            <Accordion.Body>

                                            </Accordion.Body>
                                        </Accordion.Item>
                                        )
                                    )}
                                </Accordion>
                                )
                            )
                        )
                        : <FileUpload setFileUploaded={setFileUploaded} currentPage={currentPage} refetch={refetch} />)
                }
            </Container>
        </>
    );
}

export default PageContent;