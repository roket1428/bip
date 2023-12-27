import axios from 'axios';
import { useState, useEffect } from 'react';

import { Container } from 'react-bootstrap';
import { Navbar } from 'react-bootstrap';
import { Button } from 'react-bootstrap';

import FileUpload from './FileUpload';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';

function PageContent() {
    // get indexes array at the first render call
    useEffect(() => {
        axios.get('indexes')
            .then((request) => {
                let yearArray = [];
                request.data.forEach(item => {
                    yearArray.push(item['year']);
                });
                // console.log(yearArray);
            })
            .catch((errors) => {
                if (!errors.response) {
                    console.log(errors);
                }
            })
    }, [])
    
    // we calculate current grad year from the current month
    let grad_year;
    const date = new Date();
    if (date.getMonth() >= 7) {
        grad_year = date.getFullYear() + 1;
    } else {
        grad_year = date.getFullYear();
    }

    const [currentPage, setCurrentPage] = useState(grad_year);
    // const [pageContent, setPageContent] = useState('');

    // async function fetchPageContent(pageNumber) {
    // TODO: implement this
    // }

    // useEffect(() => {
    //     fetchPageContent(currentPage);
    // }, [currentPage]);

    const goToNextPage = () => {
        setCurrentPage((prevPage) => prevPage + 1);
    };
    const goToPrevPage = () => {
        setCurrentPage((prevPage) => Math.max(prevPage - 1, 1));
    };

    return (
        <>
            <Navbar className="bg-navbar rounded-4 rounded-top-0 m-1 mt-0 shadow-sm">
                <Container fluid>
                    <Button size='lg' className='btn-menu rounded-pill' onClick={goToPrevPage}>
                        <i className="bi bi-caret-left-fill"></i>
                    </Button>
                    <h1 className='text-center'>{currentPage-1 + '-' + currentPage} Yılı Mezun Adayları Listesi</h1>
                    <Button size='lg' className='btn-menu rounded-pill' onClick={goToNextPage}>
                        <i className="bi bi-caret-right-fill"></i>
                    </Button>
                </Container>
            </Navbar>
            <Container className='d-flex fileupload-container'>
                <FileUpload />
            </Container>
        </>
    );
}

export default PageContent;