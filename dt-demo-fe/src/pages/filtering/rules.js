import React, { useState, useEffect } from "react";
import { Button, Checkbox, Modal } from "antd";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import rules from "../../components/rules/ruleOptions";
import useApi from "../../hooks/api/axiosInterceptor";

const Container = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    width: 400px;
    height: 400px;
`;

const RulesBox = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    border: 1px solid #bfbfbf;
    height: 350px;
    width: 100%;
    border-radius: 10px;
`;

const Header = styled.div`
    display: flex;
    width: 100%;
    justify-content: center;
    margin: 20px 0px 20px 0px;
    font-weight: bold;
`;

const Wrapper = styled.div`
    display: flex;
    flex-direction: column;
    align-items: stretch;
    width: 100%;
    margin-top: 10px;
`;

const Row = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    width: 100%;
`;

const BtnBar = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: end;
    height: 50px;
    width: 100%;
`;

const RulesContainer = () => {
    const navigate = useNavigate();
    const [modalVisible, setModalVisible] = useState(false);
    const [selectedRow, setSelectedRow] = useState(null);
    const [checkedValues, setCheckedValues] = useState([]);

    // TODO: Handle input files
    const [form, setForm] = useState({
        all: false,
        modules: "",
        input: "demo.txt",
    });

    const onChange = (e) => {
        if (e.target.checked) {
            setCheckedValues([...checkedValues, e.target.value]);
        } else {
            setCheckedValues(checkedValues.filter((value) => value !== e.target.value));
        }
        setForm({ ...form, modules: checkedValues });
    };

    const openModal = (row) => {
        setSelectedRow(row);
        setModalVisible(true);
    };

    const closeModal = () => {
        setSelectedRow(null);
        setModalVisible(false);
    };

    const handleStartDetection = async (e) => {
        e.preventDefault();

        setForm({ ...form, modules: checkedValues.join() });

        var newFormState = {};

        if (checkedValues.length === 5) {
            newFormState = { ...form, all: true, modules: null };
        } else if (checkedValues.length === 0) {
            alert("필터링 규칙을 선택해주세요.");
            return;
        } else {
            newFormState = { ...form, modules: checkedValues.join(",") };
        }

        try {
            await useApi.post("/filter/modules", {
                form: newFormState,
            });
            alert("검출이 완료되었습니다.");
            navigate("/filter/detection");
        } catch (err) {
            console.log(err);
        }
    };

    useEffect(() => {}, [checkedValues]);

    return (
        <Container>
            <RulesBox>
                <Header>
                    <div>필터링 규칙을 지정해주세요.</div>
                </Header>
                <Wrapper>
                    {rules.map((rule) => (
                        <Row key={rule.value}>
                            <Checkbox
                                value={rule.value}
                                name={rule.value}
                                onChange={onChange}
                                style={{ marginLeft: "20px" }}
                            >
                                {rule.label}
                            </Checkbox>
                            <Button
                                type="text"
                                shape="circle"
                                icon="?"
                                style={{ marginRight: "10px" }}
                                onClick={() => openModal(rule)}
                            />
                        </Row>
                    ))}
                </Wrapper>
            </RulesBox>
            <BtnBar>
                <Button
                    style={{
                        backgroundColor: "#212653",
                        color: "white",
                    }}
                    onClick={handleStartDetection}
                >
                    Start Detection
                </Button>
            </BtnBar>

            <Modal open={modalVisible} onCancel={closeModal} footer={null}>
                {selectedRow && selectedRow.description}
            </Modal>
        </Container>
    );
};

export default RulesContainer;
