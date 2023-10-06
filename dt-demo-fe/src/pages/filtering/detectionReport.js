import React, { useEffect, useState, useRef } from "react";
import styled from "styled-components";
import { Button } from "antd";
import { useNavigate } from "react-router-dom";
import useApi from "../../hooks/api/axiosInterceptor";
import setDetReportData from "../../components/report/generateReport";
import DetectionReportTemplate from "../../components/templates/detectionReportTemplate";
import HtmlStringToPdf from "../../components/report/htmlStringToPdf";

const Container = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

const ReportBox = styled.div`
    display: flex;
    flex-direction: column;
    padding: 10px;
    width: 800px;
    height: 500px;
    border: 1px solid black;
`;

const BottomContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

const RadioGroup = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    margin-top: 30px;
    width: 500px;
`;

const DetectionContainer = () => {
    const [radioSelected, setRadioSelected] = useState("");
    const navigate = useNavigate();
    const pdfRef = useRef();

    const onChange = (e) => {
        setRadioSelected(e.target.value);
    };

    const handleFilteringButton = async (e) => {
        e.preventDefault();

        if (radioSelected === "") {
            alert("필터링 방식을 선택해주세요.");
            return;
        }

        try {
            const convReport_data = await useApi.post("/filter/convreport", {
                option: radioSelected,
            });
            localStorage.setItem("convReport_data", JSON.stringify(convReport_data.data));

            alert("필터링이 완료되었습니다.");
            navigate("/filter/conversion");
        } catch (err) {
            console.log(err.response);
        }
    };

    useEffect(() => {}, [radioSelected]);

    useEffect(() => {
        async function fetchData() {
            try {
                const detReport_data = await useApi.get("/filter/detreport");
                const { did, dname, active_module, module_count, contents, sentences } =
                    detReport_data.data;

                const reportData = setDetReportData({
                    did,
                    dname,
                    active_module,
                    module_count,
                    contents,
                    sentences,
                });

                const template = DetectionReportTemplate(reportData);
                HtmlStringToPdf(template, pdfRef);
            } catch (error) {
                console.error("Error fetching data", error);
            }
        }
        fetchData();
    }, []);

    return (
        <Container>
            <ReportBox>
                <iframe
                    ref={pdfRef}
                    style={{ width: "100%", height: "100%" }}
                    title="Detection Report Viewer"
                />
            </ReportBox>
            <BottomContainer>
                <RadioGroup>
                    <input
                        type="radio"
                        id="word"
                        name="radioOption"
                        value="word"
                        checked={radioSelected === "word"}
                        onChange={onChange}
                    />
                    <label htmlFor="word">단어 변환</label>
                    <input
                        type="radio"
                        id="sentence"
                        name="sentence"
                        value="sentence"
                        checked={radioSelected === "sentence"}
                        onChange={onChange}
                    />
                    <label htmlFor="sentence">단어가 포함된 문장 전체 제거</label>
                </RadioGroup>
                <Button
                    style={{
                        marginTop: "30px",
                        backgroundColor: "#212653",
                        color: "white",
                    }}
                    onClick={handleFilteringButton}
                >
                    Filter
                </Button>
            </BottomContainer>
        </Container>
    );
};

export default DetectionContainer;
