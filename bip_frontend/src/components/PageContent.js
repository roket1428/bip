import axios from 'axios';
import { useState, useEffect, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';

import { Container } from 'react-bootstrap';
import { Navbar } from 'react-bootstrap';
import { Button } from 'react-bootstrap';
import { Accordion } from 'react-bootstrap';
import { Dropdown } from 'react-bootstrap';
import LoadingBar from 'react-top-loading-bar';

import FileUpload from './FileUpload';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';

function PageContent({ queryClient }) {
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
                    if (request.data.length !== 0) {
                        request.data.forEach(item => {
                            indexList.push(item['year']);
                        });
                    }
                    setIndexes(indexList);
                })
                .catch(() => {
                    console.error("Cannot get the index list from the server!");
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
            enabled: indexes.includes(currentPage),
        })

    useEffect(() => {
        loadingBar.current.complete();
    }, [isFetching]);

    const [isDeleteMode, setIsDeleteMode] = useState(false);
    const startDeleteMode = () => {
        setIsDeleteMode(true);
    }

    const submitDeleteRequest = async () => {
        const request_data = { data: {} };
        request_data['data']['year'] = currentPage;
        request_data['data']['id'] = [];

        const checkboxDivs = document.querySelectorAll("#checkbox-div");
        let isAtLeastOneChecked = false;
        checkboxDivs.forEach((v) => {
            if (v.children[0].checked) {
                request_data['data']['id'].push(v.children[0].attributes['id'].nodeValue);
                isAtLeastOneChecked = true;
            }
        });
        if (!isAtLeastOneChecked) {
            setIsDeleteMode(false);
            return;
        }
        await axios.delete('delete', request_data)
            .then(() => {
                const convertedList = request_data['data']['id'].map(Number);
                queryClient.setQueryData(['student_list', currentPage], (oldData) => {
                    oldData.forEach((v, i) => {
                        if (convertedList.includes(v['id'])) {
                            oldData.splice(i, 1);
                        }
                        return oldData;
                    })
                })
                setFileUploaded(true);
                setIsDeleteMode(false);
                loadingBar.current.complete();
            })
            .catch((error) => {
                console.error(error);
            })
    }
    useEffect(() => {
        if (isDeleteMode) {
            const checkboxDivs = document.querySelectorAll("#checkbox-div");
            checkboxDivs.forEach((v) => {
                v.children[0].addEventListener("click", (e) => {
                    e.stopPropagation();
                });
            });
        }
    }, [setIsDeleteMode, isDeleteMode]);

    return (
        <>
            <LoadingBar color='#2C56D1' ref={loadingBar} />
            <Navbar className="bg-navbar rounded-4 rounded-top-0 shadow-sm z-3">
                {!isFetchingIndexes && indexes.includes(currentPage) && !isPending && !isError ?
                    (<>
                        <div className='outer-div'>
                            <Container className='custom-secondary-container'>
                                <Button size='lg' className='btn-menu rounded-pill' onClick={goToPrevPage}>
                                    <i className="bi bi-caret-left-fill"></i>
                                </Button>
                                <h1 className='text-center'>{currentPage - 1 + '-' + currentPage} Yılı Mezun Adayları Listesi</h1>
                                <Button size='lg' className='btn-menu rounded-pill' onClick={goToNextPage}>
                                    <i className="bi bi-caret-right-fill"></i>
                                </Button>
                            </Container>
                        </div>
                        <Dropdown className='me-3'>
                            <Dropdown.Toggle className='btn-settings rounded-4' variant="primary" id="dropdown-basic">
                                Düzenle
                            </Dropdown.Toggle>

                            <Dropdown.Menu className='settings-menu' align='end'>
                                <FileUpload setFileUploaded={setFileUploaded} currentPage={currentPage} refetch={refetch} isMenu={true} />
                                <Dropdown.Item onClick={startDeleteMode}>
                                    Öğrenci Sil
                                </Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                    </>)
                    : (
                        <Container>
                            <Button size='lg' className='btn-menu rounded-pill' onClick={goToPrevPage}>
                                <i className="bi bi-caret-left-fill"></i>
                            </Button>
                            <h1 className='text-center'>{currentPage - 1 + '-' + currentPage} Yılı Mezun Adayları Listesi</h1>
                            <Button size='lg' className='btn-menu rounded-pill' onClick={goToNextPage}>
                                <i className="bi bi-caret-right-fill"></i>
                            </Button>
                        </Container>
                    )
                }
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
                                                    {isDeleteMode
                                                        ? (<div id='checkbox-div' className='me-2'>
                                                            <input id={data[i].id} className='form-check-input' type='checkbox' />
                                                        </div>)
                                                        : ""}
                                                    <p title='Öğrenci Numarası' className='p-data p-id flex-grow-1'>{data[i].student_id}</p>
                                                    <p className='p-data p-name flex-grow-1'>{data[i].name} {data[i].surname}</p>
                                                    <p title='Genel Not Ortalaması' className='p-data p-gno flex-grow-1'>GNO: {(data[i].gno).toFixed(2)}</p>
                                                    <p title='Toplam Kredi' className='p-data p-cred flex-grow-1'>Kredi: {(data[i].credits_sum).toFixed(0)}</p>
                                                    <p title='Toplam Puan' className='p-data p-point flex-grow-1'>Puan: {(data[i].points_sum).toFixed(0)}</p>
                                                </div>
                                            </Accordion.Header>
                                            <Accordion.Body>
                                                <p
                                                    className='text-center'>Zorunlu dersler alınmış mı?:
                                                    {data[i].grad_status.isTookLectures
                                                        ? <b>Evet</b>
                                                        : <b>Hayır</b>}
                                                    {!data[i].grad_status['problems']['lecture_not_taken']
                                                        ? "" : "-> Şunlar Eksik: "}
                                                    <b>{data[i].grad_status['problems']['lecture_not_taken']}</b>
                                                </p>
                                                <p
                                                    className='text-center'>Derslerde başarılı oldu mu?:
                                                    {data[i].grad_status.isPassedLetters
                                                        ? <b>Evet</b>
                                                        : <b>Hayır -{'>'}</b>}
                                                    <b>{data[i].grad_status['problems']['lecture_code']}
                                                        {data[i].grad_status['problems']['lecture_name']}
                                                        {!data[i].grad_status['problems']['grade_letter']
                                                            ? "" : "Harf Notu:"}
                                                        {data[i].grad_status['problems']['grade_letter']}
                                                    </b>
                                                </p>
                                                <p
                                                    className='text-center'>Alan dışı dersler alınmış mı?:
                                                    {data[i].grad_status.isHadAD
                                                        ? <b>Evet</b>
                                                        : <b>Hayır -{'>'} Alan dışı ders alınmamış yarıyıl: </b>}
                                                    <b>{data[i].grad_status['problems']['ad_not_taken_in_term']}</b>
                                                </p>
                                                <p
                                                    className='text-center'>Bölüm seçimlik dersler alınmış mı?:
                                                    {data[i].grad_status.isHadSD
                                                        ? <b>Evet</b>
                                                        : <b>Hayır -{'>'} Seçimlik ders alınmamış yarıyıl: </b>}
                                                    <b>{data[i].grad_status['problems']['sd_not_taken_in_term']}</b>
                                                </p>
                                                <div className='d-flex justify-content-evenly'>
                                                    <h4>Mezun Durumu: {data[i].grad_status.passed ? <b>Evet</b> : <b>Hayır</b>}</h4>
                                                    <h4>Staj onaylandı mı?: {data[i].grad_status.isInternPassed ? <b>Evet</b> : <b>Hayır</b>}</h4>
                                                </div>
                                            </Accordion.Body>
                                        </Accordion.Item>
                                    )
                                    )}
                                </Accordion>
                                )
                            )
                        )
                        : <FileUpload setFileUploaded={setFileUploaded} currentPage={currentPage} refetch={refetch} isMenu={false} />)
                }
            </Container>
            {isDeleteMode
                ? (<Button id='btn-remove-submit' className='btn-settings rounded-4' onClick={submitDeleteRequest} >Seçilenleri sil</Button>)
                : ""}
        </>
    );
}

export default PageContent;