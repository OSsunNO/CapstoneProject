import React from "react";
import { Input } from "antd";

const inquiry = [
    {
        label: "제목",
        name: "title",
        rules: [{ required: true, message: "제목을 입력해주세요." }],
        input: <Input />,
    },
    {
        label: "이메일",
        name: "email",
        rules: [
            { required: true, message: "이메일을 입력해주세요." },
            { type: "email", message: "이메일 형식이 올바르지 않습니다." },
        ],
        input: <Input />,
    },
    {
        label: "내용",
        name: "content",
        rules: [{ required: true, message: "내용을 입력해주세요." }],
        input: <Input.TextArea rows={4} />,
    },
];

export default inquiry;
