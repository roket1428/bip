import { Navbar, Container, Button } from "react-bootstrap";

function PageNavigator({
    isError,
    isPending,
    isFetchingIndexes,
    indexes,
    currentPage,
    setCurrentPage,
}) {
    const goToNextPage = () => {
        setCurrentPage((prevPage) => prevPage + 1);
    };
    const goToPrevPage = () => {
        setCurrentPage((prevPage) => prevPage - 1);
    };

    const renderNavbar = () => {
        if (!isFetchingIndexes
            && indexes.includes(currentPage)
            && !isPending
            && !isError) {
            return (
                    <div className="outer-nav">
                        <Container className="inner-nav">
                            <Button
                                size="lg"
                                className="btn-menu rounded-pill"
                                onClick={goToPrevPage}>
                                <i className="bi bi-caret-left-fill"></i>
                            </Button>
                            <h1 className="text-center">
                                {currentPage - 1 + "-" + currentPage} Yılı Mezun
                                Adayları Listesi
                            </h1>
                            <Button
                                size="lg"
                                className="btn-menu rounded-pill"
                                onClick={goToNextPage}>
                                <i className="bi bi-caret-right-fill"></i>
                            </Button>
                        </Container>
                    </div>
            )
        } else {
            return (
                <Container>
                    <Button
                        size="lg"
                        className="btn-menu rounded-pill"
                        onClick={goToPrevPage}>
                        <i className="bi bi-caret-left-fill"></i>
                    </Button>
                    <h1 className="text-center">
                        {currentPage - 1 + "-" + currentPage} Yılı Mezun
                        Adayları Listesi
                    </h1>
                    <Button
                        size="lg"
                        className="btn-menu rounded-pill"
                        onClick={goToNextPage}>
                        <i className="bi bi-caret-right-fill"></i>
                    </Button>
                </Container>
            )
        }
    }

    return (
        <Navbar className="bg-navbar rounded-4 rounded-top-0 shadow-sm z-3">
            {renderNavbar()}
        </Navbar>
    );
}

export default PageNavigator;
