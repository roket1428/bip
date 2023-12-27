import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";

// TODO: implement sending files to the api endpoint using axios.
function FileUpload() {
    const onDrop = useCallback(acceptedFiles => {
        //const formData = new FormData();
        console.log("test");
    }, []);
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