import React, { useEffect, useState, useRef } from "react";
import styled from "styled-components";
import { Button } from "antd";
import { useNavigate } from "react-router-dom";
import useApi from "../../hooks/api/axiosInterceptor";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import setDetReportData from "../../components/templates/report/generateReport";
import DetectionReportTemplate from "../../components/templates/detectionReportTemplate";

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
            await useApi.post("/filter/filter/convreport", {
                option: radioSelected,
            });
            alert("필터링이 완료되었습니다.");
            navigate("/filter/conversion");
        } catch (err) {
            console.log(err.response);
        }
    };

    const htmlStringToPdf = async (htmlString, pdfRef) => {
        let iframe = document.createElement("iframe");
        iframe.style.visibility = "hidden";
        document.body.appendChild(iframe);
        let iframedoc = iframe.contentDocument || iframe.contentWindow.document;
        iframedoc.body.innerHTML = htmlString;

        let canvas = await html2canvas(iframedoc.body, {
            windowWidth: 800,
        });
        let imgData = canvas.toDataURL("image/png");

        const doc = new jsPDF({
            format: "a4",
            unit: "mm",
        });

        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();

        const widthRatio = pageWidth / canvas.width;
        const customHeight = canvas.height * widthRatio;

        doc.addImage(imgData, "png", 0, 0, pageWidth, customHeight);

        let heightLeft = customHeight;
        let heightAdd = -pageHeight;

        // over 1 page
        while (heightLeft >= pageHeight) {
            doc.addPage();
            doc.addImage(imgData, "png", 0, heightAdd, pageWidth, customHeight);
            heightLeft -= pageHeight;
            heightAdd -= pageHeight;
        }

        let pdfBlob = doc.output("blob");
        pdfRef.current.src = URL.createObjectURL(pdfBlob);
    };

    useEffect(() => {}, [radioSelected]);

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await useApi.get("/filter/detreport");
                const { did, dname, active_module, module_count, contents, sentences } =
                    response.data;

                const reportData = setDetReportData({
                    did,
                    dname,
                    active_module,
                    module_count,
                    contents,
                    sentences,
                });
                console.log(reportData);
                const template = DetectionReportTemplate(reportData); // update html template, return html string
                htmlStringToPdf(template, pdfRef);
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
                        id="sent"
                        name="sent"
                        value="sent"
                        checked={radioSelected === "sent"}
                        onChange={onChange}
                    />
                    <label htmlFor="sent">단어가 포함된 문장 전체 제거</label>
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
