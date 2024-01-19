import axios from 'axios';
import { useState, useEffect, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useColorScheme } from '../hooks/useColorScheme';

import { Button, Container, Dropdown } from 'react-bootstrap';
import LoadingBar from 'react-top-loading-bar';

import PageNavigator from './PageNavigator';
import PageContent from './PageContent';
import FileUpload from './FileUpload';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';

function PageContainer({ queryClient }) {
    const loadingBar = useRef(null);
    const { isDark, setIsDark } = useColorScheme();

    // FileUpload component will update this state to recall fetchIndexes and trigger a re-render
    const [isFileUploaded, setFileUploaded] = useState(false);

    // indexes are list of unique graduation years
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

    const getCurrentGradYear = () => {
        let gradYear;
        const date = new Date();
        if (date.getMonth() >= 7) {
            gradYear = date.getFullYear() + 1;
        } else {
            gradYear = date.getFullYear();
        }
        return gradYear;
    }

    // current page index will start at the current graduation year
    const [currentPage, setCurrentPage] = useState(getCurrentGradYear());
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

    // finish the loading animation after isFetching changes
    useEffect(() => {
        loadingBar.current.complete();
    }, [isFetching]);

    const [isDeleteMode, setIsDeleteMode] = useState(false);
    const submitDeleteRequest = async () => {
        const request_data = { data: {} };
        request_data['data']['year'] = currentPage;
        request_data['data']['id'] = [];

        const checkboxDivs = document.querySelectorAll("#checkbox-div");
        let isNoneChecked = true;
        checkboxDivs.forEach((v) => {
            if (v.children[0].checked) {
                request_data['data']['id'].push(v.children[0].attributes['id'].nodeValue);
                isNoneChecked = false;
            }
        });
        if (isNoneChecked) {
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

    // stop triggering dropdown menu after user clicks to the checkbox
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

    function renderDeleteMenu() {
        if (!isFetchingIndexes
            && indexes.includes(currentPage)
            && !isPending
            && !isError) {

            return (
                <>
                    <FileUpload
                        setFileUploaded={setFileUploaded}
                        currentPage={currentPage}
                        refetch={refetch}
                        isMenu={true}
                    />
                    <Dropdown.Item onClick={() => setIsDeleteMode(true)}>
                        <i class="bi bi-dash-square"></i>{" "}Öğrenci Sil
                    </Dropdown.Item>
                    <hr class="hr" />
                </>
            );
        } else {
            return "";
        }
    }

    return (
        <>
            <LoadingBar color='#2C56D1' ref={loadingBar} />
            <PageNavigator
                isError={isError}
                isPending={isPending}
                isFetchingIndexes={isFetchingIndexes}
                indexes={indexes}
                currentPage={currentPage}
                setCurrentPage={setCurrentPage}
            />
            <Container className='d-flex justify-content-center'>
                <PageContent
                    error={error}
                    isError={isError}
                    isPending={isPending}
                    isFetchingIndexes={isFetchingIndexes}
                    isDeleteMode={isDeleteMode}
                    refetch={refetch}
                    indexes={indexes}
                    currentPage={currentPage}
                    setFileUploaded={setFileUploaded}
                    data={data}
                />
            </Container>
            <div className='floating-container'>
                {isDeleteMode
                    ? (<Button
                        id='btn-remove-submit'
                        className='btn-settings rounded-4'
                        onClick={submitDeleteRequest}>
                        Seçilenleri sil
                    </Button>)
                    : ""}
                <Dropdown drop="up" className='ms-2'>
                    <Dropdown.Toggle
                        className="btn-settings rounded-4"
                        variant="primary"
                        id="dropdown-basic">
                        <i class="bi bi-gear-fill"></i>
                    </Dropdown.Toggle>

                    <Dropdown.Menu className="settings-menu" align="end">
                        {renderDeleteMenu()}
                        <Dropdown.Item onClick={() => setIsDark(!isDark)}>
                            {isDark
                                ? (<>
                                    <i class="bi bi-sun-fill"></i>{" "}
                                    Aydınlık Mod
                                </>
                                )
                                : (<>
                                    <i class="bi bi-moon-fill"></i>{" "}
                                    Karanlık Mod
                                </>
                                )}
                        </Dropdown.Item>
                    </Dropdown.Menu>
                </Dropdown>
            </div>
        </>
    );
}

export default PageContainer;