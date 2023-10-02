import React, { useRef } from "react";
import { Button } from "antd";
import { useApi_file } from "../../hooks/api/axiosInterceptor";

const UploadBtn = () => {
    const fileInputRef = useRef();

    const handleButtonClick = () => {
        fileInputRef.current.value = null;
        fileInputRef.current.click();
    };

    const handleFileUpload = async (e) => {
        e.preventDefault();
        const selectedFile = e.target.files[0];

        if (!selectedFile) {
            console.log("file selection cancelled");
            return;
        }

        const fileForm = new FormData();
        fileForm.append("file", selectedFile);

        try {
            await useApi_file.post("/filter/upload", fileForm);

            // CHECK THE UPLOADED FILE
            // console.log("sent data: ", fileForm.get("file"));

            alert("파일 업로드가 완료되었습니다.");
        } catch (err) {
            console.log(err);
        }
    };

    return (
        <>
            <input
                type="file"
                accept=".txt"
                name="file"
                id="file"
                ref={fileInputRef}
                onChange={handleFileUpload}
                style={{ display: "none" }}
            />
            <Button
                style={{ backgroundColor: "#212653", color: "white" }}
                onClick={handleButtonClick}
            >
                Upload
            </Button>
        </>
    );
};

export default UploadBtn;
