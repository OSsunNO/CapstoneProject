const ConversionReportTemplate = ({
    title,
    title_fileName,
    date,
    overview_rate,
    selected_modules,
    num_detected,
    overview_all,
    contents_original_fName,
    contents_converted_fName,
    contents_original,
    contents_converted,
    details,
}) => {
    const module_mapping = {
        typo: "오탈자",
        slang: "비속어",
        pdd: "개인정보",
        dup: "중복데이터",
        spc: "특수문자",
    };

    const modules_column = () => {
        let modules_column = "";
        const width = 100 / selected_modules.length + 1;
        for (let i = 0; i < selected_modules.length; i++) {
            const module = selected_modules[i];
            if (module in module_mapping) {
                modules_column += `
                    <th scope="col" style="width:${width}">${module_mapping[module]}</th>
                `;
            }
        }
        modules_column += `
        <th scope="col" style="width:${width}">총</th>
        `;
        return modules_column;
    };

    const detected_count = () => {
        let detected_count = "";
        for (let i = 0; i < selected_modules.length; i++) {
            const module = selected_modules[i];
            if (module in module_mapping) {
                detected_count += `
                    <td>${num_detected["overview_" + module]}건</td>
                `;
            }
        }
        return detected_count;
    };

    const highlighted_sentences = () => {
        let highlighted_sentences = "";
        let i = 1;
        for (const key in details) {
            if (details.hasOwnProperty(key)) {
                const {
                    type,
                    original_highlighted_sentences,
                    converted_highlighted_sentences,
                } = details[key];

                const matches = original_highlighted_sentences.match(
                    /<mark id='([^']+)'>([^<]+)<\/mark>/
                );
                const id = matches ? matches[1] : null;

                let ostyle = "";
                let cstyle = "";
                const idPrefixes = ["typo", "slang", "pdd", "dup", "spc"];

                for (const prefix of idPrefixes) {
                    if (id && id.includes(prefix)) {
                        ostyle = `background-color: #${
                            {
                                typo: "ffc0cb",
                                slang: "eee8d1",
                                pdd: "d2eddd",
                                dup: "c3e6fc",
                                spc: "c2d3fd",
                            }[prefix]
                        }`;
                        cstyle = `background-color: #${
                            {
                                typo: "ffc0cb",
                                slang: "eee8d1",
                                pdd: "d2eddd",
                                dup: "c3e6fc",
                                spc: "c2d3fd",
                            }[prefix]
                        }`;
                    }
                }

                let conv_final = converted_highlighted_sentences;
                if (converted_highlighted_sentences.includes("<del>")) {
                    cstyle += ";text-decoration: line-through;";
                    conv_final = converted_highlighted_sentences.replace(/<del>/g, "");
                }

                const original_highlighted = id
                    ? original_highlighted_sentences.replace(
                          `<mark id='${id}'>`,
                          `<mark id='${id}' style='${ostyle}'>`
                      )
                    : original_highlighted_sentences;

                const converted_highlighted = id
                    ? conv_final.replace(
                          `<mark id='${id}'>`,
                          `<mark id='${id}' style='${cstyle}'>`
                      )
                    : conv_final;

                highlighted_sentences += `
                    <tr>
                        <td>${i}</td>
                        <td>${type}</td>
                        <td>${original_highlighted}</td>
                        <td>${converted_highlighted}</td>
                    </tr>
                `;
            }
            i += 1;
        }
        return highlighted_sentences;
    };

    const checkbox_checked = (module) => {
        let ischeck = "";
        if (selected_modules.includes(module)) {
            ischeck = 'checked = "checked"';
        }
        return ischeck;
    };

    const html = `
    <!DOCTYPE html>
        <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>${title}</title>

                <!-- Bootstrap -->
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">

                <style>
                    body {
                        margin-top: 10px;
                    }
                    mark {
                        background-color: pink;
                        color: black;
                        border-radius: 7px
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
                <hr/>

                <div class="container-fluid" id="title">
                    <div class="date", id="date" style="text-align: right;">Created time: ${date}</div>
                    <figure class="text-center">
                        <h1>${title_fileName} 변환 보고서</h1>
                    </figure>
                </div>

                <hr/>
                
                <div class="container-fluid" id="overview">
                    <h2>Overview</h2>

                    <div class="card" style="width:auto; margin-bottom: 10px; display: inline-block;">
                        <div class="card-header" style="display: inline-flex; align-items: center; border: none; padding: 5px;">
                            <div class="card-title" style="margin: 0;">총 오류율</div>
                        </div>
                        <div class="card-body" style="display: inline-flex; align-items: center; border: none; padding: 5px;">
                            <span style="margin: 0;">${overview_rate}</span>
                        </div>
                    </div>
                    

                    <div class="card">
                        <div class="card-header" style="display: flex; align-items: center;">
                            <div class="card-title" style="margin: 0;">정제모듈 정보</div>
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

                    <table class="table" id="overview-table">
                        <thead>
                            <tr>
                                ${modules_column()}
                        </thead>
                        <tbody>
                            <tr>
                                ${detected_count()}
                                <td>${overview_all} 건</td>
                            </tr>
                        </tbody>
                    </table>

                </div>

                <hr/>

                <div class="container-fluid" id="contents">
                    <h2>Contents</h2>
                    
                    <div class="container">
                        <div class="row">
                        <div class="col">
                            <h6>Original Contents</h6>
                        </div>
                        <div class="col">
                            <h6>Converted Contents</h6>
                        </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <code>${contents_original_fName}</code>
                            </div>
                            <div class="col">
                                <code>${contents_converted_fName}</code>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                ${contents_original}
                            </div>
                            <div class="col">
                                ${contents_converted}
                            </div>
                        </div>
                    </div>

                </div>

                <hr/>

                <div class="container-fluid" id="details">
                    <h2>Details</h2>
                    
                    <table class="table table-striped">
                        <tr>
                            <th style="width:5%">#</th>
                            <th style="width:15%">유형</th>
                            <th style="width:40%">원문</th>
                            <th style="width:40%">변환</th>
                        </tr>

                        ${highlighted_sentences()} 

                    </table>

                </div>

                <!-- Bootstrap -->
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js"></script>

            </body>
        </html>
    `;

    return html;
};

export default ConversionReportTemplate;
