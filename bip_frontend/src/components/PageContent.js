import { Accordion } from "react-bootstrap"
import FileUpload from "./FileUpload"

function PageContent({
    error,
    isError,
    isPending,
    isFetchingIndexes,
    isDeleteMode,
    refetch,
    indexes,
    currentPage,
    setFileUploaded,
    data
}) {

        function renderMainContent() {
        if (isFetchingIndexes) {
            return <p>Fetching indexes...</p>
        } else if (!indexes.includes(currentPage)) {
            return <FileUpload
                setFileUploaded={setFileUploaded}
                currentPage={currentPage}
                refetch={refetch}
                isMenu={false}
            />
        } else if (isPending) {
            return <p>Loading the student list..</p>
        } else if (isError) {
            return <p>Error: {error.message}</p>
        } else {
            return (
                <Accordion className='w-100' flush>
                    {Object.keys(data).map((_v, i) => (
                        <Accordion.Item eventKey={data[i].id} key={data[i].id}>
                            {ItemHeader(i)}
                            {ItemBody(i)}
                        </Accordion.Item>
                    ))}
                </Accordion>
            )
        }
    }

    function ItemHeader(i) {
        return <Accordion.Header>
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
        </Accordion.Header>;
    }

    function ItemBody(i) {
        return <Accordion.Body>
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
        </Accordion.Body>;
    }

    return renderMainContent();
}

export default PageContent;