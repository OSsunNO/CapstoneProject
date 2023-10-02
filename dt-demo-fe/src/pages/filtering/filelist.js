import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { List } from "antd";
import UploadBtn from "../../components/file/uploadBtn";
import useApi from "../../hooks/api/axiosInterceptor";

const Container = styled.div`
    display: flex;
    flex-direction: column;
    width: 400px;
    height: 400px;
    margin-right: 20px;
`;

const FileListWrapper = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

const EmptyFileList = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    height: 350px;
    width: 100%;
    border-radius: 10px;
    border: 1px solid #bfbfbf;
`;

const BtnBar = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-top: 10px;
    height: 50px;
    width: 100%;
    justify-content: space-between;
`;

const FileListContainer = () => {
    const [isFileExist, setIsFileExist] = useState(false);
    const [fileList, setFileList] = useState([]);

    // TODO: Enable file selection

    const getFiles = async () => {
        try {
            const { data } = await useApi.get("/filter/filelist");
            console.log("get files from server");
            setFileList(data);
            setIsFileExist(true);
        } catch (err) {
            console.log(err.response);
        }
    };

    useEffect(() => {
        getFiles();
    }, []);

    return (
        <Container>
            <FileListWrapper>
                {isFileExist ? (
                    <List
                        style={{
                            height: "350px",
                            width: "100%",
                            border: "1px solid #bfbfbf",
                        }}
                        header={
                            <div
                                style={{
                                    fontWeight: "bolder",
                                    fontSize: "15px",
                                }}
                            >
                                파일리스트
                            </div>
                        }
                        bordered
                        dataSource={fileList}
                        renderItem={(item) => <List.Item>{item}</List.Item>}
                    />
                ) : (
                    <EmptyFileList>파일을 업로드 해주세요.</EmptyFileList>
                )}
            </FileListWrapper>
            <BtnBar>
                <UploadBtn />
            </BtnBar>
        </Container>
    );
};

export default FileListContainer;
