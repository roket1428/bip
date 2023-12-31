import axios from "axios";
import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";

// TODO: implement sending files to the api endpoint using axios.
function FileUpload({ setFileUploaded, currentPage, refetch }) {
    const onDrop = useCallback(async (acceptedFiles) => {
        const formData = new FormData();
        formData.append('year', currentPage);
        acceptedFiles.forEach(file => {
           formData.append('file', file);
        });
        await axios.post('upload/', formData)
            .then(() => {
                refetch();
                setFileUploaded(true);
            })
            .catch((error) => {
                console.error(error);
            })
    }, [setFileUploaded, currentPage, refetch]);

    const { getRootProps, getInputProps, IsDragActive } = useDropzone({ onDrop })

    return (
        <div className="fileupload-area rounded-4 shadow-sm" {...getRootProps()}>
            <input {...getInputProps()} />
            <i className="bi bi-file-earmark-arrow-up-fill fs-1"></i>
            <p className="m-0">{IsDragActive ? 'Buraya sürükle.' : 'Dosya yükleyin.'}</p>
        </div>
    );
}

export default FileUpload;