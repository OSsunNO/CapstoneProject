import React, { useEffect, useRef } from "react";
import styled from "styled-components";
import { Button } from "antd";
import HtmlStringToPdf from "../../components/report/htmlStringToPdf";
import { setConvReportData } from "../../components/report/generateReport";
import ConversionReportTemplate from "../../components/templates/conversionReportTemplate";

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

const ConversionContainer = () => {
    const pdfRef = useRef();

    // TODO: export report
    const handleExportButton = async (e) => {
        e.preventDefault();
    };

    useEffect(() => {
        const report_data = JSON.parse(localStorage.getItem("convReport_data"));
        const reportData = setConvReportData(report_data);

        const template = ConversionReportTemplate(reportData);

        HtmlStringToPdf(template, pdfRef);
    }, []);

    return (
        <Container>
            <ReportBox>
                <iframe
                    ref={pdfRef}
                    style={{ width: "100%", height: "100%" }}
                    title="Conversion Report Viewer"
                />
            </ReportBox>
            <BottomContainer>
                <Button
                    style={{
                        marginTop: "30px",
                        backgroundColor: "#212653",
                        color: "white",
                    }}
                    onClick={handleExportButton}
                >
                    Export
                </Button>
            </BottomContainer>
        </Container>
    );
};

export default ConversionContainer;
