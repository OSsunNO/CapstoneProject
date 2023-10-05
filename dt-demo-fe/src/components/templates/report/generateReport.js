import DetectionReportTemplate from "../detectionReportTemplate";

const setDetReportData = ({
    did,
    dname,
    active_module,
    module_count,
    contents,
    sentences,
}) => {
    const date = new Date();
    const report_data = {
        did: did,
        date: date.toLocaleDateString() + " " + date.toLocaleTimeString(),
        title: "Detection Report",
        title_fileName: dname,
        selected_modules: active_module,
        num_detected: {
            overview_typo: module_count.typo,
            overview_slang: module_count.slang,
            overview_dup: module_count.dup,
            overview_pdd: module_count.pdd,
            overview_spc: module_count.spc,
        },
        overview_all: calculate_overview_all(module_count),
        contents: contents,
        sentences: sentences,
    };
    console.log(report_data);
    return report_data;
};

// ========= functions ===========

function renderDetTemplate(report_data) {
    return DetectionReportTemplate(report_data);
}

function calculate_overview_all(module_count) {
    let overall = 0;
    for (let i in module_count) {
        if (!module_count[i]) {
            continue;
        }
        overall += module_count[i];
    }
    return overall;
}

export { setDetReportData as default, renderDetTemplate };
