import React, { useRef } from "react";
import { Button } from "antd";
import { UploadOutlined } from "@ant-design/icons";
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
            const response = await useApi_file.post("/filter/upload", fileForm);
            const isSuccess = response.data.result;

            // CHECK THE UPLOADED FILE
            // console.log("sent data: ", fileForm.get("file"));

            if (isSuccess === "SUCCESS") {
                alert("파일을 정상적으로 업로드하였습니다.");
                return;
            } else if (isSuccess === "UPLOAD FAIL : DUPLICATE FILENAME") {
                alert("파일 업로드에 실패했습니다. 중복된 파일명이 존재합니다.");
                return;
            } else {
                alert("파일 업로드에 실패했습니다. 다시 시도해주세요.");
                return;
            }
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
                icon={<UploadOutlined />}
            >
                Upload
            </Button>
        </>
    );
};

export default UploadBtn;
