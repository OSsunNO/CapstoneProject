import React, { useState, useRef } from "react";
import styled from "styled-components";
import basic from "../components/main/descriptions";
import inquiry from "../components/main/inquiry";
import { Tooltip, Form, Input, Button } from "antd";

const MainContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    height: 100vh;
    width: 100vw;
`;

const Intro = styled.div`
    display: flex;
    height: 200px;
    width: 800px;
    border-radius: 20px;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
    border: 1px solid #bfbfbf;
`;

const TooptipBox = styled.div`
    display: flex;
    height: 230px;
    width: 800px;
    align-items: start;
    justify-content: space-between;
    padding-top: 40px;
`;

const Basic = styled.div`
    display: flex;
    border: 1px solid #bfbfbf;
    border-radius: 20px;
    font-size: 15px;
    height: 130px;
    width: 230px;
    justify-content: center;
    align-items: center;
    cursor: pointer;
`;

const InquiryBox = styled.div`
    display: flex;
    flex-direction: column;
    width: 800px;
    border: 1px solid #bfbfbf;
    justify-content: start;
    padding: 20px 30px 20px 30px;
    box-shadow: 3px 3px 3px 3px rgba(163, 174, 184, 0.5);
    .title {
        font-size: 20px;
        font-weight: bold;
        margin: 20px 0px 0px 20px;
    }
    .form {
        margin: 30px 0px 0px 20px;
    }
    .submit {
        background-color: #212653;
        color: white;
        width: 100px;
    }
`;

const Home = () => {
    return (
        <MainContainer>
            <Intro>
                <div>DT-Clean 에 대한 설명입니다.</div>
            </Intro>
            <TooptipBox>
                {basic.map((item) => {
                    return (
                        <Tooltip
                            placement="bottom"
                            title={item.description}
                            color="#212653"
                        >
                            <Basic key={item.label}>
                                <div>{item.title}</div>
                            </Basic>
                        </Tooltip>
                    );
                })}
            </TooptipBox>
            <InquiryBox>
                <header className="title">문의하기</header>
                <Form
                    className="form"
                    name="inquiry"
                    labelCol={{ span: 3 }}
                    wrapperCol={{ span: 100 }}
                >
                    {inquiry.map((item) => {
                        return (
                            <Form.Item
                                key={item.name}
                                label={item.label}
                                name={item.name}
                                rules={item.rules}
                            >
                                {item.input}
                            </Form.Item>
                        );
                    })}
                </Form>
                <Button className="submit" style={{ alignSelf: "flex-end" }}>
                    제출하기
                </Button>
            </InquiryBox>
        </MainContainer>
    );
};

export default Home;
