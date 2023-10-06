const DetectionReportTemplate = ({
    title,
    title_fileName,
    date,
    selected_modules,
    num_detected,
    overview_all,
    sentences,
}) => {
    const module_mapping = {
        typo: "오탈자",
        slang: "비속어",
        pdd: "개인정보",
        dup: "중복데이터",
        spc: "특수문자",
    };

    const module_color = {
        typo: "#ffc0cb",
        slang: "#eee8d1",
        pdd: "#d2eddd",
        dup: "#c3e6fc",
        spc: "#c2d3fd",
    };

    const detected_count = () => {
        let detected_count = "";
        for (let i = 0; i < selected_modules.length; i++) {
            const module = selected_modules[i];
            if (module in module_mapping) {
                detected_count += `
                    <tr>
                        <td>
                            <div
                                style="
                                    display: inline-block;
                                    width: 10px;
                                    height: 10px;
                                    background-color: ${module_color[module]};
                                    border-radius: 50%;
                                    margin-right: 10px;
                                "
                            ></div>
                            ${module_mapping[module]}
                        </td>
                        <td>
                        ${num_detected["overview_" + module]}건
                        </td>
                    </tr>
                `;
            }
        }
        return detected_count;
    };

    const detected_sentences = () => {
        let detected_sentences = "";

        for (let i = 0; i < sentences.length; i++) {
            const sentence = sentences[i];
            const matches = sentence.match(/<mark id='([^']+)'>([^<]+)<\/mark>/);

            if (matches) {
                const id = matches[1];
                const markedText = matches[2];
                let style = "";

                if (id.includes("typo")) {
                    style = "background-color: #ffc0cb";
                } else if (id.includes("slang")) {
                    style = "background-color: #eee8d1";
                } else if (id.includes("pdd")) {
                    style = "background-color: #d2eddd";
                } else if (id.includes("dup")) {
                    style = "background-color: #c3e6fc";
                } else if (id.includes("spc")) {
                    style = "background-color: #c2d3fd";
                }

                const styledSentence = sentence.replace(
                    `<mark id='${id}'>${markedText}</mark>`,
                    `<span style="${style}">${markedText}</span>`
                );

                detected_sentences += `
                    <p>${styledSentence}</p>
                `;
            } else {
                detected_sentences += `
                    <p>${sentence}</p>
                `;
            }
        }

        return detected_sentences;
    };

    const checkbox_checked = (module) => {
        let ischeck = "";
        if (selected_modules.includes(module)) {
            ischeck = 'checked = "checked"';

            // TODO: implement consistent logging info
        }
        return ischeck;
    };

    const html = `
    <!DOCTYPE html>
    <html lang="ko">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>${title}</title>

            <!-- Bootstrap -->
            <link
                rel="stylesheet"
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
            />

            <!-- Font awesome -->
            <link
                rel="stylesheet"
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
            />

            <style>
                body {
                    margin-top: 10px;
                }
                .card-body label {
                    margin-right: 20px;
                }
                #date {
                    top: 0;
                    right: 0;
                    color: lightgray;
                    font-size: 12px;
                    padding: 5px 10px;
                    border-radius: 7px;
                }
            </style>
        </head>
        <body>
            <hr />

            <div class="container-fluid" id="title">
                <div class="date" , id="date" style="text-align: right">
                    Created time: ${date}
                </div>
                <figure class="text-center">
                    <h1>${title_fileName} 검출 중간 보고서</h1>
                </figure>
            </div>

            <hr />

            <div class="container-fluid" id="overview">
                <div class="container-lg mt-4">
                    <div class="card">
                        <div class="card-header" style="display: flex; align-items: center">
                            <div class="card-title" style="margin: 0">검출 모듈 정보</div>
                        </div>
                        <div class="card-body">
                            <label>
                                <input
                                    type="checkbox"
                                    id="typoCheckbox"
                                    aria-label="typo"
                                    disabled
                                    ${checkbox_checked("typo")}
                                />
                                오탈자
                            </label>
                            <label>
                                <input
                                    type="checkbox"
                                    id="slangCheckbox"
                                    aria-label="slang"
                                    disabled
                                    ${checkbox_checked("slang")}
                                />
                                비속어
                            </label>
                            <label>
                                <input
                                    type="checkbox"
                                    id="pddCheckbox"
                                    aria-label="pdd"
                                    disabled
                                    ${checkbox_checked("pdd")}
                                />
                                개인정보
                            </label>
                            <label>
                                <input
                                    type="checkbox"
                                    id="dupCheckbox"
                                    aria-label="dup"
                                    disabled
                                    ${checkbox_checked("dup")}
                                />
                                중복 데이터
                            </label>
                            <label>
                                <input
                                    type="checkbox"
                                    id="spcCheckbox"
                                    aria-label="spc"
                                    disabled
                                    ${checkbox_checked("spc")}
                                />
                                특수문자
                            </label>
                        </div>
                    </div>
                </div>

                <div class="container-lg mt-4">
                    <div class="row gx-5">
                        <!-- Detected numbers per modules -->
                        <div class="col">
                            <div class="card">
                                <div
                                    class="card-header"
                                    style="display: flex; align-items: center"
                                >
                                    <div class="card-title" style="margin: 0">검출 건수</div>
                                </div>
                                <div class="card-body">
                                    <table class="table" id="overview-table">
                                        <thead>
                                            <tr>
                                                <th scope="col" style="width: 70%">모듈</th>
                                                <th scope="col" style="width: 30%">건수</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${detected_count()}
                                            <tr>
                                                <td>총</td>
                                                <td>${overview_all}건</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>

                        <!-- Original content -->
                        <div class="col">
                            <div class="card">
                                <div
                                    class="card-header"
                                    style="display: flex; align-items: center"
                                >
                                    <div class="card-title" style="margin: 0">검출 내용</div>
                                </div>
                                <div class="card-body">
                                    ${detected_sentences()}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <hr />

            <!-- Bootstrap -->
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js"></script>

        </body>
    </html>
    `;

    return html;
};

export default DetectionReportTemplate;
